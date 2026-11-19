"""Jetski Rotom (Electric/Dragon), after the Joseon Region fakemon art: Rotom inside a jet ski shaped like a shark.
A long orange hull over a grey keel, a black band across the deck with Rotom's lens eye on each side, a shark's grin
full of white teeth along the pointed nose, a black seat and handlebars, and blue-violet plasma trailing behind.

Front is -z, y is up. 13 units tall, 38 long; about 0.9 blocks tall.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _rotomform import bolt_plane, grin, palette, rotom_eye, solid
from _route import tone

P = palette({"aura": (90, 120, 255), "aura_light": (200, 190, 255), "iris": (226, 120, 210)})
HEIGHT = 13
SCALE = 1.1
HITBOX = [1.6, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "a shark-shaped jet ski with an orange hull, a black band with lens eyes and a toothy shark grin"


def hull(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        u = -z if face == "east" else -z                    # along the hull, nose forward
        e = rotom_eye(z + 6.6, y - 6.2, 1.6, p)            # an eye on the band, both sides
        if e:
            return e
        g = grin(-(z + 16.0) * (1 if face == "west" else -1), y - 5.2, 10.0, 3.2, p, teeth=8)
        if g and z < -10.5:
            return g, None
    if -8.6 <= z <= -4.6 and y > 4.4:                     # the black band over the deck
        return tone(p["black"], face), None
    if y < 3.2:
        return tone(p["grey_light"] if face != "down" else p["grey_dark"], face), None
    return tone(p["orange"], face), None


def build() -> Model:
    m = Model("rotom_jetski")
    top = m.bone("rotom_jetski", None, (0, 0, 0))
    body = m.bone("body", top, (0, 4, 0))
    m.round_box(body, 0, 2, 5.5, 13, 0, 4, solid(P, "grey"), cut=2.5)                 # the keel
    m.round_box(body, 0, 2, 5.5, 13, 3, 8, hull, cut=2.5)                              # the orange hull
    for i, (z0, z1, w, y0, y1) in enumerate([(-16, -11, 4.5, 1.5, 8.5), (-19, -16, 3.2, 2.5, 9), (-21.5, -19, 1.8, 3.8, 9.6)]):
        m.box(body, -w, y0, z0, w, y1, z1, hull)                                       # the pointed shark nose
    m.round_box(body, 0, 1, 3.2, 4.5, 8, 10, solid(P, "black"), cut=1.2)               # seat
    hd = m.bone("head", body, (0, 8, -7))
    rod(m, hd, (0, 8, -6.5), (0, 12, -6), 1.2, solid(P, "black"), extend=0.5)          # handlebar stem
    m.box(hd, -4, 11.5, -7, 4, 12.8, -5.6, solid(P, "black"))                          # handlebars
    m.box(hd, -4.6, 11.3, -7.2, -3.6, 13, -5.4, solid(P, "charcoal"))
    m.box(hd, 3.6, 11.3, -7.2, 4.6, 13, -5.4, solid(P, "charcoal"))
    for x, y, z, w, h, pl, fl in [(-6.5, 3, 8, 7, 9, "zy", False), (6.5, 4, 6, 8, 8, "zy", True), (-3, 6, 16, 6, 7, "xy", False),
                                  (1, 2, 17, 6, 8, "xy", True)]:
        bolt_plane(m, body, x, y, z, w, h, P, plane=pl, flip=fl)
    return m
