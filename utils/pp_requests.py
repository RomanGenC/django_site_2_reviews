from urllib.parse import urljoin

import requests

from reviews.secret import ENVIROMENT_VARIABLES
from utils.constants import DEFAULT_EXPIRE_VIEWS, DEFAULT_EXPIRE_DAYS


def create_pp_link(
        payload,
        expire_after_days: int = DEFAULT_EXPIRE_DAYS,
        expire_after_views: int = DEFAULT_EXPIRE_VIEWS
):
    url = urljoin(ENVIROMENT_VARIABLES['PP_SOURCE'], 'p.json')
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "password": {
            "payload": payload,
            "expire_after_days": expire_after_days,
            "expire_after_views": expire_after_views
        }
    }
    create_pp_response = requests.post(url, json=data, headers=headers)

    create_pp_response.raise_for_status()

    pp_url = urljoin(ENVIROMENT_VARIABLES['PP_SOURCE'], '/p/')
    return urljoin(pp_url, create_pp_response.json()['url_token'])
