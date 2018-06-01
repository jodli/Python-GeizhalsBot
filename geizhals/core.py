# -*- coding: utf-8 -*-
import re
import logging
import urllib.request
from datetime import datetime
from urllib.error import HTTPError

from pyquery import PyQuery

logger = logging.getLogger(__name__)
useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) " \
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 " \
                "Safari/537.36"


def send_request(url):
    logger.debug("Requesting url '{}'!".format(url))

    req = urllib.request.Request(
        url,
        data=None,
        headers={'User-Agent': useragent}
    )

    f = urllib.request.urlopen(req)
    html = f.read().decode('utf-8')
    return html


def parse_html(html, selector):
    pq = PyQuery(html)
    return pq(selector).text()


def parse_wishlist_price(html):
    selector = "div.productlist__footer-cell span.gh_price"
    price = parse_html(html, selector)
    price = price[2:]  # Cut off the '€ ' before the real price
    price = price.replace(',', '.')
    return price

def parse_wishlist_id(html):
    selector = ""
    id = parse_html(html, selector)
    return id

def parse_wishlist_name(html):
    selector = "h1.gh_listtitle"
    name = parse_html(html, selector)
    return name
