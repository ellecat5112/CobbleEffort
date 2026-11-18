"""Shared builder for Lady Devimon and Lady Devimon (X-Antibody) (CobbleEffort: Digital; hand-built at the detail
standard after the official art on wikimon.net): the fallen angel lady: a tall figure fully covered in a black leather
bodysuit bound with silver chains and buckles, a black hood-mask with red eyes, long white hair, a skull clasp, a long
tattered black cape-wing and one great clawed arm wreathed in shadow. X-Antibody: a grinning horned black shadow-
familiar above her head, a mechanical arm ending in a camera-eye and golden claws, and grey tattered wings. Built as
officially drawn, fully clothed. Shiny: deep violet.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import cutout, gem, leather, local, metal, noise2, skin, solid, strands
from _route import pal, tone

BASE = {"black": (40, 40, 46), "black_dark": (12, 12, 16), "black_light": (110, 110, 124), "silver": (210, 214, 224),
        "silver_dark": (100, 104, 116), "white": (240, 240, 246), "white_dark": (170, 172, 190), "red": (220, 30, 40),
        "skull": (240, 236, 226), "gold": (230, 180, 60), "grey": (130, 130, 140), "grey_dark": (60, 60, 70)}
SHINY = {"black": (60, 30, 90), "black_dark": (20, 8, 34), "black_light": (140, 100, 190)}


def P(v):
    return pal(BASE, SHINY, v)


LEATHER = leather(P, "black", "black_dark", stitch="silver")


def chainf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "south") and abs((x * 0.8 + y) % 5.0 - 2.5) < 0.35:
        return tone(p["silver"], face), None
    return LEATHER(x, y, z, face, variant, box=box, **k)


def tatter(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.16 * abs(math.sin(u * 0.9)) + 0.08 * noise2(u, 0.0, 7)


def make(name, x=False):
    def build():
        m = Model(name)
        mats = {"skin": LEATHER, "chest": chainf, "abs": chainf, "pelvis": LEATHER, "neck": LEATHER, "deltoid": LEATHER,
                "upper_arm": chainf, "forearm": LEATHER, "hand": LEATHER, "finger": LEATHER, "claw": solid(P, "red"),
                "thigh": chainf, "knee": metal(P, "silver", dark="silver_dark"), "shin": LEATHER, "calf": LEATHER,
                "foot": LEATHER, "toe": solid(P, "red")}
        a = humanoid(m, mats, bulk=0.75, arm_bulk=0.8, leg_bulk=0.85, claws=True, name=name)
        bd = a["body"]
        m.round_box(bd, 0, -3.0, 1.2, 0.5, 31.0, 33.4, solid(P, "skull"), cut=0)        # skull clasp
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 60.4, LEATHER, cut=1)
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.6, sx * 1.8), 57.4, -2.9, max(sx * 0.6, sx * 1.8), 58.0, -2.8, solid(P, "red", glow=True))
        for i in range(9):                                                         # long white hair
            ang = math.radians(-100 + i * 25)
            rod(m, hd, (2.2 * math.sin(ang), 60.0, 0.8 + 1.2 * math.cos(ang)), (3.2 * math.sin(ang), 38.0, 3.6), 1,
                strands(P, "white", "white_dark"), extend=0.3, t2=2)
        cape(m, bd, 53.0, 16.0, 46.0, cutout(tatter, leather(P, "black" if not x else "grey", "black_dark")), z=4.0,
             flare=1.0, panels=8, sweep=(0.0, 4.0))
        hl = a["arm_left"]                                                          # great clawed arm
        lx, ly, lz = hl["hand"]
        if not x:
            m.round_box(hl["bone"], lx, lz, 2.4, 2.4, ly - 4.0, ly + 1.0, LEATHER, cut=1)
            for j in range(4):
                spike(m, hl["bone"], (lx + (j - 1.5) * 1.1, ly - 4.0, lz - 1.0), (0, -1, -0.2), 0.9, 6.0, solid(P, "red"),
                      tip=0.8)
        else:                                                                       # camera-eye mechanical arm
            m.round_box(hl["bone"], lx + 2.0, lz, 3.4, 3.4, ly - 6.0, ly + 2.0, metal(P, "grey", dark="grey_dark"), cut=2)
            m.round_box(hl["bone"], lx + 2.0, lz - 3.6, 1.8, 0.4, ly - 3.6, ly - 0.4, gem(P, "red", "white"), cut=0)
            for j in range(4):
                spike(m, hl["bone"], (lx + 2.0 + (j - 1.5) * 1.4, ly - 6.0, lz), (0, -1, -0.3), 0.9, 7.0, metal(P, "gold", dark="black"),
                      tip=0.8)
            fb = m.bone("familiar", hd, (0, 66, 2))                                  # horned shadow familiar
            ball(m, fb, (0, 68.0, 2.0), 4.0, skin(P, "black", dark="black_dark"), layers=3)
            m.box(fb, -2.0, 67.4, -2.1, 2.0, 68.0, -1.9, solid(P, "white"))
            for sx in (-1, 1):
                m.box(fb, min(sx * 0.6, sx * 1.8), 69.0, -2.1, max(sx * 0.6, sx * 1.8), 70.0, -1.9, solid(P, "red", glow=True))
                pts = [(sx * 3.0, 70.0, 2.0), (sx * 6.0, 73.0, 2.0), (sx * 5.0, 76.0, 2.0)]
                for p0, p1 in zip(pts, pts[1:]):
                    rod(m, fb, p0, p1, 1, skin(P, "black", dark="black_dark"), extend=0.3, t2=2)
        return m

    return build
