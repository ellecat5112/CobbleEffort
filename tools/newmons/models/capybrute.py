"""Capybrute, the Brawler Rodent Pokémon (Ground/Fighting), built from boxes after the concept art the user shared (the
art's own name; art by @Kai_FakemonsR), inspired by capybaras and marmots.

A huge, hunched rodent: a great arched brown back like a boulder with two pale-orange slash markings along it, the
small head held low in front with a tan muzzle and jaw, a heavy orange brow over a scowling dark eye, little rounded
ears with dark rims, a dark stripe down the snout edge and two big white buck teeth; thick tan forelegs with dark
curved claws, short dark hind legs, a darker rump, and spiky fur tufts sticking out behind the hump and at the tail.

Shiny: a silver marmot (slate-grey fur, cream muzzle and forelegs, icy blue markings).

Front is -z, y is up. 27 units tall to the top of the hump; baseScale 0.9 (1.5 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, mix, rod, spike
from _route import pal, tone

SCALE = 0.9
HITBOX = [1.4, 1.5]
KIND = "quadruped"
K = 4
HEIGHT = 27
LOOK = ("a huge hunched brown capybara-marmot with an arched boulder-like back, orange slash markings, a small low "
        "head with a tan muzzle, scowling brow and big buck teeth, tan clawed forelegs and dark hind legs")

BASE = {"fur": (178, 102, 66), "fur_light": (206, 138, 96), "fur_dark": (128, 70, 46), "rump": (140, 78, 50),
        "mark": (246, 178, 96), "tan": (224, 196, 132), "tan_shade": (190, 160, 100), "dark": (58, 44, 40),
        "claw": (70, 60, 58), "tooth": (246, 244, 236), "eye": (244, 240, 230), "pupil": (30, 26, 26)}
SHINY = {"fur": (124, 128, 142), "fur_light": (160, 164, 178), "fur_dark": (88, 90, 104), "rump": (98, 100, 114),
         "mark": (150, 206, 236), "tan": (236, 230, 210), "tan_shade": (196, 190, 170), "dark": (40, 40, 52)}


def P(v):
    return pal(BASE, SHINY, v)


def slash(z, y, z0, y0, z1, y1, w):
    """Inside a tapering diagonal slash from (z0, y0) to (z1, y1) (widest in the middle)."""
    dz, dy = z1 - z0, y1 - y0
    L2 = dz * dz + dy * dy
    t = ((z - z0) * dz + (y - y0) * dy) / L2
    if not 0 <= t <= 1:
        return False
    d = abs((z - z0) * dy - (y - y0) * dz) / math.sqrt(L2)
    return d < w * math.sin(math.pi * t)


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west", "up"):
        if slash(z, y, -7, 21.5, 5, 25.5, 1.3) or slash(z, y, -2, 17, 8, 21.5, 1.1):
            return p["mark"], None                                       # the two orange slashes
        if face == "up" and slash(z, abs(x) * 2 + 20, -6, 21, 6, 23, 1.6):
            return p["mark"], None
    c = p["fur"]
    if z > 6 and y < 14:
        c = mix(p["fur"], p["rump"], min(1.0, (z - 6) / 4))               # darker rump
    if y > 18 and abs(x) < 3:
        c = mix(c, p["fur_light"], 0.35)                                   # sheen along the top of the back
    if face == "down":
        c = mix(c, p["fur_dark"], 0.5)
    return tone(c, face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        dz, dy = z + 15.6, y - 13.2
        if math.hypot(dz / 0.55, dy / 0.32) < 1 and dy < 0.1 - 0.25 * dz:
            return (p["pupil"] if dz < -0.1 else p["eye"]), None         # small scowling eye under the brow
        if math.hypot(dz / 1.2, dy / 0.8) < 1:
            return p["dark"], None                                         # dark socket round it
        if 13.6 + 0.35 * (dz + 1.5) < y < 15.2 and -17.5 < z < -13.5:
            return p["mark"], None                                         # heavy orange brow, slanting down
        if slash(z, y, -18, 11.5, -14.5, 12.8, 0.5):
            return p["mark"], None                                         # orange cheek slash
    if face == "north" and 13.9 < y < 15.1:
        return p["mark"], None
    if y < 12.4:
        return tone(p["tan"], face), None                                  # tan jaw and lower face
    return tone(p["fur"], face), None


def muzzlef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and y > 11.6:
        if abs(x) < 1.2 and y > 12.2:
            return p["dark"], None                                         # dark nose
        return tone(p["fur"], face), None
    if face == "up":
        return tone(p["fur"] if abs(x) < 1.4 else p["dark"], face), None   # dark stripe along the snout edge
    if face in ("east", "west") and y > 12:
        return p["dark"], None
    return tone(p["tan"], face), None


def earf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["dark"] if y > 15.8 or face == "north" else p["fur"], face), None


def toothf(x, y, z, face, variant, **k):
    return P(variant)["tooth"], None


def forelegf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and y < 2.6 and abs((x % 1.3) - 0.65) < 0.35:
        return p["claw"], None                                             # dark curved claws
    c = p["tan"] if y < 9 else mix(p["tan"], p["fur"], (y - 9) / 3)
    if face == "south":
        c = p["tan_shade"]
    return tone(c, face), None


def clawf(x, y, z, face, variant, **k):
    return tone(P(variant)["claw"], face), None


def hindf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["dark"] if y < 6 else mix(p["dark"], p["rump"], (y - 6) / 4), face), None


def tuftf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(mix(p["rump"], p["fur_dark"], 0.3), face), None


def build() -> Model:
    m = Model("capybrute")
    top = m.bone("capybrute", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    # the great arched back: slices front to back, following a dome that peaks over the middle and slopes low to the
    # neck and the rump (each slice rounded off on top)
    for i in range(12):
        z0 = -13 + i * 2.1
        zc = z0 + 1.05
        u = zc / 13 if zc < 0 else zc / 11
        topy = 13.5 + 13.5 * max(0.0, math.cos(math.pi / 2 * min(1.0, abs(u)))) ** 0.55
        w = 4.6 + 3.1 * max(0.0, math.cos(math.pi / 2 * min(1.0, abs(u) * 0.9))) ** 0.5
        bot = 5 + 2.5 * max(0.0, -u)
        m.box(bd, -w, bot, z0, w, topy - 1.6, z0 + 2.2, bodyf)
        m.box(bd, -w + 1.6, topy - 1.7, z0 + 0.05, w - 1.6, topy, z0 + 2.15, bodyf)
    # spiky fur behind the hump
    for (sx, y, z, d, h) in ((-3, 17, 10.5, (-0.4, 0.8, 1), 4), (2.5, 19, 9.5, (0.3, 1, 0.9), 4.5),
                             (0, 14, 11.5, (0, 0.5, 1), 4), (4.8, 15, 10, (0.8, 0.3, 1), 3.5),
                             (-5, 13, 10, (-0.8, 0.2, 1), 3.5)):
        spike(m, bd, (sx, y, z), d, 2.2, h, tuftf, tip=1)
    tl = m.bone("tail", bd, (0, 9, 11.5))
    spike(m, tl, (0, 9.5, 11.5), (0, 0.9, 1), 3, 6, tuftf, tip=1.4)              # spiky tail tuft

    hd = m.bone("head", bd, (0, 12, -13))
    m.round_box(hd, 0, -15.5, 3.6, 3, 9, 15.4, headf, cut=1)
    m.round_box(hd, 0, -19, 2.6, 1.6, 9.4, 13.2, muzzlef, cut=0.7)               # muzzle
    for sx in (-1, 1):
        m.box(hd, sx * 0.15 + (-1.3 if sx < 0 else 0), 7.4, -20.3, sx * 0.15 + (0 if sx < 0 else 1.3), 9.6, -19.6,
              toothf)                                                            # two big buck teeth
        m.box(hd, min(sx * 2.4, sx * 4.2), 14.4, -14.4, max(sx * 2.4, sx * 4.2), 16.6, -13.4, earf,
              rotation=(0, 0, sx * -18), pivot=(sx * 2.4, 15, -14))               # small rounded ears

    for nm, lx, lz in (("leg_front_left", -4.4, -8.5), ("leg_front_right", 4.4, -8.5)):
        lg = m.bone(nm, top, (lx, 12, lz))
        m.round_box(lg, lx, lz, 2.6, 2.6, 2.4, 12, forelegf, cut=0.8)          # thick tan foreleg
        m.box(lg, lx - 2.8, 0, lz - 3.4, lx + 2.8, 2.6, lz + 2.4, forelegf)     # broad paw
        for dx in (-1.6, 0, 1.6):
            spike(m, lg, (lx + dx, 1.2, lz - 3.2), (0, -0.4, -1), 1, 1.6, clawf)   # claws
    for nm, lx, lz in (("leg_back_left", -4.6, 8), ("leg_back_right", 4.6, 8)):
        lg = m.bone(nm, top, (lx, 9, lz))
        m.round_box(lg, lx, lz, 2.6, 3, 1.6, 10, hindf, cut=0.8)                # short dark hind leg
        m.box(lg, lx - 2.6, 0, lz - 3.6, lx + 2.6, 2, lz + 2, hindf)            # foot
    return m
