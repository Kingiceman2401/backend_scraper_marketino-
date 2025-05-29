from scrapers.slovenia import MercatorScraper, SparSIScraper
from scrapers.croatia import KonzumScraper, LidlHRScraper
from scrapers.bosnia import BingoScraper, MercatorBAScraper
from scrapers.serbia import IdeaScraper, MaxiScraper
from scrapers.montenegro import VoliScraper, AromaScraper
from scrapers.macedonia import TinexScraper, VeroScraper
from services.database import Database
import time

# Liste aller Scraper
SCRAPERS = [
    MercatorScraper(), SparSIScraper(),
    KonzumScraper(), LidlHRScraper(),
    BingoScraper(), MercatorBAScraper(),
    IdeaScraper(), MaxiScraper(),
    VoliScraper(), AromaScraper(),
    TinexScraper(), VeroScraper()
]

def main():
    db = Database()
    
    for scraper in SCRAPERS:
        try:
            print(f"Scraping {scraper.discounter_name} in {scraper.country}...")
            products = scraper.scrape()
            db.save_products(products)
            print(f"Saved {len(products)} products from {scraper.discounter_name}")
            time.sleep(random.uniform(2, 5))  # Zwischen den Requests warten
        except Exception as e:
            print(f"Error scraping {scraper.discounter_name}: {str(e)}")
    
    db.close()

if __name__ == "__main__":
    main()