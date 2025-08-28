from typing import Iterable
import itertools
import re
import logging
from string import ascii_lowercase

import requests

from src.utils.api_calls import make_api_call
import src.utils.constants as constants


github_regex = re.compile(r"https://github\.com/([^/]+)/([^/]+)")


def get_most_popular_packages(platform: str, count: int, from_: int) -> list[dict]:
    """Gets the most popular packages packages for a particular platform

    Example data:
    [
        {
            "name": "numpy",
            "platform": "pypi",
            "owner": "pypi",
            "version": "1.0.2"
        }
    ]
    """
    if platform == "npm":
        packages = get_most_popular_packages_npm()
    else:
        packages = get_most_popular_packages_pypi()

    packages_with_data = filter(None, map(lambda p: get_package_data(p, platform), packages))
    return list(itertools.islice(packages_with_data, from_, from_ + count))


def get_most_popular_packages_pypi() -> Iterable[str]:
    """Get a list of the most popular packages of the last 30 days from a json
    dump."""
    resp = requests.get(
        "https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json"
    )
    resp.json()
    return (row["project"] for row in resp.json()["rows"])


def get_most_popular_packages_npm() -> Iterable[str]:
    """Get a list of the most popular packages of the last 30 days from the
    npms api."""
    accumulator: set[tuple[str, float]] = set()

    request_size = 250

    for from_ in range(0, 5000, request_size):
        # somewhat cursed what we are doing here, but there is no endpoint
        # where we can just get the most popular packages, instead we search
        # for each letter where the result are sorted by popularity, and add
        # the results
        for letter in ascii_lowercase:
            resp = requests.get(
                "https://api.npms.io/v2/search",
                params=
                    f"q={letter}+boost-exact:false+score-effect:25+popularity-weight:50"
                    "&size=250"
                    f"&from={from_}",
            )
            resp.raise_for_status()
            json_resp = resp.json()
            for package in json_resp["results"]:
                accumulator.add(
                    (package["package"]["name"], package["score"]["detail"]["popularity"])
                )

        sorted = list(accumulator)
        sorted.sort(key=lambda x: x[1], reverse=True)
        yield from map(lambda x: x[0], sorted[from_: from_ + round(len(accumulator) / 4)])


def get_package_data(name: str, platform: str) -> dict | None:
    """Takes a package name and returns a dict with additional package
    information: repository owner and most recent version."""
    repo_url = get_repo_link(name, platform)
    if not repo_url:
        return None
    match = github_regex.match(repo_url)
    if match is not None:
        (owner, name_git) = match.group(1, 2)
    else:
        return None
    if name_git != name:
        logging.warning(f"name not same as repo name {name} {name_git}")
        return None
    version = get_most_recent_version(name_git, owner, platform)
    if version is None or version == "":
        return None
    return {
        "name": name,
        "platform": platform,
        "owner": owner,
        "version": version
    }


def get_repo_link(name: str, platform: str) -> str | None:
    """Get the repository link of a package."""
    url = f"https://libraries.io/api/{platform}/{name}"
    resp = make_api_call(url, constants.API_LIBRARIES)
    if not resp:
        return None
    return resp.json()["repository_url"]


def get_most_recent_version(name: str, owner: str, platform: str) -> str:
    """Get the most recent version of a package from cosy."""
    url = "http://web:3000/api/dlt/get-most-recent-version/"
    json = {
        "name": name,
        "platform": platform,
        "owner": owner,
    }
    return requests.post(url, json, timeout=10, verify=False).text
