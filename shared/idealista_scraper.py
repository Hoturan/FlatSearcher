import requests
from typing import List
from bs4 import BeautifulSoup, element

from shared.config import settings
from shared.flat_scraper import FlatScraper
from shared.logger import logger
import shared.flat as FlatModule


class IdealistaScraper(FlatScraper):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "cookie": settings.session_id,
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    }

    def scrape_link(self, url: str) -> BeautifulSoup:
        try:
            assert url.startswith("https://www.idealista.com")
            response = self.get_request_with_custom_headers(url)
            parsed_response = self.parse_request_response(response)
            self.check_if_parsed_response_is_correct(parsed_response)
            return parsed_response
        except AssertionError as e:
            logger.error(
                f"Exception {e}, url passed does not point to idealista or does not include the appropiate format."
            )

    def check_if_parsed_response_is_correct(self, parsed_response: BeautifulSoup):
        try:
            flat_container = parsed_response.findAll("article")
            assert len(flat_container) > 0
        except AssertionError as e:
            logger.error(
                f"Exception {e}, no flats contained in the css element article."
            )

    def get_request_with_custom_headers(self, url: str) -> requests.models.Response:
        try:
            response = requests.get(url=url, headers=self.headers)
            return response
        except requests.exceptions.HTTPError as e:
            logger.error(f"Exception {e}, server responds with 404.")
            raise requests.exceptions.HTTPError
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Exception {e}, connection error.")
            raise requests.exceptions.ConnectionError
        except requests.exceptions.Timeout as e:
            logger.error(f"Exception {e}, timeout.")
            raise requests.exceptions.Timeout

    def parse_request_response(
        self, response: requests.models.Response
    ) -> BeautifulSoup:
        return BeautifulSoup(response.text, features="html.parser")


class IdealistaPageParser:
    # TODO this should not be here, IdelistaPageParser does not need to know the concepts dealt with by a Flat
    item_tag_dictionary = {
        FlatModule.PRICE: "price-row",
        FlatModule.NAME: "item-description description",
        FlatModule.NUMBER_OF_ROOMS: "item-detail-char",
        FlatModule.SPACE: "item-detail-char",
        FlatModule.SUMMARY: "item-detail-char",
        FlatModule.LINK: "item-link",
        FlatModule.DESCRIPTION: "item-description description",
    }

    item_section_dictionary = {
        FlatModule.PRICE: "div",
        FlatModule.NAME: "div",
        FlatModule.NUMBER_OF_ROOMS: "div",
        FlatModule.SPACE: "div",
        FlatModule.SUMMARY: "div",
        FlatModule.LINK: "a",
        FlatModule.DESCRIPTION: "div",
    }

    """ As this information is all under the same tag, I extract it as a list. This dictionary manages the location of the info"""
    details_tag_index_dictionary = {"rooms": 1, "space": 2, "floor_summary": 3}

    def get_flats_from_parsed_response(
        self, parsed_response: BeautifulSoup
    ) -> List[FlatModule.Flat]:
        flat_container_list = self.extract_flat_container(parsed_response)
        list_of_flats = self.create_list_of_flats_from_flat_container(
            flat_container_list
        )
        return list_of_flats

    def extract_flat_container(
        self, parsed_response: BeautifulSoup
    ) -> List[element.ResultSet]:
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
            price = self.get_data_from_tag(FlatModule.PRICE, flat_container)
            name = self.get_data_from_tag(FlatModule.NAME, flat_container)
            number_of_rooms = self.get_data_from_tag(
                FlatModule.NUMBER_OF_ROOMS, flat_container
            )
            space = self.get_data_from_tag(FlatModule.SPACE, flat_container)
            summary = self.get_data_from_tag(FlatModule.SUMMARY, flat_container)
            link = self.get_data_from_tag(FlatModule.LINK, flat_container)
            description = self.get_data_from_tag(FlatModule.DESCRIPTION, flat_container)

            flat = FlatModule.Flat(
                price=price,
                name=name,
                number_of_rooms=number_of_rooms,
                space=space,
                summary=summary,
                link=link,
                description=description,
            )
            list_of_flats.append(flat)

        return list_of_flats

    def get_data_from_tag(self, flat_container: element.Tag, flat_item: str):
        found_data = flat_container.find(
            self.item_section_dictionary[flat_item],
            {"class": self.item_tag_dictionary[flat_container]},
        )

        # if it is one of the details elements, send the corresponding one
        if self.item_tag_dictionary[flat_container] == "item-detail-char":
            return found_data.text.split("\n")[
                self.details_tag_index_dictionary[flat_item]
            ]
        else:
            return found_data.text.replace("\n", "")
