"""Alphamon: Ouryuken (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Alphamon fused with the spirit of Ouryumon. The gunmetal-and-gold Royal Knight armour,
now with great swept wings of white feathers that burn yellow, orange and red toward their tips, and the Ouryuken,
a huge gold blade with a black core, held point-down in its right hand. 35 blocks tall.

Front is -z, y is up. 72 units tall; Ultimate stage. Built by alphamon.build.
"""
from __future__ import annotations

import alphamon
from alphamon import ANIM, BASE, HEIGHT, HITBOX, K, KIND, SCALE, SHINY

LOOK = ("Alphamon fused with Ouryumon: gunmetal-and-gold armour, great swept wings of white feathers burning red at "
        "the tips and the huge gold Ouryuken blade")


def build():
    return alphamon.build("alphamonouryuken", ouryuken=True)
