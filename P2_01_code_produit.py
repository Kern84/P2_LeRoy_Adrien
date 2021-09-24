#Script Python pour la récupération des informations pour un produit

import requests
from bs4 import BeautifulSoup
import csv

url = "http://books.toscrape.com/catalogue/meditations_33/index.html"
response = requests.get(url)
if response.ok:
    soup = BeautifulSoup(response.content, "html.parser")
en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
with open("P2_01_produit.csv", "w") as outf:
    writer = csv.writer(outf, delimiter=",")
    writer.writerow(en_tete)
    infos = []
    product = url
    infos.append(product)
    upc = soup.find("table", {"class" : "table table-striped"}).find_all("td") [0]
    infos.append(upc.string)
    title = soup.find("div", {"class" : "col-sm-6 product_main"}).find("h1").text
    infos.append(title)
    priceinctax = soup.find("table", {"class" : "table table-striped"}).find_all("td") [3]
    infos.append(priceinctax.text)
    priceexctax = soup.find("table", {"class" : "table table-striped"}).find_all("td") [2]
    infos.append(priceexctax.text)
    numberav = soup.find("table", {"class" : "table table-striped"}).find_all("td") [5]
    infos.append(numberav.text)
    description = soup.find("article", {"class" : "product_page"}).find_all("p") [3]
    infos.append(description.text)
    category = soup.find("ul", {"class" : "breadcrumb"}).find_all("a") [2]
    infos.append(category.text)
    review = soup.find("p", {"class" : "star-rating"}).attrs
    infos.append(review["class"][1])
    image = soup.find("div", {"class" : "content"}).find("div", {"class" : "item active"}).find("img")
    image = "http://books.toscrape.com/" + image["src"]
    infos.append(image)
    writer.writerow(infos)
