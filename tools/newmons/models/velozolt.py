"""Velozolt, the Bird Fossil Pokémon (Electric; the art the user shared, name kept): the Fossilized Bird as it really was,
a lean yellow raptor that runs on two clawed legs: a crown of jagged electric feather spikes, a beaked head with red
cheeks, feathered arms with spiky plumes, and a long tail ending in a glowing lightning-bolt plume.

Shiny: white feathers with a sky-blue crest.

Front is -z, y is up. 22 units tall; baseScale 0.75 (1.6 m).
"""
from __future__ import annotations

from _boxmodel import Model, chain, rod, spike
from _purefossil import body_along, eye_at, palette, toned
from _route import tone

BASE = {"yellow": (250, 226, 60), "yellow_dark": (214, 182, 40), "spark": (255, 250, 170), "cheek": (230, 70, 60),
        "beak": (232, 208, 60), "claw": (180, 150, 40), "eye": (40, 40, 40), "pupil": (20, 20, 20),
        "white": (250, 250, 250), "mouth": (200, 70, 80)}
SHINY = {"yellow": (240, 244, 250), "yellow_dark": (196, 206, 222), "spark": (150, 220, 255), "beak": (220, 226, 236)}
P, solid, ramp = palette(BASE, SHINY)
SCALE = 0.75
HITBOX = [1.0, 1.4]
KIND = "biped"
K = 3
HEIGHT = 22
LOOK = ("a lean yellow raptor with a crown of jagged electric feather spikes, red cheeks, spiky plumed arms and a "
        "long tail ending in a glowing lightning-bolt plume")


def body(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["yellow"] if face != "down" else p["yellow_dark"], face), None


def head(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        e = eye_at(p, z + 6.6, y - 17.6, 0.55)
        if e:
            return e, None
        if abs(z + 7.6) < 0.7 and abs(y - 16.6) < 0.5:
            return p["cheek"], None
    return tone(p["yellow"], face), None


def spark(x, y, z, face, variant, **k):
    c = P(variant)["spark"]
    return c, c


def build() -> Model:
    m = Model("velozolt")
    top = m.bone("velozolt", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    body_along(m, bd, [(-3.5, 3.5, 11.0, 2.4, 2.8)], body)                        # a lean body, leaning forward
    rod(m, bd, (0, 12.6, -3.0), (0, 16.4, -5.8), 1.8, body)                       # the long neck
    hd = m.bone("head", bd, (0, 16.5, -6))
    body_along(m, hd, [(-8.2, -4.6, 17.4, 1.5, 1.4)], head)
    spike(m, hd, (0, 16.6, -8.0), (0, -0.4, -1), 1.4, 2.2, solid("beak"), tip=0.6)   # the beak
    for i, (dx, dy, dz) in enumerate(((0, 1, 0.6), (0.7, 0.8, 0.9), (-0.7, 0.8, 0.9), (0.3, 0.5, 1), (-0.3, 0.5, 1))):
        spike(m, hd, (dx * 0.8, 18.4, -6.0 + i * 0.3), (dx, dy, dz), 1.2, 3.2 - i * 0.2, spark, tip=0.5)   # spiky crown
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        a = m.bone(nm, bd, (sx * 2.2, 12.4, -2))
        rod(m, a, (sx * 2.2, 12.4, -2.0), (sx * 3.2, 9.8, -4.4), 1.2, body)
        for i in range(3):                                                         # spiky feather plumes
            spike(m, a, (sx * 2.8, 11.6 - i * 0.6, -2.4), (sx * 0.9, 0.3, 0.6), 1.0, 2.6, spark, tip=0.4)
        spike(m, a, (sx * 3.2, 9.8, -4.4), (0, -1, -0.6), 0.7, 1.2, solid("claw"))
    tl = m.bone("tail", bd, (0, 11, 3.5))
    chain(m, tl, [(0, 11.0, 3.4), (0, 11.6, 8.0), (0, 12.4, 12.4), (0, 13.6, 16.0)], [2.2, 1.6, 1.0], body)
    for i, d in enumerate(((0.0, 0.6, 1.0), (0.5, 0.2, 1.0), (-0.5, 0.2, 1.0), (0.0, -0.4, 1.0))):   # lightning plume
        spike(m, tl, (0, 13.6, 16.0), d, 1.2, 3.6 - 0.4 * i, spark, tip=0.5)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8, 9.2, 1))
        rod(m, lg, (sx * 1.8, 9.4, 1.0), (sx * 2.2, 5.0, 2.4), 2.0, body)          # thighs
        rod(m, lg, (sx * 2.2, 5.0, 2.4), (sx * 2.2, 1.0, 0.6), 1.2, toned(P, "yellow_dark"))   # shanks
        for dx in (-0.6, 0.0, 0.6):
            spike(m, lg, (sx * 2.2 + dx, 0.4, 0.4), (dx * 0.4, -0.1, -1), 0.6, 1.8, solid("claw"))
    return m
