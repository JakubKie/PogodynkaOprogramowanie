import os
import requests
import argparse
from datetime import datetime, UTC, timedelta

# Endpoints
AIR_API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_air_data(lat: float, lon: float, start_iso: str, end_iso: str) -> dict:
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "pm10,pm2_5,carbon_monoxide",
        "timezone": "Europe/Warsaw",
        "start": start_iso,
        "end": end_iso
    }
    r = requests.get(AIR_API_URL, params=params)
    r.raise_for_status()
    return r.json()

def fetch_weather_data(lat: float, lon: float, start_iso: str, end_iso: str) -> dict:
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,pressure_msl",
        "timezone": "Europe/Warsaw",
        "start": start_iso,
        "end": end_iso
    }
    r = requests.get(WEATHER_API_URL, params=params)
    r.raise_for_status()
    return r.json()

def send_to_backend(combined_times: list, air: dict, weather: dict):
    url = "http://localhost:8000/readings"
    for t in combined_times:
        # znajdź indeksy w obu zestawach
        i_air   = air["hourly"]["time"].index(t)
        i_w     = weather["hourly"]["time"].index(t)

        payload = {
            "timestamp": t,
            "temperature":      weather["hourly"]["temperature_2m"][i_w],
            "pressure":         weather["hourly"]["pressure_msl"][i_w],
            "pm10":             air["hourly"]["pm10"][i_air],
            "pm2_5":            air["hourly"]["pm2_5"][i_air],
            "carbon_monoxide":  air["hourly"]["carbon_monoxide"][i_air],
        }
        # tylko jeśli wszystkie wartości są liczbami
        if None in payload.values():
            continue

        resp = requests.post(url, json=payload)
        print(resp.status_code, resp.json())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, default=float(os.getenv("LAT", 52.2297)))
    parser.add_argument("--lon", type=float, default=float(os.getenv("LON", 21.0122)))
    args = parser.parse_args()

    # zaokrąglij do pełnej godziny
    now = datetime.now(UTC).replace(minute=0, second=0, microsecond=0)
    start = (now - timedelta(hours=12)).strftime("%Y-%m-%dT%H:00")
    end   =  now.strftime("%Y-%m-%dT%H:00")

    # fetch
    air_data     = fetch_air_data(args.lat, args.lon, start, end)
    weather_data = fetch_weather_data(args.lat, args.lon, start, end)

    # wspólne czasy
    times_air     = set(air_data["hourly"]["time"])
    times_weather = set(weather_data["hourly"]["time"])
    common_times  = sorted(times_air & times_weather)

    # send
    send_to_backend(common_times, air_data, weather_data)

if __name__ == "__main__":
    main()
