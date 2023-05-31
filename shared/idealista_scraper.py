import requests
from bs4 import BeautifulSoup
from shared.config import settings
from shared.flat_scraper import FlatScraper
from shared.logger import logger


class IdealistaScraper(FlatScraper):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "cookie": settings.session_id,
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    }

    def scrape_idealista_link(self, url: str) -> BeautifulSoup:
        assert url.startswith("www.idealista.com")
        response = self.get_request_with_custom_headers(url)
        parsed_response = self.parse_request_response(response)
        self.check_if_parsed_response_is_correct(parsed_response)
        return parsed_response

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

class IdealistaPageParser():
    