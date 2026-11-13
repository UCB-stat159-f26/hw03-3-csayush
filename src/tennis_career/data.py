"""Download and clean career match data from tennisabstract.com."""

import re


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
