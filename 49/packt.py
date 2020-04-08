from collections import namedtuple

from bs4 import BeautifulSoup as Soup
import requests

PACKT = "https://bites-data.s3.us-east-2.amazonaws.com/packt.html"
CONTENT = requests.get(PACKT).text

Book = namedtuple("Book", "title description image link")


def get_book():
    """make a Soup object, parse the relevant html sections, and return a Book namedtuple"""
    homepage = Soup(CONTENT, "html.parser")
    book_of_the_day = homepage.find("div", class_="dotd-main-book cf")

    title = book_of_the_day.find("h2").text.strip()
    description = book_of_the_day.find("h2").find_next("div").text.strip()
    link = book_of_the_day.find("a").get("href")
    image = book_of_the_day.find("img").get("src")

    return Book(title, description, image, link)
