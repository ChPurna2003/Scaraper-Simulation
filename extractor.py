# extractor.py (simulation-aware)

import logging
from typing import Dict, Any
from apollo_client import get_api_key  # used only for non-simulate mode

# Load mock responses when simulate=True
try:
    from mock_responses import MOCK_RESPONSES
except ImportError:
    MOCK_RESPONSES = {}

logger = logging.getLogger(__name__)

CONFIDENCE_THRESHOLD = 0.75
MOBILE_CREDIT_COST = 1


class MobileCreditManager:
    def __init__(self, initial_credits: int = 1000, simulate: bool = False):
        self.simulate = simulate
        self.initial_credits = initial_credits
        self.remaining = initial_credits
        self.consumed = 0

    def use(self, amount: int = 1) -> bool:
        # SIMULATION MODE SHOULD ALSO DECREASE CREDITS
        if self.remaining >= amount:
            self.remaining -= amount
            self.consumed += amount
            return True

        return False


    def summary(self):
        return {
            "initial": self.initial_credits,
            "remaining": self.remaining,
            "consumed": self.consumed,
        }


def build_result_from_enrich(data: Dict[str, Any]) -> Dict[str, Any]:
    out = {
        "first_name": None,
        "last_name": None,
        "job_title": None,
        "company_name": None,
        "company_website": None,
        "company_industry": None,
        "verified_email": None,
        "verified_mobile": None,
        "linkedin_url": None,
        "confidence": 0.0,
        "mobile_checked": False,
    }

    if not data:
        return out

    person = data.get("person") or data

    out["first_name"] = person.get("first_name")
    out["last_name"] = person.get("last_name")
    out["job_title"] = person.get("title")

    comp = person.get("company") or {}
    out["company_name"] = comp.get("name")
    out["company_website"] = comp.get("website")
    out["company_industry"] = comp.get("industry")

    contact = person.get("contact_info") or {}
    out["verified_email"] = contact.get("email")
    out["verified_mobile"] = contact.get("mobile")

    out["linkedin_url"] = person.get("linkedin_url")
    out["confidence"] = person.get("confidence", 0.0)

    return out


def process_record(record: Dict[str, Any], api_key: str, credit_manager: MobileCreditManager, simulate: bool = False) -> Dict[str, Any]:
    linkedin_url = (record.get("linkedin_url") or "").strip()
    full_name = record.get("full_name")
    company_domain = record.get("company_domain")

    # SIMULATION MODE → Use mock data instead of Apollo API
    if simulate:
        mock_response = MOCK_RESPONSES.get(linkedin_url)
        if mock_response:
            enriched = build_result_from_enrich(mock_response)

            # simulate mobile credit usage
            if enriched.get("verified_mobile"):
                if credit_manager.use(MOBILE_CREDIT_COST):
                    enriched["mobile_checked"] = True

            # include input fields for traceability
            enriched["input_linkedin_url"] = linkedin_url
            enriched["input_full_name"] = full_name
            enriched["input_company_domain"] = company_domain
            return enriched

        # If no mock exists, return empty result
        empty = build_result_from_enrich(None)
        empty["input_linkedin_url"] = linkedin_url
        empty["input_full_name"] = full_name
        empty["input_company_domain"] = company_domain
        return empty

    # Non-simulate mode (real API) – left empty because free accounts cannot use API
    enriched = build_result_from_enrich(None)
    enriched["input_linkedin_url"] = linkedin_url
    enriched["input_full_name"] = full_name
    enriched["input_company_domain"] = company_domain
    return enriched
