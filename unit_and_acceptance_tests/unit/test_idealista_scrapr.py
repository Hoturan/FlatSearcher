import pytest
from unittest import mock
from unittest.mock import patch

from idealista_scraper import IdealistaScraper
from unit_and_acceptance_tests.unit.mock_request_response import MockRequestResponse
import tests.test_actions


@patch(
    "shared.idealista_scraper.IdealistaScraper.get_request_with_custom_headers",
    return_value=MockRequestResponse("test"),
)
@patch(
    "shared.idealista_scraper.IdealistaScraper.parse_request_response",
    return_value="mock response",
)
@patch(
    "shared.idealista_scraper.IdealistaScraper.check_if_parsed_response_is_correct",
    return_value="mock response",
)
def test_scrape_happy_link(
    mock_check_if_parsed_response_is_correct,
    mock_parse_request_response,
    mock_get_request,
    happy_idealista_url,
):
    idealista_scraper_instance = IdealistaScraper()
    mock_response = idealista_scraper_instance.scrape_link(happy_idealista_url)
    assert mock_response == "mock response"
