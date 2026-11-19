"""Trailmon Battle Form (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net): Trailmon armed for battle (after a manga drawing): a grey armoured locomotive with a sharp eye, an armoured brow and gatling barrels along both sides. 15 blocks tall.

Front is -z, y is up. Adult stage. Built by _trailmon.make.
"""
from __future__ import annotations

from _digi import sized
from _trailmon import make

HEIGHT = 19
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "Trailmon armed for battle (after a manga drawing): a grey armoured locomotive with a sharp eye, an armoured brow and gatling barrels along both sides"
build = make("trailmonbattleform", "battle")
