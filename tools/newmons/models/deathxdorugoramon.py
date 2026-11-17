"""Death-X-DORUgoramon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a great black four-legged dragon with a saw-blade steel snout, a crest of red feather spines and bone blades, and whip tails tipped with blades.
35 blocks tall.

Front is -z, y is up. 38 units tall; Ultimate stage.
"""
from _digi import sized
from _doru import goramon

HEIGHT = 38
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a great black four-legged dragon with a saw-blade steel snout, a crest of red feather spines and bone blades, and whip tails tipped with blades"
build = goramon("deathxdorugoramon", "death")
