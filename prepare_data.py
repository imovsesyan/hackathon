"""
Turn the raw ARLIS dump into the small laws.json the app reads.

Input : data/arlis_docs.jsonl.xz   (download from https://data.opendata.am/dataset/arlis-db)
Output: data/laws.json

What it does:
  1. Streams the .xz dump (it's large, so we never load it all into memory).
  2. Keeps only a hand-picked list of high-impact, in-force Armenian laws.
  3. Cleans the HTML out of each body.
  4. Splits every law's body into individual «Հոդված N» articles.
  5. Writes a compact laws.json:  [{law_id, law_title, source, pdf_link, articles:[...]}]

Run it once:
    python prepare_data.py
"""
from pathlib import Path
import lzma
import json
import html
import re

SRC = Path("data/arlis_docs.jsonl.xz")
OUT = Path("data/laws.json")

# --- 1. Which laws we care about -------------------------------------------
# We match on lowercase substrings found in the document `title`.
# Add / remove entries to curate the demo. Order here = order in the app.
TARGET_LAWS = [
    ("labor_code",     ["աշխատանքային օրենսգիրք"]),
    ("civil_code",     ["քաղաքացիական օրենսգիրք"]),
    ("consumer",       ["սպառողների իրավունքների պաշտպանության"]),
    ("family_code",    ["ընտանեկան օրենսգիրք"]),
    ("housing",        ["բնակարանային օրենսգիրք"]),
]

MAX_ARTICLES_PER_LAW = 60   # keep the demo snappy
MIN_ARTICLE_CHARS = 60      # skip near-empty stubs

TAG_RE = re.compile(r"<[^>]+>")
# «Հոդված 12.5», «Հոդված 139», «Հ ո դ վ ա ծ 5» etc. Capture the number label.
ARTICLE_RE = re.compile(r"(Հ\s*ո\s*դ\s*վ\s*ա\s*ծ\s+\d+[.\-‐-―]?\d*)", re.UNICODE)


def clean_body(text: str) -> str:
    text = html.unescape(text)
    text = TAG_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def split_into_articles(body: str) -> list[dict]:
    """Split a full law body into [{article_no, text}] using «Հոդված N» markers."""
    parts = ARTICLE_RE.split(body)
    # re.split with a capture group gives: [pre, marker1, chunk1, marker2, chunk2, ...]
    articles = []
    for i in range(1, len(parts) - 1, 2):
        marker = re.sub(r"\s+", " ", parts[i]).strip()
        chunk = parts[i + 1].strip()
        if len(chunk) < MIN_ARTICLE_CHARS:
            continue
        # First sentence-ish becomes a short heading for the sidebar.
        heading = chunk.split(".")[0][:70].strip()
        articles.append({
            "article_no": marker,
            "heading": heading,
            "text": f"{marker}. {chunk}",
        })
        if len(articles) >= MAX_ARTICLES_PER_LAW:
            break
    return articles


def pick_law_id(title: str) -> str | None:
    t = title.lower()
    for law_id, keywords in TARGET_LAWS:
        if any(k in t for k in keywords):
            return law_id
    return None


def main():
    if not SRC.exists():
        raise SystemExit(
            f"Չգտա {SRC}: Ներբեռնիր ARLIS dump-ը և դիր data/ պանակում:\n"
            "  https://data.opendata.am/dataset/arlis-db"
        )

    # We keep the LONGEST matching body per law (usually the consolidated version).
    best: dict[str, dict] = {}

    with lzma.open(SRC, "rt", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)

            if obj.get("language") != "AM":
                continue
            if obj.get("ActStatus") not in (None, "Գործում է"):
                continue

            title = obj.get("title") or ""
            law_id = pick_law_id(title)
            if not law_id:
                continue

            body = obj.get("body") or obj.get("Body") or ""
            if not isinstance(body, str) or not body:
                continue
            body = clean_body(body)

            prev = best.get(law_id)
            if prev is None or len(body) > prev["_len"]:
                best[law_id] = {
                    "law_id": law_id,
                    "law_title": title,
                    "source": obj.get("Source"),
                    "pdf_link": obj.get("pdf_link"),
                    "_len": len(body),
                    "_body": body,
                }

    laws = []
    # Preserve TARGET_LAWS order
    for law_id, _ in TARGET_LAWS:
        rec = best.get(law_id)
        if not rec:
            print(f"⚠️  չգտնվեց՝ {law_id}")
            continue
        articles = split_into_articles(rec["_body"])
        if not articles:
            print(f"⚠️  0 հոդված՝ {law_id}")
            continue
        laws.append({
            "law_id": rec["law_id"],
            "law_title": rec["law_title"],
            "source": rec["source"],
            "pdf_link": rec["pdf_link"],
            "articles": articles,
        })
        print(f"✅ {law_id}: {len(articles)} հոդված")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(laws, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nԳրված է {OUT}  ({len(laws)} օրենք)")


if __name__ == "__main__":
    main()
