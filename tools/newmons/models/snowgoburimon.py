"""Snow Goburimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a little ice-blue goblin of the snowfields with a black spiked cap, a big toothy grin, a
brown leather vest, big clawed hands and feet, and a bolt-studded wooden club. 1 block. Shamamon's body with its own
colours.

Front is -z, y is up. 64 units tall; Child stage.
"""
from __future__ import annotations

from _digi import sized
from _variant import clone

_G = clone("shamamon", "snowgoburimon",
           base={"green": (120, 170, 220), "green_dark": (50, 90, 150), "mohawk": (40, 40, 48)},
           shiny={"green": (220, 220, 236), "green_dark": (150, 150, 176), "mohawk": (200, 60, 60)})
HEIGHT = 64
SCALE, HITBOX = sized(1, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a little ice-blue goblin with a black spiked cap, a toothy grin, a brown leather vest and a bolt-studded wooden club"
build = _G.build
