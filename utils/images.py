import requests

API_KEY = "z8irXkOdbcLCVBVcF1HciC9muOQlCD7SZsXtW7CsAAJgvMXrbtQ0YCj6"
headers = {
    "Authorization": API_KEY
}

def get_car_image(brand, color, year):

    query = f"{color} {brand} {year} car"

    url = "https://api.pexels.com/v1/search"

    params = {
        "query": query,
        "per_page": 1
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    if response.status_code == 200:

        data = response.json()

        if len(data["photos"]) > 0:

            return data["photos"][0]["src"]["large"]

    return None