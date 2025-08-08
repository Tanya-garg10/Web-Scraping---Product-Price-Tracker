import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def get_price(url):
    chromedriver_autoinstaller.install()  # Automatically installs correct driver

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    try:
        price_element = driver.find_element("xpath", '//div[contains(text(),"₹") or contains(text(),"₹")]/..')
        price_text = price_element.text.replace("₹", "").replace(",", "").strip()
        price = int(''.join(filter(str.isdigit, price_text)))
    except Exception as e:
        price = None
        print("Error:", e)

    driver.quit()
    return price
