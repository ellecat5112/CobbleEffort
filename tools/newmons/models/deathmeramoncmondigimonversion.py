"""Death Meramon (C'mon Digimon Version) (a Digimon of the CobbleEffort: Digital crossover; after the manga art on
wikimon.net, the C'mon Digimon story, where Deathmon takes Death Meramon's shape): a demon of grey and black fire. A
hunched man of dark smoke-black fire licked by ash-white flames, a jagged grinning mouth and white eyes, crowned with
two great curved horns and a tall blade of black flame. 25 blocks tall.

Front is -z, y is up. 62 units tall; Perfect stage.
"""
from __future__ import annotations

from _boxmodel import rod, spike
from _digidetail import solid
from _variant import clone

_M = clone("bluemeramon", "deathmeramoncmondigimonversion",
           base={"navy": (40, 38, 44), "navy_dark": (10, 10, 14), "violet": (150, 150, 160),
                 "violet_light": (230, 230, 236), "flame": (220, 220, 230, 210), "flame_core": (255, 255, 255, 235),
                 "ice": (60, 60, 70, 210), "ice_core": (200, 200, 210, 240), "eye": (255, 255, 255),
                 "horn": (236, 230, 216)},
           shiny={"navy": (90, 30, 30), "navy_dark": (40, 8, 8), "violet": (240, 120, 60), "flame": (255, 150, 60, 210),
                  "flame_core": (255, 240, 200, 235)})

HEIGHT, SCALE, HITBOX, KIND, K, ANIM = _M.HEIGHT, _M.SCALE, _M.HITBOX, _M.KIND, _M.K, _M.ANIM
LOOK = ("a hunched demon of smoke-black fire licked by ash-white flames, a jagged grin, white eyes, two great curved "
        "horns and a tall blade of black flame on its head")


def build():
    m = _M.build()
    hb = [b for b in m.boxes if b.bone == "head"]
    top = max(b.lo[1] + b.size[1] for b in hb)
    cz = sum(b.lo[2] + b.size[2] / 2 for b in hb) / len(hb)
    for sx in (-1, 1):                                                        # two great curved horns
        pts = [(sx * 2.4, top - 3.0, cz), (sx * 5.4, top - 1.0, cz), (sx * 7.0, top + 2.6, cz - 1.0),
               (sx * 6.4, top + 6.0, cz - 2.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, "head", p0, p1, 2 if j < 2 else 1, solid(_M.P, "horn"), extend=0.4)
    spike(m, "head", (0, top - 1.0, cz + 0.5), (0, 1, 0.15), 2.4, 10.0, solid(_M.P, "navy_dark"), tip=0.3)
    return m
