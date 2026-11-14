"""Hornworm, the Hornworm Pokémon (Bug), the Nicodex's Bug type (the user's design): a fat, bright green caterpillar
like the tobacco hornworm that feasts on tobacco leaves, with white diagonal stripes down its sides, little black
eye-spots, stubby prolegs and a curved red horn on its tail end.

Shiny: a rusty brown caterpillar.

Front is -z, y is up. 10 units tall, 26 long; baseScale 0.45 (0.45 m).
"""
from __future__ import annotations

from _boxmodel import Model, spike
from _nico import palette
from _route import tone

SHINY = {"leaf": (170, 100, 60), "leaf_dark": (130, 70, 40), "leaf_light": (210, 150, 100)}
P, solid, ramp = palette(SHINY)
SCALE = 0.45
HITBOX = [0.8, 0.5]
KIND = "quadruped"
K = 5
HEIGHT = 10
LOOK = "a fat bright green tobacco hornworm caterpillar with white diagonal side stripes and a curved red tail horn"


def segf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and abs(((z * 0.9 + y) % 4.0) - 2.0) < 0.35 and y > 2.0:
        return p["white"], None                                               # diagonal stripes
    if face in ("east", "west") and abs(y - 3.0) < 0.5 and (int(z * 10) % 40) < 6:
        return p["pupil"], None                                               # spiracles
    if face == "down":
        return p["leaf_dark"], None
    return tone(p["leaf"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.5) < 0.6 and abs(y - 6.2) < 0.6:
                return p["pupil"], None
        if abs(y - 4.0) < 0.3 and abs(x) < 1.2:
            return p["leaf_dark"], None
    return tone(p["leaf_light"], face), None


def build() -> Model:
    m = Model("hornworm")
    top = m.bone("hornworm", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    for i, (z, r) in enumerate(((-6.0, 3.4), (-2.0, 3.8), (2.0, 3.8), (6.0, 3.4), (10.0, 2.8))):
        m.round_box(bd, 0, z, r, 2.2, 1.0, 1.0 + r * 2.0 - 0.4, segf, cut=1.0)
    hd = m.bone("head", bd, (0, 4, -8))
    m.round_box(hd, 0, -9.6, 2.8, 2.0, 1.6, 8.0, headf, cut=0.8)
    tl = m.bone("tail", bd, (0, 6, 11))
    spike(m, tl, (0, 6.0, 11.6), (0, 1, 0.5), 1.0, 3.6, solid("red"), tip=0.6)  # the curved red horn
    for z in (-6.0, -2.0, 2.0, 6.0):
        for sx in (-1, 1):
            m.box(bd, sx * 2.4 - 0.6, 0.0, z - 0.6, sx * 2.4 + 0.6, 1.2, z + 0.6, solid("leaf_dark"))   # prolegs
    for sx, side in ((-1, "left"), (1, "right")):
        for role, z in (("front", -4.0), ("back", 8.0)):
            lb = m.bone(f"leg_{role}_{side}", top, (sx * 2.6, 1, z))
            m.box(lb, sx * 2.6 - 0.6, 0.0, z - 0.6, sx * 2.6 + 0.6, 1.2, z + 0.6, solid("leaf_dark"))
    return m
