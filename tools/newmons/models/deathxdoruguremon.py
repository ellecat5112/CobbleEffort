"""Death-X-DORUguremon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): an upright black flying dragon with a beaked helm, huge layered red-and-black feather wings, red hooked claws and a chained iron ball.
25 blocks tall.

Front is -z, y is up. 48 units tall; Perfect stage.
"""
from _digi import sized
from _doru import guremon

HEIGHT = 48
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "floater"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "an upright black flying dragon with a beaked helm, huge layered red-and-black feather wings, red hooked claws and a chained iron ball"
build = guremon("deathxdoruguremon", "death")
