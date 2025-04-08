import json
import os
import logging
from django.shortcuts import render
from multiprocessing import Process
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from scraper.scraper.spiders.event_scrapper import EventScraper

from scraper.scraper.spiders.scruplutre import SculptureSpider
from scraper.scraper.spiders.painting import PaintingScraper



# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_spider(start_url):
    """
    Runs the Scrapy spider in a separate process to avoid Twisted reactor issues.
    """
    configure_logging({'LOG_LEVEL': 'ERROR'})
    
    process = CrawlerProcess(get_project_settings())
    
    try:
        process.crawl(EventScraper, start_urls=[start_url])
        process.start()
    except Exception as e:
        logging.error(f"Spider crawling error: {e}")

def scrape_events(request, city_id):
    """
    Django view to scrape events dynamically based on the city ID.
    """
    city_map = {
        1: "goa",
        2: "bengaluru",
        3: "mumbai",
        4: "delhi",
    }
    
    try:
        city_id = int(city_id)
        city = request.GET.get("city", city_map.get(city_id, "goa"))
        formatted_city = city.lower().replace(" ", "-")
        start_url = f"https://insider.in/all-events-in-{formatted_city}/art-%26-craft"
        
        os.makedirs('scraper', exist_ok=True)

        # Run the spider in a separate process
        spider_process = Process(target=run_spider, args=(start_url,))
        spider_process.start()
        spider_process.join()  # Wait for the process to complete

        # Ensure JSON file exists before reading
        json_file = "scraper/scraped_data.json"
        if not os.path.exists(json_file):
            logging.error(f"Scraped data file not found: {json_file}")
            return render(request, "scraper.html", {"events": [], "error": "No events found"})

        # Read and clean scraped data
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                events = json.load(f)

            if not isinstance(events, list):
                raise ValueError("Invalid JSON format - Expected a list")

            events = [event for event in events if event.get('head') and event.get('image_url')]

        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            logging.error(f"Error loading JSON: {e}")
            events = []

        return render(request, "scraper.html", {
            "events": events,
            "city": city,
            "total_events": len(events)
        })

    except Exception as e:
        logging.error(f"Error scraping events for city {city_id}: {e}")
        return render(request, "scraper.html", {
            "events": [],
            "error": f"Could not scrape events for {city}"
        })






def run_spider_s():
    process = CrawlerProcess(get_project_settings())
    process.crawl(SculptureSpider)
    process.start()

def sclupture(request):
    # Use multiprocessing to run the spider in a separate process
    spider_process = Process(target=run_spider_s)
    spider_process.start()
    spider_process.join()

    try:
        with open("scraper/scraped_data_sculpture.json", "r", encoding="utf-8") as f:
            events = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        events = []

    return render(request, 'sclupture.html', {"events": events})






def run_spider_p(start_url):
    """
    Runs the Scrapy spider in a separate process to avoid Twisted reactor issues.
    """
    configure_logging({'LOG_LEVEL': 'ERROR'})  # Reduce log verbosity

    process = CrawlerProcess(get_project_settings())

    try:
        process.crawl(PaintingScraper, start_urls=[start_url])
        process.start()
    except Exception as e:
        logging.error(f"Spider crawling error: {e}")

def painting(request):
    """
    Django view to scrape paintings dynamically.
    """
    start_url = "https://internationalgallery.org/"

    # Create 'scraper' directory if not exists
    os.makedirs('scraper', exist_ok=True)

    # Run Scrapy Spider in a separate process
    spider_process = Process(target=run_spider_p, args=(start_url,))
    spider_process.start()
    spider_process.join()  # Wait for scraping to complete

    # Read scraped data safely
    json_file = "scraper/scraped_data_painting.json"
    try:
        if not os.path.exists(json_file):
            logging.error(f"Scraped data file not found: {json_file}")
            return render(request, "painting.html", {"events": [], "error": "No paintings found"})

        with open(json_file, "r", encoding="utf-8") as f:
            events = json.load(f)

        # Validate and filter scraped data
        if not isinstance(events, list):
            raise ValueError("Invalid JSON format - Expected a list")

        events = [event for event in events if event.get('head') and event.get('image_url')]

    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        logging.error(f"Error loading JSON: {e}")
        events = []

    return render(request, "painting.html", {
        "events": events,
        "total_events": len(events)
    })
