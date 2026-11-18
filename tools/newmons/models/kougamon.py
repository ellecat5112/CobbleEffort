"""Kougamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
Kouga ninja, Igamon's rival: the same round ninja build in violet, with a horned hood, orange eyes, a buck-toothed grin,
a violet scarf, a spiked iron ball and a great iron shuriken underfoot. 15 blocks tall. A recoloured copy of Igamon's
module (_variant.clone).

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _variant import clone

_K = clone("igamon", "kougamon",
           base={"red": (110, 50, 160), "red_dark": (50, 16, 90), "red_light": (190, 140, 230), "blue": (200, 180, 60),
                 "yellow": (230, 60, 60)},
           shiny={"red": (40, 40, 50), "red_dark": (12, 12, 18), "red_light": (110, 110, 130)})
HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a round violet ninja with a pointed hood, orange eyes, a violet scarf, a ninjato, a spiked iron ball and a great shuriken underfoot"
build = _K.build
