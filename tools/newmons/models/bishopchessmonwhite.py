"""Bishop Chessmon (White) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the bishop of the white chess army. A white segmented body with a long telescoping head
capped in violet, a violet tabard with a grey cross, riveted violet shoulder plates, a long violet cape, heavy square
feet and a tall white staff topped with an arrowhead finial. 25 blocks tall.

Front is -z, y is up. 70 units tall; Perfect stage. Built by bishopchessmonblack.make(white=True).
"""
from __future__ import annotations

from bishopchessmonblack import ANIM, BASE, HEIGHT, HITBOX, K, KIND, SCALE, SHINY, make

LOOK = ("the white chess bishop: a white segmented body with a telescoping violet-capped head, a violet tabard with a "
        "cross, a long violet cape and a white staff")
build = make("bishopchessmonwhite", white=True)
