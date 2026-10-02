# ============================================================
# ROBOTS.TXT
# ============================================================
import requests
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser

robot_cache = {}


def allowed_by_robots(url):

    parsed = urlparse(url)

    domain = f"{parsed.scheme}://{parsed.netloc}"

    if domain not in robot_cache:

        robots_url = urljoin(domain, "/robots.txt")

        parser = RobotFileParser()

        parser.set_url(robots_url)

        try:
            parser.read()
        except Exception:
            return False

        robot_cache[domain] = parser

    return robot_cache[domain].can_fetch(
        "MiniSearchBot",
        url
    )
