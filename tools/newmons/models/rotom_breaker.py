"""Breaker Rotom (Electric/Ground), after the user's Rotom doodle sheet (artist not named): Rotom inside a fuse box.
A tall orange metal cabinet, its door swung open with Rotom's face on it (lens eyes, a wide grin), showing a grey
panel full of breaker switches; yellow lightning crackles round it.

Front is -z, y is up. 22 units tall; about 1.1 blocks.
"""
from __future__ import annotations

from _boxmodel import Model
from _rotomform import bolt_plane, face_on, palette, solid
from _route import tone

P = palette({"aura": (250, 220, 60), "aura_light": (255, 250, 200), "panel": (120, 124, 134)})
HEIGHT = 22
SCALE = round(1.1 * 16 / HEIGHT, 3)
HITBOX = [0.9, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "an orange fuse-box cabinet whose open door carries Rotom's grinning face, full of breaker switches"


def panel(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        if abs(x) <= 4.2 and 2 <= y <= 19:
            row = int((y - 2) // 2.4)
            fy = (y - 2) % 2.4
            col = int((x + 4.2) // 1.4)
            if 0.4 < fy < 1.8 and abs((x + 4.2) % 1.4 - 0.7) < 0.45:
                return (p["grey_light"] if (row + col) % 3 else p["black"]), None   # breaker switches
            return p["panel"], None
    return tone(p["orange"], face), None


def build() -> Model:
    m = Model("rotom_breaker")
    top = m.bone("rotom_breaker", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.box(bd, -5.5, 0, -2, 5.5, 21, 2.5, panel)                           # the cabinet and its panel
    m.box(bd, -6, 21, -2.5, 6, 22, 3, solid(P, "orange_dark"))
    hd = m.bone("head", bd, (5.5, 0, -2))                                 # the door swung open to the right,
    m.box(hd, -5.5, 0, -2.6, 5.5, 21, -2, face_on(P, (0, 12, -2.0), eyes=[(-2.4, 2.0, 1.7), (2.4, 2.0, 1.7)],
                                                  mouth=(0, -1.4, 5.0, 1.6, 6), plane="south"),
          rotation=(0, -140, 0), pivot=(5.5, 0, -2))                     # Rotom's face on its inner side
    for x, y, z, w, h, pl, fl in [(7, 12, -1, 5, 8, "xy", True), (6.5, 2, 2, 4, 6, "zy", False), (-14, 15, -6, 4, 6, "xy", False)]:
        bolt_plane(m, bd, x, y, z, w, h, P, plane=pl, flip=fl)
    return m
