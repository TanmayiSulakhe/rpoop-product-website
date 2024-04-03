from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import numpy as np


HEADERS = ({'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
            'Accepted-Language' : 'en-US, en;q=0.5'})

def amazon_products(query,all_products):
    URL= "https://www.amazon.in/s?k=" 
    URL += query
    print(URL)
    webpage = requests.get(URL,headers=HEADERS) 

    soup = BeautifulSoup(webpage.content,"html.parser")


    sections = soup.find_all("div",attrs={'class':'sg-col-inner'})

    for div in sections:
        product_info = {}
        #name of product
        name = div.find('span',attrs={'class':'a-size-base-plus a-color-base a-text-normal'})
        if name is not None:
            product_info['name'] = name.get_text()
        else:
            continue
    
        #price of product
        price = div.find('span',attrs={'class':'a-offscreen'})
        if price is not None:
            product_info['price'] = price.get_text()
        else:
            continue

        #rating of product
        rating = div.find('span',attrs={'class':'a-icon-alt'})
        if rating is not None:
            stars = rating.get_text()
            product_info['rating'] = stars[:4]
            
        else:
            continue

        #product link
        link_to_product=div.find('a',attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        link_to_product = link_to_product.get('href')
        link_to_product = "https://www.amazon.in" + link_to_product
        if "www.amazon.inhttps" in link_to_product:
            print("link corrupted")
            continue
        else:
            product_info['link'] = link_to_product
        
        #image link
        image_tag = div.find('img',attrs={'class':'s-image'})
        if image_tag:
            product_info['image'] = image_tag['src']
        
        else:
            continue
    
        all_products.append(product_info)

def flipkart_products(query,all_products):
    
    URL = "https://www.flipkart.com/search?q=" + query
    print(URL)
    webpage = requests.get(URL,headers=HEADERS) 

    soup = BeautifulSoup(webpage.content,"html.parser")

    sections = soup.find_all("div", attrs={'data-id': True})
    
    for div in sections:
        product_info = {}
        #name of product
        name = div.find('a',attrs={'class':'IRpwTa'})
        if name is not None:
            product_info['name'] = name.get('title')
        else:
            continue
    
        #price of product
        price = div.find('div',attrs={'class':'_30jeq3'})
        if price is not None:
            product_info['price'] = price.get_text()
        else:
            continue

        #rating of product
        product_info['rating'] = 4

        #product link
        link_to_product=div.find("a",attrs={'class':'_2UzuFa'})
        link_to_product = link_to_product.get('href')
        link_to_product = "https://www.flipkart.com" + link_to_product
        if "https://www.flipkart.comhttps" in link_to_product:
            print("link corrupted")
            continue
        else:
            product_info['link'] = link_to_product
        
        #image link
        image_tag = div.find('img',attrs={'class':'_2r_T1I'})
        if image_tag:
            product_info['image'] = image_tag['src']
        
        else:
            continue
    
        all_products.append(product_info)
