
import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("POSITIONSTACK_API_KEY")


def get_address():
    latitude = 6.4410
    longitude = 3.5357

    params = {
        "access_key": API_KEY,
        "query": f"{latitude},{longitude}",
        "limit": 10,
        "country": "NG"
    }

    try:
        response = requests.get(
            "https://api.apilayer.net/positionstack/v1/reverse",
            params=params,
            timeout=45
        )

        print("Status code:", response.status_code)

        data = response.json()
        print("API response:", data)

        if response.status_code != 200:
            return None

        results = data.get("data", [])

        if not results:
            print("No address results found.")
            return None

        return results[0].get("label")

    except requests.RequestException as error:
        print("Request failed:", type(error).__name__)
        return None

    except ValueError:
        print("Invalid JSON response.")
        return None


if __name__ == "__main__":
    print("API key loaded:", bool(API_KEY))

    address = get_address()

    if address:
        print("\nFull address:", address)
