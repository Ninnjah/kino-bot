from typing import Tuple

from .kinopoisk_api import KinopoiskAPI
from .player_api import BasePlayer, AllohaPlayer, IframePlayer, VoidboostPlayer, BhceshPlayer


players: Tuple[BasePlayer] = (
    AllohaPlayer(), 
    IframePlayer(), 
    VoidboostPlayer(),
    BhceshPlayer(),
)
