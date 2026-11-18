"""Modoki Betamon (a Digimon of the CobbleEffort: Digital crossover; after the official art on wikimon.net): the
"Betamon look-alike": Betamon's squat amphibian body in an olive-green hide striped dark blue, a tall jagged orange
fin, red eyes and steel claws on its four stubby legs. 1 block tall.

Front is -z, y is up. 30 units tall; Child stage. Betamon's body (betamon.make) with its own colours.
"""
from _variant import clone

_B = clone("betamon", "modokibetamon",
           base={"green": (150, 170, 70), "green_dark": (90, 110, 30), "stripe": (30, 50, 110), "fin": (240, 100, 40),
                 "fin_tip": (230, 70, 30), "fin_root": (250, 160, 70), "eye": (200, 30, 30)},
           shiny={"green": (110, 120, 200), "green_dark": (50, 60, 140), "fin": (240, 230, 90)})
HEIGHT, SCALE, HITBOX, KIND, K = _B.HEIGHT, _B.SCALE, _B.HITBOX, _B.KIND, _B.K
ANIM = getattr(_B, "ANIM", {"leg_amp": 10})
LOOK = "Betamon's squat amphibian body in olive-green hide striped dark blue, a tall jagged orange fin, red eyes and steel claws"
build = _B.make("modokibetamon")
