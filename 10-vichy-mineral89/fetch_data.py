"""
fetch_data.py — Vichy Minéral 89 study data from NCBI E-utilities

Downloads metadata and abstracts for the 5 published studies on Vichy M89.
Saves structured data to data/studies.json for use in analysis.py / notebook.

API: NCBI E-utilities (free, no API key required, max 3 req/sec without key).
Docs: https://www.ncbi.nlm.nih.gov/books/NBK25499/

Usage:
    pip install -r requirements.txt
    python fetch_data.py
"""

import json
import time
import re
import os
import urllib.request
import urllib.parse

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

# Known published studies on Vichy Minéral 89
# db: "pubmed" for PMID, "pmc" for PMC articles
STUDIES = [
    {
        "id": "33786979",
        "db": "pubmed",
        "label": "Canada post-procedure (n=47, 4 weeks)",
        "link": "https://pubmed.ncbi.nlm.nih.gov/33786979/",
    },
    {
        "id": "33538111",
        "db": "pubmed",
        "label": "Post-laser (n=51, 28 days)",
        "link": "https://pubmed.ncbi.nlm.nih.gov/33538111/",
    },
    {
        "id": "7547125",
        "db": "pmc",
        "label": "Rosacea split-face (n=20, 30 days) — Corneometer + Tewameter + Chromameter",
        "link": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7547125/",
    },
    {
        "id": "9843703",
        "db": "pmc",
        "label": "Rosacea + mask RCT (NCT05562661)",
        "link": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9843703/",
    },
    {
        "id": "9928536",
        "db": "pmc",
        "label": "Anti-aging + tretinoin (n=38, 84 days) — ELISA + instrumental",
        "link": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9928536/",
    },
]

# Numbers extracted manually from full text (ground truth for analysis)
# Used when E-utilities abstract doesn't contain all values.
KNOWN_MEASUREMENTS = {
    "33786979": {
        "hydration_pct_change": None,
        "tewl_pct_change": None,
        "erythema_pct_change": -27.6,
        "n": 47,
        "population": "Post-procedure / dry skin dermatoses",
        "design": "Open-label, 4 weeks",
        "instruments": "Clinical grading + subjective symptoms",
        "funded_by": "Vichy/L'Oréal",
        "p_lt_001": True,
    },
    "33538111": {
        "hydration_pct_change": 30.0,
        "tewl_pct_change": -10.0,
        "erythema_pct_change": -25.0,
        "n": 51,
        "population": "Post-laser skin",
        "design": "28 days, baseline comparison",
        "instruments": "Corneometer + Tewameter + Chromameter",
        "funded_by": "Vichy/L'Oréal",
        "p_lt_001": True,
    },
    "PMC7547125": {
        "hydration_pct_change": 33.0,
        "tewl_pct_change": -11.0,
        "erythema_pct_change": -28.0,
        "n": 20,
        "population": "Rosacea",
        "design": "Split-face intra-individual, 30 days",
        "instruments": "Corneometer CM825 + Tewameter TM300 + Chromameter CR400",
        "funded_by": "Vichy/L'Oréal",
        "p_lt_001": True,
    },
    "PMC9843703": {
        "hydration_pct_change": 28.0,
        "tewl_pct_change": -9.0,
        "erythema_pct_change": -22.0,
        "n": None,
        "population": "Rosacea (mask wear context)",
        "design": "RCT, NCT05562661, days 15 and 30",
        "instruments": "Instrumental + subjective",
        "funded_by": "Vichy/L'Oréal",
        "p_lt_001": True,
    },
    "PMC9928536": {
        "hydration_pct_change": 11.46,
        "tewl_pct_change": None,
        "erythema_pct_change": -48.1,
        "n": 38,
        "population": "Aging skin + tretinoin use",
        "design": "Split-face, 28 and 84 days",
        "instruments": "ELISA (IL-8, IL-1α, PGE2, SOD) + Corneometer",
        "funded_by": "Vichy/L'Oréal",
        "p_lt_001": True,
    },
}

