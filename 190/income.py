import os
from pathlib import Path
from urllib.request import urlretrieve
import xml.etree.ElementTree as ET
from collections import defaultdict

# import the countries xml file
tmp = Path(".")
countries = tmp / "countries.xml"

if not countries.exists():
    urlretrieve(
        "https://bites-data.s3.us-east-2.amazonaws.com/countries.xml", countries
    )

NAMESPACE = {"wb": "http://www.worldbank.org"}


def get_income_distribution(xml=countries):
    """
    - Read in the countries xml as stored in countries variable.
    - Parse the XML
    - Return a dict of:
      - keys = incomes (wb:incomeLevel)
      - values = list of country names (wb:name)
    """
    tree = ET.parse(xml)
    root = tree.getroot()

    countries = root.findall("wb:country", NAMESPACE)

    income_countries = defaultdict(list)
    for country in countries:
        name = country.find("wb:name", NAMESPACE).text
        income = country.find("wb:incomeLevel", NAMESPACE).text
        income_countries[income].append(name)

    return income_countries
