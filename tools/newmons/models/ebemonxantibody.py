"""EBEmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): EBEmon awakened by the X-Antibody, heavier, with a chrome skull head, a broad white shield-body, coloured capsule tanks, a red cannon arm, ribbed hose tentacles and teal lightning.
35 blocks tall.

Front is -z, y is up. 48 units tall; Ultimate stage.
"""
from _digi import sized
from _ebemon import make

HEIGHT = 48
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a heavy chrome-skulled alien cyborg with a broad white body, coloured capsule tanks, a red cannon arm, hose tentacles and teal lightning"
build = make("ebemonxantibody", x=True)
