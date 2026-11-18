"""Megadramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the cyborg dragon twin of Gigadramon: a black armoured dragon head with yellow eyes and a toothed
jaw, great violet swept-back jet wings, orange-red hide, two huge mechanical arms ending in grey drill-claw cannons and
a long orange serpentine tail. 25 blocks tall. A recoloured copy of Gigadramon's module (_variant.clone).

Front is -z, y is up. 48 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _variant import clone

_G = clone("gigadramon", "megadramon",
           base={"green": (50, 50, 62), "green_dark": (16, 16, 22), "green_light": (110, 110, 130), "violet": (220, 90, 50),
                 "violet_dark": (140, 40, 20)},
           shiny={"green": (220, 220, 236), "green_dark": (130, 130, 150), "green_light": (255, 255, 255), "violet": (60, 120, 220)})
HEIGHT = 48
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a black armoured cyborg dragon head with yellow eyes, swept jet wings, orange-red hide, drill-claw cannon arms and a serpent tail"
build = _G.build
