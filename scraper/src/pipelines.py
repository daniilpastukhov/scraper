import os

from src.db import PostgresDatabase


class PostgresPipeline:
    def __init__(self):
        self.db = PostgresDatabase()

    def open_spider(self, spider):
        spider.logger.info(
            f'Opening PostgresPipeline on {os.environ["POSTGRES_HOST"]}:{os.environ["POSTGRES_PORT"]}...')
        self.db.connect()
        spider.logger.info('Opened PostgresPipeline.')

    def close_spider(self, spider):
        spider.logger.info('Closing PostgresPipeline...')
        self.db.close()
        spider.logger.info('Closed PostgresPipeline.')

    def process_item(self, item, spider):
        spider.logger.info('Processing item...')
        self.db.execute('INSERT INTO sreality.property (id, title, locality, price, image_urls)'
                        'VALUES (%s, %s, %s, %s, %s)',
                        (
                            item.id,
                            item.title,
                            item.locality,
                            item.price,
                            item.image_urls
                        ))
        self.db.commit()
        spider.logger.info('Processed item.')
        return item
