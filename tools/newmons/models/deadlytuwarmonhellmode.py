"""Deadly Tuwarmon Hell Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): Deadly Tuwarmon studded all over with black spikes, with a heavier cannon arm set with a green gem and a
spiked tail. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from _digi import sized
from _tuwar import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 3.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("Deadly Tuwarmon studded with black spikes, with a green-gemmed cannon arm, a spiked tail and axe-blade feet")
build = make("deadlytuwarmonhellmode", hell=True)
