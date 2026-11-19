"""Toaster Rotom (Electric/Fire), after the user's Rotom doodle sheet (artist not named): Rotom inside a toaster. A
rounded orange toaster with Rotom's face on the front (lens eyes, a cheeky grin), two dark slots on top with slices
of toast popping out, a black lever on its side, and pink plasma flickering round the toast.

Front is -z, y is up. 18 units tall; about 0.8 blocks.
"""
from __future__ import annotations

from _boxmodel import Model
from _rotomform import bolt_plane, face_on, palette, solid
from _route import tone

P = palette({"aura": (240, 110, 170), "aura_light": (255, 210, 230), "toast": (230, 190, 120), "crust": (160, 100, 50)})
HEIGHT = 18
SCALE = round(0.8 * 16 / HEIGHT, 3)
HITBOX = [0.9, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "a rounded orange toaster with a cheeky face and two slices of toast popping out"


def toast(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    x0, y0, z0 = box.lo
    w, h, d = box.size
    edge = min(x - x0, x0 + w - x, y - y0, y0 + h - y) if face in ("north", "south") else 9
    return tone(p["crust"] if edge < 0.8 or face not in ("north", "south") else p["toast"], face), None


def top(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up" and abs(z) <= 1.2 and (1.0 <= abs(x) <= 4.4):
        return p["black"], None
    return tone(p["orange"], face), None


def build() -> Model:
    m = Model("rotom_toaster")
    root = m.bone("rotom_toaster", None, (0, 0, 0))
    bd = m.bone("body", root, (0, 6, 0))
    m.round_box(bd, 0, 0, 6, 4, 0, 10, face_on(P, (0, 5, -4), eyes=[(-2.4, 1.2, 1.5), (2.4, 1.2, 1.5)],
                                               mouth=(0, -1.6, 3.4, 1.2, 4)), cut=1.4)
    m.round_box(bd, 0, 0, 6, 4, 10, 11, top, cut=1.4)
    for sx in (-1, 1):                                                    # two slices of toast popping out
        m.box(bd, 2.7 * sx - 1.8, 9, -0.7, 2.7 * sx + 1.8, 15.5 + (0.8 if sx > 0 else 0), 0.7, toast)
    m.box(bd, 6, 5, -1, 7.4, 6.4, 1, solid(P, "black"))                  # the lever
    for x, y, z, w, h, pl, fl in [(-9, 9, -1, 4, 6, "xy", False), (6, 11, -1, 4, 6, "xy", True)]:
        bolt_plane(m, bd, x, y, z, w, h, P, plane=pl, flip=fl)
    return m
