from abc import ABC, abstractmethod
from collections import namedtuple
from dataclasses import dataclass
from datetime import date
from os import getenv
import os
from pathlib import Path
from typing import Any, List, Optional
from urllib.request import urlretrieve
import itertools

from bs4 import BeautifulSoup as Soup  # type: ignore

# TMP = getenv("TMP", "/tmp")
TMP = "files"
TODAY = date.today()
Candidate = namedtuple("Candidate", "name votes")
LeaderBoard = namedtuple(
    "LeaderBoard", "Candidate Average Delegates Contributions Coverage"
)
Poll = namedtuple("Poll", "Poll Date Sample Sanders Biden Gabbard Spread",)


YEAR = 2020

@dataclass
class File:
    """File represents a filesystem path.

    Variables:
        name: str -- The filename that will be created on the filesystem.
        file: Path -- Path object created from the name passed in.

    Methods:
        [property]
        data: -> Optional[str] -- If the file exists, it returns its contents.
            If it does not exists, it returns None.
    """

    name: str

    def __post_init__(self):
        self.path = Path(os.path.join(TMP, f"{TODAY}_{self.name}"))

    @property
    def data(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                return f.read()
        return None


@dataclass
class Web:
    """Web object.

    Web is an object that downloads the page from the url that is passed
    to it and stores it in the File instance that is passed to it. If the
    File already exists, it just reads the file, otherwise it downloads it
    and stores it in File.

    Variables:
        url: str -- The url of the web page.
        file: File -- The File object to store the page data into.

    Methods:
        [property]
        data: -> Optional[str] -- Reads the text from File or retrieves it from the
            web if it does not exists.

        [property]
        soup: -> Soup -- Parses the data from File and turns it into a BeautifulSoup
            object.
    """

    url: str
    file: File

    @property
    def data(self) -> Optional[str]:
        """Reads the data from the File object.

        First it checks if the File object has any data. If it doesn't, it retrieves
        it and saves it to the File. Once the. It then reads it from the File and
        returns it.

        Returns:
            Optional[str] -- The string data from the File object.
        """
        data = self.file.data
        if data:
            return data
        urlretrieve(self.url, self.file.path)
        return self.file.data

    @property
    def soup(self) -> Soup:
        """Converts string data from File into a BeautifulSoup object.

        Returns:
            Soup -- BeautifulSoup object created from the File.
        """
        return Soup(self.data, "html.parser")


class Site(ABC):
    """Site Abstract Base Class.

    Defines the structure for the objects based on this class and defines the interfaces
    that should implemented in order to work properly.

    Variables:
        web: Web -- The web object stores the information needed to process
            the data.

    Methods:
        find_table: -> str -- Parses the Web object for table elements and
            returns the first one that it finds unless an integer representing
            the required table is passed.

        [abstractmethod]
        parse_rows: -> Union[List[LeaderBoard], List[Poll]] -- Parses a BeautifulSoup
            table element and returns the text found in the td elements as
            namedtuples.

        [abstractmethod]
        polls: -> Union[List[LeaderBoard], List[Poll]] -- Does the parsing of the table
            and rows for you. It takes the table index number if given, otherwise
            parses table 0.

        [abstractmethod]
        stats: -- Formats the results from polls into a more user friendly
            representation.
    """

    web: Web

    def find_table(self, loc: int = 0) -> str:
        """Finds the table elements from the Soup object

        Keyword Arguments:
            loc {int} -- Parses the Web object for table elements and
                returns the first one that it finds unless an integer representing
                the required table is passed. (default: {0})

        Returns:
            str -- The html table
        """
        soup = self.web.soup
        tables = soup.find_all("table")
        return tables[loc]

    @abstractmethod
    def parse_rows(self, table: Soup) -> List[Any]:
        """Abstract Method
        
        Parses the row data from the html table.

        Arguments:
            table {Soup} -- Parses a BeautifulSoup table element and
                returns the text found in the td elements as NamedTuple.

        Returns:
            List[NamedTuple] -- List of NamedTuple that were created from the
                table data.
        """
        pass

    @abstractmethod
    def polls(self, table: int = 0) -> List[Any]:
        """Abstract Method

        Parses the data

        The find_table and parse_rows methods are called for you and the table index
        that is passed to it is used to get the correct table from the soup object.

        Keyword Arguments:
            table {int} -- Does the parsing of the table and rows for you.
                It takes the table index number if given, otherwise parses table 0.
                (default: {0})

        Returns:
            List[NamedTuple] -- List of NamedTuple that were created from the
                table data.
        """
        pass

    @abstractmethod
    def stats(self, loc: int = 0):
        """Abstract Method
        
        Produces the stats from the polls.

        Keyword Arguments:
            loc {int} -- Formats the results from polls into a more user friendly
            representation.
        """
        pass


@dataclass
class RealClearPolitics(Site):
    """RealClearPolitics object.

    RealClearPolitics is a custom class to parse a Web instance from the
    realclearpolitics website.

    Variables:
        web: Web -- The web object stores the information needed to process
            the data.

    Methods:
        find_table: -> str -- Parses the Web object for table elements and
            returns the first one that it finds unless an integer representing
            the required table is passed.

        parse_rows: -> List[Poll] -- Parses a BeautifulSoup table element and
            returns the text found in the td elements as Poll namedtuples.

        polls: -> List[Poll] -- Does the parsing of the table and rows for you.
            It takes the table index number if given, otherwise parses table 0.

        stats: -- Formats the results from polls into a more user friendly
            representation:

            Example:

            RealClearPolitics
            =================
                Biden: 214.0
              Sanders: 142.0
              Gabbard: 6.0

    """

    web: Web

    def parse_rows(self, table: Soup) -> List[Poll]:
        """Parses the row data from the html table.

        Arguments:
            table {Soup} -- Parses a BeautifulSoup table element and
                returns the text found in the td elements as Poll namedtuples.

        Returns:
            List[Poll] -- List of Poll namedtuples that were created from the
                table data.
        """
        rows = table.find_all("tr")[1:]

        polls = []
        for row in rows:
            columns = [tag.text for tag in row.find_all("td")]
            poll, time_stamp, sample, biden, sanders, gabbard, spread = columns

            start, end = [d.split("/") for d in time_stamp.split("-")]
            start = date(year=YEAR, month=int(start[0]), day=int(start[1]))
            end = date(year=YEAR, month=int(end[0]), day=int(end[1]))

            biden = float(biden) if biden.isdigit() else 0.0
            sanders = float(sanders) if sanders.isdigit() else 0.0
            gabbard = float(gabbard) if gabbard.isdigit() else 0.0
        
            poll = Poll(poll, (start, end), sample, sanders, biden, gabbard, spread,)
            polls.append(poll)
            
        return polls

    def polls(self, table: int = 0) -> List[Poll]:
        """Parses the data

        The find_table and parse_rows methods are called for you and the table index
        that is passed to it is used to get the correct table from the soup object.

        Keyword Arguments:
            table {int} -- Does the parsing of the table and rows for you.
                It takes the table index number if given, otherwise parses table 0.
                (default: {0})

        Returns:
            List[Poll] -- List of Poll namedtuples that were created from the
                table data.
        """
        table = self.find_table(table)
        polls = self.parse_rows(table)
        return polls

    def stats(self, loc: int = 0):
        """Produces the stats from the polls.

        Keyword Arguments:
            loc {int} -- Formats the results from polls into a more user friendly
            representation.

        """
        polls = self.polls(loc)[1:] # No average
        biden = Candidate("Biden", sum([poll.Biden for poll in polls]))
        sanders = Candidate("Sanders", sum([poll.Sanders for poll in polls]))
        gabbard = Candidate("Gabbard", sum([poll.Gabbard for poll in polls]))

        stats = "\nRealClearPolitics\n"
        stats += "="*(len(stats.strip())) + "\n"
        stats += f"{biden.name:>8}: {biden.votes}\n"
        stats += f"{sanders.name:>8}: {sanders.votes}\n"
        stats += f"{gabbard.name:>8}: {gabbard.votes}\n"

        print(stats)
        

@dataclass
class NYTimes(Site):
    """NYTimes object.

    RealClearPolitics is a custom class to parse a Web instance from the
    realclearpolitics website.

    Variables:
        web: Web -- The web object stores the information needed to process
            the data.

    Methods:
        find_table: -> str -- Parses the Web object for table elements and
            returns the first one that it finds unless an integer representing
            the required table is passed.

        parse_rows: -> List[LeaderBoard] -- Parses a BeautifulSoup table element and
            returns the text found in the td elements as LeaderBoard namedtuples.

        polls: -> List[LeaderBoard] -- Does the parsing of the table and rows for you.
            It takes the table index number if given, otherwise parses table 0.

        stats: -- Formats the results from polls into a more user friendly
            representation:

            Example:

            NYTimes
            =================================

                               Pete Buttigieg
            ---------------------------------
            National Polling Average: 10%
                   Pledged Delegates: 25
            Individual Contributions: $76.2m
                Weekly News Coverage: 3

    """

    web: Web

    def parse_rows(self, table: Soup) -> List[LeaderBoard]:
        """Parses the row data from the html table.

        Arguments:
            table {Soup} -- Parses a BeautifulSoup table element and
                returns the text found in the td elements as LeaderBoard namedtuples.

        Returns:
            List[LeaderBoard] -- List of LeaderBoard namedtuples that were created from
            the table data.
        """
        rows = table.find_all("tr")[1:]
        NUM_CANDIDATES = 3
        leaderboards = []
        for row in rows[:NUM_CANDIDATES]:
            tags = [tag for tag in row.find_all('td')]
            texts = [tag.text for tag in tags] 
            _, average, delegates, contributions, coverage = texts
            # Extract name seperatley cause there are 2 representations, only need 1.
            name = tags[0].find("span").text
            
            average = average.strip()
            delegates = int(delegates)
            contributions = contributions.strip()
            coverage = int(coverage.replace("#", ""))

            leaderboard = LeaderBoard(name, average, delegates, contributions, coverage)
            leaderboards.append(leaderboard)

        return leaderboards


    def polls(self, table: int = 0) -> List[LeaderBoard]:
        """Parses the data

        The find_table and parse_rows methods are called for you and the table index
        that is passed to it is used to get the correct table from the soup object.

        Keyword Arguments:
            table {int} -- Does the parsing of the table and rows for you.
                It takes the table index number if given, otherwise parses table 0.
                (default: {0})

        Returns:
            List[LeaderBoard] -- List of LeaderBoard namedtuples that were created from
                the table data.
        """
        table = self.find_table(table)
        return self.parse_rows(table)

    def stats(self, loc: int = 0):
        """Produces the stats from the polls.

        Keyword Arguments:
            loc {int} -- Formats the results from polls into a more user friendly
            representation.
        """
        leaderboards = self.polls(loc)

        stats = "\nNYTimes\n"
        stats += "="*33

        for name, average, delegates, contributions, coverage in leaderboards:
            stats += f"\n\n{name}\n"
            stats += "-"*33
            stats += f"\n{'National Polling Average':>24}: {average}"
            stats += f"\n{'Pledged Delegates':>24}: {delegates}"
            stats += f"\n{'Individual Contributions':>24}: {contributions}"
            stats += f"\n{'Weekly News Coverage':>24}: {coverage}"


        print(stats)


def gather_data():
    rcp_file = File("realclearpolitics.html")
    rcp_url = "https://bites-data.s3.us-east-2.amazonaws.com/2020-03-10_realclearpolitics.html"
    rcp_web = Web(rcp_url, rcp_file)
    rcp = RealClearPolitics(rcp_web)
    rcp.stats(3)

    nyt_file = File("nytimes.html")
    nyt_url = "https://bites-data.s3.us-east-2.amazonaws.com/2020-03-10_nytimes.html"
    nyt_web = Web(nyt_url, nyt_file)
    nyt = NYTimes(nyt_web)
    nyt.stats()


if __name__ == "__main__":
    gather_data()
