"""Feral Mind (Psychic/Rock), the ancient paradox Mewtwo, built from boxes after the art the user shared (artist not
named, no name given; our name).

A primal Mewtwo with a white hide: a fierce head with long swept-back white horns, little pink horns on its brow and
a red-rimmed amber eye, and a huge wild mane of dark teal hair streaming back from its head and shoulders over a ruff
of mauve fur. Mauve plates cover its belly and hips and run down its thick tail, which darkens to teal and ends in
pink-tipped fins. Its great white fists and forearms bristle with glowing green crystals.

Shiny: a pale gold mane and violet crystals.

Front is -z, y is up. 66 units tall; about 2.2 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digidetail import fur, skin
from _mewtwo import mewtwo
from _pgen1 import smooth_path
from _regi import ellipsoid
from _route import mix, pal, tone

HEIGHT = 66
SCALE = round(2.2 * 16 / HEIGHT, 3)
HITBOX = [1.2, HEIGHT / 16]
KIND = "biped"
K = 3
LOOK = ("a primal white Mewtwo with long swept-back horns, a huge streaming dark teal mane over a mauve fur ruff, "
        "mauve belly and tail plates, a pink-finned tail and great fists bristling with glowing green crystals")

BASE = {"white": (246, 244, 252), "white_dark": (204, 200, 222), "grey": (150, 146, 166), "mauve": (150, 76, 122),
        "mauve_dark": (110, 50, 90), "mauve_light": (184, 112, 156), "teal": (40, 78, 98), "teal_dark": (24, 50, 66),
        "teal_light": (70, 116, 136), "crystal": (150, 246, 170), "crystal_light": (214, 255, 220),
        "pink": (240, 110, 170), "eye": (250, 176, 50), "eye_rim": (210, 40, 50), "pupil": (40, 20, 20)}
SHINY = {"teal": (210, 180, 110), "teal_dark": (170, 136, 70), "teal_light": (240, 216, 150), "crystal": (196, 150,
                                                                                                         255),
         "crystal_light": (232, 214, 255), "mauve": (90, 70, 150), "mauve_dark": (60, 46, 110),
         "mauve_light": (130, 110, 190)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = skin(P, "white", dark="white_dark", var=0.04)
MANE = fur(P, "teal", "teal_dark", tip="teal_light", length=2.4, density=1.2, flow=(0, -1))
RUFF = fur(P, "mauve", "mauve_dark", tip="mauve_light", length=1.4, density=1.6)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def platef(x, y, z, face, variant, **k):
    """Mauve plates in rows (belly, hips)."""
    p = P(variant)
    if (y % 2.4) < 0.4:
        return tone(p["mauve_dark"], face), None
    return tone(p["mauve_light"] if face == "up" else p["mauve"], face), None


def tailf(x, y, z, face, variant, box=None, **k):
    """Mauve plates down the tail, banded (rods: z runs along the rod)."""
    p = P(variant)
    if (z % 2.6) < 0.5:
        return tone(p["mauve_dark"], face), None
    return tone(p["mauve"], face), None


def tailtipf(x, y, z, face, variant, **k):
    p = P(variant)
    if (z % 2.6) < 0.5:
        return tone(p["teal_dark"], face), None
    return tone(p["teal"], face), None


def headf(x, y, z, face, variant, **k):
    """White, a fierce amber eye rimmed in red with a red mark sweeping back from it on each side of the face."""
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 1.4, y - 59.2
            if abs(dy + dx * sx * 0.35) < 0.32 and 0.2 < dx * sx < 1.3:
                return (p["eye"] if dx * sx < 1.0 else p["eye_rim"]), None
            if abs(dy + dx * sx * 0.35) < 0.55 and 0.0 < dx * sx < 1.6:
                return p["eye_rim"], None
    if face in ("east", "west") and abs(y - (59.6 + 0.25 * (z + 1.0))) < 0.35 and -2.6 < z < 1.6:
        return p["eye_rim"], None
    return WHITE(x, y, z, face, variant, **k)


def crystal(m, bone, base, d, w, h):
    n = math.sqrt(sum(v * v for v in d))
    u = tuple(v / n for v in d)
    mid = tuple(b + uu * h * 0.65 for b, uu in zip(base, u))
    rod(m, bone, base, mid, w, solid("crystal", True), extend=0.2)
    rod(m, bone, mid, tuple(b + uu * h for b, uu in zip(base, u)), max(0.6, w * 0.45), solid("crystal_light", True),
        extend=0.2)


def lock(m, bone, pts, w0, w1):
    """One lock of mane: thick at its root, flaring, then tapering to a point."""
    path = smooth_path(pts, 10)
    for i, (p0, p1) in enumerate(zip(path, path[1:])):
        f = i / (len(path) - 2)
        w = w0 + (w1 - w0) * f + 3.0 * math.sin(math.pi * f)
        rod(m, bone, p0, p1, max(1.0, round(w * 2) / 2), MANE, extend=0.8, t2=max(1.0, round(w * 0.85 * 2) / 2))


def build() -> Model:
    m = Model("feralmind")
    mats = {"skin": WHITE, "chest": WHITE, "abs": platef, "pelvis": platef, "neck": WHITE, "deltoid": WHITE,
            "upper_arm": WHITE, "forearm": WHITE, "hand": WHITE, "finger": WHITE, "thigh": WHITE,
            "knee": WHITE, "shin": WHITE, "foot": solid("grey"), "toe": solid("grey"),
            "head": headf, "muzzle": WHITE, "horn": WHITE, "tube": WHITE, "tail": tailf, "tail_tip": tailtipf,
            "hip": platef}
    a = mewtwo(m, mats, "feralmind", horns=False, tail_w=(5.0, 2.4), tip_from=0.6)
    hd, bd = a["head"], a["body"]
    for sx in (-1, 1):                                                              # long swept-back horns
        rod(m, hd, (sx * 1.6, 61.0, 0.2), (sx * 2.8, 63.6, 3.4), 1.8, WHITE, extend=0.4)
        rod(m, hd, (sx * 2.8, 63.4, 3.2), (sx * 3.4, 64.8, 7.2), 1.2, WHITE, extend=0.4)
        spike(m, hd, (sx * 1.0, 61.2, -2.2), (sx * 0.3, 1, -0.3), 0.9, 1.8, solid("pink"))     # little pink horns
    # the wild mane: locks streaming back and outward from the head and shoulders
    mn = m.bone("mane", hd, (0, 60.0, 2.0))
    for sx, lift, spread, w0 in ((0, 4.0, 0.0, 3.0), (1, 2.0, 5.0, 2.8), (-1, 2.0, 5.0, 2.8), (1, -3.0, 8.0, 3.2),
                                 (-1, -3.0, 8.0, 3.2), (1, -8.0, 6.0, 3.0), (-1, -8.0, 6.0, 3.0)):
        root = (sx * 1.2, 60.5 + lift * 0.25, 2.6)
        pts = [root, (sx * (1.6 + spread * 0.4), 60.0 + lift * 0.6, 7.0), (sx * (2.0 + spread * 0.8), 58.0 + lift, 13.0),
               (sx * (2.4 + spread), 55.0 + lift * 1.2, 19.0)]
        lock(m, mn, pts, w0 + 1.4, 1.2)
    for sx in (-1, 1):                                                              # locks down the back like a cape
        for dx, drop in ((2.0, 0.0), (4.4, 3.0)):
            pts = [(sx * dx, 54.0, 3.4), (sx * (dx + 1.0), 50.0, 8.0), (sx * (dx + 2.4), 44.0, 12.0),
                   (sx * (dx + 3.4), 38.0 - drop, 15.0)]
            lock(m, mn, pts, 4.0, 1.2)
    for i in range(12):                                                             # the mauve fur ruff
        ang = math.radians(-150 + i * (300 / 11))
        d = (math.sin(ang), 0.15, -math.cos(ang) * 0.6 + 0.2)
        base = (d[0] * 3.2, 52.0 + 0.6 * math.cos(ang), d[2] * 3.0)
        rod(m, bd, base, tuple(b + v * 3.6 for b, v in zip(base, (d[0], -0.5, d[2]))), 1.8, RUFF, extend=0.4)
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):                             # crystal-bristling fists
        arm = a[nm]
        h, w, el = arm["hand"], arm["wrist"], arm["elbow"]
        ellipsoid(m, arm["bone"], h[0], h[1] - 1.0, h[2], 3.2, 3.2, 3.2, WHITE, step=1)
        for d in ((sx * 1, 0.2, -0.4), (sx * 0.6, 0.9, -0.5), (sx * 0.8, -0.6, -0.7), (0, 0.3, -1), (sx * 0.5, 0.5, 0.6)):
            crystal(m, arm["bone"], (h[0] + d[0] * 2.4, h[1] - 1.0 + d[1] * 2.4, h[2] + d[2] * 2.4), d, 2.0, 5.0)
        for d in ((sx * 1, 0.4, 0.2), (sx * 0.7, 0.8, -0.4)):
            mid = tuple((p + q) / 2 for p, q in zip(w, el))
            crystal(m, arm["bone"], mid, d, 1.8, 4.2)
        crystal(m, arm["bone"], (sx * 6.4, 50.6, 0.0), (sx * 0.7, 1, 0.2), 2.0, 4.6)   # on the shoulder
    tl = a["tail"]                                                                  # pink-tipped fins at the tail's end
    end = a["tail_pts"][-1]
    for d in ((0.4, 1, -0.2), (0.6, 0.6, -0.8), (0.2, 1, 0.6)):
        n = math.sqrt(sum(v * v for v in d))
        u = tuple(v / n for v in d)
        b = (end[0], end[1] + 0.6, end[2])
        mid = tuple(bb + uu * 2.4 for bb, uu in zip(b, u))
        rod(m, tl, b, mid, 1.2, tailtipf, extend=0.2)
        rod(m, tl, mid, tuple(bb + uu * 4.0 for bb, uu in zip(b, u)), 0.9, solid("pink"), extend=0.2)
    return m
