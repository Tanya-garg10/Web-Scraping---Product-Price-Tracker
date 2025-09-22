import requests
from bs4 import BeautifulSoup
import json
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
import logging
from datetime import datetime
import os
from typing import Dict, List, Optional
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('price_tracker.log'),
        logging.StreamHandler()
    ]
)

class PriceTracker:
    def __init__(self, config_file: str = 'config.json'):
        """Initialize the price tracker with configuration."""
        self.config = self.load_config(config_file)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            logging.info(f"Configuration loaded from {config_file}")
            return config
        except FileNotFoundError:
            logging.error(f"Configuration file {config_file} not found!")
            raise
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in {config_file}")
            raise
    
    def extract_price(self, html: str, price_selector: str) -> Optional[float]:
        """Extract price from HTML using CSS selector."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            price_element = soup.select_one(price_selector)
            
            if not price_element:
                logging.warning(f"Price element not found with selector: {price_selector}")
                return None
            
            # Extract price text and clean it
            price_text = price_element.get_text().strip()
            
            # Remove currency symbols and extract numeric value
            price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
            
            if price_match:
                return float(price_match.group())
            else:
                logging.warning(f"Could not extract numeric price from: {price_text}")
                return None
                
        except Exception as e:
            logging.error(f"Error extracting price: {str(e)}")
            return None
    
    def scrape_product(self, product: Dict) -> Optional[Dict]:
        """Scrape a single product's data."""
        try:
            response = self.session.get(product['url'], timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_element = soup.select_one(product['title_selector'])
            title = title_element.get_text().strip() if title_element else product.get('name', 'Unknown Product')
            
            # Extract price
            current_price = self.extract_price(response.text, product['price_selector'])
            
            if current_price is None:
                logging.warning(f"Failed to extract price for {title}")
                return None
            
            product_data = {
                'name': title,
                'url': product['url'],
                'current_price': current_price,
                'target_price': product['target_price'],
                'timestamp': datetime.now().isoformat(),
                'price_dropped': current_price <= product['target_price']
            }
            
            logging.info(f"Scraped {title}: ${current_price}")
            return product_data
            
        except requests.RequestException as e:
            logging.error(f"Request failed for {product['url']}: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error scraping {product['url']}: {str(e)}")
            return None
    
    def save_data(self, data: List[Dict], format: str = 'both'):
        """Save scraped data to CSV and/or JSON."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format in ['csv', 'both']:
            csv_filename = f"price_data_{timestamp}.csv"
            try:
                with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                    if data:
                        fieldnames = data[0].keys()
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(data)
                logging.info(f"Data saved to {csv_filename}")
            except Exception as e:
                logging.error(f"Error saving CSV: {str(e)}")
        
        if format in ['json', 'both']:
            json_filename = f"price_data_{timestamp}.json"
            try:
                with open(json_filename, 'w', encoding='utf-8') as jsonfile:
                    json.dump(data, jsonfile, indent=2, ensure_ascii=False)
                logging.info(f"Data saved to {json_filename}")
            except Exception as e:
                logging.error(f"Error saving JSON: {str(e)}")
    
    def send_email_alert(self, product_data: Dict):
        """Send email alert for price drop."""
        try:
            email_config = self.config['email']
            
            msg = MIMEMultipart()
            msg['From'] = email_config['sender_email']
            msg['To'] = email_config['recipient_email']
            msg['Subject'] = f"🎉 Price Drop Alert: {product_data['name']}"
            
            body = f"""
            Great news! The price has dropped for a product you're tracking:
            
            Product: {product_data['name']}
            Current Price: ${product_data['current_price']:.2f}
            Target Price: ${product_data['target_price']:.2f}
            Savings: ${product_data['target_price'] - product_data['current_price']:.2f}
            
            Product URL: {product_data['url']}
            
            Time: {product_data['timestamp']}
            
            Happy shopping! 🛒
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to Gmail SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_config['sender_email'], email_config['app_password'])
            
            text = msg.as_string()
            server.sendmail(email_config['sender_email'], email_config['recipient_email'], text)
            server.quit()
            
            logging.info(f"Email alert sent for {product_data['name']}")
            
        except Exception as e:
            logging.error(f"Failed to send email alert: {str(e)}")
    
    def run_tracker(self):
        """Run the price tracking for all configured products."""
        logging.info("Starting price tracking run...")
        
        scraped_data = []
        alerts_sent = 0
        
        for product in self.config['products']:
            product_data = self.scrape_product(product)
            
            if product_data:
                scraped_data.append(product_data)
                
                # Check if price dropped and send alert
                if product_data['price_dropped']:
                    self.send_email_alert(product_data)
                    alerts_sent += 1
            
            # Be respectful to servers
            time.sleep(2)
        
        # Save all scraped data
        if scraped_data:
            self.save_data(scraped_data, self.config.get('data_format', 'both'))
        
        logging.info(f"Tracking run completed. {len(scraped_data)} products scraped, {alerts_sent} alerts sent.")
        return scraped_data
    
    def start_scheduled_tracking(self):
        """Start scheduled price tracking."""
        interval = self.config.get('check_interval_hours', 6)
        
        # Schedule the tracker to run every X hours
        schedule.every(interval).hours.do(self.run_tracker)
        
        logging.info(f"Price tracker scheduled to run every {interval} hours")
        print(f"Price tracker started! Checking every {interval} hours...")
        print("Press Ctrl+C to stop")
        
        # Run once immediately
        self.run_tracker()
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logging.info("Price tracker stopped by user")
            print("\nPrice tracker stopped.")

def main():
    """Main function to run the price tracker."""
    try:
        tracker = PriceTracker()
        
        # Check if running in scheduled mode or one-time mode
        import sys
        if len(sys.argv) > 1 and sys.argv[1] == '--schedule':
            tracker.start_scheduled_tracking()
        else:
            print("Running one-time price check...")
            results = tracker.run_tracker()
            print(f"\nCompleted! Checked {len(results)} products.")
            
            # Display results
            for result in results:
                status = "🔥 PRICE DROP!" if result['price_dropped'] else "📊 No change"
                print(f"{status} {result['name']}: ${result['current_price']:.2f}")
                
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
