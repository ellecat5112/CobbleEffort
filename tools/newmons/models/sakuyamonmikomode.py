"""Sakuyamon: Miko Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a shrine maiden in a white haori and long red hakama with a gold fox mask, long silver hair and a purification wand.
35 blocks. Built by _sakuyamon.make(look="miko").

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _sakuyamon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a shrine maiden in a white haori and long red hakama with a gold fox mask, long silver hair and a purification wand"
build = make("sakuyamonmikomode", look="miko")
