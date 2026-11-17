"""Baalmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Baalmon awakened by the X-Antibody: a cloak of violet-black feathers, a white mantle,
crossed red belts, a heavy red gauntlet on its right arm and a spellbook of glowing pages in its left hand.
25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage. Built by baalmon.make(x=True).
"""
from __future__ import annotations

from baalmon import ANIM, BASE, HEIGHT, HITBOX, K, KIND, SCALE, SHINY, make

LOOK = ("Baalmon awakened by the X-Antibody: a cloak of violet feathers, a white mantle, crossed red belts, a red "
        "gauntlet arm and a glowing spellbook")
build = make("baalmonxantibody", x=True)
