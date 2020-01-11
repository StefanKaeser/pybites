import os
from pathlib import Path
from ipaddress import IPv4Network
from urllib.request import urlretrieve

import pytest

from ips import ServiceIPRange, parse_ipv4_service_ranges, get_aws_service_range

URL = "https://bites-data.s3.us-east-2.amazonaws.com/ip-ranges.json"
TMP = os.getenv("TMP", ".")
PATH = Path(TMP, "ip-ranges.json")
IP = IPv4Network("192.0.2.8/29")


@pytest.fixture(scope="module")
def json_file():
    """Import data into tmp folder"""
    urlretrieve(URL, PATH)
    return PATH


def test_ServiceIPRange():
    example = ServiceIPRange(service="AMAZON", region="eu-west-1", cidr=IP)
    assert (
        str(example)
        == "192.0.2.8/29 is allocated to the AMAZON service in the eu-west-1 region"
    )


def test_parse_ipv4_service_ranges(json_file):
    ipv4_service_ranges = parse_ipv4_service_ranges(json_file)

    assert type(ipv4_service_ranges) == list
    assert len(ipv4_service_ranges) == 1886
    assert all(
        [type(service_range) == ServiceIPRange for service_range in ipv4_service_ranges]
    )

    first_three = [
        ServiceIPRange(
            service="AMAZON", region="eu-west-1", cidr=IPv4Network("13.248.118.0/24")
        ),
        ServiceIPRange(
            service="AMAZON", region="us-east-1", cidr=IPv4Network("18.208.0.0/13")
        ),
        ServiceIPRange(
            service="AMAZON", region="us-east-1", cidr=IPv4Network("52.95.245.0/24")
        ),
    ]
    assert ipv4_service_ranges[:3] == first_three

    last_three = [
        ServiceIPRange(
            service="WORKSPACES_GATEWAYS",
            region="sa-east-1",
            cidr=IPv4Network("54.233.204.0/24"),
        ),
        ServiceIPRange(
            service="WORKSPACES_GATEWAYS",
            region="us-west-2",
            cidr=IPv4Network("54.244.46.0/23"),
        ),
        ServiceIPRange(
            service="WORKSPACES_GATEWAYS",
            region="ap-northeast-1",
            cidr=IPv4Network("54.250.251.0/24"),
        ),
    ]

    assert ipv4_service_ranges[-3:] == last_three


def test_get_aws_service_range(json_file):
    ipv4_service_ranges = parse_ipv4_service_ranges(json_file)
    service_range = get_aws_service_range("52.95.245.0", ipv4_service_ranges)
    expected = [
        ServiceIPRange(
            service="AMAZON", region="us-east-1", cidr=IPv4Network("52.95.245.0/24")
        ),
        ServiceIPRange(
            service="EC2", region="us-east-1", cidr=IPv4Network("52.95.245.0/24")
        ),
    ]
    assert service_range == expected


def test_get_aws_service_range_zero_hits(json_file):
    assert get_aws_service_range("13.248.118.0", []) == []


def test_get_aws_service_range_incorrect_address():
    with pytest.raises(ValueError, match="Address must be a valid IPv4 address"):
        get_aws_service_range("bogus", [])
