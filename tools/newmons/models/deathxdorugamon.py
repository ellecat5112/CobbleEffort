"""Death-X-DORUgamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a dark blue four-legged dragon with a riveted steel muzzle mask, head bolts, enormous swept fin-wings, red hooked claws and sparking tail wires.
15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from _digi import sized
from _doru import gamon

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a dark blue four-legged dragon with a riveted steel muzzle mask, head bolts, enormous swept fin-wings, red hooked claws and sparking tail wires"
build = gamon("deathxdorugamon", "death")
