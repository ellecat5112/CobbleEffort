"""Ulforce V-dramon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Ulforce V-dramon changed by the X-Antibody: darker navy and gold armour with long gold spikes, huge violet-and-crimson wings and a long crystal sword. 35 blocks.

Front is -z, y is up. Ultimate stage. Built by _ulforce.make.
"""
from __future__ import annotations

from _digi import sized
from _ulforce import make

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Ulforce V-dramon changed by the X-Antibody: darker navy and gold armour with long gold spikes, huge violet-and-crimson wings and a long crystal sword"
build = make("ulforcevdramonxantibody", "x")
