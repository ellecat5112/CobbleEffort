"""Arresterdramon: Superior Mode (Brave Snatcher) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the
detail standard after the official art on wikimon.net): Superior Mode armed with the Brave Snatcher: a huge steel
gauntlet on its right arm with five great crimson claws and a gold ring spinning round it. 35 blocks tall.

Front is -z, y is up. 62 units tall; Perfect stage, one-way from Superior Mode (+10 blocks).
Built by arresterdramon.make("brave").
"""
from __future__ import annotations

from _digi import sized
from arresterdramon import ANIM, BASE, HEIGHT, K, KIND, SHINY, make

SCALE, HITBOX = sized(35, HEIGHT, 2.0)
LOOK = ("Arresterdramon Superior Mode with the Brave Snatcher: a huge steel gauntlet with five crimson claws and a "
        "spinning gold ring")
build = make("arresterdramonsuperiormodebravesnatcher", "brave")
