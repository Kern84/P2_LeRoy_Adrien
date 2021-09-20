import requests
from bs4 import BeautifulSoup
import csv
"""
links =[]


for i in range(1, 51):
    url = "http://books.toscrape.com/catalogue/page-" + str(i) + ".html"
    response = requests.get(url)
    print(response)

    if response.ok:
        print("page: " + str(i))
        soup = BeautifulSoup(response.content, "html.parser")
        h3s = soup.find_all("h3")
        for h3 in h3s:
            a = h3.find("a")
            link = a["href"]
            links.append("http://books.toscrape.com/catalogue/" + link)

print(links)

with open("urls.txt", "w")as file:
    for link in links:
        file.write(link + "\n")
"""
with open("urls.txt", "r") as inf:
    with open("tableau.csv", "w") as outf:
        writer = csv.writer(outf)
        writer.writerow("product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url")
        for row in inf:
            url = row.strip()
            response = requests.get(url)
            if response.ok:
                soup = BeautifulSoup(response.content, "html.parser")
                product = row.strip()
                upc = soup.find("table", {"class" : "table table-striped"}).find_all("td") [0]
                title = soup.find("div", {"class" : "col-sm-6 product_main"}).find_all("h1")
                priceinctax = soup.find("table", {"class" : "table table-striped"}).find_all("td") [3]
                priceexctax = soup.find("table", {"class" : "table table-striped"}).find_all("td") [2]
                numberav = soup.find("table", {"class" : "table table-striped"}).find_all("td") [5]
                description = soup.find("article", {"class" : "product_page"}).find_all("p") [3]
                category = soup.find("ul", {"class" : "breadcrumb"}).find_all("a") [2]
                review = soup.find("div", {"class" : "col-sm-6 product_main"}).find("p", {"class" : "star-rating"})
                image = soup.find("div", {"class" : "content"}).find("div", {"class" : "item active"}).find("img")
                writer.writerow('product + "," + upc.text + "," + title + "," + priceinctax.text + "," + priceexctax.text + "," + numberav.text + "," + description.text + "," + category.text + "," + "http://books.toscrape.com/" + image["src"]')
                print(product, upc.text, title, priceinctax.text, priceexctax.text, numberav.text, description.text, category.text, "http://books.toscrape.com/" + image["src"])
 #               print("http://books.toscrape.com/" + image["src"])
  #              print(review)





