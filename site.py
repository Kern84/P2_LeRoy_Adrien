import requests
from bs4 import BeautifulSoup
import csv

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
            links.append("http://books.toscrape.com/" + link)

print(links)

with open("urls.txt", "w")as file:
    for link in links:
        file.write(link + "\n")

with open("urls.txt", "r") as inf:
    with open("tableau.csv", "w") as outf:
        outf.write("product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url")
        for row in inf:
            url = row.strip()
            response = requests.get(url)
            if response.ok:
                soup = BeautifulSoup(response.content, "html.parser")
#                product =
                upc = soup.find("th", "UPC").find("td")
                title = soup.find("div", {"class" : "col-sm-6 product_main"}).find("h1")
 #               priceinctax =
 #               princeexctax =
#                numberav =
 #               description =
 #               category =
 #               review =
 #               image =
                print("UPC" + upc.text + "title" + title.text)
                outf.write(upc.text, + "," + title.text + "\n")