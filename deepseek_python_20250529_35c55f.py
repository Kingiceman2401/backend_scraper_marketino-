from .base_scraper import BalkanScraper

class SerbiaScraper(BalkanScraper):
    def __init__(self):
        super().__init__("serbia", "Idea")
    
    def scrape(self):
        results = []
        url = "https://www.idea.rs/akcije"
        
        # Playwright Extraktionsscript
        extractor = """
        () => {
            const products = [];
            document.querySelectorAll('.product-item').forEach(item => {
                const name = item.querySelector('.product-name')?.innerText || '';
                const priceText = item.querySelector('.product-price')?.innerText || '';
                const price = parseFloat(priceText.replace(/[^0-9,]/g, '').replace(',', '.'));
                const image = item.querySelector('img');
                const imageUrl = image ? image.src : '';
                const category = item.closest('.category-section')?.querySelector('h2')?.innerText || '';
                const validUntil = item.querySelector('.valid-until')?.innerText || '';
                
                products.push({
                    name,
                    price,
                    imageUrl,
                    category,
                    validUntil
                });
            });
            return products;
        }
        """
        
        data = self.scrape_with_playwright(url, extractor)
        
        for item in data:
            results.append({
                "name": item["name"],
                "price": item["price"],
                "currency": "RSD",
                "image_url": item["imageUrl"],
                "category": item["category"],
                "valid_until": self._parse_date(item["validUntil"]),
                "discounter": "Idea",
                "country": "Serbia"
            })
        
        return results

# Weitere Discounter für Serbien
class MaxiScraper(BalkanScraper):
    # Ähnliche Implementierung für Maxi
    pass