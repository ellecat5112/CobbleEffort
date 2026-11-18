"""Metal Greymon: Alterous Mode (a Digimon of the CobbleEffort: Digital crossover; built after the official art on wikimon.net): MetalGreymon armed for Alterous Mode: its orange body, violet ragged wings, a gun-steel Trident Arm and a towering sword held upright in its right hand.
The Agumon line's MetalGreymon body with its own colours (_greyvar.make). Perfect stage, 25 blocks tall.

Front is -z, y is up. 42 units tall (the wings); baseScale 9.7 like MetalGreymon.
"""
from __future__ import annotations

from _greyvar import make

SCALE = 9.7
HITBOX = [1.6, 2.6]
KIND = "biped"
K = 3
HEIGHT = 42
ANIM = {"leg_amp": 12}
LOOK = "MetalGreymon armed for Alterous Mode: its orange body, violet ragged wings, a gun-steel Trident Arm and a towering sword held upright in its right hand"
_body = make("metalgreymonalterousmode", metal=True,
             base={"wing": (90, 60, 190), "wing_dark": (40, 24, 110), "helmet": (120, 124, 136), "helmet_dark": (70, 72, 84)},
             shiny={"orange": (64, 62, 70), "orange_dark": (40, 38, 46), "wing": (200, 60, 60)})


def build():
    """The body plus the towering sword upright in its right hand (a steel blade with a gold-and-black core)."""
    from _boxmodel import spike
    from _digidetail import metal, solid
    from _route import pal
    p = {"steel": (220, 224, 236), "steel_dark": (110, 114, 126), "gold": (240, 200, 70), "black": (30, 30, 36)}

    def P(v):
        return pal(p, {"steel": (250, 220, 120), "gold": (200, 60, 60)}, v)

    m = _body()
    arm = next(b for b in m.bones if b["name"] == "arm_right")["name"]
    x, z = -8.0, -10.0
    m.box(arm, x - 1.4, 18.0, z - 0.6, x + 1.4, 24.0, z + 0.6, solid(P, "black"))                 # grip
    m.box(arm, x - 3.4, 24.0, z - 1.0, x + 3.4, 25.4, z + 1.0, metal(P, "gold"))                  # guard
    m.box(arm, x - 2.6, 25.4, z - 0.5, x + 2.6, 52.0, z + 0.5, metal(P, "steel", dark="steel_dark"))   # blade
    m.box(arm, x - 0.8, 26.0, z - 0.6, x + 0.8, 50.0, z + 0.6, solid(P, "gold", glow=True))       # glowing core
    spike(m, arm, (x, 52.0, z), (0, 1, 0), 2.6, 4.0, metal(P, "steel"), tip=0.8)
    return m
