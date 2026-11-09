"""Mega Scream Tail, hand-built from boxes in Cobblemon's style.

Scream Tail (official art: an ancient Jigglypuff, a round pink body, cat-like ears with dark insides, big yellow eyes,
a small fang, rosy cheeks, a big curl of hair on its head that sweeps back into a long pink tail ending in a curl,
little wisps at its sides) as a punk-rock mega (Punk Rock): the head curl becomes a tall swooshing crest streaked
with magenta, a fluffy collar, star-shaped cheek marks, and a longer tail ending in a big fluffy curl.

Front is -z, y is up. ~30 units tall; baseScale 1.05 (about 2 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, mix

SCALE = 1.05
HITBOX = [1.5, 2.0]
LOOK = "punk rock: a tall swooshing crest streaked with magenta, star cheek marks, big yellow eyes and a fang, a fluffy collar and a long tail ending in a big curl"
KIND = "biped"

BASE = {
    "pink": (250, 196, 206), "pink_light": (255, 218, 226), "pink_shade": (236, 172, 186),
    "hair": (244, 150, 176), "hair_dark": (226, 100, 140), "streak": (200, 50, 120),
    "ear_in": (60, 50, 60), "eye": (250, 210, 50), "eye_dark": (200, 150, 30), "pupil": (40, 30, 30), "shine": (255, 255, 255),
    "cheek": (250, 130, 160), "star": (255, 240, 120), "mouth": (130, 50, 70), "fang": (255, 255, 255),
    "collar": (255, 236, 242), "collar_shade": (240, 210, 222), "foot": (236, 170, 186),
}
SHINY = {"pink": (232, 214, 250), "pink_light": (244, 232, 255), "pink_shade": (212, 192, 238),
         "hair": (170, 150, 240), "hair_dark": (130, 110, 220), "streak": (80, 200, 220), "cheek": (200, 150, 240),
         "foot": (200, 180, 236)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def body(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "down":
        return P["pink_shade"]
    return P["pink_light"] if face == "up" else P["pink"]


EYES = (10.0, 15.0)


def face(x, y, z, face, variant, **k):
    """The front: huge yellow eyes with a highlight, star cheeks, a small smile with one fang."""
    P = palette(variant)
    if face == "north":
        for side in (-1, 1):
            ex, ey = side * 4.0, 12.5
            dx, dy = x - ex, y - ey
            if abs(dx) <= 2.6 and abs(dy) <= 2.6 and not (abs(dx) > 2.0 and abs(dy) > 2.0):
                if dx * side > 0.4 and dy > 0.8:
                    return P["shine"], (255, 255, 255)
                if abs(dx) <= 1.0 and abs(dy) <= 1.3:
                    return P["pupil"]
                return (P["eye_dark"] if dy < -1.4 else P["eye"]), (P["eye"])
            # star cheek mark
            cx, cy = side * 6.5, 9.0
            if abs(x - cx) + abs(y - cy) * 1.4 < 1.6 or (abs(x - cx) < 0.6 and abs(y - cy) < 1.6):
                return P["star"]
        if 6.5 <= y <= 7.5 and abs(x) < 1.6:
            return P["mouth"]
        if 5.5 <= y < 6.5 and 0.4 < x < 1.4:
            return P["fang"]
    return body(x, y, z, face, variant)


def ear(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "north" and k.get("r", 0) >= 1 and 0 < k.get("c", 0) < k.get("cols", 1) - 1:
        return P["ear_in"]
    return P["pink"]


def hair(x, y, z, face, variant, **k):
    """The crest and tail: pink with magenta streaks running along it."""
    P = palette(variant)
    if int(math.floor(x * 1.0 + y * 0.5 + z * 0.3)) % 7 == 0:
        return P["streak"]
    return P["hair"] if face in ("up", "north", "west") else P["hair_dark"]


def collar(x, y, z, face, variant, **k):
    P = palette(variant)
    if face != "up" and k.get("r", 0) == k.get("rows", 1) - 1 and k.get("c", 0) % 2:
        return (0, 0, 0, 0)                               # a scalloped fluffy edge
    return P["collar"] if face == "up" else P["collar_shade"]


def foot(x, y, z, face, variant, **k):
    return palette(variant)["foot"]


def build() -> Model:
    m = Model("screamtail_mega")
    root = m.bone("screamtail_mega", None, (0, 0, 0))
    bodyb = m.bone("body", root, (0, 10, 0))
    # the round body (rounded with crossed boxes) and its face
    m.round_box(bodyb, 0, 0, 9, 8, 3, 19, face, cut=3)
    m.round_box(bodyb, 0, 0, 8, 7, 19, 21, body, cut=3)
    m.round_box(bodyb, 0, 0, 7, 6, 2, 3, body, cut=2)
    # a fluffy collar round its middle
    m.round_box(bodyb, 0, 0, 10, 9, 4, 6, collar, cut=3)

    head = m.bone("head", bodyb, (0, 19, 0))
    # cat ears with dark insides
    for sgn in (1, -1):
        m.box(head, sgn * 4.5 - 2, 20, -3, sgn * 4.5 + 2, 24, 1, ear)
        m.box(head, sgn * 4.5 - 1, 24, -2, sgn * 4.5 + 1, 25, 0, ear)
    # the punk crest: a tall swoosh rising from the forehead and curling back
    chain(m, head, [(0, 20, -4), (0, 25, -3), (0, 29, 1), (0, 30, 6), (0, 28, 10)], [6, 6, 5, 4], hair)
    chain(m, head, [(0, 21, -2), (0, 26, 0), (0, 28, 4)], [8, 6], hair)
    # little wisps at its sides
    for sgn in (1, -1):
        chain(m, head, [(sgn * 8.5, 16, 0), (sgn * 11, 14, 1), (sgn * 12, 12, 3)], [2, 1.5], hair)

    # arms: little nubs
    for sgn, nm in ((1, "arm_left"), (-1, "arm_right")):
        arm = m.bone(nm, bodyb, (sgn * 8.5, 11, 0))
        m.box(arm, sgn * 8.5 - 1.5, 7, -2, sgn * 8.5 + 1.5, 11, 1, body)
    # feet
    for sgn, nm in ((1, "leg_front_left"), (-1, "leg_front_right")):
        leg = m.bone(nm, root, (sgn * 4, 3, 0))
        m.box(leg, sgn * 4 - 2.5, 0, -4, sgn * 4 + 2.5, 3, 2, foot)

    # the long tail from the back of the crest, ending in a big fluffy curl
    tail = m.bone("tail", bodyb, (0, 12, 7))
    pts = [(0, 14, 7), (0, 11, 13), (0, 8, 19), (0, 7, 25), (0, 9, 30), (0, 13, 32), (0, 16, 30), (0, 16, 26), (0, 13, 25)]
    chain(m, tail, pts, [5, 5, 4, 4, 4, 4, 4, 3], hair)
    return m
