"""Harvester Rotom (Electric/Bug), after the Joseon Region fakemon art: Rotom inside a tree harvester. A boxy orange
cab with a grey windscreen, two yellow roof lights round a little cone spike, six black wheels, a black front blade,
and a long jointed orange crane arm whose end is Rotom's own head (horn, lens eyes, toothy grin), reaching out to
mulch a tree. Leaf-green plasma crackles round it.

Front is -z, y is up. 27 units tall; about 1.7 blocks.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _rotomform import ball, bolt_plane, cone, face_on, palette, solid, tyre, wheel
from _route import tone

P = palette({"aura": (120, 210, 60), "aura_light": (220, 250, 170), "iris": (200, 230, 90), "glass": (120, 128, 140),
             "lamp": (250, 230, 90)})
HEIGHT = 27
SCALE = round(1.7 * 16 / HEIGHT, 3)
HITBOX = [1.4, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "a boxy orange tree harvester whose long crane arm ends in Rotom's grinning head"


def cab(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and 9 <= y <= 15 and abs(x) <= 5:
        return (p["glass"] if not (abs(x) < 4 and 13.5 < y < 14.5) else p["grey_light"]), None
    if face in ("east", "west") and 10 <= y <= 15 and -4.5 <= z <= 2:
        return p["glass"], None
    return tone(p["orange"], face), None


def build() -> Model:
    m = Model("rotom_harvester")
    top = m.bone("rotom_harvester", None, (0, 0, 0))
    body = m.bone("body", top, (0, 6, 0))
    for sx in (-1, 1):
        for zc in (-3.5, 2.0, 7.5):                        # six wheels
            x0, x1 = (6, 9.5) if sx > 0 else (-9.5, -6)
            tyre(m, body, x0, x1, 3.2, zc, 3.2, wheel(P, centre=(0, 3.2, zc), r=3.2))
    m.box(body, -6, 3, -6, 6, 16, 9, cab)                                              # the cab
    m.box(body, -5.5, 16, -5, 5.5, 17.5, 8, solid(P, "orange_dark"))                   # roof
    for sx in (-1, 1):                                                                 # roof lights
        m.box(body, 3 * sx - 1, 17.5, -4, 3 * sx + 1, 19.2, -2, solid(P, "lamp", glow=True))
    cone(m, body, (0, 17.5, -3), (0, 1, 0), 1.8, 3.0, solid(P, "black"), steps=2)
    m.box(body, -7.5, 0.5, -9, 7.5, 4, -6, solid(P, "black"))                          # the front blade
    arm = m.bone("arm", body, (-4, 10, -7))
    rod(m, arm, (-4, 10, -6.5), (-4, 24, -10), 2.4, solid(P, "orange"))                # the crane arm
    ball(m, arm, -4, 24, -10, 1.8, solid(P, "orange_dark"), slices=2)
    rod(m, arm, (-4, 24, -10), (-3, 21, -18), 2.0, solid(P, "orange"))
    hd = m.bone("head", arm, (-3, 21, -20))
    ball(m, hd, -3, 20.5, -21, 3.6,
         face_on(P, (-3, 20.5, -24.6), eyes=[(-1.4, 0.9, 1.1), (1.4, 0.9, 1.1)], mouth=(0, -1.2, 4.2, 1.6, 5)))
    cone(m, hd, (-3, 23.8, -21), (0, 1, -0.2), 1.8, 3.2, solid(P, "black"), steps=2)
    for x, y, z, w, h, pl, fl in [(-12, 14, -14, 7, 10, "zy", False), (-8, 8, -16, 5, 8, "xy", True), (10, 8, 0, 6, 8, "zy", True)]:
        bolt_plane(m, body, x, y, z, w, h, P, plane=pl, flip=fl)
    return m
