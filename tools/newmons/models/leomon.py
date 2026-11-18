"""Leomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the lion warrior: a muscular golden lion-man with a shaggy blond mane, a bead necklace, black trousers with a belt, studded leather straps, a short sword at the hip and a tufted tail. 15 blocks tall. Built by _leomon.make(x=False).

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _leomon import make

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a muscular golden lion-man with a shaggy blond mane, a bead necklace, black trousers with a belt, studded leather straps, a short sword at the hip and a tufted tail"
build = make("leomon", x=False)
