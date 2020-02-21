import os
import urllib.request
import re
from collections import Counter

# data provided
tmp = "."
stopwords_file = os.path.join(tmp, "stopwords")
harry_text = os.path.join(tmp, "harry")
urllib.request.urlretrieve(
   'https://bites-data.s3.us-east-2.amazonaws.com/stopwords.txt',
   stopwords_file
)
urllib.request.urlretrieve(
   'https://bites-data.s3.us-east-2.amazonaws.com/harry.txt',
   harry_text
)


def get_harry_most_common_word():
    with open(harry_text) as f:
        harry = f.read()

    harry = harry.lower()
    harry = re.sub("[^a-z ']+", " ", harry)
    words = harry.split()

    with open(stopwords_file) as f:
        stopwords = f.read().split()
    words = [word for word in words if word not in stopwords]

    word_counter = Counter(words)
    return word_counter.most_common(1)[0]
