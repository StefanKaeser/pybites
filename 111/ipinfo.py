import requests
import json

IPINFO_URL = "http://ipinfo.io/{ip}/json"


def get_ip_country(ip_address):
    """Receives ip address string, use IPINFO_URL to get geo data,
       parse the json response returning the country code of the IP"""
    url = IPINFO_URL.format(ip=ip_address)
    #with requests.get(url) as r:
    #    ip_json = json.loads(r.text)
    r = requests.get(url)
    ip_json = json.loads(r.text)
    return ip_json["country"]
