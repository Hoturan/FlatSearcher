"""
Function that runs the scraping of the idealista URLs
"""

# Copyright 2016 1Strategy, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function
import json
from urllib.parse import urlparse

from idealista_scraper import IdealistaScraper, IdealistaPageParser
from logger import LOGGER as logger


def lambda_handler(event, context):
    """
    Reciever of the lambda invoke
    """
    try:
        assert isinstance(event, dict)
        assert "scrape_locations" not in event or "url_root" not in event

        flat_scaper_instance = IdealistaScraper()
        flat_parser_instance = IdealistaPageParser()
        flats_json_list = []
        for scrape_location in event["scrape_locations"]:
            prepared_url = event["url_root"] + scrape_location
            flats_list = get_flats_from_location(
                prepared_url, flat_scaper_instance, flat_parser_instance
            )
            flats_json_list = flats_json_list + flats_list
        return {
            "statusCode": 200,
            "body": json.dumps(
                {"message": "Success", "data": json.dumps(flats_json_list)}
            ),
        }
    except AssertionError as assertion_error:
        logger.error(
            "Event argument not in the expected format, \
            either expected keys are not found or the event is corrupted."
        )
        raise assertion_error


def get_flats_from_location(prepared_url, flat_scaper_instance, flat_parser_instance):
    """
    Requests and scrapes the flats from a given idealista url

    Args:
        prepared_url (str): url to scrape from
        flat_scraper_instance (FlatScraper): scaper to call to extract the flats
        flat_parser_instance (FlatParser): parser to parse the response

    Returns:
        List[dict]: list of dictionaries including the flats
    """
    flat_json_list = []
    first_url = prepared_url
    response = flat_scaper_instance.get_request_with_custom_headers(first_url)
    latest_url = ""
    i = 0
    while first_url != latest_url or i == 1:
        i += 1
        print(f"In page {i}")
        next_page = first_url + f"pagina-{i}.htm"
        response = flat_scaper_instance.get_request_with_custom_headers(next_page)
        latest_url = response.url
        #  This condition prevents the scaping of the first page again if the search returns
        #  only one page.
        if latest_url == first_url and i == 2:
            break
        parsed_response = flat_scaper_instance.parse_request_response(response.text)
        flat_list_for_page = flat_parser_instance.get_flats_from_parsed_response(
            parsed_response
        )
        for flat in flat_list_for_page:
            parsed_url = urlparse(prepared_url)
            flat.location = parsed_url.path.split("/")[2:-1]
            flat_json_list.append(flat.to_json())
    return flat_json_list
