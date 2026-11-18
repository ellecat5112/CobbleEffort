"""Gottsumon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): Gottsumon awakened by the X-Antibody: a squat hunched golem of smooth grey slabs with a one-eyed
helmeted head, a stone horn and a huge spread stone hand. Child stage, 1 block tall.

Front is -z, y is up. 26 units tall. Built by _gottsumon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _gottsumon import make

HEIGHT = 26
SCALE, HITBOX = sized(1.0, HEIGHT, 1.6)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = "a squat grey stone golem with a one-eyed helmeted head, a stone horn and a huge spread stone hand"
build = make("gottsumonxantibody", x=True)
