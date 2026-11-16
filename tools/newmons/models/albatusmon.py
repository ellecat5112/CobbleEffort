"""Albatusmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): an armoured angel of judgment. Silver plate armour edged in gold over a slate under-suit, a horned
silver helm with a spiked dark crest, great curtains of feathers in deepening sky blues sweeping down from its back to
its heels, silver talons, and a long golden staff crowned with a blazing circle of glowing runes. 35 blocks tall.

Front is -z, y is up. 72 units tall (the rune circle); Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid, shell
from _digidetail import armour, cutout, feathers, gem, local, metal, mix, skin, solid
from _route import pal, tone

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 1.8)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = ("an armoured angel: gold-edged silver plate over a slate suit, a horned silver helm with a spiked dark crest, "
        "great curtains of sky-blue feathers sweeping to its heels, silver talons and a golden staff crowned with a "
        "blazing circle of runes")

BASE = {"silver": (214, 218, 228), "silver_dark": (132, 138, 156), "silver_light": (250, 252, 255),
        "gold": (230, 186, 64), "gold_dark": (156, 116, 30), "gold_light": (255, 236, 160),
        "suit": (70, 78, 96), "suit_dark": (34, 38, 50), "suit_light": (130, 140, 166),
        "feather": (140, 226, 255), "feather_dark": (40, 140, 232), "feather_tip": (220, 246, 255), "shaft": (200, 236, 255),
        "crest": (40, 40, 52), "eye": (90, 220, 255), "rune": (255, 190, 60), "rune_core": (255, 244, 200)}
SHINY = {"feather": (250, 170, 90), "feather_dark": (190, 80, 40), "feather_tip": (255, 236, 200),
         "shaft": (255, 220, 180), "silver": (60, 62, 74), "silver_dark": (30, 32, 40), "silver_light": (120, 124, 140),
         "rune": (120, 220, 255), "rune_core": (220, 250, 255)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "silver", "silver_dark", light="silver_light", trim="gold")
PLATE_PLAIN = armour(P, "silver", "silver_dark", light="silver_light")
SUIT = skin(P, "suit", dark="suit_dark", light="suit_light", var=0.04)
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
SILVER = metal(P, "silver", dark="silver_dark", light="silver_light")
FEATHER = feathers(P, "feather", "feather_dark", shaft="shaft", size=(2.2, 4.0), flow=(0, -1), tip="feather_tip")


def featherf(x, y, z, face, variant, box=None, **k):
    """A long hanging feather (a plane): sky blue deepening toward its tip, a pale shaft down its middle."""
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    t = 1 - v / max(H, 1e-6)                                          # 0 at the top, 1 at the tip
    col = mix(p["feather"], p["feather_dark"], t ** 1.3)
    if abs(u / max(W, 1e-6) - 0.5) < 0.06:
        col = p["shaft"]
    elif (v * 2.2 + abs(u - W / 2) * 3) % 2.0 < 0.25:
        col = mix(col, p["feather_tip"], 0.4)                         # barbs
    return tone(col, face), None


def feather_inside(x, y, z, face, box):
    """Long and narrow, rounded at the top, a ragged point at the bottom."""
    u, v, W, H = local(x, y, z, face, box)
    uu, t = abs(u / max(W, 1e-6) - 0.5), v / max(H, 1e-6)
    if t < 0.18:
        return uu < 0.5 * (t / 0.18) * (0.75 + 0.25 * abs(math.sin(u * 3)))
    return uu < 0.5


def runef(x, y, z, face, variant, box=None, **k):
    """The rune circle (an xy plane): two glowing rings with runes between them and a sun at the centre."""
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    du, dv = u - W / 2, v - H / 2
    r = math.hypot(du, dv) / (W / 2)
    ang = math.atan2(dv, du)
    if r > 1.0:
        return (0, 0, 0, 0), None
    if 0.9 < r <= 1.0 or 0.62 < r < 0.7:
        return p["rune"] + (255,), p["rune"]
    if 0.7 <= r <= 0.9:
        g = (ang / (2 * math.pi) * 24) % 1.0
        if 0.25 < g < 0.75 and (int(r * 40) + int(ang * 12)) % 3 != 0:
            return p["rune"] + (255,), p["rune"]
        return (0, 0, 0, 0), None
    if r < 0.28:
        return p["rune_core"] + (255,), p["rune_core"]
    if (ang / (2 * math.pi) * 12) % 1.0 < 0.18:
        return p["rune"] + (220,), p["rune"]                          # sun rays
    return (0, 0, 0, 0), None


def helmf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(y - 58.8) < 0.4 and 0.4 < abs(x) < 2.0:
        return p["eye"], p["eye"]                                     # glowing eye slit
    return PLATE_PLAIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("albatusmon")
    mats = {"skin": SUIT, "chest": PLATE, "abs": SUIT, "pelvis": PLATE, "neck": SUIT, "deltoid": PLATE,
            "upper_arm": SUIT, "forearm": PLATE, "hand": SILVER, "finger": SILVER, "thigh": SUIT, "knee": PLATE,
            "shin": PLATE, "calf": PLATE, "foot": SILVER, "talon": SILVER}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=1.0, leg_bulk=1.05, digitigrade=True, talons=True, name="albatusmon")
    bd = a["body"]
    # armour layers: chest wrap, collar, ab plates, tassets, pauldrons, knee shells
    shell(m, bd, (0, 0, 0.4), 5.0, 41.5, 50.5, -80, 80, 9, 1.0, PLATE)
    for i in range(3):
        m.box(bd, -2.6, 35.2 + i * 2.2, -4.0, 2.6, 37.2 + i * 2.2, -3.2, PLATE)
    shell(m, bd, (0, 0, 0.4), 3.6, 50.0, 52.5, -100, 100, 8, 1.0, GOLD)
    for sx in (-1, 1):
        m.box(bd, sx * 2.0 - 2.0, 24.0, -4.4, sx * 2.0 + 2.0, 31.5, -3.6, PLATE, rotation=(-10, sx * 8, 0),
              pivot=(sx * 2.0, 31.5, -4.0))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab, sh = a[nm]["bone"], a[nm]["shoulder"]
        dome(m, ab, (sh[0] + sx * 1.0, 50.0, 0.2), 3.6, 3.6, PLATE_PLAIN, layers=3)
        a0, a1 = (25, 160) if sx > 0 else (-160, -25)
        shell(m, ab, (sh[0] + sx * 0.6, 0, 0.2), 4.0, 45.0, 50.5, a0, a1, 6, 0.9, PLATE)
        for j in range(3):                                                         # spikes along the pauldron
            spike(m, ab, (sh[0] + sx * 2.5, 52.0 - j * 1.6, 1.0 - j * 0.8), (sx * 1, 0.6, 0.2), 1.2, 3.0, GOLD, tip=0.3)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg, kn = a[nm]["bone"], a[nm]["knee"]
        shell(m, lg, kn, 2.4, 15.5, 22.0, -80, 80, 5, 0.9, PLATE)
        spike(m, lg, (kn[0], 19.0, kn[2] - 3.0), (0, 0.4, -1), 1.6, 2.6, GOLD, tip=0.3)
    # head: horned helm with a spiked crest
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.6, 2.9, 54.5, 61.5, helmf, cut=1)
    m.box(hd, -1.6, 54.0, -4.0, 1.6, 57.0, -2.4, PLATE_PLAIN, rotation=(-12, 0, 0), pivot=(0, 57, -2.4))
    for sx in (-1, 1):
        rod(m, hd, (sx * 2.4, 60.0, -0.5), (sx * 4.2, 63.5, 1.5), 1, SILVER, extend=0.2)
        spike(m, hd, (sx * 4.2, 63.5, 1.5), (sx * 0.4, 0.6, 1), 1.0, 3.0, SILVER, tip=0.25)
    for i in range(6):                                                              # spiked dark crest
        spike(m, hd, (0, 61.2, -1.6 + i * 1.2), (0, 1, 0.5 + i * 0.12), 1.2, 3.4 - i * 0.3, solid(P, "crest"), tip=0.3)
    # wings: curtains of long feathers fanned from its shoulders down past its heels
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
        w = m.bone(nm, bd, (sx * 3.0, 48.0, 3.2))
        m.round_box(w, sx * 4.0, 4.0, 2.4, 1.6, 44.0, 51.0, FEATHER, cut=1)
        for i in range(10):
            L = 32.0 + 10.0 * math.sin(i / 9 * math.pi)
            x0 = sx * (4.0 + i * 1.0)
            zz = 4.0 + i * 0.35
            m.box(w, x0 - 2.6, 50.0 - L, zz, x0 + 2.6, 52.0, zz,
                  cutout(feather_inside, featherf), rotation=(8, sx * (8 + i * 2.5), sx * (6 + i * 8.5)),
                  pivot=(x0, 52.0, zz))
    # the staff and its blazing rune circle
    al = a["arm_left"]["bone"]
    h = a["arm_left"]["hand"]
    rod(m, al, (h[0], 4.0, h[2] - 2.0), (h[0], 62.0, h[2] - 2.0), 1, GOLD, extend=0.0)
    for yy in (24.0, 44.0):
        m.round_box(al, h[0], h[2] - 2.0, 1.0, 1.0, yy, yy + 1.2, GOLD, cut=0)
    rc = m.bone("ring_runes", al, (h[0], 66.0, h[2] - 2.0))
    m.box(rc, h[0] - 7.0, 59.0, h[2] - 2.0, h[0] + 7.0, 73.0, h[2] - 2.0, runef)
    return m
