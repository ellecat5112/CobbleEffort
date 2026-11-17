"""Ballistamon MC (a Digimon of the CobbleEffort: Digital crossover; hand-built after the art on wikimon.net, a manga
drawing): Ballistamon grown into a walking fortress: a vast round armoured dome with a great grille face, lit
windows, two red-capped towers, cannons and the two-pronged horn on top. 35 blocks tall.

Front is -z, y is up. 50 units tall; no level known (Ultimate used). Built by ballistamon.make("mc").
"""
from __future__ import annotations

from _digi import sized
from ballistamon import ANIM, BASE, HEIGHT, K, SHINY, make

KIND = "biped"
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
LOOK = "Ballistamon as a walking fortress: a vast armoured dome with a grille face, lit windows, towers and cannons"
build = make("ballistamonmc", "mc")
