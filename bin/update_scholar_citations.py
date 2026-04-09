#!/usr/bin/env python

import json
import os
import sys
from datetime import datetime

import yaml
from scholarly import scholarly


CONFIG_FILE = "_data/socials.yml"
OUTPUT_FILE = "_data/citations.yml"
BADGE_OUTPUT_FILE = "assets/json/gs_data_shieldsio.json"


def load_scholar_user_id() -> str:
    if not os.path.exists(CONFIG_FILE):
        print(f"Missing configuration file: {CONFIG_FILE}")
        sys.exit(1)

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    scholar_user_id = config.get("scholar_userid")
    if not scholar_user_id:
        print("No 'scholar_userid' found in _data/socials.yml.")
        sys.exit(1)

    return scholar_user_id


def load_existing_citations():
    if not os.path.exists(OUTPUT_FILE):
        return {}

    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as exc:
        print(f"Warning: failed to read {OUTPUT_FILE}: {exc}")
        return {}


def write_badge_json(total_citations: int):
    badge_data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": str(total_citations),
        "color": "9cf",
        "labelColor": "f6f6f6",
    }
    os.makedirs(os.path.dirname(BADGE_OUTPUT_FILE), exist_ok=True)
    with open(BADGE_OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(badge_data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def get_scholar_citations():
    scholar_user_id = load_scholar_user_id()
    existing_data = load_existing_citations()
    today = datetime.now().strftime("%Y-%m-%d")

    print(f"Fetching Google Scholar profile: {scholar_user_id}")
    scholarly.set_timeout(15)
    scholarly.set_retries(3)

    try:
        author = scholarly.search_author_id(scholar_user_id)
        author_data = scholarly.fill(author)
    except Exception as exc:
        print(f"Error fetching Google Scholar data: {exc}")
        sys.exit(1)

    total_citations = author_data.get("citedby", 0)
    citation_data = {
        "metadata": {
            "last_updated": today,
            "scholar_user_id": scholar_user_id,
            "author_name": author_data.get("name", ""),
            "affiliation": author_data.get("affiliation", ""),
            "total_citations": total_citations,
        },
        "papers": {},
    }

    for pub in author_data.get("publications", []):
        pub_id = pub.get("pub_id") or pub.get("author_pub_id")
        if not pub_id:
            continue

        bib = pub.get("bib", {})
        citation_data["papers"][pub_id] = {
            "title": bib.get("title", "Unknown Title"),
            "year": bib.get("pub_year", "Unknown Year"),
            "citations": pub.get("num_citations", 0),
        }

    if existing_data == citation_data and os.path.exists(BADGE_OUTPUT_FILE):
        print("Citation data is already up to date.")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        yaml.safe_dump(citation_data, f, width=1000, sort_keys=False, allow_unicode=True)

    write_badge_json(total_citations)
    print(f"Saved citations to {OUTPUT_FILE} and badge data to {BADGE_OUTPUT_FILE}")


if __name__ == "__main__":
    get_scholar_citations()
