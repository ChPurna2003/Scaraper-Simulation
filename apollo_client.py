import os
import time
import logging
import requests
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

APOLLO_API_BASE = "https://api.apollo.io/v1"
ENRICH_ENDPOINT = f"{APOLLO_API_BASE}/enrich"
SEARCH_ENDPOINT = f"{APOLLO_API_BASE}/people/search"
ACCOUNT_ENDPOINT = f"{APOLLO_API_BASE}/account"


def get_api_key() -> str:
    api_key = os.getenv("APOLLO_API_KEY")
    if not api_key:
        raise ValueError("ERROR: APOLLO_API_KEY not found. Please export it before running.")
    return api_key


def safe_request(method: str, url: str, headers=None, params=None, json_body=None, simulate=False):
    if simulate:
        logger.debug(f"[SIMULATION] {method} {url}")
        return {"status_code": 200, "data": None}

    backoff = 1
    for attempt in range(4):
        try:
            resp = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_body,
                timeout=20
            )
            if resp.status_code in (429, 503):
                time.sleep(backoff)
                backoff *= 2
                continue

            resp.raise_for_status()
            return {"status_code": resp.status_code, "data": resp.json()}

        except Exception as e:
            time.sleep(backoff)
            backoff *= 2

    return {"status_code": None, "data": None}


def enrich_by_linkedin(linkedin_url: str, api_key: str, simulate=False):
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"linkedin_url": linkedin_url}
    return safe_request("POST", ENRICH_ENDPOINT, headers=headers, json_body=payload, simulate=simulate)


def search_person(name: str, domain: str, api_key: str, simulate=False):
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"q": name, "company_domain": domain}
    return safe_request("GET", SEARCH_ENDPOINT, headers=headers, params=params, simulate=simulate)


def get_account_credits(api_key: str, simulate=False):
    headers = {"Authorization": f"Bearer {api_key}"}
    return safe_request("GET", ACCOUNT_ENDPOINT, headers=headers, simulate=simulate)
