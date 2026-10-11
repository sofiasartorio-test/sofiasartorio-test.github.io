
import requests

URL = (
    "https://research.tudelft.nl/en/publications/"
    "bodem-water-en-groen/"
)

EXPORT_URL = URL.rstrip("/") + "/export.bib"

for test_url in (URL, EXPORT_URL):
    print("\nTest:", test_url)

    try:
        response = requests.get(
            test_url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=20,
        )

        print("HTTP status:", response.status_code)
        print("Content-Type:", response.headers.get("Content-Type"))
        print("Inizio risposta:", repr(response.text[:250]))

        if response.status_code == 200 and response.text.lstrip().startswith("@"):
            print("BIBTEX TROVATO!")
        elif response.status_code == 200:
            print("Risposta ricevuta, ma non sembra BibTeX diretto.")

    except requests.RequestException as error:
        print("Errore:", error)
