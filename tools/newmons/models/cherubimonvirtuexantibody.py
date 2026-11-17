"""Cherubimon (Virtue) (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): the holy angel beast awakened by the X-Antibody: a sphere of white light at its core, pink wings and enormous pink hands studded with gold. One of the Three Great Angels. 35 blocks tall.

Front is -z, y is up. 80 units tall; Ultimate stage (floats).
"""
from __future__ import annotations

from _cherubimon import make
from _digi import sized

HEIGHT = 80
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "the holy angel beast awakened by the X-Antibody: a sphere of white light at its core, pink wings and enormous pink hands studded with gold"

build = make("cherubimonvirtuexantibody", "virtue_x")