# Marketing claims from Vichy USA official website
MARKETING_CLAIMS = [
    {
        "claim": "Visiblemente mejora el 100% de los signos de hidratación",
        "method": "Autoevaluación",
        "n_approx": "42-53",
        "population": "No especificada",
        "source": "https://www.vichyusa.com/skin-care/mineral-89-hyaluronic-acid-serum-mineral89.html",
    },
    {
        "claim": "Piel más hidratada desde la primera hora",
        "method": "No declarado",
        "n_approx": "No declarado",
        "population": "No especificada",
        "source": "https://www.vichyusa.com",
    },
    {
        "claim": "72 horas de hidratación duradera",
        "method": "No declarado",
        "n_approx": "No declarado",
        "population": "No especificada",
        "source": "https://www.vichyusa.com",
    },
]


def fetch_esummary(study_id: str, db: str) -> dict:
    """Fetch metadata (title, authors, journal, year) via eSummary."""
    url = f"{BASE_URL}esummary.fcgi?db={db}&id={study_id}&retmode=json"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            result = data.get("result", {})
            uids = result.get("uids", [study_id])
            return result.get(uids[0] if uids else study_id, {})
    except Exception as e:
        print(f"  Warning: could not fetch eSummary for {study_id}: {e}")
        return {}


def fetch_abstract(study_id: str, db: str) -> str:
    """Fetch plain-text abstract via eFetch."""
    url = f"{BASE_URL}efetch.fcgi?db={db}&id={study_id}&rettype=abstract&retmode=text"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return response.read().decode("utf-8").strip()
    except Exception as e:
        print(f"  Warning: could not fetch abstract for {study_id}: {e}")
        return ""


def extract_numbers_from_abstract(text: str) -> dict:
    """Extract key numerical values from abstract text using regex."""
    extracted = {}

    patterns = {
        "hydration_pct": r"(\d+\.?\d*)\s*%[^\n]*hydrat",
        "tewl_pct": r"TEWL[^\n]*(\d+\.?\d*)\s*%|(\d+\.?\d*)\s*%[^\n]*TEWL",
        "erythema_pct": r"(\d+\.?\d*)\s*%[^\n]*erythem",
        "n_subjects": r"(?:n\s*=\s*|enrolled\s+|included\s+)(\d+)",
        "p_value": r"[pP]\s*[<=>]\s*0\.(\d+)",
        "duration_days": r"(\d+)\s*(?:days?|day)",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            val = match.group(1)
            if val is None:
                continue
            try:
                extracted[key] = float(val) if "." in val else int(val)
            except ValueError:
                extracted[key] = val

    return extracted


def main():
    os.makedirs("data", exist_ok=True)

    output = {
        "pubmed_studies": [],
        "marketing_claims": MARKETING_CLAIMS,
        "known_measurements": KNOWN_MEASUREMENTS,
    }

    print("Fetching study data from NCBI E-utilities...\n")

    for study in STUDIES:
        study_id = study["id"]
        db = study["db"]
        label = study["label"]
        pmc_key = f"PMC{study_id}" if db == "pmc" else study_id

        print(f"  [{db.upper()} {study_id}] {label}")

        summary = fetch_esummary(study_id, db)
        time.sleep(0.4)  # stay under 3 req/sec

        abstract = fetch_abstract(study_id, db)
        time.sleep(0.4)

        extracted = extract_numbers_from_abstract(abstract)

        record = {
            "id": study_id,
            "db": db,
            "label": label,
            "link": study["link"],
            "title": summary.get("title", ""),
            "authors": summary.get("authors", []),
            "journal": summary.get("source", ""),
            "year": summary.get("pubdate", "")[:4] if summary.get("pubdate") else "",
            "abstract": abstract[:800] + "..." if len(abstract) > 800 else abstract,
            "extracted_from_abstract": extracted,
            "known_measurements": KNOWN_MEASUREMENTS.get(pmc_key, KNOWN_MEASUREMENTS.get(study_id, {})),
        }

        output["pubmed_studies"].append(record)
        print(f"     title: {record['title'][:60]}..." if record["title"] else "     title: (not retrieved)")
        print(f"     extracted: {extracted}")

    with open("data/studies.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSaved {len(output['pubmed_studies'])} studies to data/studies.json")
    print(f"Marketing claims included: {len(MARKETING_CLAIMS)}")


if __name__ == "__main__":
    main()
