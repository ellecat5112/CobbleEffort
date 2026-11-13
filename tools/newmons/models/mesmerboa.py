"""Mesmerboa, the Hypnosis Mouse Pokémon (Electric/Psychic), built from boxes after a design by NyonTox (used with
permission) and the user's idea.

Jerbolt grown into a big-eared jerboa floating calmly: a round head with a gentle smile, dark eyes, a little blue
nose and yellow cheek pads, two huge long ears, white inside and rimmed in red, a pear-shaped body with a pale belly,
tiny red-brown paws and big feet, and a tail so long it curls into a great hypnotic ring all round it, banded yellow
and violet, with a big zigzag lightning-bolt flag at its end, turning without end.

Front is -z, y is up. Floats; 38 units tall with its ring; baseScale 0.3 (0.7 m to the tips of its ears).
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _jerboa import P, bolt_points, bolt_shader, fur, red, ring
from _route import dot_eye, tone

SCALE = 0.3
HITBOX = [2.33, 2.67]
KIND = "floater"
K = 5
HEIGHT = 38
LOOK = ("a floating big-eared yellow jerboa with a gentle smile, huge red-rimmed white ears and a tail curled into "
        "a great turning yellow-and-violet ring round it, ending in a big zigzag lightning bolt")

CY = 17


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = dot_eye(x - sx * 1.6, y - 20.3, 0.55, 0.65)
            if e:
                return e
            if ((x - sx * 3.0) / 1.0) ** 2 + ((y - 18.6) / 0.9) ** 2 < 1:
                return p["cheek"], None
        if abs(y - 18.4 + 0.25 * x * x) < 0.18 and abs(x) < 1.0:            # a gentle smile
            return p["outline"], None
        if abs(x) < 0.55 - (19.6 - y) * 0.5 and 19.0 < y < 19.6:
            return p["nose"], None
    return fur()(x, y, z, face, variant)


def ear(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "south") and box is not None:
        u = (x - box.lo[0]) / max(box.size[0], 1e-6)
        if 0.18 < u < 0.82 and y < box.lo[1] + box.size[1] - 0.8:
            return p["white"], None
    return tone(p["red"], face), None


def build() -> Model:
    m = Model("mesmerboa")
    top = m.bone("mesmerboa", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    m.round_box(bd, 0, 0.5, 4, 3.5, 11, 18, fur(belly_y=15), cut=2)       # pear-shaped body
    hd = m.bone("head", bd, (0, 18, -0.5))
    m.round_box(hd, 0, -0.5, 4.5, 3.5, 17, 23, headf, cut=2)
    for sx in (-1, 1):                                                       # little horn tufts and huge ears
        m.box(hd, sx * 2.6 - 0.5, 22.8, -1.5, sx * 2.6 + 0.5, 24.2, -0.5, fur())
        x0, x1 = sorted((sx * 0.8, sx * 3.8))
        m.box(hd, x0, 22.5, -0.5, x1, 34, -0.5, ear, rotation=(-8, 0, sx * 20), pivot=(sx * 2.3, 22.5, -0.5))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        a = m.bone(nm, bd, (sx * 3, 15, -2.5))
        m.box(a, sx * 3 - 0.8, 13, -4.5, sx * 3 + 0.8, 15, -2.5, red)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 2.5, 12, 0))
        m.box(lg, sx * 2.5 - 1.2, 9.5, -3.5, sx * 2.5 + 1.2, 11, 1.5, red)  # big feet
    rod(m, bd, (0, 12.5, 3.5), (0, 9.5, 6.5), 1.4, fur())                    # the tail leaving its rump
    rg = m.bone("ring", bd, (0, CY, 6.5))
    ring(m, rg, 0, CY, 6.5, 15, 2.2, 1.2, n=28)
    pts = bolt_points(9.4, CY + 10.6, 2.6)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    m.box(rg, min(xs), min(ys), 6.5, max(xs), max(ys), 6.5, bolt_shader(pts))   # the big zigzag bolt
    return m
