import scrapy
from scrapy.spiders import CrawlSpider, Spider
import re
from datetime import datetime
from notebooks.items import NotebookItem

class ComputersSpider(CrawlSpider):
    name = 'scrapNotik'
    allowed_domains = ['notik.ru']
    start_urls = ["https://www.notik.ru/search_catalog/filter/brand.htm"]

    default_headers = {}

    def scrap_computers(self, response):
        book_item = NotebookItem()
        for card in response.xpath("//tr[@class='goods-list-table']"):
            price_selector = card.xpath(".//td[@class='glt-cell gltc-cart']")
            price = re.findall(r'\d+', price_selector.xpath(".//b").css("::text").get())
            book_item['price_rub'] = int("".join(price))
            book_item['name'] = price_selector.xpath(".//a").attrib.get("ecname").encode('ascii', errors='ignore').decode()
            href_selector = card.xpath(".//td[@class='glt-cell gltc-title show-mob hide-desktop']")
            book_item['url'] = "https://www."+ComputersSpider.allowed_domains[0]+href_selector.xpath(".//a").attrib.get("href")
            cpu_hhz_selector = card.xpath(".//td[@class='glt-cell w4']/text()").extract()[2]
            book_item['cpu_hhz'] = float("".join(re.findall(r'\d+', cpu_hhz_selector)[0])) / 1000
            ram_gb_selector = card.xpath(".//td[@class='glt-cell w4']").extract()[1]
            book_item['ram_gb'] = int(re.findall(r'\d+', ram_gb_selector)[1])
            book_item['ram_gb'] = int(re.findall(r'\d+', ram_gb_selector)[1])
            book_item['ssd_gb'] = int(re.findall(r'\d+', ram_gb_selector)[4])
            book_item['visited_at'] = datetime.now()
            book_item['rank'] = round(book_item['ram_gb'] * 5.6 + book_item['price_rub'] * (-0.0001), 2)
            yield book_item

            for i in range(2, 11):
                next_page = "https://www.notik.ru/search_catalog/filter/brand.htm?page=" + str(i)
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.scrap_computers)

    def parse_start_url(self, response, **kwargs):
        url = self.start_urls[0]
        return response.follow(
            url, callback=self.scrap_computers, headers=self.default_headers
        )


# scrapy crawl scrapNotik -o damp.json
