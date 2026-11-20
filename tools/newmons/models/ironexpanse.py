"""Iron Expanse (Water/Steel), the future paradox Palkia, built from boxes after the art the user shared (artist and
name not given; our name).

A sleek robot Palkia of white plating banded with violet stripes, its arms, waist and inner thighs dark gunmetal.
Long white blades striped in violet sweep up and back from its shoulders like wings, pearls sit in violet mounts on
its shoulders, and a white crest blade tops its head. Above and behind it floats a halo: a violet eight-pointed star
ringed with white vents round a dark lens full of stars.

Shiny: white plating with teal stripes and a teal halo.

Front is -z, y is up. 76 units tall (to the halo); about 6.0 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _palkia import palkia
from _pgen1 import CLEAR, stars
from _regi import ellipsoid, lit
from _route import mix, pal, tone

HEIGHT = 76
SCALE = round(6.0 * 16 / HEIGHT, 3)
HITBOX = [3.0, 58 / 16]
KIND = "biped"
K = 3
LOOK = ("a sleek white robot Palkia banded in violet with gunmetal arms, long striped wing blades and a floating halo "
        "of a violet star round a dark starry lens")

BASE = {"white": (242, 242, 250), "white_dark": (196, 196, 216), "violet": (150, 70, 164), "violet_light": (204, 128, 206),
        "metal": (92, 92, 106), "metal_dark": (60, 60, 72), "pearl": (236, 170, 236), "eye": (210, 60, 60),
        "lens": (24, 24, 44), "star": (255, 255, 255)}
SHINY = {"violet": (40, 160, 170), "violet_light": (110, 214, 220), "pearl": (160, 236, 236)}
HC = (5.0, 62.0, 7.0)      # the halo's centre


def P(v):
    return pal(BASE, SHINY, v)


def platef(x, y, z, face, variant, **k):
    """White plating banded with violet stripes that curve round the body."""
    p = P(variant)
    w = (y * 0.45 + abs(x) * 0.55 - z * 0.15) % 5.0
    if w < 1.1:
        return tone(p["violet"], face), None
    if face == "up":
        return p["white"], None
    return lit(p["white"], face, y, 30, 18), None


def metalf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["metal"] if face != "down" else p["metal_dark"], face), None


def whitef(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["white"] if face != "down" else p["white_dark"], face), None


def violetf(x, y, z, face, variant, **k):
    return tone(P(variant)["violet"], face), None


def pearlf(x, y, z, face, variant, **k):
    c = P(variant)["pearl"]
    return c, c


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and math.hypot(z + 10.4, y - 52.6) < 0.8:
        return p["eye"], p["eye"]
    if face in ("east", "west") and abs(y - (52.0 + (z + 10.0) * 0.3)) < 0.35:
        return p["violet"], None
    return whitef(x, y, z, face, variant)


def bladef(x, y, z, face, variant, box=None, **k):
    """A wing blade: white with a violet stripe along it (rods: y across the broad face)."""
    p = P(variant)
    cy = box.lo[1] + box.size[1] / 2
    v = (y - cy) / (box.size[1] / 2)
    if -0.15 < v < 0.35:
        return tone(p["violet"], face), None
    return tone(p["white"], face), None


def halof(x, y, z, face, variant, **k):
    """The halo (an xy plane): a violet eight-pointed star, a ring of white vents, a dark starry lens."""
    p = P(variant)
    dx, dy = x - HC[0], y - HC[1]
    r = math.hypot(dx, dy)
    a = math.atan2(dy, dx)
    if r < 4.8:
        if stars(x, y, z, face, cell=0.9, r=0.18, prob=0.35):
            return p["star"], p["star"]
        return p["lens"], None
    if r < 7.0:
        vent = (math.degrees(a) % 22.5) < 9
        return (p["white"] if vent else p["white_dark"]), None
    spikes = 7.0 + (7.0 if (math.degrees(a) % 90) < 45 else 4.6) * abs(math.cos(4 * a)) ** 2
    if r < spikes:
        return (p["violet_light"] if r < 8.6 else p["violet"]), None
    return CLEAR


def build() -> Model:
    m = Model("ironexpanse")
    mats = {"skin": platef, "belly": metalf, "neck": platef, "head": headf, "arm": metalf, "hand": metalf,
            "claw": whitef, "thigh": platef, "shin": platef, "foot": whitef, "talon": whitef, "tail": platef,
            "tail_tip": violetf, "pearl": pearlf, "mount": violetf, "crest": whitef}
    a = palkia(m, mats, "ironexpanse")
    bd = a["body"]
    for nm, sx in (("wing_left", 1), ("wing_right", -1)):                        # long striped wing blades
        wg = m.bone(nm, bd, (sx * 5.0, 42.0, 3.0))
        for i, (ang, L) in enumerate(((50, 24.0), (70, 26.0), (92, 20.0))):
            r = math.radians(ang)
            d = (sx * math.cos(r) * 0.9, math.sin(r), 0.5)
            root = (sx * (5.0 + i * 0.6), 42.0 - i * 1.6, 3.0 + i)
            n = math.sqrt(sum(v * v for v in d))
            mid = tuple(q + v / n * L * 0.55 for q, v in zip(root, d))
            end = tuple(q + v / n * L for q, v in zip(root, d))
            rod(m, wg, root, mid, 1.2, bladef, extend=0.4, t2=6.0)
            rod(m, wg, mid, end, 1.2, bladef, extend=0.4, t2=4.0)
            spike(m, wg, end, d, 2.0, 3.6, whitef, tip=0.8)
    ring = m.bone("ring_halo", a["top"], HC)                                        # the floating halo
    R = 14.2
    m.box(ring, HC[0] - R, HC[1] - R, HC[2], HC[0] + R, HC[1] + R, HC[2], halof)
    ellipsoid(m, ring, HC[0], HC[1], HC[2] + 0.6, 4.6, 4.6, 0.8, metalf, step=1)
    for sx in (-1, 1):                                                           # violet bands on the arms
        arm = a["arm_left" if sx > 0 else "arm_right"]
        m.box(arm["bone"], arm["elbow"][0] - 1.9, arm["elbow"][1] - 0.6, arm["elbow"][2] - 1.9,
              arm["elbow"][0] + 1.9, arm["elbow"][1] + 0.6, arm["elbow"][2] + 1.9, violetf)
    return m
