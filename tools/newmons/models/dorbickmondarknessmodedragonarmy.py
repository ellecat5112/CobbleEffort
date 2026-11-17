"""Dorbickmon Darkness Mode (Dragon Army) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Dorbickmon in its darkness mode, spreading two vast golden bat wings.
35 blocks tall.

Front is -z, y is up. 72 units tall; Ultimate stage.
"""
from _digi import sized
from _dorbickmon import make

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "an armoured crimson dragon-man edged with black spikes, spreading two vast golden bat wings"
build = make("dorbickmondarknessmodedragonarmy", "army")
