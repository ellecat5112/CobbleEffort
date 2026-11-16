"""Armamon: Burst Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Armamon at the peak of its power: bronze-gold armour bristling with blades, a tattered
crimson cape, blazing flames behind it and a ring of floating swords. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage. Built by armamon.make(burst=True).
"""
from __future__ import annotations

from armamon import ANIM, HEIGHT, HITBOX, K, KIND, SCALE, make

LOOK = ("Armamon at its peak: bronze-gold armour bristling with blades, a tattered crimson cape, flames behind it and "
        "a ring of floating swords")
build, P = make("armamonburstmode", burst=True)
