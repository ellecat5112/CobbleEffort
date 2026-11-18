"""Prince Mamemon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art
on wikimon.net): the X prince with big blue eyes, a tall red crown, a vast ermine robe and a golden-orb sceptre.
35 blocks. Built by _princemamemon.make(x=True).

Front is -z, y is up. 38 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _princemamemon import make

HEIGHT = 38
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = "a round yellow face with big blue eyes, a tall red crown, a vast red-and-white ermine robe and a golden-orb sceptre"
build = make("princemamemonxantibody", x=True)
