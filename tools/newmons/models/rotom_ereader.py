"""E-Reader Rotom (Electric/Psychic), after the user's Rotom doodle sheet (artist not named): Rotom inside an
e-reader. An orange tablet with pink lens eyes in its top bezel and a pale e-ink screen showing "Chapter 6" and lines
of text, propped on a pink hardback book with white page edges.

Front is -z, y is up. 22 units tall; about 0.8 blocks.
"""
from __future__ import annotations

from _boxmodel import Model
from _rotomform import palette, rotom_eye, solid
from _route import tone

P = palette({"aura": (240, 120, 200), "aura_light": (255, 220, 245), "iris": (240, 120, 200), "ink": (210, 212, 204),
             "book": (230, 110, 170)}, {"book": (110, 170, 240)})
HEIGHT = 22
SCALE = round(0.8 * 16 / HEIGHT, 3)
HITBOX = [0.8, HEIGHT / 16]
KIND = "floater"
K = 4
LOOK = "an orange e-reader with pink lens eyes in its bezel and \"Chapter 6\" on its e-ink screen, on a pink book"


def tablet(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = rotom_eye(x - 2.4 * sx, y - 19.4, 1.2, p)
            if e:
                return e
        if abs(x) <= 4.8 and 6 <= y <= 17.2:
            if 15.2 <= y <= 16.4 and abs(x) <= 3.2:
                return (p["charcoal"] if int((x + 3.2) * 2.5) % 3 else p["ink"]), None   # "Chapter 6"
            if (y - 6.6) % 1.6 < 0.5 and y < 14.2 and abs(x) <= (4.2 if int(y) % 3 else 3.0):
                return p["grey_dark"], None                 # lines of text
            return p["ink"], None
    return tone(p["orange"], face), None


def book(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("north", "east") and 0.8 < y < 3.4 and (face == "east" or abs(x) < 6.6):
        return (p["white"] if int(y * 3) % 2 else p["grey_light"]), None                # page edges
    return tone(p["book"], face), None


def build() -> Model:
    m = Model("rotom_ereader")
    top = m.bone("rotom_ereader", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.box(bd, -7.5, 0, -5, 7.5, 4.2, 5, book)                                         # the pink book
    m.box(bd, -6, 4.2, -0.8, 6, 21.5, 1.2, tablet, rotation=(-10, 0, 0), pivot=(0, 4.2, 0))   # the e-reader
    return m
