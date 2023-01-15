# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker
from notebooks.models import db_connect, create_table, Computers


class NotebooksPipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        query = insert(Computers).values(url=item["url"],
                                         visited_at=item["visited_at"],
                                         name=item["name"],
                                         cpu_hhz=item["cpu_hhz"],
                                         ram_gb=item["ram_gb"],
                                         ssd_gb=item["ssd_gb"],
                                         price_rub=item["price_rub"],
                                         rank=item["rank"])

        try:
            session.execute(query)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item

