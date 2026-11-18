"""Mamemon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Mamemon awakened by the X-Antibody: a round silver head, flame-painted black armour and two spiked fists swinging on long blue straps like flails.
25 blocks tall. Built by _mamemon.make(x=True).

Front is -z, y is up. 22 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _mamemon import make

HEIGHT = 22
SCALE, HITBOX = sized(25, HEIGHT, 2.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = "a round silver head, flame-painted black armour and two spiked fists swinging on long blue straps like flails"
build = make("mamemonxantibody", x=True)
