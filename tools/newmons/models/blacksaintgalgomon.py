"""Black Saint Galgomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Saint Galgomon's dark twin: a heavy grey armoured mech with missile pods and red
warheads on its back, gatlings on both arms and spiked steel knee bands. 35 blocks tall.

Front is -z, y is up. 72 units tall; Ultimate stage. Built by _galgomon.make(black=True).
"""
from __future__ import annotations

from _digi import sized
from _galgomon import make

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("Saint Galgomon's dark twin: a heavy grey armoured mech with missile pods and red warheads on its back, "
        'gatlings on both arms and spiked steel knee bands')
build = make("blacksaintgalgomon", "ultimate", black=True)
