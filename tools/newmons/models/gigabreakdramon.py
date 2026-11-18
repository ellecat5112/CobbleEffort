"""Giga Breakdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Breakdramon rebuilt as a giant: the colossal demolition dragon in teal-green plating
over a purple chassis on its treads, two long hydraulic necks with drill-snouted heads, golden drills on its arms
and a crown of steel spikes. 35 blocks tall.

Front is -z, y is up. 40 units tall; Ultimate stage (no level on wikimon). Built on the Breakdramon model with its
own colours.
"""
from __future__ import annotations

from _variant import clone

_B = clone("breakdramon", "gigabreakdramon",
           base={"camo": (40, 130, 120), "camo_dark": (14, 70, 64), "camo_light": (110, 200, 190), "green": (110, 40, 140),
                 "green_dark": (50, 14, 70), "steel": (230, 200, 70), "steel_dark": (150, 110, 20)},
           shiny={"camo": (170, 60, 50), "camo_dark": (90, 20, 14), "camo_light": (230, 130, 110)})
HEIGHT, SCALE, HITBOX, KIND, K = _B.HEIGHT, _B.SCALE, _B.HITBOX, _B.KIND, _B.K
ANIM = getattr(_B, "ANIM", {"leg_amp": 4})
LOOK = ("a colossal demolition dragon in teal-green plating over a purple chassis on treads, two drill-snouted heads on "
        "hydraulic necks and golden arm drills")
build = _B.build
