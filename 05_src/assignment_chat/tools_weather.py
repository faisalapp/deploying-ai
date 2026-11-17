from langchain.tools import tool
import requests


@tool
def get_current_weather(city:str) -> str:
    """Get the current weather conditions for a city.
    Use this tool for any question about current weather, temperature,
    rain, or wind in a specific city. Requires a city name.
    Returns temperature (Celsius), humidity, precipitation, and wind speed.
    """
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1}
    )
    results = geo.json().get("results")
    if not results:
        return f"City '{city}' was not found."
    location = results[0]
    latitude = location["latitude"]
    longitude = location["longitude"]

    forecast = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
            "timezone": "auto",
        }
    )
    current = forecast.json()["current"]

    # Step C: return the facts as a compact string — the MODEL (Marlowe)
 # turns these into the final answer, which is how we satisfy the
    # "never verbatim" rule: raw data in, persona out.
    return (
        f"Location: {location['name']}, {location.get('country', '')}. "
        f"Temperature: {current['temperature_2m']} C. "
        f"Humidity: {current['relative_humidity_2m']} %. "
        f"Precipitation: {current['precipitation']} mm. "
        f"Wind: {current['wind_speed_10m']} km/h."
    )