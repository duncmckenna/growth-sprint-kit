import csv
import json
import os
import re
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parent.parent
# PROSPECTOR_HOME lets tests (or a second run) use a separate working folder.
HOME = Path(os.environ.get("PROSPECTOR_HOME", ROOT))
DATA = HOME / "data"
OUT = HOME / "out"

# Domains that show up in ad captions but are never the advertiser's own store.
NOISE_DOMAINS = {
    "facebook.com", "fb.me", "instagram.com", "google.com", "youtube.com", "amazon.co.uk",
    "amazon.com", "ebay.co.uk", "etsy.com", "linktr.ee", "bit.ly", "wa.me", "apple.com",
    "play.google.com", "tiktok.com", "shopify.com", "myshopify.com", "wayfair.co.uk",
    "whatsapp.com", "calendly.com", "linkin.bio", "typeform.com", "gov.uk", "gofundme.com",
    "eventbrite.co.uk", "eventbrite.com", "trustpilot.com", "messenger.com", "threads.net", "fb.com", "m.me",
    "temu.com", "alibaba.com", "aliexpress.com", "yahoo.com", "tinyurl.com", "shein.com", "joybuy.co.uk", "lookfantastic.com",
}

# Advertisers that aren't D2C retailers but whose ad text matches furniture keywords:
# serial-fiction / short-drama apps, lead-gen "advisor" sites. Dropped at seed time.
NONRETAIL_PATTERNS = [r"novel", r"reel", r"netshort|readshort|bestreels|drama", r"playlet", r"(^|[.-])books?\b",
                      r"bookcraze|mobobooks|mylibapps", r"stor(y|ys|ies)\b", r"manga|comic", r"advisorssearch"]

# Two-level public suffixes we need to keep intact when stripping subdomains.
_TWO_LEVEL = {"co.uk", "org.uk", "ac.uk", "gov.uk", "ltd.uk", "plc.uk", "me.uk", "net.uk",
              "com.au", "net.au", "org.au", "co.nz", "co.za", "com.br", "co.in", "co.jp", "com.sg"}


def registrable(domain):
    """'uk.koala.com' -> 'koala.com'; 'read.brand.co.uk' -> 'brand.co.uk'."""
    parts = domain.split(".")
    n = 3 if ".".join(parts[-2:]) in _TWO_LEVEL else 2
    return ".".join(parts[-n:]) if len(parts) >= n else domain


def is_nonretail(domain):
    return bool(domain) and any(re.search(p, domain) for p in NONRETAIL_PATTERNS)


# Throwaway / dropship-looking domains: hyphenated fake-TLD names and cheap gTLDs.
JUNK_PATTERNS = [r"-(com|co|uk|shop|store)\.", r"\.(store|shop|online|site|top|xyz|click|buzz|live)$"]


def is_junk_domain(domain):
    return bool(domain) and any(re.search(p, domain) for p in JUNK_PATTERNS)


def load_config(path=None):
    with open(path or ROOT / "config.yaml") as f:
        return yaml.safe_load(f)


_DOMAIN_RE = re.compile(r"(?i)\b((?:[a-z0-9-]+\.)+[a-z]{2,})\b")


def normalise_domain(value):
    """Turn a URL, caption ('WWW.BRAND.CO.UK') or bare domain into 'brand.co.uk'. None if junk."""
    if not value:
        return None
    v = str(value).strip().lower()
    if "://" in v:
        v = urlparse(v).netloc or v
    m = _DOMAIN_RE.search(v)
    if not m:
        return None
    d = registrable(m.group(1).strip("."))
    if d in NOISE_DOMAINS or is_nonretail(d):
        return None
    return d


def read_json(path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text())


def write_json(path, obj):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False))


def load_accounts():
    """Master account table keyed by domain: data/accounts.json."""
    return read_json(DATA / "accounts.json", default={})


def save_accounts(accounts):
    write_json(DATA / "accounts.json", accounts)


def upsert(accounts, domain, **fields):
    acc = accounts.setdefault(domain, {"domain": domain, "sources": []})
    src = fields.pop("source", None)
    if src and src not in acc["sources"]:
        acc["sources"].append(src)
    for k, v in fields.items():
        if v in (None, "", []):
            continue
        if isinstance(v, list) and isinstance(acc.get(k), list):
            acc[k] = sorted(set(acc[k]) | set(v))
        else:
            acc[k] = v
    return acc


def write_csv(path, rows, columns):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: ("; ".join(map(str, r[c])) if isinstance(r.get(c), list) else r.get(c, "")) for c in columns})
