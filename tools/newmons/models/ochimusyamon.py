"""Ochi Musyamon (a Digimon of the CobbleEffort: Digital crossover; after the manga panel on wikimon.net): the fallen
samurai: Musyamon gone to seed, its lacquer armour faded to battered grey and black, a wild white mane and beard, a
dull blade and a torn dark cape. 15 blocks tall.

Front is -z, y is up. 66 units tall; Adult stage (no level on wikimon; Musyamon's). Musyamon's body (musyamon.py) with
its own colours.
"""
from _variant import clone

_M = clone("musyamon", "ochimusyamon",
           base={"red": (130, 130, 136), "red_dark": (60, 60, 66), "green": (150, 140, 120), "green_dark": (90, 80, 64),
                 "blond": (240, 240, 236), "blond_dark": (180, 180, 176), "violet": (60, 56, 70),
                 "violet_dark": (24, 22, 30), "gold": (150, 140, 110), "steel": (170, 170, 176)},
           shiny={"red": (130, 90, 60), "red_dark": (70, 40, 20)})
HEIGHT, SCALE, HITBOX, KIND, K, ANIM = _M.HEIGHT, _M.SCALE, _M.HITBOX, _M.KIND, _M.K, _M.ANIM
LOOK = "a fallen samurai in battered grey-and-black armour with a wild white mane and beard, a dull blade and a torn dark cape"
build = _M.build
