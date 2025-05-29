import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        self._create_table()
    
    def _create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                currency VARCHAR(10) NOT NULL,
                image_url VARCHAR(255),
                category VARCHAR(100),
                discounter VARCHAR(50) NOT NULL,
                country VARCHAR(50) NOT NULL,
                valid_until DATE NOT NULL,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            self.conn.commit()
    
    def save_products(self, products):
        with self.conn.cursor() as cur:
            for product in products:
                cur.execute("""
                INSERT INTO products (name, price, currency, image_url, category, discounter, country, valid_until)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    product['name'],
                    product['price'],
                    product['currency'],
                    product['image_url'],
                    product['category'],
                    product['discounter'],
                    product['country'],
                    product['valid_until']
                ))
            self.conn.commit()
    
    def close(self):
        self.conn.close()