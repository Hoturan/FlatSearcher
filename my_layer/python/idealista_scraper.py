""" This module deals with both the scraping and the parsing of the idealista website. """

import re
from typing import List
import requests
from bs4 import BeautifulSoup, element

from flat_scraper import FlatScraper
import flat as FlatModule
from logger import LOGGER as logger

class IdealistaScraper(FlatScraper):
    """ Contians all code for the scraping of the idealista webpage """

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
          AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "cookie": "SESSION=88b3e9dc5e9b8b33~3c9cc824-0077-44e9-a045-74e00b9025cb",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    }

    def scrape_link(self, url: str) -> BeautifulSoup:
        """
        Given an idealista url, performs a get request, parses it into a beautifulsoup4 object
        and returns the parsed object. 

        Args:
            url (str): string containing an idealista url for a particular search
        
        Returns:
            BeautifulSoup: BeautifulSoup object containing the http code. 
        """
        try:
            assert url.startswith("https://www.idealista.com")
            response = self.get_request_with_custom_headers(url)
            parsed_response = self.parse_request_response(response.text)
            self.check_if_parsed_response_is_correct(parsed_response)
            return parsed_response
        except AssertionError as assertion_error:
            logger.error(
                f"Exception {assertion_error}, url passed does not point to idealista  \
                or does not include the appropiate format."
            )
            raise AssertionError

    def check_if_parsed_response_is_correct(self, parsed_response: BeautifulSoup):
        """
        Checks if a response is in the correct shape by checking if there are flats
        in the code ("articles")

        Args:
            parsed_response (BeautifulSoup): BeautifulSoup containing an idealista http code.
        
        Returns:
            Boolean: true if articles where found in the code
        """

        try:
            flat_container = parsed_response.findAll("article")
            assert len(flat_container) > 0
        except AssertionError as assertion_error:
            logger.error(
                f"Exception {assertion_error}, no flats contained in the css element article."
            )

    def get_request_with_custom_headers(self, url: str) -> requests.models.Response:
        """
        Performs the request call with the headers specified at the class level.

        Args:
            url (str): url to call to. 
        
        Returns:
            requests.models.Response: response object.
        """

        try:
            response = requests.get(url=url, headers=self.headers, timeout=10)
            return response
        except requests.exceptions.HTTPError as HTTPerror:
            logger.error(f"Exception {HTTPerror}, server responds with 404.")
            raise requests.exceptions.HTTPError
        except requests.exceptions.ConnectionError as connection_error:
            logger.error(f"Exception {e}, connection error.")
            raise requests.exceptions.ConnectionError
        except requests.exceptions.Timeout as e:
            logger.error(f"Exception {e}, timeout.")
            raise requests.exceptions.Timeout

    def parse_request_response(self, response_text: str) -> BeautifulSoup:
        """
        Parses the response text from a response call and turns it into a beautifulsoup object.

        Args:
            response_text (str): text from a get request.
        
        Returns:
            BeautifulSoup: parsed object.
        """

        return BeautifulSoup(response_text, features="html.parser")


