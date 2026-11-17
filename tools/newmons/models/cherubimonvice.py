"""Cherubimon (Vice) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): the fallen angel beast: dark violet hide, a green belly, a crest of blue spikes round its face, horned ears and monstrous clawed arms. One of the Three Great Angels. 35 blocks tall.

Front is -z, y is up. 80 units tall; Ultimate stage (floats).
"""
from __future__ import annotations

from _cherubimon import make
from _digi import sized

HEIGHT = 80
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "the fallen angel beast: dark violet hide, a green belly, a crest of blue spikes round its face, horned ears and monstrous clawed arms"

build = make("cherubimonvice", "vice")
