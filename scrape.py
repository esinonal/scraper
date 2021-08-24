import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrapeAndDownloadBooks():
    # Get all the links we will need
    allLinksList = []
    linkBase = "https://books.toscrape.com/catalogue/"

    for i in range(1, 51):
        URL = f"https://books.toscrape.com/catalogue/category/books_1/page-{i}.html" 
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        h3s = soup.find_all("h3")

        for h3 in h3s:
            a = h3.find("a")
            allLinksList.append(linkBase + str(a['href'][6:]))
    print("Got links to scrape")

    # Get info on each page
    listOfValues = []
    for link in allLinksList:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")

        title = soup.find_all("h1")[0].text
        available =soup.find("p", class_="instock availability").text.split()[2][1:]
        price = soup.find("p", class_= "price_color").text[1:]
        desc = soup.find(id="content_inner").find(class_="product_page").find_all("p")[3].text
        theme = soup.find(class_ = "breadcrumb").text.split("\n")[8]

        isZero = soup.find(class_="col-sm-6 product_main").find(class_="star-rating Zero") 
        isOne = soup.find(class_="col-sm-6 product_main").find(class_="star-rating One") 
        isTwo = soup.find(class_="col-sm-6 product_main").find(class_="star-rating Two") 
        isThree = soup.find(class_="col-sm-6 product_main").find(class_="star-rating Three") 
        isFour = soup.find(class_="col-sm-6 product_main").find(class_="star-rating Four") 
        isFive = soup.find(class_="col-sm-6 product_main").find(class_="star-rating Five") 
        listrating = [isZero, isOne, isTwo, isThree, isFour, isFive]
        rating = next(idx for idx, item in enumerate(listrating) if item is not None)

        values = [title, available, price, theme, rating, desc]
        listOfValues.append(values)
    
    print("Scraped the links")
    dataframe = pd.DataFrame(listOfValues)
    dataframe = dataframe.rename(columns={0: "Name", 1: "Available", 2: "Price",  3: "Theme", 4: "Rating", 5:"Desc"})
    print(dataframe)
    dataframe.to_csv(r'/Users/esin/Documents/interview/c4ads/scrapedBooks.csv', index=False)

def analyzeBooks():
    #Get dataframe with "Theme", "Number of Books in theme", "Average Rating per theme".

    dataframe = pd.read_csv("/Users/esin/Documents/interview/c4ads/scrapedBooks.csv")
    results = dataframe.groupby(['Theme'])[['Rating']].agg(['mean', 'count'])
    results.to_csv(r'/Users/esin/Documents/interview/c4ads/theme.csv')


scrapeAndDownloadBooks()
analyzeBooks()