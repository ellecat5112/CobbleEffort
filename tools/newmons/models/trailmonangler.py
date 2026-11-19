"""Trailmon Angler (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net): a living locomotive: a teal train with an orange skirt, a white grille jaw, red eyes, a glowing lure on a stalk over its nose and a tail fin. 15 blocks tall.

Front is -z, y is up. Adult stage. Built by _trailmon.make.
"""
from __future__ import annotations

from _digi import sized
from _trailmon import make

HEIGHT = 24
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a living locomotive: a teal train with an orange skirt, a white grille jaw, red eyes, a glowing lure on a stalk over its nose and a tail fin"
build = make("trailmonangler", "angler")
