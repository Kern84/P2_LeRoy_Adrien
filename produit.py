#Script Python pour la récupération des informations pour un produit

import requests
from bs4 import BeautifulSoup
import csv

url = "http://books.toscrape.com/catalogue/meditations_33/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

nom = []
valeur = []



titre = soup.find_all("li", "active")
for titres in titre:
    valeur.append(titres.string)

nom.append("title")
"""
description = soup.find_all("meta", "content")
for descriptions in description:
    valeur.append(descriptions.string)
"""
description = soup.find_all("div")
for art in description:
    p = art.find("p")
    valeur.append(p.string)


nom.append("description")

category = soup.find_all("a", href="../category/books/philosophy_7/index.html")
for categories in category:
    valeur.append(categories.string)

nom.append("category")

noms = soup.find_all("th")
for resultat in noms:
    nom.append(resultat.string)

valeurs = soup.find_all("td")
for reponse in valeurs:
    valeur.append(reponse.string)

image = soup.find_all("img", "src")
for images in image:
    valeur.append(images)

nom.append("image")

nom.remove("Product Type")
nom.remove("Tax")
valeur.remove("Books")
valeur.remove("£0.00")

print(nom)
print(valeur)

with open("test.csv", "w") as f:
    writer = csv.writer(f, delimiter = ",")
    writer.writerow(nom)
    writer.writerow(valeur)
