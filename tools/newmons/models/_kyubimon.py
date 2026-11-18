"""Shared builder for Kyubimon and Kyubimon (Silver) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the nine-tailed fox: a slender golden fox with a white chest ruff and a pointed snout, a red-and-white
twisted rope collar ending in two golden bells, a red rope round each foreleg, and a great fan of nine golden tails
wreathed in ghostly blue foxfire. Silver: grey-white fur with darker tips and red-orange flames. Shiny: rose pink.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import quadruped
from _digidetail import cutout, flame_inside, fur, local, metal, solid, twisted
from _route import pal, tone


def make(name, silver=False):
    base = {"gold": (250, 210, 60) if not silver else (190, 190, 200), "gold_dark": (200, 150, 20) if not silver else (110, 110, 124),
            "white": (250, 248, 240), "white_dark": (200, 196, 186), "red": (220, 40, 40), "bell": (240, 200, 60),
            "bell_dark": (160, 120, 20), "eye": (30, 30, 34), "mouth": (160, 40, 50), "tooth": (250, 250, 246),
            "fire": (130, 150, 255, 200) if not silver else (255, 120, 40, 210),
            "fire_core": (230, 235, 255, 230) if not silver else (255, 230, 150, 240)}
    shiny = {"gold": (250, 170, 200), "gold_dark": (200, 100, 140)}

    def P(v):
        return pal(base, shiny, v)

    FUR = fur(P, "gold", "gold_dark", tip="white" if not silver else "gold_dark", length=1.4)

    def firef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
        return c, c[:3]

    def build():
        m = Model(name)
        mats = {"skin": FUR, "belly": fur(P, "white", "white_dark"), "neck": fur(P, "white", "white_dark"), "head": FUR,
                "snout": FUR, "jaw": fur(P, "white", "white_dark"), "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"),
                "leg_upper": FUR, "leg_lower": FUR, "paw": FUR, "claw": solid(P, "white"), "tail": FUR}
        a = quadruped(m, mats, name, length=24.0, body_y=14.0, body_rx=4.0, body_ry=4.4, chest_bulk=1.3,
                      neck=((0, 18, -10), (0, 22, -13)), head_len=9.0, head_w=3.0, head_h=3.4, snout=1.0, mouth_open=6,
                      teeth=2, leg_bulk=0.9, toes=3, tail=((0, 16, 12), (0, 18, 15)), tail_r=(1.6, 1.4))
        bd, hd = a["body"], a["head"]
        ex, ey, ez = a["eye"]
        hc = a["head_c"]
        for sx in (-1, 1):
            m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3, ez - 0.7, max(sx * ex, sx * (ex + 0.3)), ey + 0.3, ez + 0.7,
                  solid(P, "eye"))
            spike(m, hd, (sx * 1.6, hc[1] + 2.4, hc[2] + 1.4), (sx * 0.3, 1, 0.3), 1.6, 4.0, FUR, tip=0.8)   # ears
        ROPE = twisted(P, "red", "white", period=1.2)
        nk = a["neck"]
        for i in range(10):                                                          # rope collar
            a0, a1 = 2 * math.pi * i / 10, 2 * math.pi * (i + 1) / 10
            rod(m, nk, (3.0 * math.cos(a0), 19.0 + 3.0 * math.sin(a0) * 0.3, -11.0 + 3.0 * math.sin(a0)),
                (3.0 * math.cos(a1), 19.0 + 3.0 * math.sin(a1) * 0.3, -11.0 + 3.0 * math.sin(a1)), 1, ROPE, extend=0.3, t2=1)
        for sx in (-1, 1):                                                           # rope ends + bells
            rod(m, nk, (sx * 2.0, 18.0, -13.6), (sx * 6.0, 15.0, -17.0), 1, ROPE, extend=0.2, t2=1)
            m.round_box(nk, sx * 6.4, -17.4, 1.4, 1.4, 12.0, 15.0, metal(P, "bell", dark="bell_dark"), cut=1)
        tb = a["tail"]                                                               # nine tails + foxfire
        for i in range(9):
            ang = math.radians(-60 + i * 15)
            root = (0, 17.0, 14.0)
            end = (14.0 * math.sin(ang), 24.0 + 6.0 * math.cos(ang), 22.0 + 4.0 * math.cos(ang))
            rod(m, tb, root, end, 2, FUR, extend=0.6)
            if i % 2 == 0:
                for rot in (0, 90):
                    m.box(tb, end[0] - 2.0, end[1], end[2], end[0] + 2.0, end[1] + 6.0, end[2],
                          cutout(flame_inside(3, 0.1, i), firef), rotation=(0, rot, 0), pivot=end)
        return m

    return build
