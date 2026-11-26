import csv
import sys
from urllib.parse import urlencode
from urllib.request import urlopen


def import_updates(rows, base_url):
    for row in rows:
        record_id = row["id"]
        payload = urlencode({"name": row["name"]}).encode()
        with urlopen(f"{base_url}/records/{record_id}", data=payload) as response:
            print(record_id, response.status)


if __name__ == "__main__":
    with open(sys.argv[1], newline="", encoding="utf-8") as source:
        import_updates(csv.DictReader(source), "http://127.0.0.1:8000")
