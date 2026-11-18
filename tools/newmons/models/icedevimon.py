"""Ice Devimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the frozen fallen angel: a gaunt white Devimon of ice with long clawed arms, a mask face
with red eyes, curling horns, frost-white hair and great tattered white bat wings. 15 blocks tall.

Front is -z, y is up. 66 units tall; Adult stage. Built by _icedevimon.make(absorbent=False).
"""
from __future__ import annotations

from _digi import sized
from _icedevimon import make

HEIGHT = 66
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a gaunt white ice devil with long clawed arms, a red-eyed mask face, curling horns and tattered white bat wings"
build = make("icedevimon", absorbent=False)
