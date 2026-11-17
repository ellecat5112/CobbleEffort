"""Shared builder for Dracomon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): a sturdy
little teal dragon with a cream belly, red antler horns, small red bat wings, a big head with red eyes and a toothy
grin, clawed hands, thick legs with pale talons and a long tail. make(x=True): Dracomon (X-Antibody), leaner and
fiercer, a darker teal fading to navy, a gold X mark on its brow, tall pink translucent crest horns, a pink chest gem,
bigger red wings and a longer whip tail. Shiny: crimson scales.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import bat_wing, theropod
from _digidetail import cutout, gem, scales, skin, solid
from _route import pal, tone

BASE = {"teal": (50, 150, 150), "teal_dark": (14, 70, 80), "teal_light": (130, 210, 210), "navy": (30, 40, 90),
        "cream": (240, 220, 190), "cream_dark": (190, 160, 130), "red": (210, 50, 30), "red_dark": (130, 20, 10),
        "pink": (255, 120, 140, 200), "pink_light": (255, 210, 220, 220), "gold": (250, 210, 60), "talon": (240, 230, 214),
        "mouth": (180, 40, 50), "tooth": (250, 250, 246), "eye": (220, 40, 30)}
SHINY = {"teal": (180, 50, 60), "teal_dark": (90, 14, 20), "teal_light": (240, 130, 130), "navy": (80, 20, 30)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    HIDE = scales(P, "teal", "teal_dark", size=1.2, light="teal_light", rim_mix=0.3)
    BELLY = skin(P, "cream", dark="cream_dark", var=0.03)

    def wingf(xx, y, z, face, variant, box=None, **k):
        return tone(P(variant)["red"], face), None

    def build():
        m = Model(name)
        mats = {"skin": HIDE, "belly": BELLY, "neck": HIDE, "head": HIDE, "snout": HIDE, "jaw": BELLY,
                "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "arm": HIDE, "hand": HIDE,
                "claw": solid(P, "talon"), "thigh": HIDE, "shin": HIDE, "foot": HIDE, "talon": solid(P, "talon"),
                "tail": HIDE, "tail_tip": HIDE}
        a = theropod(m, mats, name, hip_y=9.0, hip_z=2.0, chest=(0, 16.0, -1.0), body_r=5.0, chest_r=4.6,
                     neck_top=(0, 20.0, -2.0), head_len=8.0 if not x else 9.0, head_w=4.0, head_h=4.4,
                     mouth_open=14 if not x else 24, teeth=4, arm_len=5.0, arm_bulk=1.1, leg_bulk=1.5, stance=3.6,
                     tail=((0, 9, 6), (0, 6, 12), (0, 4, 18)) if not x else ((0, 9, 6), (2, 7, 13), (4, 6, 20),
                                                                              (6, 8, 26)),
                     tail_r=(3.0, 2.2, 1.4) if not x else (2.6, 2.0, 1.4, 0.8))
        bd, hd = a["body"], a["head"]
        ex, ey, ez = a["eye"]
        for sx in (-1, 1):
            m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.5, ez - 0.7, max(sx * ex, sx * (ex + 0.3)), ey + 0.5,
                  ez + 0.7, solid(P, "eye"))
            if not x:                                                              # red antler horns
                pts = [(sx * 2.0, ey + 2.0, ez + 2.0), (sx * 2.6, ey + 6.0, ez + 3.0), (sx * 3.6, ey + 9.0, ez + 3.0)]
                for p0, p1 in zip(pts, pts[1:]):
                    rod(m, hd, p0, p1, 1, solid(P, "red"), extend=0.4, t2=2)
                spike(m, hd, (sx * 2.4, ey + 6.0, ez + 3.0), (-sx * 0.6, 1, 0), 0.8, 2.6, solid(P, "red"))
            else:                                                                  # tall pink crest horns
                for j in range(2):
                    spike(m, hd, (sx * 1.6, ey + 2.0, ez + 2.0 + j * 2.0), (sx * 0.3, 1, 0.6), 1.4, 8.0 - j * 2,
                          gem(P, "pink", "pink_light", glow=False), tip=0.3)
        if x:
            for sx in (-1, 1):                                                     # gold X on the brow
                rod(m, hd, (sx * 1.2, ey + 2.4, ez - 1.0), (-sx * 1.2, ey + 0.4, ez - 1.0), 1, solid(P, "gold"),
                    extend=0)
            m.box(bd, -1.0, 15.0, -6.0, 1.0, 17.4, -5.2, gem(P, "pink", "pink_light"))
        for side in (1, -1):                                                       # red bat wings
            wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 2.4, 17.0, 3.0))
            bat_wing(m, wb, (side * 2.4, 17.0, 3.0), 9.0 if not x else 14.0, 9.0 if not x else 12.0, 3,
                     solid(P, "red_dark"), cutout(lambda *a_: True, wingf), side=side, sweep=25)
        return m
    return build
