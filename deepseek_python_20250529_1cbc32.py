import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import re
import time
import random
from datetime import datetime, timedelta

class BalkanScraper:
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    ]
    
    def __init__(self, country, discounter_name):
        self.country = country
        self.discounter_name = discounter_name
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": random.choice(self.USER_AGENTS)})
        self.proxies = self._load_proxies()
    
    def _load_proxies(self):
        # Proxies für Balkan-Länder
        return [
            "http://proxy-si.example.com:8000",  # Slowenien
            "http://proxy-hr.example.com:8080",  # Kroatien
            "http://proxy-ba.example.com:8888",  # Bosnien
            "http://proxy-rs.example.com:3128",  # Serbien
            "http://proxy-me.example.com:8080",  # Montenegro
            "http://proxy-mk.example.com:8000"   # Nordmazedonien
        ]
    
    def _get_proxy(self):
        return {"http": random.choice(self.proxies), "https": random.choice(self.proxies)}
    
    def _parse_date(self, date_text):
        # Übersetzer für Balkan-Datumsformate
        month_translations = {
            'slo': {'januar': 1, 'februar': 2, 'marec': 3, 'april': 4, 'maj': 5, 'junij': 6,
                    'julij': 7, 'avgust': 8, 'september': 9, 'oktober': 10, 'november': 11, 'december': 12},
            'cro': {'siječanj': 1, 'veljača': 2, 'ožujak': 3, 'travanj': 4, 'svibanj': 5, 'lipanj': 6,
                    'srpanj': 7, 'kolovoz': 8, 'rujan': 9, 'listopad': 10, 'studeni': 11, 'prosinac': 12},
            # ... für alle Länder
        }
        
        today = datetime.now()
        if "do" in date_text.lower() or "valid until" in date_text.lower():
            match = re.search(r'\d{1,2}\.\d{1,2}\.\d{4}', date_text)
            if match:
                return datetime.strptime(match.group(), '%d.%m.%Y').date()
        
        # Fallback: 7 Tage ab heute
        return (today + timedelta(days=7)).date()
    
    def scrape(self):
        """Hauptmethode die implementiert werden muss"""
        raise NotImplementedError("Subclasses must implement this method")
    
    def scrape_with_playwright(self, url, extractor_script):
        """Für JavaScript-lastige Seiten"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=random.choice(self.USER_AGENTS),
                viewport={"width": 1920, "height": 1080}
            )
            page = context.new_page()
            page.goto(url, timeout=60000)
            
            # Warte auf Ladevorgang
            page.wait_for_load_state("networkidle")
            
            # Führe Extraktionsscript aus
            result = page.evaluate(extractor_script)
            
            browser.close()
            return result