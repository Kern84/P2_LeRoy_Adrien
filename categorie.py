import requests
from bs4 import BeautifulSoup
import csv

links =[]

url = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
response = requests.get(url)

if response.ok:
    soup = BeautifulSoup(response.content, "html.parser")
    h3s = soup.find_all("h3")
    for h3 in h3s:
        a = h3.find("a")
        link = a["href"]
        link = link.replace("../", "")
        links.append("http://books.toscrape.com/catalogue/" + link)

with open("urls2.txt", "w")as file:
    for link in links:
        file.write(link + "\n")

en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
with open("urls2.txt", "r") as inf:
    with open("tableau2.csv", "w") as outf:
        writer = csv.writer(outf, delimiter=",")
        writer.writerow(en_tete)
        for row in inf:
            url = row.strip()
            response = requests.get(url)
            if response.ok:
                soup = BeautifulSoup(response.content, "html.parser")
                product = row.strip()
                products = []
                products.append(product)
                upc = soup.find("table", {"class" : "table table-striped"}).find_all("td") [0]
                upcs = []
                for item in upc:
                    upcs.append(item.string)
                title = soup.find("div", {"class" : "col-sm-6 product_main"}).find_all("h1")
                titles = []
                for tit in title:
                    titles.append(tit.string)
                priceinctax = soup.find("table", {"class" : "table table-striped"}).find_all("td") [3]
                priceht = []
                for price in priceinctax:
                    priceht.append(price)
                priceexctax = soup.find("table", {"class" : "table table-striped"}).find_all("td") [2]
                pricetc = []
                for pricetax in priceexctax:
                    pricetc.append(pricetax)
                numberav = soup.find("table", {"class" : "table table-striped"}).find_all("td") [5]
                numbers = []
                for num in numberav:
                    numbers.append(num)
                description = soup.find("article", {"class" : "product_page"}).find_all("p") [3]
                descriptions = []
                for desc in description:
                    descriptions.append(desc)
                category = soup.find("ul", {"class" : "breadcrumb"}).find_all("a") [2]
                categories = []
                for cat in category:
                    categories.append(cat)
                review = soup.find("p", {"class" : "star-rating"}).attrs
                reviews =[]
                for rev in review:
                    reviews.append(review["class"][1])
                image = soup.find("div", {"class" : "content"}).find("div", {"class" : "item active"}).find("img")
                image = "http://books.toscrape.com/" + image["src"]
                images = []
                images.append(image)
                for prod, item, tit, price, pricetax, num, desc, cat, rev, img in zip(products, upcs, titles, priceht, pricetc, numbers, descriptions, categories, reviews, images):
                    writer.writerow([prod, item, tit, price, pricetax, num, desc, cat, rev, img])