import json
import re

import pandas as pd
import requests

MATCH_COLUMNS = {0: "date",1: "tournament",2: "surface",4: "result",11: "opponent",16: "opponent_dob_or_age"}
DAYS_PER_YEAR = 365.25
BASE_URL = "https://www.tennisabstract.com/jsmatches"
REQUEST_TIMEOUT = 10


def _format_player_name(player_name):
    # e.g. "serena williams" -> "SerenaWilliams", the format used in URLs
    if not isinstance(player_name, str):
        raise TypeError("player_name must be a string, e.g. 'Serena Williams'")
    if not player_name.strip():
        raise ValueError("player_name cannot be empty, e.g. 'Serena Williams'")
    pieces = re.split(r"[\s-]+", player_name.strip())
    return "".join(piece[:1].upper() + piece[1:] for piece in pieces)


def _extract_match_rows(js_text):
    #Extracing list of match rows from a career JS file's text
    start, end = js_text.find("["), js_text.rfind("]")
    if start == -1:
        raise ValueError("Could not find match data in the career file")
    if end < start:
        raise ValueError("Could not find match data in the career file")
    js_end = end + 1
    return json.loads(js_text[start:js_end])


def _build_match_frame(rows):
    # Keeping only fields in MATCH_COLUMNS and turning date strings into dates
    kept = [[row[position] for position in MATCH_COLUMNS] for row in rows]
    matches = pd.DataFrame(kept, columns=list(MATCH_COLUMNS.values()))
    matches["date"] = pd.to_datetime(matches["date"], format="%Y%m%d")
    return matches


def _years_between(start_dates, end_dates):
    return (end_dates-start_dates).dt.days/DAYS_PER_YEAR


def _add_opponent_age(matches):
    # because womens files give opponent birth dates but men's give ages
    matches = matches.copy()
    raw = matches.pop("opponent_dob_or_age")
    is_dob = raw.str.fullmatch(r"\d{8}")
    dob = pd.to_datetime(raw.where(is_dob), format="%Y%m%d", errors="coerce")
    given_age = pd.to_numeric(raw, errors="coerce")
    age_from_dob = _years_between(dob, matches["date"])
    matches["opponent_age"] = age_from_dob.where(is_dob, given_age)
    return matches


def _extract_player_dob(js_text):
    # player's JS file has a line like: var dob=19810926
    found = re.search(r"var dob\s*=\s*(\d{8})", js_text)
    if found is None:
        raise ValueError("Could not find the player's date of birth")
    return found.group(1)


def _add_player_age(matches, player_dob):
    # negative age_diff means the opponent was older
    matches = matches.copy()
    dob = pd.to_datetime(str(player_dob), format="%Y%m%d")
    matches["player_age"] = _years_between(dob, matches["date"])
    matches["age_diff"] = matches["player_age"] - matches["opponent_age"]
    return matches


def _build_js_url(player_name, career_file):
    if career_file:
        file_ending = "Career.js"
    else:
        file_ending = ".js"
    return f"{BASE_URL}/{player_name}{file_ending}"


def _download_js_file(player_name, career_file):
    url = _build_js_url(player_name, career_file)
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as error:
        raise ConnectionError("Couldn't connect to tennisabstract.com") from error
    if response.status_code == 404:
        raise ValueError(f"No player named '{player_name}' found")
    if response.status_code >= 400:
        raise ConnectionError(f"tennisabstract.com returned status {response.status_code}")
    return response.text


def get_career_data(player_name):
    # getting career matches for one player
    formatted_name = _format_player_name(player_name)
    career_text = _download_js_file(formatted_name, True)
    player_text = _download_js_file(formatted_name, False)
    rows = _extract_match_rows(career_text)
    matches = _build_match_frame(rows)
    matches = _add_opponent_age(matches)
    player_dob = _extract_player_dob(player_text)
    matches = _add_player_age(matches, player_dob)
    return matches
