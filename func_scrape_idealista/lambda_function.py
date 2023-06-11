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
import tomli
from urllib.parse import urlparse

from flat import Flat
from idealista_scraper import IdealistaScraper, IdealistaPageParser



def get_lambda_configs():
    """
    Opens the function_config.toml to gather the Locations to scrape from idealista
    """
    with open("function_config.toml", mode="rb") as fb:
        config = tomli.load(fb)
    return config


def lambda_handler(event, context):
    
    config = get_lambda_configs()
    flat_scaper_instance = IdealistaScraper()
    flat_parser_instance = IdealistaPageParser()
    flats_json_list = []
    for scrape_location in config["scrape_locations"]:
        prepared_url = config["idealista_url_root"] + scrape_location
        flats_list = get_flats_from_location(prepared_url,
                                            flat_scaper_instance,
                                            flat_parser_instance)
        flats_json_list = flats_json_list + flats_list
    
    
    return {
        "statusCode": 200,
        "body": json.dumps(
            {"message": "Success", "data": json.dumps(flats_json_list)}
        ),
    }

def get_flats_from_location(prepared_url, flat_scaper_instance, flat_parser_instance):
    flat_json_list = []
    first_url = prepared_url
    response = flat_scaper_instance.get_request_with_custom_headers(first_url)
    latest_url = ""
    i = 0
    while (first_url != latest_url or i==1):
        i += 1
        print (f"In page {i}")
        next_page = first_url + f"pagina-{i}.htm"
        response = flat_scaper_instance.get_request_with_custom_headers(next_page)
        latest_url = response.url
        if latest_url==first_url and i==2:
            break
        parsed_response = flat_scaper_instance.parse_request_response(response.text)
        flat_list_for_page = flat_parser_instance.get_flats_from_parsed_response(parsed_response)
        for flat in flat_list_for_page:
            parsed_url = urlparse(prepared_url)
            flat.location = parsed_url.path.split("/")[2:-1]
            flat_json_list.append(flat.to_json())
    
    return flat_json_list
    
