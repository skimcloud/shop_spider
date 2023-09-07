from pathlib import Path
from datetime import datetime

import scrapy
import re
import random

class ShopSpider(scrapy.Spider):
    name = "shoppy"
    product_names = []
    page_number = 1
    # Future: Have updating store urls by automating browser events to search for product and then obtaining link structure
        # Feed AI model HTML code to find target for automated browser event # Too resource intensive
        # Use web crawler (search engine to find search link and then process the link structure )
    # Dynamic list of stores based on product from Google
    
    # store_urls = {"amazon": "https://www.amazon.com/s?k=", "walmart": "https://www.walmart.com/search?q="}
    stores = {"amazon", "walmart", "bestbuy"}
    # postfix = {"amazon": "&page=", "walmart": "&page="}

    user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/88.0.705.74 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/88.0.705.74 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.78',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.52',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36 Edg/94.0.992.31',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.20',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        ]
    
    def start_requests(self):
        url = "https://kobolldo-dev.herokuapp.com/apis/dashboard/items?section=SUGGESTIONS&offset=0&limit=10"
        # yield scrapy.Request(url=url, callback=self.getPrices)
        yield scrapy.Request(url=url, callback=self.get_google_results)

    def get_google_results(self, response):
        pattern = r'"shortDescription":"([^"]*)"'
        names = re.findall(pattern, response.text)
        processed_names = [name.replace(" ", "+") for name in names]

        main_url = "https://www.google.com/search?q=site%3A"
        for store in self.stores:
            for product_name in processed_names:
                google_url = f"{main_url}www.{store}.com+search+{product_name}"
                user_agent = random.choice(self.user_agents)
                headers = {'User-Agent': user_agent}
                yield scrapy.Request(
                    url=google_url,
                    callback=self.parse_google_results,
                    headers=headers,
                    meta={'store': store, 'product_name': product_name}
                )
    
    def parse_google_results(self, response):
        store = response.meta['store']
        product_name = response.meta['product_name']

        # Extract all URLs from the Google search results page

        #pattern = r'https://www\.\w+\.\w+(?:/\S*)?'
        pattern = rf'https://www\.{re.escape(store)}\.com\S*'
        urls = re.findall(pattern, response.text)
        self.log(f"Store: {store}")
        self.log(f"Searching for product: {product_name}")
        for url in urls:
            self.log(url)
            if store in url and product_name in url:
                self.log("INSIDE PARSE GOOGLE RESULTS BRUH")
                self.log(url)
                user_agent = random.choice(self.user_agents)
                headers = {'User-Agent': user_agent}
                yield scrapy.Request(
                    url=url,
                    callback=self.check_result,
                    meta={'result_url': url, 'store': store, 'product_name': product_name},
                    headers=headers
                )
    
    def check_result(self, response):
        self.log("Top check_result")
        result_url = response.meta['result_url']
        store = response.meta['store']
        product_name = response.meta['product_name']
        
        price_pattern = r'\$\d+\.\d{2}'  # Example: $123.45
        prices = re.findall(price_pattern, response.text) # Find all matches of the price pattern in the raw text
        if len(prices) > 5:
            self.log("BROSKI!!")
            self.log("Ready to write prices: > len(5)")
            mean = sum(float(price[1:]) for price in prices[:6]) / 6.0 # mean price calculation
            lower_threshold = mean - (mean * 0.60)
            upper_threshold = mean + (mean * 0.60)
            processed_prices = []
            for num in prices:
                stripped_price = float(num[1:])
                if lower_threshold <= stripped_price <= upper_threshold:
                    processed_prices.append(stripped_price)
                    print(f"{num} is within the ±60% threshold of {mean}")
                else:
                    print(f"{num} is NOT within the ±60% threshold of {mean}")

            minimum = min(processed_prices)
            maximum = max(processed_prices)
            
            for price in processed_prices:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                self.log(f'Found price: {price} for product: {product_name} at time {current_time}')

            # Save the extracted prices to a file
            page = response.url
            with open(f'{product_name}_prices.txt', 'a') as f:
                for price in processed_prices:
                    f.write(f'{price}\n')
                    f.write(f'{price} at time {current_time} from {page}\n')
                f.write(f'*****max: {maximum}\n')
                f.write(f'*****min: {minimum}\n')
        
        self.log('Price extraction complete')

    # get_prices function version which does no product name processing, gets array directly
    def array_get_prices(self, processed_names):
        # processed_names = [name.replace(" ", "+") for name in names]
        for key in self.store_urls:
            for product_name in processed_names:
                user_agent = random.choice(self.user_agents)
                headers = {'User-Agent': user_agent}
                self.page_number = 1 # Reset page number with each product
                yield scrapy.Request(
                    url=f"{self.store_urls[key]}{product_name}",
                    callback=self.parse,
                    meta={'store_url': self.store_urls[key], 'product_name': product_name, 'page_number': self.page_number},
                    headers=headers
                )

    # Change parameter to processed names instead of response
    # Move + sign processing into start_requests
    def get_prices(self, response):
        # link = meta
        # post = meta
        pattern = r'"shortDescription":"([^"]*)"'
        names = re.findall(pattern, response.text)
        processed_names = [name.replace(" ", "+") for name in names]

        # for product_name in processed_names:
        #    user_agent = random.choice(self.user_agents)
        #    headers = {'User-Agent': user_agent}
        #    self.page_number = 1 # Reset page number with each product
        #    yield scrapy.Request(
        #        url=f"https://www.amazon.com/s?k={product_name}",
        #        callback=self.parse,
        #        meta={'product_name': product_name, 'page_number': self.page_number},
        #        headers=headers
        #    )
        for key in self.store_urls:
            for product_name in processed_names:
                user_agent = random.choice(self.user_agents)
                headers = {'User-Agent': user_agent}
                self.page_number = 1 # Reset page number with each product
                yield scrapy.Request(
                    # Change url to given url in crawl meta data
                    url=f"{self.store_urls[key]}{product_name}",
                    callback=self.parse,
                    # Eventually change this meta data to only left link{product_name},{postfix} and page_number
                    meta={'store_url': self.store_urls[key], 'product_name': product_name, 'page_number': self.page_number},
                    headers=headers
                )

    # Create parse function with link as parameter to get rid of link processing altogether, we can get links directly from crawl

    def parse(self, response):
        # page = response.url.split("=")[-1]
        # Future: Randomize product + page number call to guarantee efficient scraping

        # product_name = self.product_names[self.page_number % len(self.product_names)]
        store = response.meta['store_url']
        product_name = response.meta['product_name']
        self.page_number = response.meta['page_number']
        # self.log(f'Now scraping: {product_name} - Page {self.page_number}')
        self.log(f'Now scraping: {product_name} - Page {self.page_number} - Store {store}')

        raw_text = response.text
        
        # Regular expression pattern for identifying prices
        price_pattern = r'\$\d+\.\d{2}'  # Example: $123.45

        # Find all matches of the price pattern in the raw text
        prices = re.findall(price_pattern, raw_text)

        page = response.url

        # Backtest mean5 avg calculation with historical data
        # Use recursive function to figure out which n in sum(mean[:n])/n is results in a value closest to "priceValue" from API

        # Use mean price as "real price" and makes sure it doesn't deviate too high when calculating minimum and maximum 60% threshhold
        mean5 = sum(float(price[1:]) for price in prices[:8]) / 8.0 # mean price calculation
        lower_threshold = mean5 - (mean5 * 0.60)
        upper_threshold = mean5 + (mean5 * 0.60)
        processed_prices = []
        for num in prices:
            stripped_price = float(num[1:])
            if lower_threshold <= stripped_price <= upper_threshold:
                processed_prices.append(stripped_price)
                print(f"{num} is within the ±60% threshold of {mean5}")
            else:
                print(f"{num} is NOT within the ±60% threshold of {mean5}")

        minimum = min(processed_prices)
        maximum = max(processed_prices)
        
        for price in processed_prices:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            # self.log(f'Found price: {price} on page: {self.page_number} for product: {product_name}')
            self.log(f'Found price: {price} on page: {self.page_number} for product: {product_name} at time {current_time}')
        
        self.log("Size of processed_prices: ", len(processed_prices))

        # Save the extracted prices to a file
        with open(f'{product_name}_prices.txt', 'a') as f:
            for price in processed_prices:
                f.write(f'{price}\n')
                f.write(f'{price} at time {current_time} from {page}\n')
            f.write(f'*****max: {maximum}\n')
            f.write(f'*****min: {minimum}\n')
        
        self.log('Prices processed')

        # if len(processed_prices < 20):
        #   # Construct the URL for the next page
        #    self.page_number += 1 # Increment page number
        #    # next_page_url = f'https://www.amazon.com/s?k={product_name}&page={self.page_number}'
        #    next_page_url = f'store_urls[store]{product_name}postfix[store]{self.page_number}'
        #    
        #    user_agent = random.choice(self.user_agents)
        #    headers = {'User-Agent': user_agent}
        #    yield scrapy.Request(
        #        url=next_page_url,
        #        callback=self.parse,
        #        meta={'product_name': product_name, 'page_number': self.page_number},
        #        headers=headers
        #    )

        self.log('Price extraction complete')