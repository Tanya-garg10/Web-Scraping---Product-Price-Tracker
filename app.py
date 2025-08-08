import streamlit as st
import json
from scraper import get_price

st.title("🛒 Flipkart Product Price Tracker")

with open("config.json") as f:
    config = json.load(f)

url = config["product_url"]
target_price = config["target_price"]

st.markdown(f"### Tracking: [Product Link]({url})")
st.write(f"Target Price: ₹{target_price}")

if st.button("Check Current Price"):
    current_price = get_price(url)
    if current_price:
        st.success(f"Current Price: ₹{current_price}")
        if current_price <= target_price:
            st.balloons()
            st.success("Good time to buy! 🟢")
        else:
            st.warning("Still above your target price. 🔴")
    else:
        st.error("Couldn't fetch the price.")
