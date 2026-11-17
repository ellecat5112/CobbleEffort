"""Dark Knightmon (Bagramon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): Darkness Bagramon fused with Dark Knightmon's armour: a hulking body with a massive bone-white skeletal arm, black plate banded in steel, gold horns and a tattered black cape. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

from _darknessbagramon import make
from _digi import sized

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 3.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "Darkness Bagramon fused with Dark Knightmon's armour: a hulking body with a massive bone-white skeletal arm, black plate banded in steel, gold horns and a tattered black cape"

build = make("darkknightmonbagramon", dk=True)
