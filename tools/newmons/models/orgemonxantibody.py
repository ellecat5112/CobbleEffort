"""Orgemon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Orgemon changed by the X-Antibody: dark green skin scarred with glowing red seams, black studded wraps, a red-and-white mane and a great bloodied guitar-axe. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage. Built by _orgemon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _orgemon import make

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Orgemon changed by the X-Antibody: dark green skin scarred with glowing red seams, black studded wraps, a red-and-white mane and a great bloodied guitar-axe"
build = make("orgemonxantibody", x=True)
