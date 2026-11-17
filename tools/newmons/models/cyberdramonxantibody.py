"""Cyberdramon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a sleek glossy black armoured dragon traced with glowing orange lines, a long-horned head, long claws and hexagon-patterned blade-wings. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

from _cyberdramon import make
from _digi import sized

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a sleek glossy black armoured dragon traced with glowing orange lines, a long-horned head, long claws and hexagon-patterned blade-wings"

build = make("cyberdramonxantibody", x=True)
