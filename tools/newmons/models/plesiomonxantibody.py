"""Plesiomon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): the sleek white X plesiosaur with a blond mane, long whip blade fins and blue-dipped flippers. 35 blocks.
Built by _plesiomon.make(x=True).

Front is -z, y is up. 50 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _plesiomon import make

HEIGHT = 50
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a sleek white plesiosaur with a blond mane, long whip-like blade fins, blue-dipped flippers and a gold-banded belly"
build = make("plesiomonxantibody", x=True)
