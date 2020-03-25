# nice snippet: https://gist.github.com/tonybruess/9405134
from collections import namedtuple
import re

social_platforms = """Twitter
  Min: 1
  Max: 15
  Can contain: a-z A-Z 0-9 _

Facebook
  Min: 5
  Max: 50
  Can contain: a-z A-Z 0-9 .

Reddit
  Min: 3
  Max: 20
  Can contain: a-z A-Z 0-9 _ -
"""

# note range is of type range and regex is a re.compile object
Validator = namedtuple("Validator", "range regex")


def parse_social_platforms_string():
    """Convert the social_platforms string above into a dict where
       keys = social platformsname and values = validator namedtuples"""
    name_validator = dict()

    regex = r"(\w*)\n\s*Min: (\d+)\n\s+Max: (\d*)\n\s*Can contain: (.*)"
    for social_platform in social_platforms.split("\n\n"):
        name, min, max, contains = re.match(regex, social_platform).groups()
        contains = "".join(contains.split())

        name_validator[name] = Validator(
            range(int(min), int(max)), re.compile(rf"[{contains}]*")
        )

    return name_validator


def validate_username(platform, username):
    """Receives platforms(Twitter, Facebook or Reddit) and username string,
       raise a ValueError if the wrong platform is passed in,
       return True/False if username is valid for entered platform"""
    all_validators = parse_social_platforms_string()
    try:
        validator = all_validators[platform]
    except KeyError:
        raise ValueError(f"There exists no validator for the platform '{platform}'.")

    print(validator)
    if len(username) not in validator.range:
        return False
    return bool(validator.regex.fullmatch(username))
