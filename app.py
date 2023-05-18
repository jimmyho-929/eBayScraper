import streamlit as st
import os
import shutil
import time
import threading
import pandas as pd
from scraper_ebay import main as scrape_ebay

def create_download_link(filename):
    with open(filename, "rb") as f:
        st.download_button(
            label="Download CSV",
            data=f,
            file_name="kitchen_appliances.csv",
            mime="text/csv",
        )

def convert_price(price):
    if ' to ' in price:
        low, high = price.split(' to ')
        return (float(low) + float(high)) / 2
    else:
        return float(price)

st.title("Creospan's eBay Scraper!!")

st.markdown("Welcome to Creospan's eBay Scraper! Press the button below to scrape and export a list of current listings.")

if st.button("Scrape eBay Listings"):
    progress = st.progress(0)
    progress_pct = 0

    # Start a separate thread for the eBay scraping
    def run_scrape():
        global progress_pct
        scrape_ebay()
        progress_pct = 100

    t = threading.Thread(target=run_scrape)
    t.start()

    # Update the progress bar in the main thread
    while progress_pct < 100:
        progress.progress(progress_pct)
        progress_pct += 2
        time.sleep(0.15)

    t.join()  # Wait for the scraping thread to complete

    # Load the scraped data
    data = pd.read_csv("kitchen_appliances.csv")

    # # Make sure 'price' column is numeric.
    data['price'] = data['price'].str.replace('$', '').apply(convert_price)
    
    # # Display the data in a table
    st.dataframe(data)
    
     # Display some basic statistics
    st.markdown(f"Number of products: {len(data)}")
    st.markdown(f"Average price: ${data['price'].mean():.2f}")
    #st.markdown(f"Number of free shipping offers: {data['Free Shipping'].sum()}")
    
     #Display a histogram of prices
    st.bar_chart(data['price'])
    
    create_download_link("kitchen_appliances.csv")


    # Recomended buys
        # # Make sure 'price' column is numeric.
        # if data['price'].dtype == 'object':
        #     data['price'] = data['price'].apply(lambda x: str(x).replace('$', '') if isinstance(x, str) else x)
        #     data['price'] = data['price'].apply(convert_price)
        #
        # # Load the recommended buys
        # with open('kitchen_appliances.csv', 'r') as f:
        #     reader = csv.DictReader(f)
        #     recommended_buys = [row for row in reader][-3:]  # assuming the recommended buys are the last 3 lines
        #
        # # Display the recommended buys
        # for i, recommended_buy in enumerate(recommended_buys):
        #     recommended_buy_title = recommended_buy.get('title', 'N/A')
        #     recommended_buy_price = recommended_buy.get('price', 'N/A')
        #     st.markdown(f"Recommended Buy #{i+1}: {recommended_buy_title} for {recommended_buy_price}")
        #
        #     if st.button(f"Buy Now #{i+1}"):
        #         print("recommended_buy: ")
        #         print(recommended_buy['URL'])
        #         webbrowser.open(recommended_buy['URL'])
        #
        # # Make sure 'price' column is numeric.
        # if data['price'].dtype == 'object':
        #     data['price'] = data['price'].apply(lambda x: str(x).replace('$', '') if isinstance(x, str) else x)
        #     data['price'] = data['price'].apply(convert_price)
        # else:
        #     data['price'] = data['price'].apply(convert_price)
