# Price Tracker Usage Guide 📖

## Quick Start (5 minutes)

### Step 1: Set up Gmail App Password
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Security → 2-Step Verification → App passwords
3. Generate password for "Mail"
4. Copy the 16-character password

### Step 2: Configure Your First Product
1. Open 'config.json'
2. Replace the example with your product:
   json
   {
     "name": "iPhone 15",
     "url": "https://store.example.com/iphone-15",
     "price_selector": ".price",
     "title_selector": "h1",
     "target_price": 999.99
   }

### Step 3: Update Email Settings
json
"email": {
  "sender_email": "youremail@gmail.com",
  "app_password": "abcd efgh ijkl mnop",
  "recipient_email": "youremail@gmail.com"
}

### Step 4: Run the Tracker
bash
python scripts/price_tracker.py

## Finding CSS Selectors 🎯

### Method 1: Browser Inspector
1. Right-click on price → "Inspect" or "Inspect Element"
2. Right-click on highlighted HTML → "Copy" → "Copy selector"
3. Paste into config (remove quotes if needed)

### Method 2: Common Patterns
Try these common selectors:

Price selectors:
- '.price'
- '.price-current'
- '[data-price]'
- '.amount'
- '.cost'

Title selectors:
- 'h1'
- '.product-title'
- '.product-name'
- '[data-product-title]'

## Real Website Examples 🌐

### Amazon Product
json
{
  "name": "Amazon Product",
  "url": "https://amazon.com/dp/PRODUCT_ID",
  "price_selector": ".a-price-whole",
  "title_selector": "#productTitle",
  "target_price": 50.00
}

### eBay Listing
json
{
  "name": "eBay Item",
  "url": "https://ebay.com/itm/ITEM_ID",
  "price_selector": ".notranslate",
  "title_selector": "h1#x-title-label-lbl",
  "target_price": 75.00
}

## Scheduling Options ⏰

### Run Every 6 Hours (Default)
bash
python scripts/price_tracker.py --schedule

### Custom Intervals
Edit the script to change timing:
python
# Every 2 hours
schedule.every(2).hours.do(self.run_tracker)

# Every day at 9 AM
schedule.every().day.at("09:00").do(self.run_tracker)

# Every Monday
schedule.every().monday.do(self.run_tracker)

## Data Analysis 📊

### View Price History
The tracker saves data in both CSV and JSON formats:

CSV Format (Excel-friendly):
csv
name,url,current_price,target_price,timestamp,price_dropped
iPhone 15,https://...,899.99,999.99,2024-01-15T10:30:00,true

JSON Format (programming-friendly):
json
[
  {
    "name": "iPhone 15",
    "current_price": 899.99,
    "target_price": 999.99,
    "timestamp": "2024-01-15T10:30:00",
    "price_dropped": true
  }
]

## Email Alert Customization 📧

### Custom Email Template
Edit the 'send_email_alert' method:
python
body = f"""
🎉 PRICE ALERT! 🎉

{product_data['name']} is now ${product_data['current_price']:.2f}
(was targeting ${product_data['target_price']:.2f})

Buy now: {product_data['url']}
"""

### Multiple Recipients
json
"email": {
  "recipient_email": "buyer1@gmail.com,buyer2@gmail.com"
}

## Troubleshooting Common Issues 🔧

### Issue: "Price element not found"
Solution:
1. Check if selector is correct
2. Website may have changed layout
3. Try different selector patterns

### Issue: "Request blocked" or 403 error
Solution:
1. Add delays between requests
2. Use different user-agent strings
3. Check if site allows scraping

### Issue: Email not sending
Solution:
1. Verify app password (not regular password)
2. Check Gmail 2FA is enabled
3. Test email settings separately

### Issue: Script stops running
Solution:
1. Check logs in 'price_tracker.log'
2. Add error handling for specific sites
3. Use try-catch blocks around problematic code

## Best Practices 🌟

### 1. Be Respectful
- Don't check prices more than once per hour
- Add delays between requests
- Respect robots.txt files

### 2. Test First
- Always run one-time check before scheduling
- Verify selectors work correctly
- Test email alerts

### 3. Monitor Logs
- Check 'price_tracker.log' regularly
- Watch for pattern changes
- Update selectors when needed

### 4. Backup Configuration
- Keep backup of working 'config.json'
- Document working selectors
- Save successful configurations

## Advanced Features 🚀

### Multiple Price Thresholds
json
{
  "name": "Laptop",
  "url": "https://...",
  "price_selector": ".price",
  "title_selector": "h1",
  "target_price": 800,
  "alert_levels": [1000, 900, 800, 700]
}


### Price History Tracking
The script automatically saves historical data. You can analyze trends:
python
import pandas as pd
df = pd.read_csv('price_data_20240115_103000.csv')
print(df.groupby('name')['current_price'].mean())

### Webhook Integration
Instead of email, send to Discord/Slack:
python
import requests

def send_webhook_alert(self, product_data):
    webhook_url = "https://hooks.slack.com/..."
    message = f"Price drop: {product_data['name']} - ${product_data['current_price']}"
    requests.post(webhook_url, json={"text": message})

## Getting Help 🆘

1. Check the logs first: 'price_tracker.log'
2. Test selectors in browser developer tools
3. Verify configuration syntax with JSON validator
4. Start simple with one product first
5. Use one-time runs before scheduling

Happy price tracking! 🎯
