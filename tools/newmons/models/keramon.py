"""Keramon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the bug that eats data: a pale lavender head with green ringed eyes and a wide stitched grin, a spiky yellow collar, long wavy antennae, a skirt of dangling tendrils and long arms with big clawed hands.
Child stage, 1 block tall. Built by _keramon.make(x=False).

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

from _digi import sized
from _keramon import make

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 2.0)
KIND = "floater"
K = 4
LOOK = "a pale lavender data bug with a stitched grin, a spiky yellow collar, wavy antennae, dangling tendrils and big clawed hands"
build = make("keramon", x=False)
