"""Phanturn, the Phantom Lure Pokémon (Ghost/Electric), Lanturn evolved, after the art the user shared (artist and
name not given; the name is ours): a ghostly deep-sea angler. A long blue body hangs down like a tattered cloak behind
a head capped with a golden dome marked with a dark cross. Under the cap, a red slit-pupilled eye and a gaping pink
mouth with white fangs, caged by golden bars like fingers. Two blue fins with pale spots and yellow tips stand up from
its head, a long swept tail fin trails up behind it, ragged pale-blue fins hang at its sides, and thin golden threads
dangle glowing pearls round it, one of them a little golden ghost-fish with crosses for eyes: its lure.

Shiny: a violet body, silver cap and pearls, green eye.

Front is -z, y is up. 29 units tall to its fin tips; baseScale 0.9 (1.6 m). A floater.
"""
from __future__ import annotations

import math

from _afake import round_eye, solid_of
from _boxmodel import Model, rod, spike
from _route import along, pal, tone

SCALE = 0.9
HITBOX = [1.4, 1.8]
KIND = "floater"
K = 4
HEIGHT = 29
LOOK = ("a ghostly blue deep-sea angler with a golden cross-marked cap, a red eye, a fanged mouth caged by golden bars, "
        "spotted head fins, a swept tail fin and golden threads dangling glowing pearls and a little ghost-fish lure")
L = 3.0                                                                         # everything is lifted off the ground

BASE = {"blue": (78, 118, 200), "blue_dark": (52, 84, 162), "blue_light": (176, 206, 238), "spot": (190, 210, 236),
        "gold": (240, 214, 120), "gold_dark": (196, 162, 70), "gold_light": (252, 238, 184), "cross": (70, 66, 70),
        "eye": (214, 64, 40), "pupil": (30, 20, 20), "white": (250, 250, 246), "mouth": (210, 110, 120),
        "mouth_dark": (150, 60, 76), "pearl": (250, 236, 170), "yellow": (246, 212, 96)}
SHINY = {"blue": (112, 82, 176), "blue_dark": (80, 54, 140), "blue_light": (196, 176, 236), "spot": (210, 196, 240),
         "gold": (220, 224, 236), "gold_dark": (170, 176, 196), "gold_light": (244, 246, 252), "eye": (90, 210, 90),
         "pearl": (236, 242, 255), "yellow": (210, 220, 240)}


def P(v):
    return pal(BASE, SHINY, v)


solid = solid_of(P)


