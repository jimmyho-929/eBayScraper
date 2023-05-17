import requests
from bs4 import BeautifulSoup
import csv
import re

def get_ebay_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def parse_ebay_product_data(product):
# This code is supposed to help scrape for title listings and replace 'N/A' results    
# =============================================================================
#     title_tag = product.find("span", role_="heading")
#     title = title_tag.text if title_tag else product.find("div", class_="s-item__title").text.strip()
# =============================================================================
    title_tag = product.find("h3", class_="s-item__title")
    title = title_tag.text if title_tag else "N/A"
    price_tag = product.find("span", class_="s-item__price")
    price = price_tag.text if price_tag else "N/A"
    manufacturer_tag = product.find("span", class_="s-item__seller-info-text")
    manufacturer = manufacturer_tag.text if manufacturer_tag else "N/A"
    watchers_tag = product.find("span", class_="s-item__hotness s-item__itemHotness")
    watchers = watchers_tag.text.strip() if watchers_tag else "N/A"
    units_sold_tag = product.find("span", class_="s-item__dynamic s-item__additionalItemInfo")
    units_sold = units_sold_tag.text if units_sold_tag else "N/A"
    url_tag = product.find("a", class_="s-item__link")
    url = url_tag["href"] if url_tag else "N/A"
    condition_tag = product.find("span", class_="SECONDARY_INFO")
    condition = condition_tag.text if condition_tag else "N/A"

    seller_match = re.search(r'(.+)\s\((\d+)\)\s([\d.]+%)', manufacturer)
    if seller_match:
        seller, num_ratings, rating = seller_match.groups()
    else:
        seller, num_ratings, rating = "N/A", "N/A", "N/A"

    return {
        "title": title,
        "price": price,
        "Condition": condition,
        "Seller": seller,
        "Number of Ratings": num_ratings,
        "Rating": rating,
        "Watchers": watchers,
        "Units Sold": units_sold,
        "URL": url,
    }

def save_to_csv(products, filename):
    keys = products[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(products)

def main():
    base_url = "https://www.ebay.com/sch/i.html?_nkw=kitchen+appliances&_sacat=0&_ipg=100&_pgn="
    max_products = 250
    products = []

    page = 1
    while len(products) < max_products:
        url = base_url + str(page)
        soup = get_ebay_data(url)

        products_list = soup.find_all("div", class_="s-item__info clearfix")
        print(f"Products found on page {page}: {len(products_list)}")

        for product in products_list:
            if len(products) >= max_products:
                break

            product_data = parse_ebay_product_data(product)
            products.append(product_data)

        page += 1

    if not products:
        print("No products found.")
        return

    save_to_csv(products, "kitchen_appliances.csv")
    print(f"Data saved to kitchen_appliances.csv. Total products scraped: {len(products)}")
if __name__ == "__main__":
    main()
