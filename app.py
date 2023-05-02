import streamlit as st
import os
import shutil
import time
from scraper_ebay import main as scrape_ebay

def create_download_link(filename):
    with open(filename, "rb") as f:
        st.download_button(
            label="Download CSV",
            data=f,
            file_name="kitchen_appliances.csv",
            mime="text/csv",
        )

st.title("Creospan's eBay Scraper")

st.markdown("Welcome to Creospan's eBay Scraper! Press the button below to scrape and export a list of current listings.")

if st.button("Scrape eBay Listings"):
    progress = st.progress(0)
    progress_pct = 0

    # Start a separate thread for the eBay scraping
    def run_scrape():
        global progress_pct
        scrape_ebay()
        progress_pct = 100

    import threading
    t = threading.Thread(target=run_scrape)
    t.start()

    # Update the progress bar in the main thread
    while progress_pct < 100:
        progress.progress(progress_pct)
        progress_pct += 2
        time.sleep(0.15)

    t.join()  # Wait for the scraping thread to complete
    create_download_link("kitchen_appliances.csv")
