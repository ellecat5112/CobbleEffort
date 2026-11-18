"""Mach Leomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the only picture on wikimon.net, a
manga sketch): a lean, muscular lion warrior with a long flowing mane, loose trousers with a belt, strapped forearms
and a sword at the hip. The sketch is uncoloured; the colours follow Leomon's.
25 blocks tall. A recoloured copy of the Leomon builder (_variant.clone) (its base look).

Front is -z, y is up. 64 units tall; Perfect stage (no level on wikimon).
"""
from __future__ import annotations

from _digi import sized
from _variant import clone

_L = clone("_leomon", "machleomon", base={"tan": (230, 190, 130), "tan_dark": (160, 120, 70), "mane": (250, 236, 200),
                                          "mane_dark": (190, 170, 130), "black": (220, 214, 200), "black_dark": (160, 150, 130)},
           shiny={"tan": (200, 200, 210), "mane": (120, 140, 200)})
HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a lean muscular lion warrior with a very long pale mane, loose trousers, strapped forearms and a sword at the hip"
build = _L.make("machleomon", x=False)
