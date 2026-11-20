"""Iron Deity (Normal/Steel), the future paradox Arceus, built from boxes after the art the user shared (artist and name
not given; our name).

A towering robot Arceus standing upright before its golden wheel, now a great halo ringed in orange light and crossed
with dark bars. Its white armour is split in two: on its right side navy plates bristle with spikes and a cyan eye
glows in the helmet's dark half; on its left, pale lilac plates open on purple panels full of stars, and its left arm
ends in a folded lilac fan of blades tipped in purple. A yellow eye shines from its white helmet under a crest, and
its long legs taper to points with gold diamonds at the knees.

Shiny: black armour with gold and crimson halves.

Front is -z, y is up. 68 units tall (to the halo); about 4.6 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import humanoid
from _pgen1 import CLEAR, stars
from _regi import ellipsoid, lit
from _route import mix, pal, tone

HEIGHT = 68
SCALE = round(4.6 * 16 / HEIGHT, 3)
HITBOX = [1.8, 64 / 16]
KIND = "biped"
K = 3
LOOK = ("a towering white robot Arceus before a golden halo, its armour split into spiked navy plates on one side and "
        "starry lilac plates with a folded fan of blades on the other")

BASE = {"white": (240, 240, 246), "white_dark": (196, 196, 212), "navy": (40, 60, 110), "navy_light": (70, 96, 150),
        "lilac": (210, 196, 230), "lilac_dark": (170, 150, 200), "space": (110, 60, 160), "star": (255, 255, 255),
        "black": (36, 36, 44), "gold": (240, 200, 70), "halo": (246, 196, 70), "halo_glow": (255, 160, 60),
        "bar": (60, 54, 50), "eye": (250, 220, 70), "cyan": (110, 220, 255)}
SHINY = {"white": (60, 60, 70), "white_dark": (40, 40, 50), "navy": (190, 150, 50), "navy_light": (230, 196, 90),
         "lilac": (200, 70, 80), "lilac_dark": (150, 40, 56), "space": (90, 20, 40)}
HC = (0.0, 50.0, 6.0)       # the halo's centre
HR = 17.0


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def armourf(x, y, z, face, variant, **k):
    """White armour; its right side (x < 0) plated navy on the outer faces, its left lilac."""
    p = P(variant)
    if x < -3.0 and face in ("west", "north", "up") and (y > 40 or y < 30):
        return tone(p["navy"], face), None
    if x > 3.0 and face in ("east", "north", "up") and (y > 40 or y < 30):
        return tone(p["lilac"], face), None
    if face == "up":
        return p["white"], None
    return lit(p["white"], face, y, 34, 20), None


def blackf(x, y, z, face, variant, **k):
    return tone(P(variant)["black"], face), None


def helmetf(x, y, z, face, variant, **k):
    """The white helmet: its right half dark navy with a cyan eye, a yellow eye in its white half."""
    p = P(variant)
    if face == "north":
        if math.hypot(x - 1.2, y - 58.6) < 0.6:
            return p["eye"], p["eye"]
        if math.hypot(x + 1.4, y - 58.6) < 0.6:
            return p["cyan"], p["cyan"]
    if x < -0.4:
        return tone(p["navy"], face), None
    return lit(p["white"], face, y, 58, 3), None


def spacef(x, y, z, face, variant, **k):
    p = P(variant)
    if stars(x, y, z, face, cell=1.2, r=0.2, prob=0.35):
        return p["star"], p["star"]
    return p["space"], None


def lilacf(x, y, z, face, variant, box=None, **k):
    """A fan blade: pale lilac, purple and starry at its tip (rods: z runs back from the root)."""
    p = P(variant)
    d = (box.lo[2] + box.size[2] - z) / max(box.size[2], 0.01)
    if d > 0.72:
        return spacef(x, y, z, face, variant)
    return tone(p["lilac"] if face != "down" else p["lilac_dark"], face), None


def navyf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["navy"] if face != "up" else p["navy_light"], face), None


def halof(x, y, z, face, variant, **k):
    """The golden halo (an xy plane): a gold ring rimmed in orange light, crossed by dark bars at four points."""
    p = P(variant)
    dx, dy = x - HC[0], y - HC[1]
    r = math.hypot(dx, dy)
    if abs(r - HR) < 1.4:
        a = math.degrees(math.atan2(dy, dx)) % 90
        if abs(a - 45) < 4 and abs(r - HR) < 1.0:
            return p["bar"], None
        c = p["halo"] if abs(r - HR) < 0.9 else p["halo_glow"]
        return c, c
    return CLEAR


def build() -> Model:
    m = Model("irondeity")
    mats = {"skin": armourf, "abs": blackf, "pelvis": blackf, "neck": blackf, "hand": blackf, "finger": blackf,
            "knee": solid("gold"), "foot": armourf, "toe": armourf}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=0.9, leg_bulk=1.0, name="irondeity", fingers=3, toes=2)
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55.0, 0))
    m.round_box(hd, 0, -0.4, 2.8, 3.0, 55.0, 61.4, helmetf, cut=1)                  # helmet
    spike(m, hd, (0, 61.0, -0.6), (0, 1, 0.5), 2.0, 5.0, helmetf, tip=0.8)          # crest
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.4, 60.0, 0.4), (sx * 0.6, 0.7, 0.5), 1.4, 3.4, navyf if sx < 0 else lilacf, tip=0.6)
    # its right side: navy spiked plates on shoulder and hip
    ar = a["arm_right"]["bone"]
    m.box(ar, -10.8, 46.0, -3.0, -5.6, 53.6, 3.0, navyf)
    for d in ((-1, 0.6, 0), (-1, 0.2, -0.6), (-1, 0.9, 0.5), (-0.6, 1, 0)):
        spike(m, ar, (-9.6, 51.0, 0.0), d, 2.4, 6.0, navyf, tip=1.0)
    m.box(bd, -7.0, 28.0, -3.8, -3.6, 36.0, 3.0, navyf)
    # its left side: lilac plates opening on starry purple, and a folded fan of blades on its arm
    al = a["arm_left"]
    m.box(al["bone"], 5.6, 46.0, -3.0, 10.4, 53.6, 3.0, solid("lilac"))
    m.box(al["bone"], 6.4, 46.6, -3.2, 9.6, 52.8, -3.2, spacef)
    wr = al["wrist"]
    for i in range(5):
        ang = math.radians(-24 + i * 12)
        d = (math.sin(ang), -1, -0.15)
        spike(m, al["bone"], (wr[0] + 0.6, wr[1] + 2.0, wr[2]), d, 2.2, 13.0 - abs(i - 2) * 1.4, lilacf, tip=1.2)
    for nm in ("leg_left", "leg_right"):                                          # long tapering pointed legs
        lg = a[nm]
        k = lg["knee"]
        spike(m, lg["bone"], (k[0], 16.0, k[2] - 1.0), (0, -1, -0.1), 3.6, 9.0, armourf, tip=1.6)
        ellipsoid(m, lg["bone"], k[0], 18.6, k[2] - 2.0, 1.4, 1.4, 1.0, solid("gold", True), step=1)
    hl = m.bone("ring_halo", a["top"], HC)                                          # the golden halo
    R = HR + 1.6
    m.box(hl, HC[0] - R, HC[1] - R, HC[2], HC[0] + R, HC[1] + R, HC[2], halof)
    return m
