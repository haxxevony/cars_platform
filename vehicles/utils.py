import requests
import logging

def fetch_external_metadata(vin):
    url = f"https://external-api.example.com/vehicles/{vin}"
    headers = {
        # 'Authorization': 'Bearer YOUR_API_KEY',  # Optional: if external API requires auth
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            logging.warning(f"Metadata fetch failed for VIN {vin}: {response.status_code}")
    except requests.RequestException as e:
        logging.error(f"Metadata fetch error for VIN {vin}: {e}")

    # Fallback structure
    return {
        "engine": None,
        "transmission": None,
        "country_of_origin": None
    }
