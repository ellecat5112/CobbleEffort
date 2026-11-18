"""Kodokugumon Child (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a bulbous violet-striped spider with brass spikes, a golden horned face plate with green eyes, furry red-banded legs and skull-marked fangs.
Child stage, 1.0 blocks tall. Built by _kodoku.make(child=True).

Front is -z, y is up. 20 units tall.
"""
from __future__ import annotations

from _digi import sized
from _kodoku import make

HEIGHT = 20
SCALE, HITBOX = sized(1.0, HEIGHT, 2.4)
KIND = "quadruped"
K = 4
LOOK = "a bulbous violet-striped spider with brass spikes, a golden horned face plate with green eyes, furry red-banded legs and skull-marked fangs"
build = make("kodokugumonchild", child=True)
