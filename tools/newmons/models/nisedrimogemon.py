"""Nise Drimogemon (a Digimon of the CobbleEffort: Digital crossover; after the official art on wikimon.net): the
"fake" Drimogemon: Drimogemon's shaggy cream mole body with a violet mane and a violet drill, a dizzy spiral eye and
a gaping fanged mouth, violet drill-tipped claws. 15 blocks tall.

Front is -z, y is up. 34 units tall; Adult stage. Drimogemon's body (drimogemon.py) with its own colours.
"""
from _variant import clone

_D = clone("drimogemon", "nisedrimogemon",
           base={"yellow": (250, 246, 200), "yellow_dark": (200, 190, 140), "mane": (130, 80, 170),
                 "mane_dark": (70, 40, 110), "steel": (150, 110, 190), "steel_dark": (80, 50, 120)},
           shiny={"yellow": (240, 210, 170), "mane": (60, 150, 100), "mane_dark": (20, 90, 50)})
HEIGHT, SCALE, HITBOX, KIND, K, ANIM = _D.HEIGHT, _D.SCALE, _D.HITBOX, _D.KIND, _D.K, _D.ANIM
LOOK = "a shaggy cream mole with a violet mane, a violet drill, a dizzy eye, a gaping fanged mouth and violet drill claws"
build = _D.build
