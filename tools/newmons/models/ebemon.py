"""EBEmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a grey alien cyborg with a long white domed head, a dark visor and red eye-lens, a laser gun, a probe arm and a skirt of ribbed steel hoses.
35 blocks tall.

Front is -z, y is up. 38 units tall; Ultimate stage.
"""
from _digi import sized
from _ebemon import make

HEIGHT = 38
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a small white-and-chrome alien cyborg with a long domed head, a dark visor, a laser gun, a probe arm and ribbed hose legs"
build = make("ebemon")
