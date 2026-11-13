from pathlib import Path

import pytest

from tennis_career.data import _extract_match_rows, _format_player_name

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
