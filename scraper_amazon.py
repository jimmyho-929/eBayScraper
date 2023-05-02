import requests
from bs4 import BeautifulSoup
import csv

def get_amazon_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def parse_product_data(product):
    title = product.find("span", class_="a-size-medium a-color-base a-text-normal").text
    price = product.find("span", class_="a-price-whole")
    price = price.text if price else "N/A"
    manufacturer = product.find("span", class_="a-size-base s-underline-text a-text-normal")
    manufacturer = manufacturer.text if manufacturer else "N/A"

    return {"title": title, "price": price, "manufacturer": manufacturer}

def save_to_csv(products, filename):
    keys = products[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(products)

def main():
    # url = "https://www.amazon.com/s?k=kitchen+appliances&i=garden&rh=n%3A1055398&dc"
    url = "https://www.amazon.com/Apple-Watch-Cellular-Midnight-Aluminum/product-reviews/B09PB1PTH8/ref=cm_cr_othr_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    soup = get_amazon_data(url)

    print(soup.prettify())
    products_list = soup.find_all("div", class_="s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col sg-col-12-of-16")

    print("Products found:", len(products_list))

    products = []
    for product in products_list[:100]:
        product_data = parse_product_data(product)
        products.append(product_data)

    if not products:
        print("No products found.")
        return

    save_to_csv(products, "kitchen_appliances.csv")
    print("Data saved to kitchen_appliances.csv")

if __name__ == "__main__":
    main()
