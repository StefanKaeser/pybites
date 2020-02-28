import os
import urllib.request
from collections import defaultdict

TMP = os.getenv("TMP", "/tmp")
DATA = "safari.logs"
SAFARI_LOGS = os.path.join(".", DATA)
PY_BOOK, OTHER_BOOK = "🐍", "."

urllib.request.urlretrieve(
    f"https://bites-data.s3.us-east-2.amazonaws.com/{DATA}", SAFARI_LOGS
)


def create_chart():
    with open(SAFARI_LOGS, "r") as f:
        lines = f.readlines()

    dates_books = defaultdict(list)
    for entry_line, action_line in zip(lines[::2], lines[1::2]):
        action = action_line.split("-")[-1].strip()

        if action == "sending to slack channel":
            date = entry_line.split()[0]
            book = entry_line.split("-")[-1].strip()

            dates_books[date].append(book)
    # Ordering the dates is not necessary, because the key insertion order
    # is preserved in a dictionary since python 3.6.
    #unique_dates = sorted(set(dates_books.keys()), key=lambda x: int(x[-2:]))
    for date in dates_books.keys():
        books = dates_books[date]
        book_icons = "".join(
            [PY_BOOK if "python" in book.lower() else OTHER_BOOK for book in books]
        )
        print(f"{date} {book_icons}")
