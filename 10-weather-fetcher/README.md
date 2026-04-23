# Project 10 — Weather Fetcher

Ask for a city. Go fetch the actual current weather for that city. Print the temperature and a one-line description.

This is your **graduation project**. Everything you know so far — input, output, functions, dictionaries, JSON, error handling — all gets used, in service of a program that **talks to the internet**. After this, you're genuinely not an absolute beginner any more.

## What you'll learn

- **`pip install`** — how to add packages to Python that didn't ship with it.
- **`requests`** — the de-facto library for making HTTP calls. Your first external dependency.
- **HTTP GET** — ask a web server for something, it responds with data.
- **Query parameters** — the `?name=Berlin&count=1` part of a URL, built for you by `requests`.
- **API responses as dictionaries** — the JSON that comes back plugs straight into the `dict` skills from Project 7.
- **`response.raise_for_status()`** — turn a "404" or "500" from the server into a Python exception.
- **`requests.RequestException`** — the catch-all for "couldn't reach the internet / server was rude / something went wrong."
- **Chaining two API calls** — one to find the city, one to get its weather.

## Before you start: install `requests`

Up until now, every project has used only Python that came pre-installed. This one needs an extra package. In your terminal, run:

```
python3 -m pip install requests
```

**What just happened?**

- **`pip`** is Python's package manager — a tool for downloading and installing third-party libraries.
- **`requests`** is the package name. It lives at [pypi.org](https://pypi.org) along with ~500,000 others.
- **`python3 -m pip ...`** asks the Python you're using to run its own `pip`. (That's a tiny bit more robust than just typing `pip install requests`, which can get confused if you have multiple Pythons on your machine.)

If you see `Successfully installed requests-...`, you're ready. If you see an error about permissions, try adding `--user`:

```
python3 -m pip install --user requests
```

You only need to do this once per machine.

## What is an API?

An **API** ("application programming interface") is a way for one program to talk to another. When your browser loads a weather site, the site's server is doing roughly what *you're* about to do — ask an API for today's weather, get back some JSON, format it nicely.

For this project we use **Open-Meteo**. Two reasons it's a great starter API:

- **No API key required.** Most APIs make you sign up and copy a secret token first. Open-Meteo just works — visit their URL, get data. One fewer side-quest.
- **Returns plain JSON.** Exactly the dict-of-dicts-and-lists shape you saw in Project 8.

## How the program works

Open-Meteo's weather endpoint takes a latitude and longitude, not a city name. So the program makes **two** calls:

```
ask for a city name

call #1 -> geocoding API: "what are the coordinates of <city>?"
        -> returns { results: [ { name, country, latitude, longitude } ] }

call #2 -> weather API: "what's the current weather at (lat, lon)?"
        -> returns { current: { temperature_2m, weather_code } }

translate weather_code into plain English (using a dict lookup)
print everything
```

Each call can fail — the internet could be down, the city could be misspelled, the server could be grumpy. The program handles each one without crashing.

## Key ideas, explained

### `requests.get(url, params=..., timeout=...)`

```python
import requests

response = requests.get(
    "https://geocoding-api.open-meteo.com/v1/search",
    params={"name": "Berlin", "count": 1},
    timeout=10,
)
```

- **`url`** — the endpoint.
- **`params={}`** — a dict of query parameters. `requests` takes care of turning them into the `?name=Berlin&count=1` part of the URL, including any ugly escaping (spaces, special characters).
- **`timeout=10`** — if the server hasn't responded in 10 seconds, give up and raise an error. Without a timeout, a hung server could make your program hang forever.

The return value is a `Response` object.

### `.raise_for_status()` and `.json()`

```python
response.raise_for_status()      # raise an error on HTTP 4xx/5xx
data = response.json()           # parse the body from JSON to a Python value
```

- **`raise_for_status()`** — if the server returned a "bad" status code (400 Not Found, 500 Internal Server Error, etc.), raise an exception. Otherwise, do nothing.
- **`.json()`** — take the raw response text (JSON) and parse it into a Python value (usually a dict). Same idea as `json.load()` from Project 8, but reading from the HTTP response instead of a file.

### Two dict lookups back-to-back

From the geocoding response:

```python
data = response.json()
results = data.get("results")    # a list of matches
if not results:
    return None
return results[0]                # the first match, a dict
```

Each level is just a dict or list step. No magic.

### Translating a weather code with `.get()`

The weather API returns a numeric code (`3`) instead of `"overcast"`. We have a lookup table:

