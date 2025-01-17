#!/usr/bin/env python3
#
# Copyright 2020 IBM
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.IBM Confidential
#

import os
import requests
import logging

API_VER = "2020-10-20"
logger = logging.getLogger(__name__)


def get_wml_api_date_version():
    return API_VER


def get_wml_credentials():
    logger.debug('get_wml_credentials()')
    wml_api_key = os.getenv('WML_API_KEY') or ''

    url = os.getenv('WML_AUTH_URL') or "https://iam.cloud.ibm.com/identity/token"

    payload = 'grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey=' + wml_api_key
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    logger.debug(f'auth url: {url}, key is empty: {wml_api_key == ""}')
    response = requests.request("POST", url, headers=headers, data=payload)
    response.raise_for_status()

    wml_token = response.json()['access_token']
    wml_url = os.getenv('WML_URL') or ''
    if wml_url.endswith('/v4'):
        wml_url = wml_url[:-3]
        
    wml_space_id = os.getenv('WML_SPACE_ID') or ''

    wml_credentials = {
        "token": wml_token,
        "space_id": wml_space_id,
        "url": wml_url
    }
    return wml_credentials
