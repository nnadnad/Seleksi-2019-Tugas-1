import urllib.request
import json
import bs4
import time
import requests
import copy
import os


def getDataRestoran(url):
    hasilFinal = []
    with urllib.request.urlopen(url) as response:
        page = response.read()
    sp = bs4.BeautifulSoup(page, 'html.parser')

    # resto dan daerahnya
    resto = sp.find("span", class_="hdn").strip().split(",")
    namaResto = resto[0].strip()
    daerahResto = resto[1].strip()
    hasilFinal.append(namaResto)
    hasilFinal.append(daerahResto)

    # cuisine
    listOfCuisine = []
    cuisine = sp.find("a", class_="zred").text
    cuisineResto = cuisine.split(",")
    for jenisCuisine in cuisineResto:
        listOfCuisine.append(jenisCuisine)
    hasilFinal.append(listOfCuisine)

    # tipe Resto
    listOfTipe = []
    tipe = sp.find("a", class_="grey-text fontsize3").text
    tipeResto = tipe.split(",")
    for tipeDariResto in tipeResto:
        listOfTipe.append(tipeDariResto)
    hasilFinal.append(listOfTipe)

    # Harga
    harga = sp.find("span", tabindex="0").text
    hargaResto = harga.strip().split(" for")
    hasilFinal.append(hargaResto)

    # rate
    rating = sp.find("span", class_="ratingtext hidden").text
    hasilFinal.append(rating)

    return hasilFinal

def getFromWebsite(hasil, idx):
    pageResto = []
    baseUrl = 'https://www.zomato.com/'
    pageUrl = 'https://www.zomato.com/bandung/restaurants?page=' + str(idx)
    with urllib.request.urlopen(pageUrl) as respon:
        page = respon.read()
    sp = bs4.BeautifulSoup(page, 'html.parser')
    for i in sp.find_all("a", href=True):
        link = str(i['href'])
        if (link.startswith("/bandung/restaurants")):
            if (link not in pageResto):
                pageResto.append(link)
    for halamanResto in pageResto:
        fixUrl = baseUrl + halamanResto
        doScrape = getDataRestoran(fixUrl)
        hasil.append(doScrape)

def convertJson(listOfResto):
    dataJson = {}
    data = []

    for resto in listOfResto:
        dataJson['Nama Resto'] = resto[0]
        dataJson['Daerah Resto'] = resto[1]

        listOfCuisine = resto[2]
        cuisineResto = []
        for i in listOfCuisine:
            cuisineResto.append({"Cuisines Resto": i})
        dataJson['Cuisines Resto'] = cuisineResto
        
        listOfTipe = resto[3]
        tipeResto = []
        for i in listOfTipe:
            tipeResto.append({"Tipe Resto": i})
        dataJson['Tipe Resto'] = tipeResto

        dataJson['Harga Resto'] = resto[4]
        dataJson['Rating Resto'] = resto[5]

        data.append(copy.deepcopy(dataJson))

    pathFile = 'data/'
    jsonName = 'data.json'
    with open(os.path.join(pathFile, jsonName), 'w') as f:
        json.dump(data, f, indent=4)

def main():
    resto = []
    for i in range(1,5):
        getFromWebsite(resto, i)
        time.sleep(0.5)
    convertJson(resto)

if __name__ == "__main__":
    main()



    