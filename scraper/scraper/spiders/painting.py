import scrapy
import json
from urllib.parse import urljoin
from scraper.scraper.items import ScraperItem  # Ensure correct import

class PaintingScraper(scrapy.Spider):
    name = "painting"

    def __init__(self, start_urls=None, *args, **kwargs):
        super(PaintingScraper, self).__init__(*args, **kwargs)
        self.start_urls = start_urls or ["https://internationalgallery.org/"]

    def parse(self, response):
        items = []
        all_div_items = response.css('div.products div.thumbnail')

        for e_item in all_div_items:
            item = ScraperItem()
            item['head'] = e_item.css('.title::text').get()
            relative_image_url = e_item.css('img::attr(src)').get()
            item['image_url'] = urljoin(response.url, relative_image_url) if relative_image_url else None
            items.append(dict(item))

        # Save scraped data
        with open("scraper/scraped_data_painting.json", "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=4)

        self.log(f"Scraped {len(items)} items")
