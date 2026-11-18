"""Ice Devimon Enhancement Absorbent (a Digimon of the CobbleEffort: Digital crossover; hand-built after the
official art on wikimon.net): Ice Devimon after absorbing enhancement data: one arm swollen into a huge bandaged ice
arm with crystal claws, and ice spikes along its wings. 15 blocks tall.

Front is -z, y is up. 66 units tall; Adult stage. Built by _icedevimon.make(absorbent=True).
"""
from __future__ import annotations

from _digi import sized
from _icedevimon import make

HEIGHT = 66
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a gaunt white ice devil with one huge bandaged ice arm, crystal claws and ice-spiked tattered wings"
build = make("icedevimonenhancementabsorbent", absorbent=True)
