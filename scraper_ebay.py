import requests
from bs4 import BeautifulSoup
import csv
import re
import webbrowser
from collections import defaultdict

def get_ebay_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def parse_ebay_product_data(product):
    title_tag = product.find("h3", class_="s-item__title")
    title = title_tag.text if title_tag else "N/A"
    price_tag = product.find("span", class_="s-item__price")
    # price = price_tag.text.replace('$', '') if price_tag else "N/A"
    price = price_tag.text if price_tag else "N/A"
    # price = convert_price(price)
    # price = convert_price(price)
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
    brand_match = re.search(r'\b(\w+)\b', title) # Extract brand from the title
    brand = brand_match.group(0) if brand_match else "N/A"
    shipping_tag = product.find("span", class_="s-item__shipping s-item__logisticsCost")
    free_shipping = "Free shipping" in shipping_tag.text if shipping_tag else False

    # Sort data to make buy recommendations
    # for product_name in product:
    #     if isinstance(product_name["price"], str):
    #         price_values = [float(val) for val in re.findall(r'\d+\.\d+', product_name["price"])]
    #         if price_values:
    #             brand_prices[product_name["Brand"]].append(price_values[0])
    #     if product_name["Free Shipping"]:
    #         free_shipping_count += 1

    # Convert Number of Ratings, Rating, and Price into sortable numeric values
    for product_name in product:
        product_name["Number of Ratings"] = int(product_name["Number of Ratings"]) if product_name["Number of Ratings"] != "N/A" else 0
        product_name["Rating"] = float(product_name["Rating"].replace('%', '')) if product_name["Rating"] != "N/A" else 0
        product_name["price"] = convert_price(product_name["price"].replace('$', '')) if "$" in product_name["price"] else float('inf')

    # Sort by number of ratings, seller rating, and price, then take the top 3
    recommended_buys = sorted(product, key=lambda p: (p['Number of Ratings'], p['Rating'], p['price']), reverse=True)[:3]

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
        "Brand": brand,
        "Free Shipping": free_shipping,
        "Recommended Buys": recommended_buys,
    }

def save_to_csv(products, filename):
    keys = products[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(products)

def analyze_data(products):
    brand_prices = defaultdict(list)
    free_shipping_count = 0

    for product in products:
        if isinstance(product["price"], str):
            price_values = [float(val) for val in re.findall(r'\d+\.\d+', product["price"])]
            if price_values:
                brand_prices[product["Brand"]].append(price_values[0])
        if product["Free Shipping"]:
            free_shipping_count += 1

    # Convert Number of Ratings, Rating, and Price into sortable numeric values
    for product in products:
        product["Number of Ratings"] = int(product["Number of Ratings"]) if product["Number of Ratings"] != "N/A" else 0
        product["Rating"] = float(product["Rating"].replace('%', '')) if product["Rating"] != "N/A" else 0
        product["price"] = convert_price(product["price"].replace('$', '')) if "$" in product["price"] else float('inf')

    avg_prices = {brand: sum(prices) / len(prices) for brand, prices in brand_prices.items()}
    most_popular_brands = sorted(avg_prices, key=avg_prices.get, reverse=True)[:3]
    free_shipping_ratio = free_shipping_count / len(products)

    # Sort by number of ratings, seller rating, and price, then take the top 3
    recommended_buys = sorted(products, key=lambda p: (p['Number of Ratings'], p['Rating'], p['price']), reverse=True)[:3]

    return {
        "Average Prices": avg_prices,
        "Most Popular Brands": most_popular_brands,
        "Free Shipping Ratio": free_shipping_ratio,
        "Recommended Buys": recommended_buys,
    }


def convert_price(price):
    if price == "N/A":
        return price
    if ' to ' in price:
        low, high = price.split(' to ')
        return (float(low) + float(high)) / 2
    else:
        return float(price)

def save_aggregated_data_to_csv(aggregated_data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Brand", "Average Price"])
        for brand, avg_price in aggregated_data["Average Prices"].items():
            writer.writerow([brand, avg_price])

        writer.writerow(["Most Popular Brands"])
        writer.writerow(aggregated_data["Most Popular Brands"])

        writer.writerow(["Free Shipping Ratio"])
        writer.writerow([aggregated_data["Free Shipping Ratio"]])


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

            product_price = product.get('price', 'N/A')
            product['price'] = convert_price(product_price)
            product_data = parse_ebay_product_data(product)
            products.append(product_data)

        page += 1

    if not products:
        print("No products found.")
        return

    save_to_csv(products, "kitchen_appliances.csv")
    print(f"Data saved to kitchen_appliances.csv. Total products scraped: {len(products)}")
    aggregated_data = analyze_data(products)
    save_aggregated_data_to_csv(aggregated_data, "aggregated_kitchen_appliances_data.csv")
    print(f"Aggregated data saved to aggregated_kitchen_appliances_data.csv.")

if __name__ == "__main__":
    main()
