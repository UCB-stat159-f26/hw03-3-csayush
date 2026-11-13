import json
import re

import pandas as pd

MATCH_COLUMNS = {0: "date",1: "tournament",2: "surface",4: "result",
                 11: "opponent",16: "opponent_dob_or_age"}
DAYS_PER_YEAR = 365.25


def _format_player_name(player_name):
    """Convert a player's name to the format used in tennisabstract URLs.

    Splits on spaces and hyphens, capitalizes the first letter of each
    piece, and joins them, e.g. "serena williams" -> "SerenaWilliams".
    """
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
