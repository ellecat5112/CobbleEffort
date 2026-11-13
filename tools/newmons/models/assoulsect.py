"""Assoulsect, the Hive Mind Pokémon (Bug/Ghost), built from boxes after the concept art the user shared (the art's own
name; art by @mazenta_inku), with the user's idea: thousands of fallen Bug Pokémon bound into one corrupt hive mind by
a zombie-ant fungus (Ophiocordyceps unilateralis).

A swollen violet fog-cloud of souls on a dark armoured base and two thin black legs with red-and-white hooked feet.
The heads of the fallen are sunk in the fog: a red horned beetle face in the middle (its main head), a red cricket head
with long antennae and black curled whiskers on top, a gold ninja mask on its right and a green rock-scaled head on
its left. Their weapons bristle out all round: a blue forked horn rising from the top, a grey spiked scythe and a red
striped horn on the left, a crooked blue-grey lance and a white cone lance below them, a violet wing with a gold
crescent and two red bladed legs on the right, and two long white claws hanging from the base. Ophiocordyceps
stalks (dark, with swollen tan fruiting tips that glow with spores) sprout from the heads and the cloud, and a
translucent haze of souls drifts round the fog.

Shiny: the fungus has won. A mossy green fog, the armour dark teal, the gold silver, and the spore tips glow red.

Front is -z, y is up. 48 units tall to the top of the horn; baseScale 0.75 (2.25 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, mix, rod, spike
from _route import pal, tone

SCALE = 0.75
HITBOX = [1.5, 2.3]
KIND = "biped"
K = 4
HEIGHT = 50
LOOK = ("a violet fog-cloud of fallen bug souls on two thin black legs, with bug heads sunk in it and blades, horns, "
        "lances and a wing bristling out, overgrown by glowing cordyceps fungus stalks")

BASE = {"fog": (138, 112, 196), "fog_light": (176, 156, 226), "fog_dark": (96, 72, 156), "haze": (196, 176, 240),
        "robe": (54, 40, 104), "robe_dark": (34, 26, 70), "gold": (214, 172, 78), "gold_dark": (150, 112, 44),
        "leg": (44, 42, 52), "leg_light": (92, 90, 104), "foot_red": (168, 40, 44), "white": (236, 236, 242),
        "red": (198, 74, 46), "red_dark": (130, 44, 34), "black": (22, 20, 28), "green": (138, 196, 120),
        "green_dark": (84, 140, 84), "blue": (86, 140, 196), "blue_dark": (54, 92, 146), "steel": (176, 178, 190),
        "steel_dark": (120, 122, 138), "stripe": (176, 70, 96), "stripe_light": (220, 150, 168),
        "lance": (122, 146, 176), "wing": (70, 40, 120), "crimson": (210, 64, 54),
        "stalk": (70, 52, 40), "stalk_light": (124, 96, 66), "spore": (214, 176, 112), "spore_glow": (200, 176, 96)}
SHINY = {"fog": (110, 158, 104), "fog_light": (150, 196, 132), "fog_dark": (70, 116, 76), "haze": (176, 222, 160),
         "robe": (30, 76, 80), "robe_dark": (18, 48, 54), "gold": (200, 206, 214), "gold_dark": (130, 136, 150),
         "wing": (30, 86, 84), "spore": (220, 120, 96), "spore_glow": (220, 80, 60)}


def P(v):
    return pal(BASE, SHINY, v)


def blob(x, y, z, cx, cy, cz):
    """Soft violet light spots on the fog (deterministic, from model space)."""
    v = math.sin(x * 0.9 + cz * 0.3) * math.cos(y * 0.8 - cx * 0.2) + math.sin((z + y) * 0.7 + cy)
    return v


def fogf(cx=0.0, cy=0.0, cz=0.0):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        v = blob(x, y, z, cx, cy, cz)
        c = p["fog"]
        if v > 1.0:
            c = mix(p["fog"], p["fog_light"], min(1.0, (v - 1.0) * 1.6))      # lighter soul-lumps
        elif v < -1.1:
            c = mix(p["fog"], p["fog_dark"], min(1.0, (-v - 1.1) * 1.8))
        return tone(c, face), None
    return s


def hazef(x, y, z, face, variant, **k):
    """The translucent haze of souls round the fog (painted part-transparent: the shell layer)."""
    p = P(variant)
    v = blob(x * 1.3, y * 1.3, z * 1.3, 1, 2, 3)
    a = 120 if v > 0.3 else 70
    return tuple(p["haze"]) + (a,), None


def robef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(x) + abs(y - 19.5) * 1.2 < 3.2:            # gold diamond plate on the front
        return (p["gold"] if abs(x) + abs(y - 19.5) * 1.2 < 2.4 else p["gold_dark"]), None
    if face == "north" and abs(abs(x) - 3.4) < 0.6 and y > 20:             # gold seams
        return p["gold_dark"], None
    return tone(p["robe"] if y > 17 else p["robe_dark"], face), None


def podf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("north", "south") and 18.5 < y < 20:
        return p["gold"], None
    return tone(mix(p["robe"], p["fog_dark"], 0.35), face), None


def legf(x, y, z, face, variant, **k):
    p = P(variant)
    if 13 < y < 14.4:
        return p["gold"], None                                               # gold band at the knee
    if face == "north" and abs(x - round(x)) < 0.25 and y > 6:
        return p["leg_light"], None                                          # armour plate edges
    return tone(p["leg"], face), None


def footf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["white"] if z < -1.2 or y < 0.8 else p["foot_red"], face), None


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return tone(c, face), (c if glow else None)
    return s


def beetlef(x, y, z, face, variant, **k):
    """The main head: a red-orange beetle face with two big black eyes."""
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot((x - sx * 1.2) / 0.9, (y - 29.2) / 1.0) < 1:
                return p["black"], None
        if abs(y - 27.6) < 0.25 and abs(x) < 1.0:
            return p["red_dark"], None
    return tone(p["red"], face), None


def cricketf(x, y, z, face, variant, **k):
    """The top head: a dark red cricket head with black eyes."""
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot((x - sx * 1.1) / 0.75, (y - 40.6) / 0.8) < 1:
                return p["black"], None
    return tone(p["red_dark"] if y < 39.6 else mix(p["red_dark"], p["red"], 0.4), face), None


def maskf(x, y, z, face, variant, **k):
    """The gold ninja mask on its right: black eye holes and white mouth bars."""
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot((x - 6.0 - sx * 1.0) / 0.7, (y - 33.6) / 0.6) < 1:
                return p["black"], None
        if 31.4 < y < 32.6 and abs(x - 6.0) < 1.6:
            return (p["white"] if int((x - 4.4) * 2.5) % 2 == 0 else p["black"]), None
    return tone(p["gold"] if y > 32.6 else p["gold_dark"], face), None


def greenf(x, y, z, face, variant, **k):
    """The green rock-scaled head on its left: a dark eye slit and scale lines."""
    p = P(variant)
    if face in ("north", "west") and abs(y - 29.3) < 0.3 and -8.8 < x < -6.8:
        return p["black"], None
    if (int(y * 1.5) + int(z * 1.5)) % 3 == 0:
        return tone(p["green_dark"], face), None
    return tone(p["green"], face), None


def stripef(x, y, z, face, variant, **k):
    p = P(variant)
    t = (x * 0.6 + y * 0.8) % 2.2
    return tone(p["stripe"] if t < 1.1 else p["stripe_light"], face), None


def scythef(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(mix(p["steel"], p["white"], 0.25) if face in ("up", "north") else p["steel"], face), None


def wingf(x, y, z, face, variant, **k):
    """The violet wing: a gold crescent and a red swirl, on both faces."""
    p = P(variant)
    u, v = x - 10.5, y - 38.5
    r = math.hypot(u, v)
    if 1.6 < r < 2.4 and u > -0.6:
        return p["gold"], None
    if 0.6 < math.hypot(u + 1.8, v + 2.2) < 1.2:
        return p["crimson"], None
    edge = y > 43.2 or x > 15.2
    return tone(p["wing"] if not edge else p["robe_dark"], face), None


def stalkf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["stalk"] if (int(y * 2) % 3) else p["stalk_light"], face), None


def sporef(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["spore"], face), p["spore_glow"]


def clump(m, bone, cx, cy, cz, rx, ry, rz, shader):
    """A rounded fog clump: three stacked rounded blocks (narrower at top and bottom)."""
    m.round_box(bone, cx, cz, rx * 0.72, rz * 0.72, cy - ry, cy - ry * 0.45, shader)
    m.round_box(bone, cx, cz, rx, rz, cy - ry * 0.5, cy + ry * 0.5, shader)
    m.round_box(bone, cx, cz, rx * 0.72, rz * 0.72, cy + ry * 0.45, cy + ry, shader)


def cordyceps(m, bone, base, d, h):
    """An Ophiocordyceps stalk: a thin dark stalk with a swollen, spore-glowing fruiting tip."""
    n = math.sqrt(sum(v * v for v in d))
    u = tuple(v / n for v in d)
    tip = tuple(b + v * h for b, v in zip(base, u))
    rod(m, bone, base, tip, 1, stalkf, extend=0.5)
    rod(m, bone, tuple(t - v * 0.3 for t, v in zip(tip, u)), tuple(t + v * 1.7 for t, v in zip(tip, u)), 1.4, sporef,
        extend=0, t2=1.4)


def build() -> Model:
    m = Model("assoulsect")
    top = m.bone("assoulsect", None, (0, 0, 0))

    # legs: thin black armour, gold knee bands, red-and-white hooked feet
    for nm, lx in (("leg_left", -3.6), ("leg_right", 3.6)):
        lg = m.bone(nm, top, (lx, 16, 0))
        m.box(lg, lx - 1.5, 9, -1.5, lx + 1.5, 17, 1.5, legf)                    # thigh plate
        m.box(lg, lx - 1, 2, -1, lx + 1, 9.5, 1, legf)                            # shin
        m.box(lg, lx - 1.4, 0, -3, lx + 1.4, 2, 1.5, footf)                       # foot
        spike(m, lg, (lx, 0.6, 1.2), (0, -0.2, 1), 1.2, 2, footf)                 # hooked heel spur

    bd = m.bone("body", top, (0, 18, 0))
    # the armoured base (a dark robe with a gold diamond) and its side pods
    m.round_box(bd, 0, 0, 6, 4.5, 14.5, 24, robef, cut=1.5)
    for sx in (-1, 1):
        m.round_box(bd, sx * 6.2, 0.5, 2.2, 3, 15.5, 23, podf, cut=0.8)
    # the fog of souls: a big swollen cloud of clumps
    clump(m, bd, 0, 30, 0.5, 8.5, 7.5, 6.5, fogf(0, 0, 0))
    clump(m, bd, -1, 37.5, 0.5, 6.5, 4.5, 5, fogf(1, 2, 0))
    clump(m, bd, -6.5, 28, -0.5, 4.5, 5, 4.5, fogf(2, 1, 1))
    clump(m, bd, 6.5, 31, 0.5, 4.5, 5, 4.5, fogf(0, 3, 2))
    clump(m, bd, 1.5, 24.8, -2, 6, 3.5, 4.5, fogf(3, 0, 1))
    clump(m, bd, -3.5, 41, 1, 3.5, 2.5, 3, fogf(2, 2, 2))                       # lumps on the top...
    clump(m, bd, 3.5, 40, 0, 3, 2.5, 3, fogf(1, 3, 1))
    clump(m, bd, 8, 26.5, -0.5, 3, 3, 3, fogf(3, 1, 0))                         # ...and the sides
    clump(m, bd, -9.5, 32.5, 1, 2.5, 2.5, 2.5, fogf(0, 1, 3))
    clump(m, bd, 0, 32, 6, 5.5, 5, 2.5, fogf(2, 0, 2))                           # back
    # wisps of souls drifting off the fog (translucent: the shell layer)
    for cx, cy, cz, r in ((-10.5, 38, 2, 2), (10.5, 37, 3, 2.2), (-4, 45, 3, 1.6), (5.5, 45, 2.5, 1.5), (0, 33, 9.5, 2)):
        clump(m, bd, cx, cy, cz, r, r, r, hazef)

    # the heads of the fallen
    hd = m.bone("head", bd, (0, 28, -6))
    m.round_box(hd, 0, -6.8, 2.4, 1.8, 26.5, 31, beetlef, cut=0.7)               # main head: red beetle face
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.3, 30.6, -7.2), (sx * 0.2, 1, -0.15), 1, 2.6, solid("black"))   # two black horns
    ht = m.bone("head_top", bd, (0, 39, -4))
    m.round_box(ht, 0, -4.5, 2, 1.8, 38.8, 42.4, cricketf, cut=0.7)              # cricket head on top
    for sx in (-1, 1):
        a = (sx * 0.9, 42, -4.8)
        b = (sx * 3.4, 45.5, -6)
        rod(m, ht, a, b, 0.5, solid("red_dark"), extend=0, t2=0.5)               # long antennae...
        m.box(ht, b[0] - 0.6, b[1] - 0.6, b[2] - 0.6, b[0] + 0.6, b[1] + 0.6, b[2] + 0.6, solid("red"))  # ...knobbed
        for i in range(3):                                                     # black curled whiskers
            ang = math.radians(-60 - i * 50)
            p0 = (sx * (1.4 + i * 0.7), 38.8 - i * 0.6, -6.3)
            p1 = (p0[0] + sx * 0.9 * math.cos(ang), p0[1] + 0.9 * math.sin(ang), -6.4)
            rod(m, ht, p0, p1, 0.6, solid("black"), extend=0.3, t2=0.6)
    hm = m.bone("head_mask", bd, (6, 33, -4))
    m.round_box(hm, 6, -4.6, 2.2, 1.6, 31, 35, maskf, cut=0.6)                   # gold ninja mask on its right
    for sx in (-1, 1):
        spike(m, hm, (6 + sx * 1.8, 34.8, -4.6), (sx * 0.6, 1, 0), 0.8, 1.6, solid("gold"))
    hg = m.bone("head_green", bd, (-7, 28, -3))
    m.round_box(hg, -7.6, -3.5, 1.8, 2.4, 26.6, 31, greenf, cut=0.7)             # green rock-scaled head, left
    spike(m, hg, (-7.6, 30.8, -3.6), (-0.2, 1, 0.3), 1.6, 3, greenf, tip=0.8)    # its crest
    spike(m, hg, (-9.2, 29, -4.5), (-1, 0.1, -0.6), 1.4, 2.6, solid("green"))    # snout

    # the blue forked horn on top
    hn = m.bone("horn", bd, (0, 41, 0))
    rod(m, hn, (0, 40.5, 0.5), (0, 47, 0.5), 2, solid("blue"), extend=0)
    for sx in (-1, 1):
        rod(m, hn, (0, 46.5, 0.5), (sx * 3, 50, 0.5), 1.4, solid("blue"), extend=0.4, t2=1.4)
    m.box(hn, -0.5, 45.5, -0.5, 0.5, 47.5, 1.5, solid("blue_dark"))

    # left side: grey spiked scythe, red striped horn, crooked lance, white cone lance
    al = m.bone("arm_left", bd, (-6, 33, 0))
    pts = [(-6, 34, 1), (-9, 38.5, 1.5), (-11.5, 42, 2), (-12.5, 45.5, 2.5), (-12, 48, 3)]
    for a, b, t in zip(pts, pts[1:], (2.6, 2.4, 2, 1.4)):
        rod(m, al, a, b, t, scythef, t2=1.2)
    for a, b in zip(pts[:3], pts[1:4]):
        mid = tuple((aa + bb) / 2 for aa, bb in zip(a, b))
        spike(m, al, mid, (1, -0.3, 0), 1, 1.8, solid("white"))                 # spikes along its inner edge
    pts = [(-8, 30, 0), (-11.5, 30.5, 0.5), (-14, 32.5, 1), (-15.5, 35, 1.5)]
    for a, b, t in zip(pts, pts[1:], (2.2, 1.8, 1.2)):
        rod(m, al, a, b, t, stripef)                                             # red striped horn
    pts = [(-6, 22, -1), (-9, 18, -1.5), (-8.5, 14, -1.5), (-11.5, 9, -2), (-12, 6, -2)]
    for a, b, t in zip(pts, pts[1:], (1.8, 1.6, 1.4, 1)):
        rod(m, al, a, b, t, solid("lance"))                                      # crooked blue-grey lance
    rod(m, al, (-3, 26, -5), (-7.5, 20.5, -7.5), 3, solid("white"), extend=0)  # white cone lance
    rod(m, al, (-7, 21, -7.3), (-9.5, 18, -8.5), 1.6, solid("white"), extend=0)

    # right side: the violet wing with its red bladed legs, and two long white claws from the base
    ar = m.bone("arm_right", bd, (6, 36, 1))
    m.box(ar, 5, 32, 1, 16, 44, 1, wingf, rotation=(0, -30, -10), pivot=(5, 36, 1))   # wing plane (both faces)
    for i, (dy, ln) in enumerate(((0, 9), (2.5, 8))):
        a = (10 + i, 38 + dy, 2)
        b = (a[0] + ln * 0.8, a[1] - ln * 0.6, 2.5)
        rod(m, ar, a, b, 1, solid("crimson"), t2=1)                              # red bladed legs
        spike(m, ar, b, (0.8, -0.6, 0), 0.8, 2, solid("black"))
    cl = m.bone("claws", bd, (6, 22, 0))
    rod(m, cl, (6, 22, 0), (10, 17, -1), 2.2, solid("leg"))
    for dz in (-1.6, 0.8):
        rod(m, cl, (9.6, 17.5, dz - 0.5), (12, 8.5, dz - 1), 1.2, solid("white"), t2=1.6)   # long white claws

    # Ophiocordyceps: fungus stalks sprouting from the heads and the fog, their tips glowing with spores
    cordyceps(m, hd, (1.5, 30, -7.5), (0.4, 1, -0.5), 3.5)
    cordyceps(m, ht, (-1.2, 42, -4), (-0.4, 1, -0.2), 3)
    cordyceps(m, hm, (6.6, 35, -4.4), (0.5, 1, -0.3), 3)
    cordyceps(m, hg, (-8.2, 30.5, -3), (-0.6, 1, 0.1), 3)
    for base, d, h in (((2.5, 42, 1), (0.3, 1, 0.2), 4), ((-5, 43, 2), (-0.5, 1, 0.4), 3), ((3, 34, 8), (0.2, 0.6, 1), 3),
                       ((-4, 30, 8), (-0.3, 0.4, 1), 3)):
        cordyceps(m, bd, base, d, h)
    return m
