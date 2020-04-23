from collections import namedtuple
import os
import pickle
import urllib.request
import re
from datetime import timedelta

# prework
# download pickle file and store it in a tmp file
pkl_file = "pycon_videos.pkl"
data = f"https://bites-data.s3.us-east-2.amazonaws.com/{pkl_file}"
# tmp = os.getenv("TMP", "/tmp")
tmp = "."
pycon_videos = os.path.join(tmp, pkl_file)
urllib.request.urlretrieve(data, pycon_videos)

# the pkl contains a list of Video namedtuples
Video = namedtuple("Video", "id title duration metrics")


def load_pycon_data(pycon_videos=pycon_videos):
    """Load the pickle file (pycon_videos) and return the data structure
       it holds"""
    pycon_data = pickle.load(open(pycon_videos, "rb"))
    return pycon_data


def get_most_popular_talks_by_views(videos):
    """Return the pycon video list sorted by viewCount"""
    sorted_videos = sorted(videos, key=get_view_count, reverse=True)
    return sorted_videos


def get_view_count(video):
    return get_from_metrics(video, "viewCount")


def get_from_metrics(video, key):
    return int(video.metrics[key])


def get_most_popular_talks_by_like_ratio(videos):
    """Return the pycon video list sorted by most likes relative to
       number of views, so 10 likes on 175 views ranks higher than
       12 likes on 300 views. Discount the dislikeCount from the likeCount.
       Return the filtered list"""
    sorted_videos = sorted(videos, key=get_abs_likes_relative_to_views, reverse=True)
    return sorted_videos


def get_abs_likes(video):
    likes = get_from_metrics(video, "likeCount")
    dislikes = get_from_metrics(video, "dislikeCount")
    return likes - dislikes


def get_abs_likes_relative_to_views(video):
    likes = get_abs_likes(video)
    views = get_from_metrics(video, "viewCount")
    return likes / views


def get_talks_gt_one_hour(videos):
    """Filter the videos list down to videos of > 1 hour"""
    one_hour = timedelta(hours=1)
    return [video for video in videos if get_duration(video) > one_hour]


def get_duration(video):
    duration_str = video.duration
    return parse_duration(duration_str)


def parse_duration(time_stamp):
    unit_regex = {"seconds": r"\d+(?=S)", "minutes": r"\d+(?=M)", "hours": r"\d+(?=H)"}

    unit_value = {}
    for unit, regex in unit_regex.items():
        match = re.search(regex, time_stamp)
        if match:
            unit_value[unit] = int(match.group(0))

    return timedelta(**unit_value)


def get_talks_lt_twentyfour_min(videos):
    """Filter videos list down to videos that have a duration of less than
       24 minutes"""
    twenty_four_minutes = timedelta(minutes=24)
    return [video for video in videos if get_duration(video) < twenty_four_minutes]
