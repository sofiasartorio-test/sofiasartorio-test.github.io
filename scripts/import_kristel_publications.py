
import re
import html
import requests
import xml.etree.ElementTree as ET
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

RSS_URL = (
    "https://research.tudelft.nl/en/persons/"
    "ja-pascoe/publications/?format=rss"
)

OUTPUT_DIR = Path("content/publications")
HEADERS = {"User-Agent": "Mozilla/5.0"}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def clean_text(value):
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def slugify(value):
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "publication"


def get_meta(soup, name):
    tag = soup.find(
        "meta",
        attrs={"name": name},
    )
    return clean_text(tag.get("content", "")) if tag else ""


def yaml_quote(value):
    value = clean_text(value)
    value = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{value}"'


def main():
    response = SESSION.get(RSS_URL, timeout=30)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    items = root.findall(".//item")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    created = 0
    skipped = 0
    errors = 0

    print(f"Pubblicazioni trovate nel feed: {len(items)}")

    for item in items:
        title = clean_text(item.findtext("title"))
        url = clean_text(item.findtext("link"))

        if not title or not url:
            print("Salto una voce senza titolo o link.")
            skipped += 1
            continue

        try:
            page_response = SESSION.get(url, timeout=30)
            page_response.raise_for_status()
            soup = BeautifulSoup(page_response.text, "html.parser")

            meta_title = get_meta(soup, "citation_title")
            title = meta_title or title

            authors = [
                clean_text(tag.get("content", ""))
                for tag in soup.find_all(
                    "meta", attrs={"name": "citation_author"}
                )
                if clean_text(tag.get("content", ""))
            ]

            year = (
                get_meta(soup, "citation_publication_date")
                or clean_text(item.findtext("{http://purl.org/dc/elements/1.1/}date"))
                or clean_text(item.findtext("pubDate"))[:4]
            )
            match = re.search(r"\d{4}", year)
            year = match.group(0) if match else "1900"

            book = get_meta(soup, "citation_inbook_title")
            journal = get_meta(soup, "citation_journal_title")
            publisher = get_meta(soup, "citation_publisher")
            doi = get_meta(soup, "citation_doi")
            abstract = get_meta(soup, "citation_abstract")
            first_page = get_meta(soup, "citation_firstpage")
            last_page = get_meta(soup, "citation_lastpage")

            publication = journal or book or publisher
            if book and publisher:
                publication = f"{book}. {publisher}"
            elif not publication:
                publication = publisher

            page_slug = slugify(title)
            destination = OUTPUT_DIR / page_slug

            # Non sovrascrivere mai una pubblicazione già esistente.
            if destination.exists():
                print(f"ESISTE GIÀ, salto: {title}")
                skipped += 1
                continue

            date = f"{year}-01-01T00:00:00Z"
            year = date[:4]
            authors_yaml = "\n".join(
                f"  - {yaml_quote(author)}" for author in authors
            ) or f"  - {yaml_quote('John-Alan Pascoe')}"

            abstract_yaml = (
                f"abstract: {yaml_quote(abstract)}\n"
                if abstract else ""
            )
            doi_yaml = f"doi: {yaml_quote(doi)}\n" if doi else ""

            details = []
            if first_page and last_page:
                details.append(f"Pages {first_page}–{last_page}")
            elif first_page:
                details.append(f"Page {first_page}")
            if publisher and publisher not in publication:
                details.append(f"Publisher: {publisher}")

            body = (
                f"\n\n[View publication on TU Delft PURE]({url})\n"
            )
            if details:
                body += "\n" + " · ".join(details) + "\n"

            front_matter = (
                "---\n"
                f"title: {yaml_quote(title)}\n"
                f"date: '{date}'\n"
                f"year: {year}\n"
                "authors:\n"
                f"{authors_yaml}\n"
                "publication_types: ['manuscript']\n"
                f"publication: {yaml_quote(publication)}\n"
                f"{doi_yaml}"
                f"{abstract_yaml}"
                f"url_source: {yaml_quote(url)}\n"
                "draft: false\n"
                "---\n"
            )

            destination.mkdir(parents=True)
            (destination / "index.md").write_text(
                front_matter + body,
                encoding="utf-8",
            )

            print(f"CREATA: {title}")
            created += 1

        except Exception as error:
            print(f"ERRORE per {title}: {error}")
            errors += 1

    print("\n--- RIEPILOGO ---")
    print(f"Create: {created}")
    print(f"Saltate: {skipped}")
    print(f"Errori: {errors}")
    print("Controlla le nuove cartelle in content/publications/")


if __name__ == "__main__":
    main()