class IdealistaPageParser:
    """ Contians all code for the parsing of the idealista webpage """

    item_tag_dictionary = {
        FlatModule.ID: "item-link",
        FlatModule.NAME: "item-link",
        FlatModule.PRICE: "price-row",
        FlatModule.PRICE_CURRENCY: "price-row",
        FlatModule.NUMBER_OF_ROOMS: "item-detail-char",
        FlatModule.SPACE: "item-detail-char",
        FlatModule.LINK: "item-link",
        FlatModule.DESCRIPTION: "item-description description",
        FlatModule.SUMMARY: "item-detail-char",
    }

    item_section_dictionary = {
        FlatModule.ID: "a",
        FlatModule.PRICE: "div",
        FlatModule.PRICE_CURRENCY: "div",
        FlatModule.NAME: "a",
        FlatModule.NUMBER_OF_ROOMS: "div",
        FlatModule.SPACE: "div",
        FlatModule.SUMMARY: "div",
        FlatModule.LINK: "a",
        FlatModule.DESCRIPTION: "div",
    }

    """ As this information is all under the same tag, I extract it as a list. This dictionary manages the location of the info"""
    details_tag_index_dictionary = {
        FlatModule.NUMBER_OF_ROOMS: 1,
        FlatModule.SPACE: 2,
        FlatModule.SUMMARY: 3,
    }

    def get_flats_from_parsed_response(
        self, parsed_response: BeautifulSoup
    ) -> List[FlatModule.Flat]:
        """
        Creates a list of Flatsd given a BeautifulSoup oobject conainting the response of
        a idealista page.

        Args:
            parsed_response (BeautifulSoup): contains the idealista html data
        
        Returns:
            List[FlatModule.Flat]: List of found Flats
        """
        flat_container_list = self.extract_flat_container(parsed_response)
        list_of_flats = self.create_list_of_flats_from_flat_container(
            flat_container_list
        )
        return list_of_flats

    def extract_flat_container(
        self, parsed_response: BeautifulSoup
    ) -> List[element.ResultSet]:
        """
        Gets all the "article" tags from a beautifulsoup object. Flats in idealista are included
        under the article sections.

        Args:
            parsed_response (BeautifulSoup): contains the idealista html data
        
        Returns:
            List[element.ResultSet]: List of found articles
        """
        try:
            flat_container_list = parsed_response.findAll("article")
            assert len(flat_container_list) > 0
            return flat_container_list
        except AssertionError as e:
            logger.error(
                f"Exception {e}, no articles found when extracting the flat containers out of the parsed response."
            )
            raise e
        except Exception as e:
            logger.error(
                f"Exception {e}, error when extracting flat containers out of the parsed response."
            )
            raise e

    def create_list_of_flats_from_flat_container(
        self,
        flat_container_list: List[element.ResultSet],
    ) -> List[FlatModule.Flat]:
        list_of_flats = []
        for flat_container in flat_container_list:
            try:
                flat = self.extract_items_from_flat(flat_container)
                list_of_flats.append(flat)
            except:
                continue
        return list_of_flats

    def extract_items_from_flat(self, flat_container) -> FlatModule.Flat:
        try:
            id = self.get_data_from_tag(flat_container, FlatModule.ID)
            price = self.get_data_from_tag(flat_container, FlatModule.RICE)
            price_currency = self.get_data_from_tag(
                flat_container, FlatModule.PRICE_CURRENCY
            )
            name = self.get_data_from_tag(flat_container, FlatModule.NAME)
            number_of_rooms = self.get_data_from_tag(
                flat_container, FlatModule.NUMBER_OF_ROOMS
            )
            space = self.get_data_from_tag(flat_container, FlatModule.SPACE)
            summary = self.get_data_from_tag(flat_container, FlatModule.SUMMARY)
            link = self.get_data_from_tag(flat_container, FlatModule.LINK)
            description = self.get_data_from_tag(flat_container, FlatModule.DESCRIPTION)

            flat = FlatModule.Flat(
                id=id,
                price=price,
                price_currency=price_currency,
                name=name,
                number_of_rooms=number_of_rooms,
                space=space,
                summary=summary,
                link=link,
                description=description
            )
            return flat
        except Exception as e:
            logger.error(f"Exception {e}, article found is not a flat.")
            raise e

    def get_data_from_tag(self, flat_container: element.Tag, flat_item: str):
        found_data = flat_container.find(
            self.item_section_dictionary[flat_item],
            {"class": self.item_tag_dictionary[flat_item]},
        )

        # if it is one of the details elements, send the corresponding one
        if self.item_tag_dictionary[flat_item] == "item-detail-char":
            return found_data.text.split("\n")[
                self.details_tag_index_dictionary[flat_item]
            ]
        if flat_item == FlatModule.PRICE_CURRENCY:
            return self.get_currency_from_price_string(found_data.text)
        if flat_item == FlatModule.PRICE:
            return self.get_value_from_price_string(found_data.text)
        if flat_item == FlatModule.LINK:
            return found_data["href"]
        if flat_item == FlatModule.ID:
            # splits the string "/inmueble/98978138/" and takes the id
            return found_data["href"].split("/")[2]
        
        return found_data.text.replace("\n", "")

    def get_currency_from_price_string(self, price_string):
        return re.sub(r"[a-zA-Z]", "", price_string).strip()[-1]

    def get_value_from_price_string(self, price_string):
        return re.sub(r"[a-zA-Z]", "", price_string).strip()[:-1]
