
import requests
import xml.etree.ElementTree as ET

URL = "https://research.tudelft.nl/en/persons/kristel-aalbers/publications/?format=rss"

response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=20,
)
response.raise_for_status()

root = ET.fromstring(response.content)
items = root.findall(".//item")

print("Numero di pubblicazioni:", len(items))

if items:
    item = items[0]

    print("\n--- DATI DELLA PRIMA PUBBLICAZIONE ---")

    for field in item:
        value = (field.text or "").strip()
        print(f"{field.tag}: {value[:500]}")
else:
    print("Nessuna pubblicazione trovata.")
