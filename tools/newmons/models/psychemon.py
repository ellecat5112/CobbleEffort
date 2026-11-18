"""Psychemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a psychedelic Gabumon: a hot-pink reptile under a white wolf pelt splashed with purple stripes,
a striped horn, green claws and a green skull emblem on its belly. 1 block. Built by a fresh copy of _gabumon with its
own colours (shiny: teal hide, orange stripes).

Front is -z, y is up. 30 units tall; Child stage.
"""
from __future__ import annotations

from _digi import sized
from _greyvar import _fresh

_G = _fresh("_gabumon", "psychemon")
_G.BASE.update({"hide": (230, 60, 150), "hide_dark": (150, 20, 90), "pelt": (248, 246, 252), "pelt_dark": (200, 190, 220),
                "stripe": (120, 40, 170), "claw": (60, 180, 60), "emblem": (70, 160, 60), "emblem2": (30, 90, 30),
                "eye": (110, 50, 170)})
_G.BLACK = {"hide": (40, 170, 170), "hide_dark": (14, 100, 100), "stripe": (240, 140, 30), "claw": (240, 200, 40),
            "eye": (240, 140, 30)}
HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 14}
LOOK = "a hot-pink reptile under a white wolf pelt splashed with purple stripes, a striped horn, green claws and a skull emblem"
_real = _G.Model
_G.Model = lambda _n, *a, **k: _real("psychemon", *a, **k)
build = _G.make("psychemon", "base")
