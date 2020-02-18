"""Checks community branch dir structure to see who submitted most
   and what challenge is more popular by number of PRs"""
from collections import Counter, namedtuple
import os
import urllib.request

# prep
# tmp = os.getenv("TMP", "/tmp")
tempfile = os.path.join("./", "dirnames")
urllib.request.urlretrieve(
    "https://bites-data.s3.us-east-2.amazonaws.com/dirnames.txt", tempfile
)

IGNORE = "static templates data pybites bbelderbos hobojoe1848".split()

users, popular_challenges = Counter(), Counter()

Stats = namedtuple("Stats", "user challenge")


def gen_file():
    with open(tempfile, "r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        file_or_dir, is_dir = line.split(",")
        if is_dir == "True":
            yield file_or_dir


def diehard_pybites():
    """Return a Stats namedtuple (defined above) that contains the user that
       made the most PRs (ignoring the users in IGNORE) and a challenge tuple
       of most popular challenge and the amount of PRs for that challenge.
       Calling this function on the dataset (held tempfile) should return:
       Stats(user='clamytoe', challenge=('01', 7))
    """
    challenges, users = zip(*[dir.split("/") for dir in gen_file()])

    users = [user for user in users if user not in IGNORE]
    most_active_user = Counter(users).most_common(1)[0][0]
    most_common_challenge = Counter(challenges).most_common(1)[0]
    return Stats(most_active_user, most_common_challenge)
