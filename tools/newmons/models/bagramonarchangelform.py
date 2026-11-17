"""Bagramon (Archangel Form) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the art on wikimon.net,
a manga sketch): Bagramon as the archangel it once was, before its fall: a tall figure in a long white hooded robe,
long black hair falling past its shoulders, white wings and gentle open hands. 35 blocks tall.

Front is -z, y is up. 70 units tall; no level known (Ultimate used). Built by bagramon.make(archangel=True).
"""
from __future__ import annotations

from bagramon import ANIM, BASE, HEIGHT, HITBOX, K, KIND, SCALE, SHINY, make

LOOK = "the archangel Bagramon once was: a long white hooded robe, long black hair, white wings and gentle open hands"
build = make("bagramonarchangelform", archangel=True)
