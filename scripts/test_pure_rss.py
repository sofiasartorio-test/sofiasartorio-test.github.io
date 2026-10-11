
import requests
import xml.etree.ElementTree as ET

URL = (
    "https://research.tudelft.nl/en/persons/"
    "kristel-aalbers/publications/?format=rss"
)

try:
    response = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20,
    )

    print("HTTP status:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))

    response.raise_for_status()

    root = ET.fromstring(response.content)
    items = root.findall(".//item")

    print("Pubblicazioni trovate nel feed:", len(items))

    for item in items[:3]:
        title = item.findtext("title", default="Senza titolo")
        link = item.findtext("link", default="Nessun link")
        print("\nTitolo:", title)
        print("Link:", link)

    if not items:
        print("Il feed non contiene elementi RSS <item>.")

except requests.RequestException as error:
    print("Errore HTTP:", error)
except ET.ParseError as error:
    print("La risposta non è XML valido:", error)
