"""Shared builder for Whamon and Whamon Perfect (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a colossal blue whale: a deep-blue body rippled with darker waves, a great grey-brown armoured head
like a battering ram, a huge gaping mouth lined with teeth over a red throat, ribbed baleen at the jaw hinge, ragged
fins and a broad fluked tail. Shiny: grey-green."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, slab_z
from _digidetail import metal, skin, solid
from _route import pal, tone

BASE = {"blue": (60, 80, 180), "blue_dark": (24, 34, 100), "head": (120, 110, 100), "head_dark": (60, 54, 48),
        "mouth": (190, 30, 60), "tooth": (250, 240, 200), "baleen": (90, 80, 70), "eye": (250, 220, 60)}
SHINY = {"blue": (90, 140, 120), "blue_dark": (40, 80, 64)}


def make(name):
    def P(v):
        return pal(BASE, SHINY, v)

    def bodyf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face != "down" and abs(math.sin(z * 0.5 + y * 0.6 + x * 0.2)) > 0.92:
            return tone(p["blue_dark"], face), None
        return skin(P, "blue", dark="blue_dark")(x, y, z, face, variant, box=box, **k)

    HEAD = metal(P, "head", dark="head_dark")

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 12, 0))
        for i in range(8):
            z0 = -8.0 + i * 4.0
            r = 8.0 - i * 0.8
            slab_z(m, bd, 0, 12.0 + i * 0.4, z0, z0 + 4.2, r, r * 0.9, bodyf)
        hd = m.bone("head", bd, (0, 12, -8))
        slab_z(m, hd, 0, 14.0, -20.0, -8.0, 8.6, 6.0, HEAD)                               # armoured upper head
        m.box(hd, -7.6, 6.0, -19.6, 7.6, 9.6, -8.0, solid(P, "mouth"))                      # gaping mouth
        jb = m.bone("jaw", hd, (0, 6, -8))
        slab_z(m, jb, 0, 4.4, -19.0, -8.0, 7.0, 2.4, HEAD)
        for j in range(8):
            for sx in (-1, 1):
                spike(m, hd, (sx * 7.0, 8.6, -19.0 + j * 1.4), (0, -1, 0), 1.0, 2.4, solid(P, "tooth"), tip=0.8)
                spike(m, jb, (sx * 6.4, 6.4, -18.4 + j * 1.4), (0, 1, 0), 0.9, 1.8, solid(P, "tooth"), tip=0.8)
        for sx in (-1, 1):
            for j in range(4):
                m.box(hd, min(sx * 7.6, sx * 8.4), 8.0 + j * 1.4, -9.0, max(sx * 7.6, sx * 8.4), 8.8 + j * 1.4, -7.6,
                      solid(P, "baleen"))
            ball(m, hd, (sx * 8.4, 15.0, -12.0), 0.9, solid(P, "eye", glow=True), layers=1)
            fb = m.bone("fin_left" if sx > 0 else "fin_right", bd, (sx * 7.0, 8.0, 0))
            for j in range(3):
                spike(m, fb, (sx * 7.0, 8.0, -2.0 + j * 2.0), (sx, -0.4, 0.5), 1.6, 8.0 - j, bodyf, tip=0.8)
        for j in range(3):
            spike(m, bd, (0, 19.0, 4.0 + j * 4.0), (0, 1, 0.5), 1.2, 3.0, bodyf, tip=0.8)
        tl = m.bone("tail", bd, (0, 14, 24))
        rod(m, tl, (0, 14.0, 24.0), (0, 18.0, 32.0), 3, bodyf, extend=0.6)
        for sx in (-1, 1):
            m.box(tl, min(0, sx * 10.0), 18.0, 31.0, max(0, sx * 10.0), 19.4, 37.0, bodyf, rotation=(0, sx * 20, sx * 10),
                  pivot=(0, 18.6, 33.0))
        return m
    return build
