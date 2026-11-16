"""Alphamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the phantom Royal Knight. Gunmetal silver plate armour edged in gold, huge gold-rimmed rounded
pauldrons rising behind its head, gold triangle emblems, red gems set in its breastplate, a dragon-visored helm with
a swept horn, heavy gold rings at its wrists, folded wings of long gold-banded feathers and a vast tattered navy cape.
35 blocks tall.

Front is -z, y is up. 72 units tall (the pauldrons); Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, dome, humanoid, shell
from _digidetail import armour, cutout, fabric, gem, local, metal, mix, solid
from _route import pal, tone

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a Royal Knight in gunmetal silver plate edged in gold: huge gold-rimmed pauldrons, red breast gems, a "
        "dragon-visored helm, gold wrist rings, folded gold-banded wings and a vast tattered navy cape")

BASE = {"steel": (128, 132, 146), "steel_dark": (40, 42, 52), "steel_light": (226, 230, 240),
        "gold": (226, 180, 60), "gold_dark": (150, 108, 30), "gold_light": (255, 236, 160),
        "cape": (40, 54, 120), "cape_dark": (18, 24, 64), "cape_light": (90, 110, 180), "red": (220, 30, 40),
        "red_light": (255, 140, 140), "eye": (255, 60, 40), "black": (30, 30, 36),
        "white": (250, 250, 248), "fire_y": (255, 200, 60), "fire_r": (220, 40, 40)}
SHINY = {"steel": (60, 60, 70), "steel_dark": (24, 24, 30), "steel_light": (130, 132, 150), "cape": (130, 24, 40),
         "cape_dark": (70, 10, 20), "cape_light": (200, 70, 90), "red": (40, 180, 220), "red_light": (170, 240, 255)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "steel", "steel_dark", light="steel_light", trim="gold")
PLATE_PLAIN = armour(P, "steel", "steel_dark", light="steel_light", seams=(4.0,))
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
STEEL = metal(P, "steel", dark="steel_dark", light="steel_light")
CAPE = fabric(P, "cape", "cape_dark", axis="y", period=3.0)
GEM = gem(P, "red", "red_light")


def triangle_plate(x, y, z, face, variant, box=None, **k):
    """A steel plate with a gold triangle emblem (the triangles on its pauldrons and belt)."""
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    uu, vv = u / max(W, 1e-6) - 0.5, v / max(H, 1e-6)
    if face in ("north", "east", "west", "south") and 0.25 < vv < 0.75 and abs(uu) < (0.75 - vv) * 0.8:
        return tone(p["gold"], face), None
    return PLATE(x, y, z, face, variant, box=box, **k)


def featherf(x, y, z, face, variant, box=None, **k):
    """A long wing feather: steel with a gold band near its tip and a gold edge."""
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    t = v / max(H, 1e-6)
    if 0.12 < t < 0.24 or min(u, W - u) < 0.35:
        return tone(p["gold"], face), None
    return STEEL(x, y, z, face, variant, box=box, **k)


def helmf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 57.4 < y < 58.4 and 0.4 < abs(x) < 2.0:
        return p["eye"], p["eye"]
    return PLATE(x, y, z, face, variant, box=box, **k)


def firefeather(x, y, z, face, variant, box=None, **k):
    """A white feather burning yellow, orange and red toward its tip."""
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    t = 1 - v / max(H, 1e-6)                                      # 0 at the root (top), 1 at the tip
    if min(u, W - u) < 0.3:
        return tone(p["steel_light"], face), None
    col = p["white"] if t < 0.45 else mix(p["fire_y"], p["fire_r"], (t - 0.45) / 0.55)
    return tone(col, face), None


def blade_shape(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    t = v / max(H, 1e-6)
    half = 0.5 if t > 0.12 else 0.5 * t / 0.12
    return abs(u / max(W, 1e-6) - 0.5) < half


def bladef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if abs(u / max(W, 1e-6) - 0.5) < 0.16:
        return tone(p["black"], face), None
    return GOLD(x, y, z, face, variant, box=box, **k)


def build(name="alphamon", ouryuken=False):
    m = Model(name)
    mats = {"skin": PLATE_PLAIN, "chest": PLATE, "abs": PLATE_PLAIN, "pelvis": PLATE, "neck": STEEL,
            "deltoid": PLATE, "upper_arm": PLATE_PLAIN, "forearm": PLATE, "hand": PLATE_PLAIN, "finger": STEEL,
            "thigh": PLATE, "knee": GOLD, "shin": PLATE, "calf": PLATE_PLAIN, "foot": PLATE, "toe": GOLD,
            "talon": GOLD}
    a = humanoid(m, mats, bulk=1.15, arm_bulk=1.2, leg_bulk=1.2, hand_pose="fist", name=name, talons=True)
    bd = a["body"]
    # helm: dragon visor, jaw guard, horn sweeping back
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.6, 3.0, 54.5, 61.0, helmf, cut=1)
    m.box(hd, -1.8, 54.6, -5.4, 1.8, 57.0, -2.6, PLATE_PLAIN, rotation=(-12, 0, 0), pivot=(0, 56, -2.6))  # visor jaw
    m.box(hd, -0.5, 58.0, -4.6, 0.5, 61.4, -2.0, GOLD)                                  # gold nose ridge
    rod(m, hd, (0, 61.0, -1.5), (0, 64.0, 2.5), 2, PLATE_PLAIN, extend=0.3)
    spike(m, hd, (0, 64.0, 2.5), (0, 0.4, 1), 1.6, 4.0, GOLD, tip=0.6)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.6, 59.5, 0.0), (sx * 0.5, 0.5, 1), 1.0, 3.2, GOLD)
    # breastplate: wrap plate, central red gem, gems at the solar plexus, gold collar ring
    shell(m, bd, (0, 0, 0.6), 5.6, 43.0, 51.0, -80, 80, 9, 1.0, PLATE)
    m.round_box(bd, 0, -5.6, 1.1, 0.6, 46.0, 48.4, GEM, cut=1)
    m.round_box(bd, 0, -4.8, 0.8, 0.5, 40.0, 41.8, GEM, cut=1)
    shell(m, bd, (0, 0, 0.4), 3.6, 50.8, 52.6, -110, 110, 8, 1.0, GOLD)
    # the huge pauldrons: domes with a broad gold rim that rises behind the head, a triangle plate below
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = a[nm]["bone"]
        sh = a[nm]["shoulder"]
        c = (sh[0] + sx * 2.0, 50.0, 0.6)
        dome(m, ab, c, 5.6, 5.0, PLATE_PLAIN, layers=4)
        a0, a1 = (-10, 190) if sx > 0 else (-190, 10)
        shell(m, ab, (c[0], 0, c[2]), 5.8, 49.0, 51.0, a0, a1, 10, 1.0, GOLD, tilt=-6)
        shell(m, ab, (c[0], 0, c[2]), 5.6, 51.0, 55.0, a0, a1, 10, 1.0, PLATE_PLAIN, tilt=-6)
        rod(m, ab, (c[0] - sx * 1.0, 54.0, 3.0), (c[0] - sx * 3.0, 62.0, 4.0), 3, GOLD, extend=0.3)   # rising rim
        rod(m, ab, (c[0] - sx * 3.0, 62.0, 4.0), (c[0] - sx * 5.0, 64.0, 3.0), 2, GOLD, extend=0.3)
        x0, x1 = sorted((c[0] + sx * 4.6, c[0] + sx * 5.6))
        m.box(ab, x0, 42.0, -2.4, x1, 48.0, 2.6, triangle_plate)
        wr, el = a[nm]["wrist"], a[nm]["elbow"]
        p = tuple(w + (e - w) * 0.2 for w, e in zip(wr, el))
        rod(m, ab, wr, p, 5, GOLD, extend=0.4)                                          # heavy gold wrist ring
        shell(m, ab, (el[0], 0, el[2]), 2.2, 35.0, 39.5, -180, 180, 6, 0.8, PLATE)      # elbow guard
    # belt with a triangle buckle, tassets, knee guards, gold-trimmed greaves
    m.box(bd, -4.9, 31.4, -4.0, 4.9, 34.0, 4.0, PLATE)
    m.box(bd, -1.6, 30.6, -4.6, 1.6, 34.6, -3.8, triangle_plate)
    for sx in (-1, 1):
        m.box(bd, sx * 3.8 - 2.2, 25.0, -4.4, sx * 3.8 + 2.2, 32.0, -3.4, PLATE, rotation=(-8, 0, sx * 8),
              pivot=(sx * 3.8, 32.0, -3.9))
        lg = a["leg_left" if sx > 0 else "leg_right"]
        kn = lg["knee"]
        dome(m, lg["bone"], (kn[0], 17.5, kn[2] - 0.8), 2.6, 2.6, GOLD, layers=2)
        shell(m, lg["bone"], (kn[0], 0, 0.6), 2.8, 4.0, 15.0, -90, 90, 6, 1.0, PLATE)
    if ouryuken:
        # Ouryumon's spirit: great swept wings of white feathers burning red, orange and gold toward the tips
        for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
            wb = m.bone(nm, bd, (sx * 4.0, 50.0, 4.0))
            rod(m, wb, (sx * 4.0, 50.0, 4.0), (sx * 12.0, 62.0, 8.0), 3, GOLD, extend=0.4)
            rod(m, wb, (sx * 12.0, 62.0, 8.0), (sx * 20.0, 70.0, 12.0), 2, GOLD, extend=0.4)
            for i in range(11):
                t = i / 10
                base = (sx * (4.0 + 16.0 * t), 50.0 + 20.0 * t, 4.0 + 8.0 * t)
                ln = 16.0 + 14.0 * t
                m.box(wb, base[0] - 1.3, base[1] - ln, base[2], base[0] + 1.3, base[1], base[2], firefeather,
                      rotation=(-14 - 10 * t, 0, -sx * (60 - 40 * t)), pivot=base)
        # the Ouryuken: a huge gold-and-black blade held point-down in its right hand
        ar = a["arm_right"]
        h = ar["hand"]
        sw = m.bone("sword", ar["bone"], h)
        m.box(sw, h[0] - 1.0, h[1] - 1.0, h[2] - 1.0, h[0] + 1.0, h[1] + 6.0, h[2] + 1.0, solid(P, "black"))   # grip
        m.box(sw, h[0] - 3.5, h[1] - 2.4, h[2] - 1.4, h[0] + 3.5, h[1] - 0.8, h[2] + 1.4, GOLD)                 # guard
        m.box(sw, h[0] - 4.0, h[1] - 36.0, h[2], h[0] + 4.0, h[1] - 2.0, h[2], cutout(blade_shape, bladef))
        m.box(sw, h[0], h[1] - 34.0, h[2] - 2.2, h[0], h[1] - 2.0, h[2] + 2.2, cutout(blade_shape, bladef))
    else:
        # folded wings of long gold-banded feathers behind the shoulders
        for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
            wb = m.bone(nm, bd, (sx * 4.0, 50.0, 4.0))
            rod(m, wb, (sx * 4.0, 50.0, 4.0), (sx * 9.0, 56.0, 7.0), 3, GOLD, extend=0.4)
            for i in range(7):
                base = (sx * (5.0 + i * 0.7), 55.0 - i * 0.6, 6.0 + i * 0.4)
                m.box(wb, base[0] - 1.1, base[1] - 22.0 + i * 1.5, base[2], base[0] + 1.1, base[1], base[2],
                      featherf, rotation=(-10, sx * (20 + i * 4), -sx * (4 + i * 2)), pivot=base)
        # the vast tattered navy cape
        cb = m.bone("cap", bd, (0, 51, 4))
        cape(m, cb, 52.0, 22.0, 50.0, CAPE, z=5.0, flare=0.8, panels=10, sweep=(0, 6))
    return m
