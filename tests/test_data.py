import pytest

from tennis_career.data import _format_player_name


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
