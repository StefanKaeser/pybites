from pathlib import Path
from urllib.request import urlretrieve
from dataclasses import dataclass
import re

from bs4 import BeautifulSoup

url = "https://bites-data.s3.us-east-2.amazonaws.com/" "best-programming-books.html"
tmp = Path("./")
html_file = tmp / "books.html"

if not html_file.exists():
    urlretrieve(url, html_file)


@dataclass
class Book:
    """Book class should instatiate the following variables:

    title - as it appears on the page
    author - should be entered as lastname, firstname
    year - four digit integer year that the book was published
    rank - integer rank to be updated once the books have been sorted
    rating - float as indicated on the page
    """

    title: str
    author: str
    year: int
    rank: int
    rating: float

    def __str__(self):
        return (
            f"[{str(self.rank).zfill(3)}] {self.title} ({self.year})\n"
            f"      {self.author} {float(round(self.rating, 2))}"
        )


def _get_soup(file):
    return BeautifulSoup(file.read_text(), "html.parser")


def display_books(books, limit=10, year=None):
    """Prints the specified books to the console

    :param books: list of all the books
    :param limit: integer that indicates how many books to return
    :param year: integer indicating the oldest year to include
    :return: None
    """
    if year:
        books = [book for book in books if book.year >= year]
    for book in books[:limit]:
        print(book)


def load_data():
    """Loads the data from the html file

    Creates the soup object and processes it to extract the information
    required to create the Book class objects and returns a sorted list
    of Book objects.

    Books should be sorted by rating, year, title, and then by author's
    last name. After the books have been sorted, the rank of each book
    should be updated to indicate this new sorting order.The Book object
    with the highest rating should be first and go down from there.
    """
    soup = _get_soup(html_file)
    book_tags = extract_book_tags(soup)

    books = []
    for book_tag in book_tags:
        if not all(
            [has_python_in_title(book_tag), has_author(book_tag), has_year(book_tag)]
        ):
            continue

        title = extract_title(book_tag)
        author = extract_author(book_tag)
        year = extract_year(book_tag)
        rank = extract_rank(book_tag)
        rating = extract_rating(book_tag)

        book = Book(title, author, year, rank, rating)
        books.append(book)

    books = sort_books(books)

    return books


def extract_book_tags(soup):
    book_list_tag = soup.find("div", class_="books")
    book_tags = book_list_tag.find_all("div", class_="book accepted normal")
    return book_tags


def has_python_in_title(book_tag):
    title = book_tag.find("h2", class_="main").text
    if "python" in title.lower():
        return True
    return False


def extract_title(book_tag):
    title = book_tag.find("h2", class_="main").text
    return title


def has_author(book_tag):
    try:
        author = book_tag.find("h3", class_="authors").find("a").text
        return True
    except AttributeError:
        return False


def extract_author(book_tag):
    author = book_tag.find("h3", class_="authors").find("a").text
    match = re.match(r"([\w\s\.]+) (\w+)", author)
    first_name, last_name = match.groups()
    author = f"{last_name}, {first_name}"
    return author


def extract_rank(book_tag):
    rank = book_tag.find("div", class_="rank").text
    return int(rank)


def extract_rating(book_tag):
    rating = book_tag.find("span", class_="our-rating").text
    return round(float(rating), 2)


def has_year(book_tag):
    try:
        year = book_tag.find("span", class_="date").text.split()[-1]
        return True
    except AttributeError:  # no year found
        return False


def extract_year(book_tag):
    year = book_tag.find("span", class_="date").text.split()[-1]
    return int(year)


def sort_books(books):
    books = sorted(
        books,
        key=lambda book: (-book.rating, book.year, book.title.lower(), book.author),
    )
    rank_books_in_given_order(books)
    return books


def rank_books_in_given_order(books):
    for rank, book in enumerate(books, 1):
        book.rank = rank


def main():
    books = load_data()
    display_books(books, limit=5, year=2017)
    """If done correctly, the previous function call should display the
    output below.
    """


if __name__ == "__main__":
    main()


"""
[001] Python Tricks (2017)
      Bader, Dan 4.74
[002] Mastering Deep Learning Fundamentals with Python (2019)
      Wilson, Richard 4.7
[006] Python Programming (2019)
      Fedden, Antony Mc 4.68
[007] Python Programming (2019)
      Mining, Joseph 4.68
[009] A Smarter Way to Learn Python (2017)
      Myers, Mark 4.66
"""
