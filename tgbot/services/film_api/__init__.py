from typing import Tuple

from .player_api import (
    BasePlayer,
    AllohaPlayer,
    IframePlayer,
    VoidboostPlayer,
    BhceshPlayer,
    CollapsPlayer,
)


players: Tuple[BasePlayer] = (
    AllohaPlayer(),
    IframePlayer(),
    VoidboostPlayer(),
    BhceshPlayer(),
    CollapsPlayer(),
)
