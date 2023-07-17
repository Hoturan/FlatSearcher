"""
Module containing the abstact for FlatScraper, in case the project was extended with
other websites.
"""
import abc
from bs4 import BeautifulSoup


class FlatScraper(metaclass=abc.ABCMeta):
    """
    Abstract class to define what functions a scraper should have,
    to keep it extenable to other websites.
    """

    @abc.abstractmethod
    def scrape_link(self, url: str) -> BeautifulSoup:
        """
        Perfoms a call to the passed url and returns a beautifulsoup object with the
        found contents.

        Args:
            url (str): url pointing to a flat website

        Returns:
            BeautifulSoup: Parsed html contents
        """

    @abc.abstractmethod
    def parse_request_response(self, response_text: str) -> BeautifulSoup:
        """
        Parses a request response text into a beautifulsoup object.

        Args:
            response_text (str): response text

        Returns:
            BeautifulSoup: Parsed html contents
        """
