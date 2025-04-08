import scrapy
import json
import os
from ..items import ScraperItem

class EventScraper(scrapy.Spider):
    name = "event"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def __init__(self, start_urls=None, *args, **kwargs):
        super(EventScraper, self).__init__(*args, **kwargs)
        self.start_urls = start_urls or []
        self.unique_items = set()
        self.scraped_data = []  # Store data in memory before writing

    def parse(self, response):
        all_div_items = response.css('li.card-list-item')

        for e_items in all_div_items:
            head = e_items.css('.css-17ztqjg::text').get() or 'No Title'
            image_url = e_items.css('#event_image img::attr(src)').get() or ''

            unique_key = f"{head}_{image_url}"
            if unique_key not in self.unique_items:
                self.unique_items.add(unique_key)
                item = ScraperItem()
                item['head'] = head
                item['image_url'] = image_url
                self.scraped_data.append(dict(item))

        # Ensure scraper directory exists
        os.makedirs('scraper', exist_ok=True)

        # Save data to JSON - Ensure it's properly formatted
        with open("scraper/scraped_data.json", "w", encoding="utf-8") as f:
            json.dump(self.scraped_data, f, ensure_ascii=False, indent=4)

        self.log(f"Scraped {len(self.scraped_data)} unique items")
