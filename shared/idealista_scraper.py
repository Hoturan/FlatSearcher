import requests
from bs4 import BeautifulSoup
from shared.config import settings
from shared.flat_scraper import Scraper
from shared.logger import logger


class IdealistaScraper(Scraper):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "cookie": "SESSION=88b3e9dc5e9b8b33~3c9cc824-0077-44e9-a045-74e00b9025cb",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    }

    def scrape_link(url: str):
        return

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

    def parse_request_response(response: requests.models.Response) -> BeautifulSoup:
        return BeautifulSoup(response)
