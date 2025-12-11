import csv
import argparse
import logging

from extractor import process_record, MobileCreditManager
from apollo_client import get_api_key


logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
logger = logging.getLogger(__name__)


# ---------------------------- READ CSV -----------------------------

def read_csv(path: str):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ---------------------------- WRITE CSV -----------------------------

def write_csv(path: str, rows):
    if not rows:
        return

    # Clean professional column order
    ordered_columns = [
        "first_name",
        "last_name",
        "job_title",
        "company_name",
        "company_website",
        "company_industry",
        "verified_email",
        "verified_mobile",
        "linkedin_url",
        "confidence",
        "mobile_checked",
        "credit_initial",
        "credit_remaining",
        "credit_consumed",
        "input_full_name",
        "input_company_domain",
        "input_linkedin_url"
    ]

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=ordered_columns)
        writer.writeheader()
        writer.writerows(rows)


# ---------------------- OPTIONAL TERMINAL TABLES ---------------------

def print_markdown_table(rows):
    if not rows:
        return

    headers = list(rows[0].keys())

    print("\n### Markdown Table Output\n")
    print("| " + " | ".join(headers) + " |")
    print("|" + " | ".join(["---"] * len(headers)) + " |")

    for row in rows:
        print("| " + " | ".join(str(row[h]) for h in headers) + " |")


def print_clean_terminal_table(rows):
    if not rows:
        return

    headers = list(rows[0].keys())

    # Determine width of each column
    widths = {h: max(len(h), *(len(str(r[h])) for r in rows)) for h in headers}

    print("\n### Clean Terminal Table Output\n")
    print(" | ".join(h.ljust(widths[h]) for h in headers))
    print("-+-".join("-" * widths[h] for h in headers))

    for r in rows:
        print(" | ".join(str(r[h]).ljust(widths[h]) for h in headers))


# ------------------------------ MAIN ------------------------------

def main():
    parser = argparse.ArgumentParser(description="Apollo.io Simulation Extractor")
    parser.add_argument("--input", default="input.csv")
    parser.add_argument("--output", default="output.csv")
    parser.add_argument("--simulate", action="store_true")
    args = parser.parse_args()

    try:
        api_key = get_api_key()
    except:
        api_key = "SIMULATED_KEY"

    credit_manager = MobileCreditManager(initial_credits=1000, simulate=args.simulate)

    rows = read_csv(args.input)
    results = []

    for row in rows:
        enriched = process_record(row, api_key, credit_manager, simulate=args.simulate)

        # track credits in CSV
        enriched["credit_initial"] = credit_manager.initial_credits
        enriched["credit_remaining"] = credit_manager.remaining
        enriched["credit_consumed"] = credit_manager.consumed

        results.append(enriched)

    # Save clean CSV output
    write_csv(args.output, results)

    print("\n✔ Extraction Completed Successfully!")
    print("Credits used:", credit_manager.consumed)
    print("Credits remaining:", credit_manager.remaining)

    # Print tables
    print_markdown_table(results)
    print_clean_terminal_table(results)

    print("\nCSV Saved To:", args.output)


if __name__ == "__main__":
    main()
