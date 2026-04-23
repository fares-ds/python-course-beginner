# Weather Fetcher — your GRADUATION project.
#
# Ask the user for a city, then go fetch the current weather from the
# internet and print it. Two new superpowers in one program:
#   1. Use `pip` to install a package (`requests`) that isn't built into Python.
#   2. Make an HTTP request to a real web API (Open-Meteo — no API key needed).
#
# You'll also use every data skill from the earlier projects: reading a
# dictionary (Project 7), handling errors (Project 2, Project 8), and chaining
# small functions together (Project 3). This is where it all clicks.
#
# Before running: make sure you've installed requests first.
#   python3 -m pip install requests

import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# Open-Meteo returns a numeric "WMO weather code". This dict turns it into
# human-readable text. (If a rare code shows up that we don't have, the
# .get() call below falls back to a generic message.)
WEATHER_DESCRIPTIONS = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog",
    48: "freezing fog",
    51: "light drizzle",
    53: "drizzle",
    55: "heavy drizzle",
    61: "light rain",
    63: "rain",
    65: "heavy rain",
    71: "light snow",
    73: "snow",
    75: "heavy snow",
    80: "light rain showers",
    81: "rain showers",
    82: "violent rain showers",
    95: "thunderstorm",
    96: "thunderstorm with light hail",
    99: "thunderstorm with heavy hail",
}


def describe_weather(code):
    # Same .get() pattern from Project 7: return the value if the key exists,
    # otherwise return the default.
    return WEATHER_DESCRIPTIONS.get(code, f"unknown weather (code {code})")


def look_up_city(name):
    # Ask the geocoding API for this city's coordinates.
    # `params=` lets `requests` build the URL for us with proper escaping.
    params = {"name": name, "count": 1}
    response = requests.get(GEOCODING_URL, params=params, timeout=10)
    # raise_for_status() turns HTTP errors (404, 500, etc.) into an exception.
    response.raise_for_status()
    # .json() parses the response body from JSON text into a Python dict.
    data = response.json()
    results = data.get("results")
    if not results:
        return None
    # results is a list; we asked for just 1, so take the first.
    return results[0]


def fetch_current_weather(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,weather_code",
    }
    response = requests.get(WEATHER_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data["current"]


# ---------- main ----------

print("Weather Fetcher")
print("===============")

city_name = input("Which city? ").strip()
if city_name == "":
    print("You didn't type a city.")
    exit()

# --- Step 1: find the city's coordinates. ---
try:
    city = look_up_city(city_name)
except requests.RequestException as e:
    print(f"Couldn't reach the geocoding service: {e}")
    exit()

if city is None:
    print(f"I couldn't find a place called '{city_name}'.")
    exit()

country = city.get("country", "(unknown country)")
print(f"Found: {city['name']}, {country}.")

# --- Step 2: fetch the current weather at those coordinates. ---
try:
    current = fetch_current_weather(city["latitude"], city["longitude"])
except requests.RequestException as e:
    print(f"Couldn't reach the weather service: {e}")
    exit()

temperature = current["temperature_2m"]
code = current["weather_code"]
summary = describe_weather(code)

print(f"Temperature: {temperature}°C")
print(f"Conditions:  {summary}")
