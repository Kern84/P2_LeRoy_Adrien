# Scripte Python pour la récupération des informations pour tout le site par catégorie

import requests
from bs4 import BeautifulSoup
import csv

links =[]
categories1 = []

url = "http://books.toscrape.com/catalogue/category/books_1/index.html"
response = requests.get(url)

if response.ok:
    soup = BeautifulSoup(response.content, "html.parser")
    lis = soup.find("ul", {"class" : "nav nav-list"}).find_all("a")[1:]
    for href in lis:
        link = href["href"]
        link = link.replace("../", "")
        links.append("http://books.toscrape.com/catalogue/category/" + link)
    categories = soup.find("ul", {"class" : "nav nav-list"}).find_all("a")
    categories = categories[1:]
    for cat in categories:
        cat1 = cat.text.strip()
        categories1.append(cat1)

with open("urls_site.txt", "w")as file:
    for link in links:
        file.write(link + "\n")

x = 0
for x in range(51):
    categorie1 = links[x]
    resp = requests.get(categorie1)
    soup = BeautifulSoup(resp.content, "html.parser")
    results = soup.find("form", {"class": "form-horizontal"}).find_all("strong")[0]
    resultat = results.text
    if int(resultat) <= 20:
        links2 =[]
        h3s = soup.find_all("h3")
        for h3 in h3s:
            a = h3.find("a")
            link2 = a["href"]
            link2 = link2.replace("../", "")
            links2.append("http://books.toscrape.com/catalogue/" + str(link2))

        with open("urls_site_categorie" + str(x) + ".txt", "w") as file:
            for link in links2:
                file.write(link + "\n")

        en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
                   "number_available", "product_description", "category", "review_rating", "image_url"]
        with open("urls_site_categorie" + str(x) + ".txt", "r") as inf:
            with open("P2_03_" + str(categories1[x]) + ".csv", "w") as outf:
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
                        upc = soup.find("table", {"class": "table table-striped"}).find_all("td")[0]
                        upcs = []
                        for item in upc:
                            upcs.append(item.string)
                        title = soup.find("div", {"class": "col-sm-6 product_main"}).find_all("h1")
                        titles = []
                        for tit in title:
                            titles.append(tit.string)
                        priceinctax = soup.find("table", {"class": "table table-striped"}).find_all("td")[3]
                        priceht = []
                        for price in priceinctax:
                            priceht.append(price)
                        priceexctax = soup.find("table", {"class": "table table-striped"}).find_all("td")[2]
                        pricetc = []
                        for pricetax in priceexctax:
                            pricetc.append(pricetax)
                        numberav = soup.find("table", {"class": "table table-striped"}).find_all("td")[5]
                        numbers = []
                        for num in numberav:
                            numbers.append(num)
                        description = soup.find("article", {"class": "product_page"}).find_all("p")[3]
                        descriptions = []
                        for desc in description:
                            descriptions.append(desc)
                        category = soup.find("ul", {"class": "breadcrumb"}).find_all("a")[2]
                        categories = []
                        for cat in category:
                            categories.append(cat)
                        review = soup.find("p", {"class": "star-rating"}).attrs
                        reviews = []
                        for rev in review:
                            reviews.append(review["class"][1])
                        image = soup.find("div", {"class": "content"}).find("div", {"class": "item active"}).find("img")
                        linkImg = image["src"]
                        nom = image["alt"]
                        nom = nom.replace("/", "").replace(":", "").replace("(", "").replace(")", "")
                        image1 = "http://books.toscrape.com/" + linkImg
                        images = []
                        images.append(image1)
                        with open(str(nom) + ".jpg", "wb") as img:
                            im = requests.get("http://books.toscrape.com/" + str(image))
                            img.write(im.content)
                        for prod, item, tit, price, pricetax, num, desc, cat, rev, img in zip(products, upcs, titles,
                                                                                              priceht, pricetc, numbers,
                                                                                              descriptions, categories,
                                                                                              reviews, images):
                            writer.writerow([prod, item, tit, price, pricetax, num, desc, cat, rev, img])

    if int(resultat) > 20 and int(resultat) <= 40:
        for y in range(1,3):
            categorie1 = categorie1.replace("index.html", "")
            categorie2 = categorie1 + "page-" + str(y) + ".html"
            resp = requests.get(categorie2)
            soup = BeautifulSoup(resp.content, "html.parser")
            links3 = []
            h3s = soup.find_all("h3")
            for h3 in h3s:
                a = h3.find("a")
                link3 = a["href"]
                link3 = link3.replace("../", "")
                links3.append("http://books.toscrape.com/catalogue/" + str(link3))

            with open("urls_site_categorie" + str(x) + ".txt", "w") as file:
                for link in links3:
                    file.write(link + "\n")

            en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
                       "number_available", "product_description", "category", "review_rating", "image_url"]
            with open("urls_site_categorie" + str(x) + ".txt", "r") as inf:
                with open("P2_03_" + str(categories1[x]) + ".csv", "a+") as outf:
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
                            upc = soup.find("table", {"class": "table table-striped"}).find_all("td")[0]
                            upcs = []
                            for item in upc:
                                upcs.append(item.string)
                            title = soup.find("div", {"class": "col-sm-6 product_main"}).find_all("h1")
                            titles = []
                            for tit in title:
                                titles.append(tit.string)
                            priceinctax = soup.find("table", {"class": "table table-striped"}).find_all("td")[3]
                            priceht = []
                            for price in priceinctax:
                                priceht.append(price)
                            priceexctax = soup.find("table", {"class": "table table-striped"}).find_all("td")[2]
                            pricetc = []
                            for pricetax in priceexctax:
                                pricetc.append(pricetax)
                            numberav = soup.find("table", {"class": "table table-striped"}).find_all("td")[5]
                            numbers = []
                            for num in numberav:
                                numbers.append(num)
                            description = soup.find("article", {"class": "product_page"}).find_all("p")[3]
                            descriptions = []
                            for desc in description:
                                descriptions.append(desc)
                            category = soup.find("ul", {"class": "breadcrumb"}).find_all("a")[2]
                            categories = []
                            for cat in category:
                                categories.append(cat)
                            review = soup.find("p", {"class": "star-rating"}).attrs
                            reviews = []
                            for rev in review:
                                reviews.append(review["class"][1])
                            image = soup.find("div", {"class": "content"}).find("div", {"class": "item active"}).find(
                                "img")
                            linkImg = image["src"]
                            nom = image["alt"]
                            nom = nom.replace("/", "").replace(":", "").replace("(", "").replace(")", "")
                            image1 = "http://books.toscrape.com/" + linkImg
                            images = []
                            images.append(image1)
                            with open(str(nom) + ".jpg", "wb") as img:
                                im = requests.get("http://books.toscrape.com/" + str(image))
                                img.write(im.content)
                            for prod, item, tit, price, pricetax, num, desc, cat, rev, img in zip(products, upcs, titles,
                                                                                                  priceht, pricetc, numbers,
                                                                                                  descriptions, categories,
                                                                                                  reviews, images):
                                writer.writerow([prod, item, tit, price, pricetax, num, desc, cat, rev, img])

    if int(resultat) > 40 and int(resultat) <= 60 :
        for y in range(1,4):
            categorie1 = categorie1.replace("index.html", "")
            categorie2 = categorie1 + "page-" + str(y) + ".html"
            resp = requests.get(categorie2)
            soup = BeautifulSoup(resp.content, "html.parser")
            links2 = []
            h3s = soup.find_all("h3")
            for h3 in h3s:
                a = h3.find("a")
                link2 = a["href"]
                link2 = link2.replace("../", "")
                links2.append("http://books.toscrape.com/catalogue/" + str(link2))

            with open("urls_site_categorie" + str(x) + ".txt", "w") as file:
                for link in links2:
                    file.write(link + "\n")

            en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
                       "number_available", "product_description", "category", "review_rating", "image_url"]
            with open("urls_site_categorie" + str(x) + ".txt", "r") as inf:
                with open("P2_03_" + str(categories1[x]) + ".csv", "a+") as outf:
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
                            upc = soup.find("table", {"class": "table table-striped"}).find_all("td")[0]
                            upcs = []
                            for item in upc:
                                upcs.append(item.string)
                            title = soup.find("div", {"class": "col-sm-6 product_main"}).find_all("h1")
                            titles = []
                            for tit in title:
                                titles.append(tit.string)
                            priceinctax = soup.find("table", {"class": "table table-striped"}).find_all("td")[3]
                            priceht = []
                            for price in priceinctax:
                                priceht.append(price)
                            priceexctax = soup.find("table", {"class": "table table-striped"}).find_all("td")[2]
                            pricetc = []
                            for pricetax in priceexctax:
                                pricetc.append(pricetax)
                            numberav = soup.find("table", {"class": "table table-striped"}).find_all("td")[5]
                            numbers = []
                            for num in numberav:
                                numbers.append(num)
                            description = soup.find("article", {"class": "product_page"}).find_all("p")[3]
                            descriptions = []
                            for desc in description:
                                descriptions.append(desc)
                            category = soup.find("ul", {"class": "breadcrumb"}).find_all("a")[2]
                            categories = []
                            for cat in category:
                                categories.append(cat)
                            review = soup.find("p", {"class": "star-rating"}).attrs
                            reviews = []
                            for rev in review:
                                reviews.append(review["class"][1])
                            image = soup.find("div", {"class": "content"}).find("div", {"class": "item active"}).find(
                                "img")
                            linkImg = image["src"]
                            nom = image["alt"]
                            nom = nom.replace("/", "").replace(":", "").replace("(", "").replace(")", "")
                            image1 = "http://books.toscrape.com/" + linkImg
                            images = []
                            images.append(image1)
                            with open(str(nom) + ".jpg", "wb") as img:
                                im = requests.get("http://books.toscrape.com/" + str(image))
                                img.write(im.content)
                            for prod, item, tit, price, pricetax, num, desc, cat, rev, img in zip(products, upcs, titles,
                                                                                                  priceht, pricetc, numbers,
                                                                                                  descriptions, categories,
                                                                                                  reviews, images):
                                writer.writerow([prod, item, tit, price, pricetax, num, desc, cat, rev, img])

    if int(resultat) > 60 and int(resultat) <= 80:
        for y in range(1,5):
            categorie1 = categorie1.replace("index.html", "")
            categorie2 = categorie1 + "page-" + str(y) + ".html"
            resp = requests.get(categorie2)
            soup = BeautifulSoup(resp.content, "html.parser")
            links2 = []
            h3s = soup.find_all("h3")
            for h3 in h3s:
                a = h3.find("a")
                link2 = a["href"]
                link2 = link2.replace("../", "")
                links2.append("http://books.toscrape.com/catalogue/" + str(link2))

            with open("urls_site_categorie" + str(x) + ".txt", "w") as file:
                for link in links2:
                    file.write(link + "\n")

            en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
                       "number_available", "product_description", "category", "review_rating", "image_url"]
            with open("urls_site_categorie" + str(x) + ".txt", "r") as inf:
                with open("P2_03_" + str(categories1[x]) + ".csv", "a+") as outf:
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
                            upc = soup.find("table", {"class": "table table-striped"}).find_all("td")[0]
                            upcs = []
                            for item in upc:
                                upcs.append(item.string)
                            title = soup.find("div", {"class": "col-sm-6 product_main"}).find_all("h1")
                            titles = []
                            for tit in title:
                                titles.append(tit.string)
                            priceinctax = soup.find("table", {"class": "table table-striped"}).find_all("td")[3]
                            priceht = []
                            for price in priceinctax:
                                priceht.append(price)
                            priceexctax = soup.find("table", {"class": "table table-striped"}).find_all("td")[2]
                            pricetc = []
                            for pricetax in priceexctax:
                                pricetc.append(pricetax)
                            numberav = soup.find("table", {"class": "table table-striped"}).find_all("td")[5]
                            numbers = []
                            for num in numberav:
                                numbers.append(num)
                            description = soup.find("article", {"class": "product_page"}).find_all("p")[3]
                            descriptions = []
                            for desc in description:
                                descriptions.append(desc)
                            category = soup.find("ul", {"class": "breadcrumb"}).find_all("a")[2]
                            categories = []
                            for cat in category:
                                categories.append(cat)
                            review = soup.find("p", {"class": "star-rating"}).attrs
                            reviews = []
                            for rev in review:
                                reviews.append(review["class"][1])
                            image = soup.find("div", {"class": "content"}).find("div", {"class": "item active"}).find(
                                "img")
                            linkImg = image["src"]
                            nom = image["alt"]
                            nom = nom.replace("/", "").replace(":", "").replace("(", "").replace(")", "")
                            image1 = "http://books.toscrape.com/" + linkImg
                            images = []
                            images.append(image1)
                            with open(str(nom) + ".jpg", "wb") as img:
                                im = requests.get("http://books.toscrape.com/" + str(image))
                                img.write(im.content)
                            for prod, item, tit, price, pricetax, num, desc, cat, rev, img in zip(products, upcs, titles,
                                                                                                  priceht, pricetc, numbers,
                                                                                                  descriptions, categories,
                                                                                                  reviews, images):
                                writer.writerow([prod, item, tit, price, pricetax, num, desc, cat, rev, img])

    if int(resultat) > 80 and int(resultat) <= 100:
        for y in range(1,6):
            categorie1 = categorie1.replace("index.html", "")
            categorie2 = categorie1 + "page-" + str(y) + ".html"
            resp = requests.get(categorie2)
            soup = BeautifulSoup(resp.content, "html.parser")
            links2 = []
            h3s = soup.find_all("h3")
            for h3 in h3s:
                a = h3.find("a")
                link2 = a["href"]
                link2 = link2.replace("../", "")
                links2.append("http://books.toscrape.com/catalogue/" + str(link2))

            with open("urls_site_categorie" + str(x) + ".txt", "w") as file:
                for link in links2:
                    file.write(link + "\n")

            en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
                       "number_available", "product_description", "category", "review_rating", "image_url"]
            with open("urls_site_categorie" + str(x) + ".txt", "r") as inf:
                with open("P2_03_" + str(categories1[x]) + ".csv", "a+") as outf:
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
                            upc = soup.find("table", {"class": "table table-striped"}).find_all("td")[0]
                            upcs = []
                            for item in upc:
                                upcs.append(item.string)
                            title = soup.find("div", {"class": "col-sm-6 product_main"}).find_all("h1")
                            titles = []
                            for tit in title:
                                titles.append(tit.string)
                            priceinctax = soup.find("table", {"class": "table table-striped"}).find_all("td")[3]
                            priceht = []
                            for price in priceinctax:
                                priceht.append(price)
                            priceexctax = soup.find("table", {"class": "table table-striped"}).find_all("td")[2]
                            pricetc = []
                            for pricetax in priceexctax:
                                pricetc.append(pricetax)
                            numberav = soup.find("table", {"class": "table table-striped"}).find_all("td")[5]
                            numbers = []
                            for num in numberav:
                                numbers.append(num)
                            description = soup.find("article", {"class": "product_page"}).find_all("p")[3]
                            descriptions = []
                            for desc in description:
                                descriptions.append(desc)
                            category = soup.find("ul", {"class": "breadcrumb"}).find_all("a")[2]
                            categories = []
                            for cat in category:
                                categories.append(cat)
                            review = soup.find("p", {"class": "star-rating"}).attrs
                            reviews = []
                            for rev in review:
                                reviews.append(review["class"][1])
                            image = soup.find("div", {"class": "content"}).find("div", {"class": "item active"}).find(
                                "img")
                            linkImg = image["src"]
                            nom = image["alt"]
                            nom = nom.replace("/", "").replace(":", "").replace("(", "").replace(")", "")
                            image1 = "http://books.toscrape.com/" + linkImg
                            images = []
                            images.append(image1)
                            with open(str(nom) + ".jpg", "wb") as img:
                                im = requests.get("http://books.toscrape.com/" + str(image))
                                img.write(im.content)
                            for prod, item, tit, price, pricetax, num, desc, cat, rev, img in zip(products, upcs, titles,
                                                                                                  priceht, pricetc, numbers,
                                                                                                  descriptions, categories,
                                                                                                  reviews, images):
                                writer.writerow([prod, item, tit, price, pricetax, num, desc, cat, rev, img])

    if int(resultat) > 100 and int(resultat) <= 120:
        for y in range(1,7):
            categorie1 = categorie1.replace("index.html", "")
            categorie2 = categorie1 + "page-" + str(y) + ".html"
            resp = requests.get(categorie2)
            soup = BeautifulSoup(resp.content, "html.parser")
            links2 = []
            h3s = soup.find_all("h3")
            for h3 in h3s:
                a = h3.find("a")
                link2 = a["href"]
                link2 = link2.replace("../", "")
                links2.append("http://books.toscrape.com/catalogue/" + str(link2))

            with open("urls_site_categorie" + str(x) + ".txt", "w") as file:
                for link in links2:
                    file.write(link + "\n")

            en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
                       "number_available", "product_description", "category", "review_rating", "image_url"]
            with open("urls_site_categorie" + str(x) + ".txt", "r") as inf:
                with open("P2_03_" + str(categories1[x]) + ".csv", "a+") as outf:
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
                            upc = soup.find("table", {"class": "table table-striped"}).find_all("td")[0]
                            upcs = []
                            for item in upc:
                                upcs.append(item.string)
                            title = soup.find("div", {"class": "col-sm-6 product_main"}).find_all("h1")
                            titles = []
                            for tit in title:
                                titles.append(tit.string)
                            priceinctax = soup.find("table", {"class": "table table-striped"}).find_all("td")[3]
                            priceht = []
                            for price in priceinctax:
                                priceht.append(price)
                            priceexctax = soup.find("table", {"class": "table table-striped"}).find_all("td")[2]
                            pricetc = []
                            for pricetax in priceexctax:
                                pricetc.append(pricetax)
                            numberav = soup.find("table", {"class": "table table-striped"}).find_all("td")[5]
                            numbers = []
                            for num in numberav:
                                numbers.append(num)
                            description = soup.find("article", {"class": "product_page"}).find_all("p")[3]
                            descriptions = []
                            for desc in description:
                                descriptions.append(desc)
                            category = soup.find("ul", {"class": "breadcrumb"}).find_all("a")[2]
                            categories = []
                            for cat in category:
                                categories.append(cat)
                            review = soup.find("p", {"class": "star-rating"}).attrs
                            reviews = []
                            for rev in review:
                                reviews.append(review["class"][1])
                            image = soup.find("div", {"class": "content"}).find("div", {"class": "item active"}).find(
                                "img")
                            linkImg = image["src"]
                            nom = image["alt"]
                            nom = nom.replace("/", "").replace(":", "").replace("(", "").replace(")", "")
                            image1 = "http://books.toscrape.com/" + linkImg
                            images = []
                            images.append(image1)
                            with open(str(nom) + ".jpg", "wb") as img:
                                im = requests.get("http://books.toscrape.com/" + str(image))
                                img.write(im.content)
                            for prod, item, tit, price, pricetax, num, desc, cat, rev, img in zip(products, upcs, titles,
                                                                                                  priceht, pricetc, numbers,
                                                                                                  descriptions, categories,
                                                                                                  reviews, images):
                                writer.writerow([prod, item, tit, price, pricetax, num, desc, cat, rev, img])

    if int(resultat) > 120 and int(resultat) <= 140:
        for y in range(1,8):
            categorie1 = categorie1.replace("index.html", "")
            categorie2 = categorie1 + "page-" + str(y) + ".html"
            resp = requests.get(categorie2)
            soup = BeautifulSoup(resp.content, "html.parser")
            links2 = []
            h3s = soup.find_all("h3")
            for h3 in h3s:
                a = h3.find("a")
                link2 = a["href"]
                link2 = link2.replace("../", "")
                links2.append("http://books.toscrape.com/catalogue/" + str(link2))

            with open("urls_site_categorie" + str(x) + ".txt", "w") as file:
                for link in links2:
                    file.write(link + "\n")

            en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
                       "number_available", "product_description", "category", "review_rating", "image_url"]
            with open("urls_site_categorie" + str(x) + ".txt", "r") as inf:
                with open("P2_03_" + str(categories1[x]) + ".csv", "a+") as outf:
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
                            upc = soup.find("table", {"class": "table table-striped"}).find_all("td")[0]
                            upcs = []
                            for item in upc:
                                upcs.append(item.string)
                            title = soup.find("div", {"class": "col-sm-6 product_main"}).find_all("h1")
                            titles = []
                            for tit in title:
                                titles.append(tit.string)
                            priceinctax = soup.find("table", {"class": "table table-striped"}).find_all("td")[3]
                            priceht = []
                            for price in priceinctax:
                                priceht.append(price)
                            priceexctax = soup.find("table", {"class": "table table-striped"}).find_all("td")[2]
                            pricetc = []
                            for pricetax in priceexctax:
                                pricetc.append(pricetax)
                            numberav = soup.find("table", {"class": "table table-striped"}).find_all("td")[5]
                            numbers = []
                            for num in numberav:
                                numbers.append(num)
                            description = soup.find("article", {"class": "product_page"}).find_all("p")[3]
                            descriptions = []
                            for desc in description:
                                descriptions.append(desc)
                            category = soup.find("ul", {"class": "breadcrumb"}).find_all("a")[2]
                            categories = []
                            for cat in category:
                                categories.append(cat)
                            review = soup.find("p", {"class": "star-rating"}).attrs
                            reviews = []
                            for rev in review:
                                reviews.append(review["class"][1])
                            image = soup.find("div", {"class": "content"}).find("div", {"class": "item active"}).find(
                                "img")
                            linkImg = image["src"]
                            nom = image["alt"]
                            nom = nom.replace("/", "").replace(":", "").replace("(", "").replace(")", "")
                            image1 = "http://books.toscrape.com/" + linkImg
                            images = []
                            images.append(image1)
                            with open(str(nom) + ".jpg", "wb") as img:
                                im = requests.get("http://books.toscrape.com/" + str(image))
                                img.write(im.content)
                            for prod, item, tit, price, pricetax, num, desc, cat, rev, img in zip(products, upcs, titles,
                                                                                                  priceht, pricetc, numbers,
                                                                                                  descriptions, categories,
                                                                                                  reviews, images):
                                writer.writerow([prod, item, tit, price, pricetax, num, desc, cat, rev, img])

    if int(resultat) > 140 and int(resultat) <= 160:
        for y in range(1,9):
            categorie1 = categorie1.replace("index.html", "")
            categorie2 = categorie1 + "page-" + str(y) + ".html"
            resp = requests.get(categorie2)
            soup = BeautifulSoup(resp.content, "html.parser")
            links2 = []
            h3s = soup.find_all("h3")
            for h3 in h3s:
                a = h3.find("a")
                link2 = a["href"]
                link2 = link2.replace("../", "")
                links2.append("http://books.toscrape.com/catalogue/" + str(link2))

            with open("urls_site_categorie" + str(x) + ".txt", "w") as file:
                for link in links2:
                    file.write(link + "\n")

            en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
                       "number_available", "product_description", "category", "review_rating", "image_url"]
            with open("urls_site_categorie" + str(x) + ".txt", "r") as inf:
                with open("P2_03_" + str(categories1[x]) + ".csv", "a+") as outf:
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
                            upc = soup.find("table", {"class": "table table-striped"}).find_all("td")[0]
                            upcs = []
                            for item in upc:
                                upcs.append(item.string)
                            title = soup.find("div", {"class": "col-sm-6 product_main"}).find_all("h1")
                            titles = []
                            for tit in title:
                                titles.append(tit.string)
                            priceinctax = soup.find("table", {"class": "table table-striped"}).find_all("td")[3]
                            priceht = []
                            for price in priceinctax:
                                priceht.append(price)
                            priceexctax = soup.find("table", {"class": "table table-striped"}).find_all("td")[2]
                            pricetc = []
                            for pricetax in priceexctax:
                                pricetc.append(pricetax)
                            numberav = soup.find("table", {"class": "table table-striped"}).find_all("td")[5]
                            numbers = []
                            for num in numberav:
                                numbers.append(num)
                            description = soup.find("article", {"class": "product_page"}).find_all("p")[3]
                            descriptions = []
                            for desc in description:
                                descriptions.append(desc)
                            category = soup.find("ul", {"class": "breadcrumb"}).find_all("a")[2]
                            categories = []
                            for cat in category:
                                categories.append(cat)
                            review = soup.find("p", {"class": "star-rating"}).attrs
                            reviews = []
                            for rev in review:
                                reviews.append(review["class"][1])
                            image = soup.find("div", {"class": "content"}).find("div", {"class": "item active"}).find(
                                "img")
                            linkImg = image["src"]
                            nom = image["alt"]
                            nom = nom.replace("/", "").replace(":", "").replace("(", "").replace(")", "")
                            image1 = "http://books.toscrape.com/" + linkImg
                            images = []
                            images.append(image1)
                            with open(str(nom) + ".jpg", "wb") as img:
                                im = requests.get("http://books.toscrape.com/" + str(image))
                                img.write(im.content)
                            for prod, item, tit, price, pricetax, num, desc, cat, rev, img in zip(products, upcs, titles,
                                                                                                  priceht, pricetc, numbers,
                                                                                                  descriptions, categories,
                                                                                                  reviews, images):
                                writer.writerow([prod, item, tit, price, pricetax, num, desc, cat, rev, img])
