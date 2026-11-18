"""Garurumon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard
after the official art on wikimon.net): Garurumon awakened by the X-Antibody: shaggy lavender-grey fur, a row of great
steel spikes along its back bound by a red-striped band, and steel claws. Adult stage, 15 blocks tall.

Front is -z, y is up. 34 units tall. Built by _garurumon.make(look="x").
"""
from __future__ import annotations

from _digi import sized
from _garurumon import make

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a shaggy lavender-grey wolf with great steel spikes along its back and steel claws"
build = make("garurumonxantibody", "x")
