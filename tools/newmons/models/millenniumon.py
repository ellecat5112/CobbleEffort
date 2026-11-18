"""Millenniumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the fusion of Kimeramon and Mugendramon: a hulking black chimera dragon crouched on long clawed
limbs, red-striped hide, a fanged dragon head with red eyes, extra claw-arms with red talons, and two great steel
cannons on its back wreathed in yellow light. 35 blocks tall.

Front is -z, y is up. 48 units tall; Ultimate stage. Built by _millenniumon.make.
"""
from __future__ import annotations

from _digi import sized
from _millenniumon import make

HEIGHT = 48
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a hulking black chimera dragon with red-striped hide, extra red-taloned claw-arms and two great steel cannons "
        "on its back wreathed in yellow light")
build = make("millenniumon")
