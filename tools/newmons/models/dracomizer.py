"""Dracomizer, the Drake Fossil Pokémon (Dragon; the art the user shared, name kept): the Fossilized Drake as it really
was, a heavy four-legged dragon: dark green hide striped with red, a rough red back studded with rows of tall salmon
plates down to the tip of its tail, a small blunt head with a red brow crest and a wide mouth, and stubby legs with
pink claws.

Shiny: teal hide with gold plates.

Front is -z, y is up. 20 units tall; baseScale 1.0 (1.8 m long).
"""
from __future__ import annotations

from _boxmodel import Model, chain, rod, spike
from _purefossil import body_along, eye_at, palette, plates, toned
from _route import tone

BASE = {"green": (36, 112, 84), "green_dark": (24, 76, 60), "red": (206, 52, 72), "red_dark": (150, 34, 54),
        "plate": (242, 132, 150), "claw": (236, 150, 160), "belly": (60, 140, 104), "eye": (40, 40, 40),
        "pupil": (20, 20, 20), "white": (250, 250, 250), "mouth": (150, 40, 60)}
SHINY = {"green": (40, 140, 150), "green_dark": (24, 96, 104), "red": (230, 170, 50), "red_dark": (180, 120, 30),
         "plate": (252, 214, 110), "claw": (252, 220, 140)}
P, solid, ramp = palette(BASE, SHINY)
SCALE = 1.0
HITBOX = [1.6, 1.25]
KIND = "quadruped"
K = 3
HEIGHT = 20
LOOK = ("a heavy four-legged dragon with dark green hide striped red, rows of tall salmon plates down its back and tail, "
        "a small blunt head with a red brow crest and pink claws")


def hide(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up" or y > 11.8:
        return tone(p["red"], face), None                              # the rough red back
    if face in ("east", "west") and abs(((z + 30) * 0.42) % 2 - 1) < 0.28 and y > 7:
        return tone(p["red_dark"], face), None                         # red stripes down its flanks
    if face == "down":
        return tone(p["belly"], face), None
    return tone(p["green"], face), None


def head(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        e = eye_at(p, z + 10.6, y - 10.6, 0.6)
        if e:
            return e, None
    if face == "up" or y > 11.4:
        return tone(p["red"], face), None
    if face == "north" and y < 9.0:
        return tone(p["mouth"], face), None
    return tone(p["green"], face), None


def build() -> Model:
    m = Model("dracomizer")
    top = m.bone("dracomizer", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 0))
    body_along(m, bd, [(-6, -2, 9.2, 3.4, 3.0), (-2, 4, 9.6, 4.0, 3.4), (4, 8, 9.2, 3.6, 3.0)], hide)
    plates(m, bd, [(0, 12.4, z, h, -0.15) for z, h in ((-5, 3.4), (-2.6, 4.4), (0, 5.2), (2.4, 5.0), (4.8, 4.0), (7.0, 3.0))],
           solid("plate"), w=1.8)
    for sx in (-1, 1):                                                  # smaller plates down its flanks
        plates(m, bd, [(sx * 3.2, 11.2, z, 2.4, 0) for z in (-3.6, 0.0, 3.6)], solid("plate"), w=1.2)
    hd = m.bone("head", bd, (0, 10, -6))
    body_along(m, hd, [(-11.0, -6.0, 10.0, 2.2, 1.8)], head)                          # the small blunt head
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.6, 11.6, -8.6), (sx * 0.6, 1, 0.6), 1.2, 1.8, solid("red"), tip=0.5)   # brow crest
    tl = m.bone("tail", bd, (0, 9, 8))
    chain(m, tl, [(0, 9.2, 7.6), (0, 9.6, 12.0), (0, 10.4, 16.0), (0, 11.4, 19.4)], [4.4, 3.4, 2.2], hide)
    plates(m, tl, [(0, 11.4, 10.0, 3.2, 0.3), (0, 11.6, 13.4, 2.8, 0.3), (0, 12.4, 16.6, 2.2, 0.3)], solid("plate"), w=1.4)
    for i, (lz, nm) in enumerate(((-4.0, "front"), (4.4, "back"))):
        for sx, side in ((1, "left"), (-1, "right")):
            lg = m.bone(f"leg_{nm}_{side}", top, (sx * 3.2, 7.5, lz))
            rod(m, lg, (sx * 3.2, 7.6, lz), (sx * 3.6, 1.4, lz - 0.4), 2.6, toned(P, "green_dark"))
            m.round_box(lg, sx * 3.6, lz - 0.8, 1.6, 1.8, 0, 1.6, toned(P, "green_dark"), cut=0.5)
            for dx in (-0.8, 0.0, 0.8):
                spike(m, lg, (sx * 3.6 + dx, 0.5, lz - 2.4), (0, -0.2, -1), 0.7, 1.0, solid("claw"))
    return m
