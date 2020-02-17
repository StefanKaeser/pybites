import os
from collections import Counter
import urllib.request
import re

# prep
tempfile = os.path.join("./", "feed")
urllib.request.urlretrieve(
    "https://bites-data.s3.us-east-2.amazonaws.com/feed", tempfile
)

with open(tempfile) as f:
    content = f.read().lower()

XML_TAG = "category"


def get_pybites_top_tags(n=10):
    """use Counter to get the top 10 PyBites tags from the feed
       data already loaded into the content variable"""

    tags = re.findall(rf"<{XML_TAG}>(\w+)</{XML_TAG}>", content)
    tag_counter = Counter(tags)
    return tag_counter.most_common(n)
