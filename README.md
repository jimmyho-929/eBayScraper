# Creospan's eBay Scraper
Demo: https://ebay-scraper-smzlbqiv4q-uc.a.run.app/

![scraper screenshot](https://github.com/jsocarras/eBayScraper/assets/37901304/f1f74ea9-836e-48a0-a490-be73be5d9e46)

## Introduction
Creospan's eBay Scraper is a powerful tool that simplifies the process of scraping eBay product listings. Built using Python, this application can be run locally or deployed as a web app. The scraper searches for kitchen appliances on eBay and exports the collected data to a CSV file. With an easy-to-use web interface, users can download the CSV containing the data, making it convenient for further analysis or processing.

## Value Proposition Thesis
Our solution is a highly adaptable and extendable web scraper system that can be customized to extract data from any eCommerce platform like Amazon, eBay, etc. It is designed with a microservices-first approach, making it easy to add new features such as user authentication, transaction history, and more. This system can help businesses access vital eCommerce data, understand market trends, assess product pricing strategies, and eventually even automate the purchase of underpriced products. It's an all-in-one tool for data-driven decision making in eCommerce.

## Possible Go-To-Market Strategies
### Go-to-Market Strategy 1: SaaS Model
Launch the scraper as a web application where users can subscribe on a monthly or yearly basis to use your service. They can input what data they want to scrape, and our service will provide them with the scraped data in a structured format such as CSV. This is a straightforward approach, easily measurable by user acquisition, engagement and subscription revenue.

### Go-to-Market Strategy 2: Custom Solutions Provider
Instead of a standalone web app, we could offer our service as a custom solutions provider. Customers would describe what they need, and we would provide them a fully functioning scraper program. We could charge a fee for the initial setup, and then a maintenance fee for keeping the program updated and functional. This approach will be more resource-intensive but might attract larger businesses and lead to bigger deals.

### Go-to-Market Strategy 3: Data Reseller
Use our scraper to gather eCommerce data, analyze it for insights, and then sell these insights to interested parties. This could be pricing data, popular products, trends over time, etc. We could set up a subscription service for regular reports or charge on a per-report basis. It would be easy to measure the success of this model by the number of reports sold or subscriptions received.

### Go-to-Market Strategy 4: Product Arbitrage
Use our scraper to automatically find undervalued products, buy them, and then resell them at a higher price. This would require some initial investment and would involve more risk, but the potential rewards could also be significant. This strategy would be measured by the profit made from buying and selling products.


## Getting Started
### Prerequisites
To run the eBay Scraper locally, you will need:

Python 3.8 or higher
pip (Python package installer)

## Installation
Clone the GitHub repository or download the source code as a ZIP file:
git clone https://github.com/your_username/ebay_scraper.git

Navigate to the project directory:
cd ebay_scraper

Install the required Python packages:
pip install -r requirements.txt

## Running the Scraper
To run the scraper locally, use the following command:
python scraper_ebay.py
This will save the scraped data to a file named kitchen_appliances.csv in the project directory.

Alternatively, you can access the deployed web app at https://ebay-scraper-smzlbqiv4q-uc.a.run.app/. Click the "Scrape eBay Listings" button to begin the scraping process, and then download the CSV file once the scraping is complete.

# Code Overview
The eBay Scraper comprises two main components:
1. scraper_ebay.py: The core script responsible for scraping eBay product listings.
2. app.py: The Streamlit web app that provides a user-friendly interface for interacting with the scraper.

### scraper_ebay.py:
This script contains several functions that work together to scrape eBay listings:
- get_ebay_data(url): Sends an HTTP request to the specified URL and returns a BeautifulSoup object containing the page content.
- parse_ebay_product_data(product): Extracts relevant product information from the BeautifulSoup object and returns a dictionary containing the data.
- save_to_csv(products, filename): Writes the scraped product data to a CSV file.

The main() function orchestrates the scraping process by generating URLs for each eBay search results page, calling get_ebay_data() to fetch the page content, and then parsing and saving the product data.

### app.py:
This script uses Streamlit to create a web app that allows users to interact with the eBay Scraper. When the "Scrape eBay Listings" button is clicked, the app calls the scrape_ebay() function from scraper_ebay.py. Once the scraping is complete, a "Download CSV" button is displayed, allowing users to download the kitchen_appliances.csv file.

A progress bar is also displayed during the scraping process to provide visual feedback to the user.

### Dockerization and Deployment:
#### All Commands:
gcloud init

gcloud config set project creospandataanalyzer

docker build -t gcr.io/creospandataanalyzer/ebay-scraper .

docker login

docker scan gcr.io/creospandataanalyzer/ebay-scraper

docker push gcr.io/creospandataanalyzer/ebay-scraper

gcloud run deploy ebay-scraper \
--image gcr.io/creospandataanalyzer/ebay-scraper \
--platform managed \
--port 8501 \
--memory 1Gi \
--allow-unauthenticated \
--region us-central1 \
--set-env-vars=STREAMLIT_SERVER_PORT=8501

#### Explanation:
The eBay Scraper web app is containerized using Docker, with the Dockerfile specifying the necessary steps to build the Docker image.

To deploy the Dockerized app to Google Cloud Platform (GCP), we used Google Cloud Run, a fully managed serverless platform that enables running stateless containers.

The deployment process involves building the Docker image, pushing it to the Google Container Registry (GCR), and then deploying it to Cloud Run. The web app is then accessible through a generated URL.

Build the Docker Image: docker build -t gcr.io/creospandataanalyzer/ebay-scraper .

Push the Docker image to Google Container Registry: docker push gcr.io/creospandataanalyzer/ebay-scraper

Deploy Streamlit app to Cloud Run:
gcloud run deploy ebay-scraper \
  --image gcr.io/creospandataanalyzer/ebay-scraper \
  --platform managed \
  --port 8501 \
  --memory 1Gi \
  --allow-unauthenticated \
  --region us-central1 \
  --set-env-vars=STREAMLIT_SERVER_PORT=8501

### Additional Information:
The eBay Scraper is a flexible and easy-to-use tool that can be extended to scrape additional product categories or incorporate additional features. By providing a user-friendly web interface and detailed documentation, we hope to streamline the process of getting started with the eBay Scraper and make it accessible to both technical and non-technical users alike.

## Troubleshooting and Common Issues
#### Timeout Error
If you encounter a timeout error during the scraping process, it may be caused by a slow internet connection or a temporary issue with the eBay website. In this case, try rerunning the script or refreshing the web app.
#### Missing Data
If some fields in the CSV file are marked as "N/A," it could mean that the data was not available in the eBay listing, or the scraper failed to parse the data correctly. Double-check the URL associated with the product to confirm the data's availability.
#### Updating the Search Query
To modify the search query, update the base_url variable in scraper_ebay.py. Replace the search term in the URL with your desired query. For example, to search for "laptops" instead of "kitchen appliances," change the URL to:

base_url = "https://www.ebay.com/sch/i.html?_nkw=laptops&_sacat=0&_ipg=100&_pgn="

### Future Enhancements
- Add support for additional eBay categories or search filters.
- Implement user authentication to allow multiple users to access the web app simultaneously without affecting each other's scraping sessions.
- Integrate additional scraping sources or platforms to expand the app's capabilities.
- Implement a scheduling feature to automate the scraping process at specific intervals.
- Add data visualization tools within the web app to help users analyze the scraped data more effectively.
- Remember to ensure that your scraper respects the eBay robots.txt and terms of service to avoid any potential legal and ethical issues.

### Contributing
We welcome contributions from the community! To contribute, please follow these steps:
- Fork the repository on GitHub.
- Create a new branch for your changes.
- Make your changes and commit them to your branch.
- Create a pull request with a description of your changes.
- We will review your pull request and provide feedback. Once your changes are approved, they will be merged into the main repository.

### Support
If you have any questions, issues, or suggestions for improvement, please feel free to open an issue on the GitHub repository or contact the maintainers directly.

We appreciate your interest in Creospan's eBay Scraper and look forward to helping you make the most of this powerful tool!
