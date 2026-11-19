"""Shared builder for Shakomon and Shakomon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a giant clam. Shakomon: a pink-and-black clam shell gaping open with fanged rims, a pair of yellow eyes
peeking from the upper shell, and a fuzzy green blob of a body sitting inside. X-Antibody: a huge lilac shell like a
helmet marked with magenta flame patterns, small spikes along its ridge, a big green frog-like face with yellow eyes
peering out, and a steel clamp at its hinge. Shiny: blue / gold.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import armour, fur, metal, skin, solid
from _route import pal, tone


def make(name, x=False):
    base = {"pink": (240, 120, 160) if not x else (230, 210, 240), "pink_dark": (40, 30, 40) if not x else (170, 140, 190),
            "magenta": (160, 40, 120), "green": (90, 180, 60), "green_dark": (40, 110, 20), "eye": (250, 220, 40),
            "black": (24, 20, 24), "tooth": (250, 246, 236), "steel": (190, 194, 206), "steel_dark": (100, 104, 118)}
    shiny = {"pink": (90, 150, 230), "pink_dark": (24, 40, 100)} if not x else {"pink": (250, 220, 130),
                                                                               "pink_dark": (190, 150, 60)}

    def P(v):
        return pal(base, shiny, v)

    def shellf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if x and face in ("up", "north", "east", "west") and abs(math.sin(xx * 0.6 + z * 0.4) + math.cos(z * 0.5)) > 1.4:
            return tone(p["magenta"], face), None
        if not x and (xx + z) % 4.0 < 1.4:
            return tone(p["pink_dark"], face), None
        return armour(P, "pink", "pink_dark" if x else "pink")(xx, y, z, face, variant, box=box, **k)

    def facef(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                d = math.hypot(xx - sx * 2.6, y - (6.6 if x else 4.6))
                if d < 0.5:
                    return tone(p["black"], face), None
                if d < 1.2:
                    return tone(p["eye"], face), None
        return (skin(P, "green", dark="green_dark") if x else fur(P, "green", "green_dark", length=1.0))(
            xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 2, 0))
        if not x:
            m.round_box(bd, 0, 0, 6.0, 5.0, 0.0, 3.0, shellf, cut=2)                     # lower shell
            ball(m, bd, (0, 4.6, 0.4), 3.6, facef, layers=3, ry=3.0)                     # fuzzy green blob
            for j in range(6):
                spike(m, bd, (-5.0 + j * 2.0, 3.0, -4.6), (0, 1, 0), 0.8, 1.4, solid(P, "tooth"), tip=0.8)
            sh = m.bone("shell_top", bd, (0, 8, 4))
            m.round_box(sh, 0, 1.0, 6.0, 5.0, 8.0, 11.0, shellf, cut=2)                  # upper shell, propped open
            for sx in (-1, 1):
                ball(m, sh, (sx * 2.4, 11.0, -3.6), 1.2, solid(P, "black"), layers=1)
                m.box(sh, sx * 2.4 - 0.5, 10.6, -4.9, sx * 2.4 + 0.5, 11.4, -4.7, solid(P, "eye"))
            for j in range(6):
                spike(m, sh, (-5.0 + j * 2.0, 8.0, -4.0), (0, -1, 0), 0.8, 1.4, solid(P, "tooth"), tip=0.8)
            return m
        ball(m, bd, (0, 6.0, 0), 7.0, facef, layers=5, ry=5.0)                           # big green face
        for i in range(5):                                                               # helmet shell
            r = 9.0 - i * 1.4
            m.round_box(bd, 0, 1.0 + i * 0.4, r, r, 8.0 + i * 2.0, 10.0 + i * 2.0, shellf, cut=max(1, round(r * 0.35)))
        m.round_box(bd, 0, 1.0, 9.0, 9.0, 0.0, 3.0, shellf, cut=3)
        for j in range(5):
            spike(m, bd, (0, 17.4, -4.0 + j * 2.4), (0, 1, 0.2), 1.0, 2.0, metal(P, "steel"), tip=0.8)
        m.box(bd, 8.4, 4.0, 2.0, 10.4, 9.0, 6.0, metal(P, "steel", dark="steel_dark"))     # hinge clamp
        return m

    return build