```python
WEATHER_DESCRIPTIONS = {0: "clear sky", 1: "mainly clear", ..., 3: "overcast", ...}

WEATHER_DESCRIPTIONS.get(3)                                  # -> "overcast"
WEATHER_DESCRIPTIONS.get(999, "unknown weather (code 999)")  # -> "unknown weather (code 999)"
```

The same `.get()` trick from Project 7. Every code we know about maps to a phrase; every code we don't falls back to a generic message with the number shown, so the user at least learns *something* when the table is incomplete.

### Handling network errors

```python
try:
    city = look_up_city(city_name)
except requests.RequestException as e:
    print(f"Couldn't reach the geocoding service: {e}")
    exit()
```

- **`requests.RequestException`** is the "parent" exception for everything that can go wrong with an HTTP call — timeouts, DNS failures, connection resets, bad statuses (after `raise_for_status`), etc. Catching it means we cover all the common failure modes in one line.
- **`exit()`** ends the program right away. You could wrap everything in a big `if/else` instead, but early `exit()` on a fatal problem keeps the main code flat and readable.

## Run it

```
python3 solution.py
```

Try a few cities. Real ones like `Berlin`, `Tokyo`, `São Paulo`. Misspelled ones like `xyzznowhere`. Empty input (just press Enter). Each one should behave sensibly — no tracebacks, just a friendly message.

## Example run

```
$ python3 solution.py
Weather Fetcher
===============
Which city? Berlin
Found: Berlin, Germany.
Temperature: 8.8°C
Conditions:  overcast
```

The numbers will be different when you run it, because the weather is, you know, the weather.

### What a "city not found" looks like

```
$ python3 solution.py
Weather Fetcher
===============
Which city? xyzznowhere
I couldn't find a place called 'xyzznowhere'.
```

### What a network failure looks like

Unplug your Wi-Fi, or disconnect Ethernet, then run it:

```
$ python3 solution.py
Weather Fetcher
===============
Which city? Berlin
Couldn't reach the geocoding service: HTTPSConnectionPool(...): Max retries exceeded...
```

Ugly message, sure — but not a crash. That's the point.

## Check yourself

Before calling this complete, can you answer these out loud?

1. What's the difference between `import json` (which you used in Project 8) and `import requests` (which you used here)? Which one needed `pip install`?
2. Walk through the program's two API calls. What does the first one return? Which fields does the program pull out of the response? What does the second one return?
3. What exactly does `WEATHER_DESCRIPTIONS.get(code, f"unknown weather (code {code})")` do if `code = 3`? What does it do if `code = 999`?

## Try these extensions

1. **Keep asking until a real city.** If the city isn't found, loop back and ask again instead of exiting. (Pairs with Project 2's input validation.)
2. **Five-day forecast.** Open-Meteo's `forecast` endpoint also accepts a `daily=temperature_2m_max,temperature_2m_min,weather_code` parameter and a `forecast_days=5` parameter. Print the next 5 days as a table. (You'll get back parallel lists you loop over with `enumerate`.)
3. **Disambiguate.** If the geocoder returns more than one match (e.g. "Springfield"), show the list and let the user pick.
4. **Cache the last result.** After fetching, save the response to `last_weather.json` (Project 8 territory). On start-up, if the file exists and is less than an hour old, use it instead of hitting the API. Ties together files, JSON, `datetime`, and APIs in one little program.
5. **Unit toggle.** Open-Meteo accepts `temperature_unit=fahrenheit`. Ask the user at the start whether they want °C or °F.
6. **Nicer error messages.** Instead of printing the raw `RequestException`, check its type (`Timeout`, `ConnectionError`, `HTTPError`) and print a tailored message for each.

## Graduation

That's the curriculum. From Mad Libs to a program that talks to weather stations around the world. You have the full beginner toolkit now:

- input / output / variables / strings
- conditionals, loops, randomness, errors
- functions and decomposition
- lists, dictionaries, sets
- files and JSON (reading and writing)
- time, datetime
- HTTP, APIs, external packages

The honest next step isn't another tutorial — it's a project **you** want to build. Pick something small, messy, and specifically interesting to you. A tool for a hobby. A script to rename a folder of photos. A Discord bot. Whatever. You will hit walls you can't see coming; that's not a sign you're failing, it's what programming actually is. You now have the vocabulary to ask good questions, read documentation, and debug your own code. That's the whole game.

Go build something.
