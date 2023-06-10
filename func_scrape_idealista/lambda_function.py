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
import pandas as pd
import json
import tomli
from urllib.parse import urlparse

from lambda_layers.python.idealista_scraper import IdealistaScraper, IdealistaPageParser

print("Loading function")


def get_lambda_configs():
    with open("function_config.toml", mode="rb") as fb:
        config = tomli.load(fb)
    return config


def lambda_handler(event, context):
    config = get_lambda_configs()

    idealista_scrape_locations = config["scrape_locations"]
    idealista_root_url = config["idealista_url_root"]

    flat_scaper_instance = IdealistaScraper()
    flat_parser_instance = IdealistaPageParser()
    flats_json_list = []
    for scrape_location in idealista_scrape_locations:
        prepared_url = idealista_root_url + scrape_location
        flats_list = get_flats_from_location(prepared_url, flat_scaper_instance, flat_parser_instance)
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
    while (first_url != latest_url & i>1):
        i += 1
        print (f"In page {i}")
        next_page = first_url + f"pagina-{i}.htm"
        response = flat_scaper_instance.get_request_with_custom_headers(next_page)
        latest_url = response.url
        parsed_response = flat_scaper_instance.parse_request_response(response.text)
        flat_list_for_page = flat_parser_instance.get_flats_from_parsed_response(parsed_response)
        for flat in flat_list_for_page:
            parsed_url = urlparse(prepared_url)
            flat.location = parsed_url.path.split("/")[2:-1]
            flat_json_list.append(flat.to_json())
    

    
