# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
"""
Created on Tue Jan 12 02:45:05 2021
@author: mahmoud
"""

"""
    *******   PyCharm IDE has been used in this project with Python2.7   *******
"""

import requests
from bs4 import BeautifulSoup
import csv

f = csv.writer(open("Data Crawled From Jumia.csv", "w"))
f.writerow(['Company Name', 'Product Name', 'Page URL', 'Page Number', 'Image Link', 'Price range', 'Rating'])

print("Please enter your link to scrap: ")
# example link: "https://www.jumia.com.eg/catalog/?q=macbook+pro"
url = input()
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

products = soup.findAll(class_="prd _fb col c-prd")

productsList = []

i = 0
while 1:
    pages = soup.findAll(class_="pg _act")
    for product in products:
        product_page = pages[0].get_text()
        product_name = product.find(class_="name").get_text()
        company_name = product.find('a')['data-brand']
        price = product.find(class_="prc").get_text()
        page_url = "https://www.jumia.com.eg" + product.find('a')['href']

        try:
            rating = product.find(class_="stars _s").get_text()
        except:
            rating = 'No Rating!'

        image_link = product.find(class_="img-c").find('img')['data-src']
        d = [company_name, product_name, page_url, product_page, image_link, price, rating]
        productsList.append(d)
    tempUrl = url+"&page="+str((i+2))+"#catalog-listing"
    response = requests.get(tempUrl)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.findAll(class_="prd _fb col c-prd")
    i += 1
    if not pages:
        break
    print("Scraping Page " + pages[0].get_text())

productsList.sort(key=lambda e: e[0])
for product in productsList:
    f.writerow([product[0], product[1], product[2], product[3], product[4], product[5], product[6]])

print ("\n*** Done Scraping! ***")
