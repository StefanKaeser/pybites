import requests
from bs4 import BeautifulSoup
import re
from collections import namedtuple

cached_so_url = "https://bites-data.s3.us-east-2.amazonaws.com/so_python.html"

multiplier_str_to_float = {"": 1, "k": 10e3, "m": 10e6}

Question = namedtuple("Question", "title votes view")
    
VIEW_FILTER = 10e6

def _views_string_to_int(views):
    match = re.search(r"(\d+\.*\d*)(\w*) views", views)
    number, multiplier_str = match.groups()
    return int(float(number) * multiplier_str_to_float[multiplier_str])


def top_python_questions(url=cached_so_url):
    """Use requests to retrieve the url / html,
       parse the questions out of the html with BeautifulSoup,
       filter them by >= 1m views ("..m views").
       Return a list of (question, num_votes) tuples ordered
       by num_votes descending (see tests for expected output).
    """
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    titles = soup.find_all("a", class_="question-hyperlink")
    votes = soup.find_all("span", class_="vote-count-post")
    views = soup.find_all("div", class_="views")

    questions = []
    for title, vote, view in zip(titles, votes, views):
        question = Question(
            title.text.strip(), int(vote.text), _views_string_to_int(view.text)
        )
        if question.view >= VIEW_FILTER:
            questions.append(question)
    questions = sorted(questions, key=lambda x: x.votes, reverse=True)
    return [(question.title, question.votes) for question in questions]
