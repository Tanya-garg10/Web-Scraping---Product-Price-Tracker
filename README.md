# Product Price Tracker 🛒

A Python web scraper that monitors product prices from e-commerce websites and sends email alerts when prices drop below your target threshold.

## Features ✨

- **Multi-site Support**: Track products from different e-commerce websites
- **Email Alerts**: Get notified instantly when prices drop
- **Data Storage**: Save price history in CSV and JSON formats
- **Scheduled Monitoring**: Automatic price checking at regular intervals
- **Error Handling**: Robust error handling and logging
- **Configurable**: Easy setup through JSON configuration

## Installation 📦

1. **Clone or download the project files**

2. **Install required packages:**
\`\`\`bash
pip install requests beautifulsoup4 schedule
\`\`\`

3. **Set up Gmail App Password:**
   - Go to Google Account settings
   - Enable 2-Factor Authentication
   - Generate an App Password for "Mail"
   - Use this app password in your config

## Configuration ⚙️

### 1. Edit `config.json`

\`\`\`json
{
  "products": [
    {
      "name": "Your Product Name",
      "url": "https://store.com/product-url",
      "price_selector": ".price-class",
      "title_selector": "h1.title",
      "target_price": 99.99
    }
  ],
  "email": {
    "sender_email": "your-email@gmail.com",
    "app_password": "your-app-password",
    "recipient_email": "alerts@gmail.com"
  },
  "check_interval_hours": 6,
  "data_format": "both"
}
\`\`\`

### 2. Finding CSS Selectors

To find the right selectors for price and title:

1. **Open the product page in your browser**
2. **Right-click on the price → Inspect Element**
3. **Copy the CSS selector or class name**
4. **Repeat for the product title**

**Common price selectors:**
- Amazon: `.a-price-whole`
- eBay: `.notranslate`
- Generic: `.price`, `[data-price]`, `.amount`

## Usage 🚀

### One-time Price Check
\`\`\`bash
python scripts/price_tracker.py
\`\`\`

### Scheduled Monitoring
\`\`\`bash
python scripts/price_tracker.py --schedule
\`\`\`

### Example Output
\`\`\`
🔥 PRICE DROP! Gaming Laptop: $899.99
📊 No change Wireless Headphones: $199.99
\`\`\`

## File Structure 📁

\`\`\`
price-tracker/
├── scripts/
│   └── price_tracker.py      # Main script
├── config.json               # Configuration file
├── .env.example              # Environment variables template
├── README.md                 # This file
├── price_tracker.log         # Log file (auto-generated)
├── price_data_YYYYMMDD_HHMMSS.csv  # Price data (auto-generated)
└── price_data_YYYYMMDD_HHMMSS.json # Price data (auto-generated)
\`\`\`

## Configuration Options 🔧

| Option | Description | Default |
|--------|-------------|---------|
| `check_interval_hours` | Hours between price checks | 6 |
| `data_format` | Save format: "csv", "json", or "both" | "both" |
| `target_price` | Price threshold for alerts | Required |

## Troubleshooting 🔧

### Common Issues:

1. **"Price element not found"**
   - Check if the CSS selector is correct
   - Website might have changed their layout
   - Try inspecting the element again

2. **Email not sending**
   - Verify Gmail app password is correct
   - Check if 2FA is enabled on Gmail
   - Ensure sender email matches the app password account

3. **Request blocked**
   - Some sites block automated requests
   - The script includes user-agent headers to help
   - Consider adding delays between requests

### Debugging:

- Check `price_tracker.log` for detailed error messages
- Test individual product URLs manually
- Verify CSS selectors in browser developer tools

## Legal Considerations ⚖️

- **Respect robots.txt**: Check website's robots.txt file
- **Rate limiting**: Don't overwhelm servers with requests
- **Terms of service**: Ensure compliance with website ToS
- **Personal use**: This tool is intended for personal price monitoring

## Advanced Usage 🔬

### Adding New Products:

1. Find the product page URL
2. Inspect price and title elements
3. Add to `config.json` products array
4. Test with one-time run first

### Custom Scheduling:

Modify the schedule in `start_scheduled_tracking()`:
\`\`\`python
# Check every 2 hours
schedule.every(2).hours.do(self.run_tracker)

# Check daily at 9 AM
schedule.every().day.at("09:00").do(self.run_tracker)
\`\`\`

## Contributing 🤝

Feel free to submit issues and enhancement requests!

## License 📄

This project is for educational purposes. Use responsibly and in accordance with website terms of service.

