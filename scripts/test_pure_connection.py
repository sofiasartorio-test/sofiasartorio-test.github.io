
import requests

URL = "https://research.tudelft.nl/en/persons/kristel-aalbers/publications/"

try:
    response = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20,
    )

    print("URL:", URL)
    print("HTTP status:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))
    print("Dimensione risposta:", len(response.text), "caratteri")

    if response.status_code == 200:
        print("OK: il portale ha risposto.")
    else:
        print("ATTENZIONE: risposta HTTP inattesa.")

except requests.RequestException as error:
    print("ERRORE DI CONNESSIONE:", error)
