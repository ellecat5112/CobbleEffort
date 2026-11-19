"""Triceramon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Triceramon changed by the X-Antibody: a broad green frill fringed with spikes, three long drill horns
blazing with fire and steel-blue riveted armour studded with spikes. 25 blocks.

Front is -z, y is up. Perfect stage. Built by _triceramon.make.
"""
from __future__ import annotations

from _digi import sized
from _triceramon import make

HEIGHT = 53
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a green-frilled triceratops with three flaming drill horns and steel-blue spiked armour"
build = make("triceramonxantibody", True)
