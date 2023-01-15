import scrapy
from scrapy.spiders import CrawlSpider, Spider
import re
from datetime import datetime

from notebooks.items import NotebookItem


class ComputersSpider(CrawlSpider):
    name = 'scrapKNS'
    allowed_domains = ['kns.ru']
    start_urls = ["https://www.kns.ru/catalog/noutbuki/"]

    default_headers = {}

    def scrap_computers(self, response):
        for card in response.xpath("//div[@class='goods-list-item mx-auto']"):
            url = "https://www."+ComputersSpider.allowed_domains[0]+card.xpath(".//a[@class='name d-block']")\
                .attrib.get("href")+"characteristics/"
            name = card.xpath(".//a[@class='name d-block']").attrib.get("title").encode('ascii', errors='ignore')\
                .decode()
            price = int(card.xpath(".//span[@class='price my-1']/text()").extract()[0].encode('ascii', errors='ignore')
                        .decode())

            yield scrapy.Request(url, callback=self.full_parse,
                                 meta={'name': name,
                                       'price': price,
                                       'url': url})
            for i in range(2, 7):
                next_page = "https://www.kns.ru/catalog/noutbuki/page" + str(i)+"/"
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.scrap_computers)

    def full_parse(self, response):
        book_item = NotebookItem()
        for card in response.xpath("//div[@class='col pr-md-2']"):
            try:
                cpu_hhz_selector = card.xpath(".//div[@data-id='1404400234']/text()").extract()[0]
            except:
                cpu_hhz = None
            else:
                cpu_hhz = float("".join(re.findall(r'\d+', cpu_hhz_selector))) / 10
            try:
                ram_gb_selector = card.xpath(".//div[@data-id='1404400241']/text()").extract()[0]
            except:
                ram_gb = None
            else:
                ram_gb = int(int(re.findall(r'\d+', ram_gb_selector)[0])/1000)
            try:
                ssd_gb_selector = card.xpath(".//div[@data-id='1404404218']/text()").extract()[0]
            except:
                ssd_gb = None
            else:
                ssd_gb = int(re.findall(r'\d+', ssd_gb_selector)[0])
            visited_at = datetime.now()
            try:
                rank = round(ram_gb * 5.6 + response.meta.get('price') * (-0.0001), 2)
            except:
                rank = None

            book_item['visited_at'] = visited_at
            book_item['cpu_hhz'] = cpu_hhz
            book_item['ram_gb'] = ram_gb
            book_item['ssd_gb'] = ssd_gb
            book_item['rank'] = rank
            book_item['price_rub'] = response.meta.get('price')
            book_item['name'] = response.meta.get('name')
            book_item['url'] = response.meta.get('url')
        return book_item

    def parse_start_url(self, response, **kwargs):
        url = self.start_urls[0]
        return response.follow(
            url, callback=self.scrap_computers, headers=self.default_headers
        )



# scrapy crawl scrapKNS -o damp1.json