
import requests
from bs4 import BeautifulSoup

URL = "https://research.tudelft.nl/en/publications/bodem-water-en-groen/"

response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=20,
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

print("HTTP:", response.status_code)
print("\n--- METADATI BIBLIOGRAFICI ---")

found = 0

for meta in soup.find_all("meta"):
    name = meta.get("name") or meta.get("property") or ""
    if name.lower().startswith(("citation_", "dc.", "dcterms.")):
        content = meta.get("content", "")
        print(f"{name}: {content}")
        found += 1

print("\nTotale metadati trovati:", found)
