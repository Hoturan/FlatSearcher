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

from lambda_layers.python.flat_scraper import FlatScraper

print("Loading function")


def get_lambda_configs():
    with open("function_config.toml", mode="rb") as fb:
        config = tomli.load(fb)
    return config


def lambda_handler(event, context):
    count = event["count"]
    data = []
    config = get_lambda_configs()

    scrape_locations = config["scrape_locations"]

    return {
        "statusCode": 200,
        "body": json.dumps(
            {"message": "Success", "data": json.dumps(scrape_locations)}
        ),
    }
