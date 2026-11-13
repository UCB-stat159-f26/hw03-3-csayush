from pathlib import Path

import pandas as pd
import pytest

from tennis_career.data import (_add_opponent_age,_build_match_frame,_extract_match_rows,_format_player_name)

FIXTURES = Path(__file__).parent / "fixtures"


def read_fixture(file_name):
    return (FIXTURES / file_name).read_text()


@pytest.mark.parametrize(
    "player_name, expected",
    [
        ("serena williams", "SerenaWilliams"),
        ("Serena Williams", "SerenaWilliams"),
        ("SerenaWilliams", "SerenaWilliams"),
        (" rafael   nadal ", "RafaelNadal"),
        ("Felix Auger-Aliassime", "FelixAugerAliassime"),
    ],
)
def test_format_player_name_valid(player_name, expected):
    assert _format_player_name(player_name) == expected


@pytest.mark.parametrize("player_name", ["", "   "])
def test_format_player_name_empty(player_name):
    with pytest.raises(ValueError):
        _format_player_name(player_name)


@pytest.mark.parametrize("player_name", [None, 42])
def test_format_player_name_not_string(player_name):
    with pytest.raises(TypeError):
        _format_player_name(player_name)


def test_extract_match_rows_female():
    rows = _extract_match_rows(read_fixture("FemalePlayerCareer.js"))
    assert len(rows) == 3
    assert rows[0][0] == "19951030"
    assert rows[0][11] == "Anne Miller"
    assert rows[0][16] == "19770119"


def test_extract_match_rows_male():
    rows = _extract_match_rows(read_fixture("MalePlayerCareer.js"))
    assert len(rows) == 3
    assert rows[0][0] == "20010910"
    assert rows[0][11] == "Guillermo Platel"
    assert rows[0][16] == "22.264202601"


def test_extract_match_rows_no_array():
    with pytest.raises(ValueError):
        _extract_match_rows("var morematchmx = ;")


def build_fixture_frame(file_name):
    return _build_match_frame(_extract_match_rows(read_fixture(file_name)))


def test_build_match_frame_columns():
    matches = build_fixture_frame("FemalePlayerCareer.js")
    assert list(matches.columns) == ["date", "tournament", "surface", "result", "opponent",
        "opponent_dob_or_age"]
    assert len(matches) == 3


def test_build_match_frame_female_values():
    matches = build_fixture_frame("FemalePlayerCareer.js")
    assert matches["date"].iloc[0] == pd.Timestamp("1995-10-30")
    assert matches["tournament"].iloc[0] == "Canadian Open"
    assert list(matches["result"]) == ["L", "L", "L"]
    assert matches["opponent"].iloc[2] == "Magui Serna"
    assert matches["opponent_dob_or_age"].iloc[2] == "19790301"


def test_build_match_frame_male_values():
    matches = build_fixture_frame("MalePlayerCareer.js")
    assert matches["date"].iloc[1] == pd.Timestamp("2001-09-17")
    assert matches["surface"].iloc[1] == "Clay"
    assert list(matches["result"]) == ["L", "L", "W"]
    assert matches["opponent"].iloc[2] == "Israel Matos Gil"
    assert matches["opponent_dob_or_age"].iloc[2] == "18.7597535934"


def test_add_opponent_age_female():
    matches = _add_opponent_age(build_fixture_frame("FemalePlayerCareer.js"))
    assert "opponent_dob_or_age" not in matches.columns
    assert list(matches["opponent_age"].round(2)) == [18.78, 26.84, 18.43]


def test_add_opponent_age_male():
    matches = _add_opponent_age(build_fixture_frame("MalePlayerCareer.js"))
    expected = [22.264202601, 24.2902121834, 18.7597535934]
    assert list(matches["opponent_age"]) == pytest.approx(expected)


def test_add_opponent_age_missing_value():
    matches = build_fixture_frame("MalePlayerCareer.js")
    matches.loc[0, "opponent_dob_or_age"] = ""
    assert pd.isna(_add_opponent_age(matches)["opponent_age"].iloc[0])
