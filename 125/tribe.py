from collections import Counter, namedtuple

from bs4 import BeautifulSoup
import requests

AMAZON = "amazon.com"
# static copy
TIM_BLOG = "https://bites-data.s3.us-east-2.amazonaws.com/" "tribe-mentors-books.html"
MIN_COUNT = 3


def get_top_books(content=None):
    """Make a BeautifulSoup object loading in content,
       find all links that contain AMAZON, extract the book title
       and count them.
       Return a list of (title, count) tuples where
       count is at least MIN_COUNT
    """
    if content is None:
        content = load_content_of_tims_blog()

    soup = BeautifulSoup(content, "html.parser")

    amazon_tags = extract_all_hyperlink_tags(soup, must_include=AMAZON)
    titles = [get_book_title(tag) for tag in amazon_tags]

    return get_books_mentioned_atleast_num_times(titles, num=MIN_COUNT)


def load_content_of_tims_blog():
    """Download the blog html and return its decoded content"""
    with requests.Session() as session:
        return session.get(TIM_BLOG).content.decode("utf-8")


load_page = load_content_of_tims_blog


def extract_all_hyperlink_tags(soup, must_include=""):
    return [tag for tag in soup.find_all("a") if must_include in tag.get("href")]


def get_book_title(tag):
    return tag.text


def get_books_mentioned_atleast_num_times(titles, num):
    books = [
        Book(title, num_times_mentioned)
        for (title, num_times_mentioned) in Counter(titles).most_common()
    ]
    return [tuple(book) for book in books if book.num_times_mentioned >= num]


Book = namedtuple("Book", "title num_times_mentioned")