def capf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up" and math.hypot(x, z + 4.0) < 2.4 and (abs(x) < 0.35 or abs(z + 4.0) < 0.35):
        return p["cross"], None                                               # the dark cross on its cap
    return tone(p["gold_light"] if face == "up" else p["gold"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and (x / 2.9) ** 2 + ((y - (11.8 + L)) / 1.9) ** 2 < 1:
        return (p["mouth_dark"] if y < 11.2 + L else p["mouth"]), None        # its gaping mouth
    if face in ("east", "west"):
        e = round_eye(z + 4.6, y - (13.4 + L), 0.85, p, "eye", ry=0.95, iris_frac=0.95, pupil_frac=0.2)
        if e:
            return e, None
    return tone(p["blue"], face), None


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["blue_dark"] if face == "down" else p["blue"], face), None


def head_fin(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = along(z, box)
    if t > 0.84:
        return tone(p["yellow"], face), None
    cx = box.lo[0] + box.size[0] / 2
    if face in ("up", "down") and abs(t - 0.5) < 0.16 and abs(x - cx) < 0.6:
        return p["spot"], None                                                # a pale oval spot
    return tone(p["blue"], face), None


def tail_fin(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["yellow"] if face == "down" else p["blue"], face), None


def pearl(m, bone, c, r):
    m.round_box(bone, c[0], c[2], r, r, c[1] - r, c[1] + r, solid("pearl", glow=True), cut=max(0.6, r * 0.5))


def ghostfish(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - (-12.0 + sx * 0.8), y - (15.2 + L)
            if abs(dx) < 0.45 and abs(dy) < 0.45 and (abs(dx - dy) < 0.16 or abs(dx + dy) < 0.16):
                return p["cross"], None                                       # crosses for eyes
    return p["gold_light"], p["gold_light"]


def build() -> Model:
    m = Model("phanturn")
    top = m.bone("phanturn", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10 + L, 2))
    m.round_box(bd, 0, 1.5, 4.2, 4.2, 6.0 + L, 14.0 + L, bodyf, cut=1.6)         # the cloak-like body
    m.round_box(bd, 0, 3.4, 3.2, 3.0, 2.4 + L, 7.0 + L, bodyf, cut=1.2)
    m.round_box(bd, 0, 5.0, 2.0, 1.8, -1.6 + L, 3.0 + L, bodyf, cut=0.8)
    for sx in (-1, 1):                                                          # ragged pale fins at its sides
        rod(m, bd, (sx * 3.6, 11.0 + L, 1.0), (sx * 7.4, 7.0 + L, 3.6), 3.4, solid("blue_light"), extend=0.3, t2=0.8)
        spike(m, bd, (sx * 6.6, 7.6 + L, 3.2), (sx * 0.6, -1, 0.3), 1.6, 2.6, solid("blue_light"))
    rod(m, bd, (0, 14.0 + L, 5.0), (0, 20.0 + L, 18.0), 3.0, tail_fin, extend=0.4, t2=1.2)   # the swept tail fin
    spike(m, bd, (0, 19.6 + L, 17.2), (0, 0.3, 1), 2.0, 3.0, tail_fin, tip=0.8)

    hd = m.bone("head", bd, (0, 13 + L, -2))
    m.round_box(hd, 0, -3.0, 3.8, 3.6, 9.5 + L, 14.4 + L, headf, cut=1.2)
    m.round_box(hd, 0, -4.0, 4.4, 4.0, 14.0 + L, 19.0 + L, capf, cut=1.6)      # the golden cap
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.4, 10.4 + L, -6.4), (0, 1, -0.3), 1.0, 1.6, solid("white"))   # fangs
        spike(m, hd, (sx * 2.6, 13.4 + L, -6.4), (0, -1, -0.3), 1.0, 1.4, solid("white"))
        rod(m, hd, (sx * 1.5, 18.0 + L, 1.0), (sx * 2.6, 26.0 + L, 4.0), 2.4, head_fin, extend=0.4, t2=1.0)   # head fins
    for x in (-1.8, 0.0, 1.8):                                                  # the golden bars caging its mouth
        rod(m, hd, (x, 14.4 + L, -8.0), (x * 1.1, 9.6 + L, -7.8), 1.0, solid("gold"), extend=0.3)
        rod(m, hd, (x * 1.1, 9.8 + L, -7.8), (x * 1.1, 9.2 + L, -5.6), 1.0, solid("gold_dark"), extend=0.2)

    # golden threads with glowing pearls (and a little ghost-fish lure), on swaying bones
    lures = {
        "lure_left": ([(-3, 10, 0), (-8, 8, -2), (-11, 4, -2), (-9.6, 1.8, -1)], [((-8.4, 1.8, -1), 2.4)]),
        "lure_right": ([(3, 10, 2), (8, 11, 3), (12, 7, 3), (11.6, 3.6, 2)], [((11.2, 1.8, 2), 2.6),
                                                                              ((14.0, 15.6, 4), 1.6)]),
        "lure_fish": ([(-2, 14, 0), (-7, 20, -1), (-11, 21, -1), (-12, 18, -2)], [((-4.5, 4.0, -3), 1.1)]),
    }
    extra = {"lure_right": [(3, 14, 3), (9, 16, 4), (13.2, 15.6, 4)], "lure_fish": [(-1, 8, -2), (-4.2, 5.0, -3)]}
    for name, (pts, pearls) in lures.items():
        b = m.bone(name, bd, (pts[0][0], pts[0][1] + L, pts[0][2]))
        for chain in (pts, extra.get(name, [])):
            for a, c in zip(chain, chain[1:]):
                rod(m, b, (a[0], a[1] + L, a[2]), (c[0], c[1] + L, c[2]), 1.0, solid("gold"), extend=0.4)
        for c, r in pearls:
            pearl(m, b, (c[0], c[1] + L, c[2]), r)
        if name == "lure_fish":                                                 # the little golden ghost-fish
            m.round_box(b, -12.0, -2.0, 1.9, 1.6, 13.4 + L, 16.8 + L, ghostfish, cut=0.6)
            for sx in (-1, 1):
                spike(m, b, (-12.0 + sx * 1.8, 15.8 + L, -2.0), (sx * 1, 0.4, 0), 1.0, 1.4, solid("gold_light", glow=True))
    return m
