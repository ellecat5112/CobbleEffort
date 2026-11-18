"""Shared builder for Kuwagamon and Kuwagamon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the red stag beetle: a scarlet armoured insect with two huge serrated pincers rising from its head, a
gaping fanged maw, black tiger stripes on its carapace, four clawed arms, two digitigrade legs and two pairs of veined
wings. X-Antibody: a more upright, slimmer red insect with longer straight pincers, a wider purple maw and more limbs.
Shiny: green.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digidetail import armour, cutout, local, solid
from _route import pal, tone

BASE = {"red": (210, 50, 40), "red_dark": (120, 14, 10), "red_light": (250, 140, 120), "black": (30, 20, 20),
        "mouth": (120, 40, 110), "tooth": (250, 246, 230), "wing": (210, 225, 245, 150), "wing_vein": (140, 150, 190, 210),
        "steel": (130, 134, 146), "eye": (250, 220, 60)}
SHINY = {"red": (70, 170, 60), "red_dark": (20, 90, 20), "red_light": (160, 230, 140)}


def P(v):
    return pal(BASE, SHINY, v)


def wing_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6), v / max(H, 1e-6) - 0.5
    return abs(b) < 0.5 * math.sqrt(max(0.0, 1 - a * a)) + 0.02


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return (p["wing_vein"] if (u % 3.0) < 0.3 else p["wing"]), None


def make(name, x=False):
    def shellf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if not x and face in ("north", "up") and abs(math.sin(xx * 0.9 + y * 0.4)) > 0.92:
            return tone(p["black"], face), None
        return armour(P, "red", "red_dark", light="red_light")(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 16, 0))
        m.round_box(bd, 0, 1.0, 6.0 if not x else 4.6, 5.0, 16.0, 30.0, shellf, cut=2)
        hd = m.bone("head", bd, (0, 30, -3))
        m.round_box(hd, 0, -3.0, 4.0, 3.4, 26.0, 34.0, shellf, cut=1)
        m.round_box(hd, 0, -6.4, 2.6, 0.4, 27.0, 31.0, solid(P, "mouth"), cut=0)
        for sx in (-1, 1):
            for j in range(3):
                spike(m, hd, (sx * (0.6 + j * 0.8), 31.0, -6.4), (0, -1, -0.3), 0.8, 1.6, solid(P, "tooth"), tip=0.8)
            m.box(hd, min(sx * 2.6, sx * 3.6), 32.0, -5.6, max(sx * 2.6, sx * 3.6), 33.0, -5.4, solid(P, "eye", glow=True))
            pts = ([(sx * 2.4, 33.6, -2.0), (sx * 7.0, 40.0, -3.0), (sx * 5.0, 48.0, -2.0), (sx * 2.0, 50.0, -1.0)] if not x
                   else [(sx * 2.0, 33.6, -2.0), (sx * 4.0, 42.0, -2.0), (sx * 3.6, 52.0, -2.0)])    # huge pincers
            for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
                rod(m, hd, p0, p1, 2 if j == 0 else 1, shellf, extend=0.4, t2=2)
                spike(m, hd, p1, (-sx, 0.3, 0), 0.9, 2.0, shellf, tip=0.8)
        for side in (1, -1):                                                         # veined wings
            wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 2.0, 30.0, 4.0))
            for j, (ln, rz) in enumerate(((22.0, 55), (18.0, 30))):
                x0, x1 = sorted((side * 2.0, side * (2.0 + ln)))
                m.box(wb, x0, 27.0, 5.0 + j, x1, 33.0, 5.0 + j, cutout(wing_in, wingf),
                      rotation=(0, side * -20, side * rz), pivot=(side * 2.0, 30.0, 5.0 + j))
        for row, (y0, nm) in enumerate(((27.0, "arm"), (22.0, "arm2"))):            # four clawed arms
            for sx in (-1, 1):
                ab = m.bone("%s_%s" % (nm, "left" if sx > 0 else "right"), bd, (sx * 5.6, y0, -1.0))
                el = (sx * 11.0, y0 + 1.0, -4.0)
                hand = (sx * 12.0, y0 - 6.0, -7.0)
                rod(m, ab, (sx * 5.6, y0, -1.0), el, 1, shellf, extend=0.4, t2=2)
                rod(m, ab, el, hand, 1, shellf, extend=0.4, t2=2)
                for j in range(3):
                    spike(m, ab, hand, (sx * 0.3 + (j - 1) * 0.4, -1, -0.5), 0.9, 3.4, shellf, tip=0.8)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                          # digitigrade legs
            lg = m.bone(nm, bd, (sx * 3.6, 16.0, 1.0))
            kn = (sx * 6.0, 9.0, -3.0)
            rod(m, lg, (sx * 3.6, 16.0, 1.0), kn, 2, shellf, extend=0.6)
            rod(m, lg, kn, (sx * 6.0, 1.0, 2.0), 1, shellf, extend=0.4, t2=2)
            for j in range(3):
                spike(m, lg, (sx * 6.0, 0.8, 1.6), ((j - 1) * 0.5, -0.1, -1), 1.0, 3.6, shellf, tip=0.8)
        return m

    return build
