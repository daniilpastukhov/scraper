import re

from scrapy import Spider, Request
from scrapy_playwright.page import PageMethod

from src.items import PropertyItem

from src.db import PostgresDatabase

BASE_URL = 'https://www.sreality.cz/hledani/prodej/byty?strana=%d'

TITLE_SELECTOR = 'span.name::text'
LOCALITY_SELECTOR = 'span.locality::text'
PRICE_SELECTOR = 'span.norm-price::text'
IMAGES_SELECTOR = 'preact img::attr(src)'

PROPERTY_SELECTOR = 'div.property'

LIMIT = 500  # required number of items
ITEMS_PER_PAGE = 20  # number of items per page

# Connect to the database and retrieve number of properties
db = PostgresDatabase()
db.connect()
n = db.number_of_properties()
db.close()


class SrealitySpider(Spider):
    name: str = 'sreality'
    total_parsed_items: int = n
    current_page_number: int = total_parsed_items // ITEMS_PER_PAGE + 1

    def start_requests(self):
        yield Request(
            url=BASE_URL % self.current_page_number,
            callback=self.parse,
            meta={
                'playwright': True,
                'playwright_context': self.current_page_number,
                'playwright_page_methods': [PageMethod('wait_for_selector', PROPERTY_SELECTOR)],
                'errback': self.errback
            }
        )

    async def parse(self, response, **kwargs):
        properties = response.css(PROPERTY_SELECTOR)

        # Iterate over all properties and select required data per property
        for prop in properties:
            if self.total_parsed_items >= LIMIT:
                break

            title = prop.css(TITLE_SELECTOR).extract_first()
            locality = prop.css(LOCALITY_SELECTOR).extract_first()
            price = prop.css(PRICE_SELECTOR).extract_first()
            image_urls = prop.css(IMAGES_SELECTOR).getall()

            # Filter out relative URLs
            filtered_image_urls = list(filter(lambda x: re.match(r'https://*', x), image_urls))
            yield PropertyItem(
                id=self.total_parsed_items,
                title=title,
                locality=locality,
                price=price,
                image_urls=filtered_image_urls
            )

            self.total_parsed_items += 1

        # Continue to the next page if limit is not reached, stop otherwise
        if self.total_parsed_items < LIMIT:
            self.current_page_number += 1
            yield Request(
                url=BASE_URL % self.current_page_number,
                callback=self.parse,
                meta={
                    'playwright': True,
                    'playwright_context': self.current_page_number,
                    'playwright_page_methods': [PageMethod('wait_for_selector', PROPERTY_SELECTOR)],
                    'errback': self.errback
                }
            )

    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()
