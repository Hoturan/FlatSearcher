import abc
from bs4 import BeautifulSoup


class FlatScraper(metaclass=abc.ABCMeta):
    """Abstract class to define what functions a scraper should have, to keep it extenable to other websites."""

    @abc.abstractmethod
    def scrape_link(url: str) -> BeautifulSoup:
        pass