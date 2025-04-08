import scrapy
import json
from ..items import ScraperItem
import os

class SculptureSpider(scrapy.Spider):
    name = "sculpture"
    
    def __init__(self, start_urls=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls or [
            "https://www.metmuseum.org/art/collection/search?showOnly=withImage&department=3"
        ]
    
    def parse(self, response):
        items = []
        all_div_items = response.css('figure.collection-object_collectionObject__SuPct')
        
        for e_items in all_div_items:
            item = {
                'head': e_items.css('.collection-object_link__qM3YR::text').get(),
                'image_url': e_items.css('.collection-object_image__XVQPm.collection-object_gridView__8kZLF::attr(src)').get()
            }
            items.append(item)
        
        # Ensure the directory exists
        os.makedirs('scraper', exist_ok=True)
        
        # Save data to JSON
        with open("scraper/scraped_data_sculpture.json", "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=4)
        
        self.log(f"Scraped {len(items)} items")
