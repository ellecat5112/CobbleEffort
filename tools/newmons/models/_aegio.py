"""Aegiomon and the Aegiochusmon (CobbleEffort: Digital, built after the official art on wikimon.net): god-men with
goat's horns and legs (white armoured thigh-guards strapped over furred goat legs, black hooves). Aegiomon is a
white-haired youth with a red scarf, a black vest and one big white glove; Aegiochusmon a red-skinned giant with
tattoos, a fur mantle and long white hair. Its four other forms: Blue (blue cyber-armour and a giant floating
gauntlet), Dark (black fur, black wings, a scythe), Green (leaf armour, vine whips with spiked pink seed-pods), Holy
(white-gold armour, golden gear gauntlets, a halo and a sun of spikes behind it)."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _route import pal, tone

LOOKS = {
    "aegiomon": dict(skin=(250, 214, 190), body=(36, 36, 44), hair=(236, 236, 240), horn=(52, 50, 58),
                     fur=(130, 96, 70), fur_dark=(96, 68, 50), armour=(232, 234, 240), armour_dark=(160, 164, 176),
                     accent=(210, 40, 40), eye=(200, 40, 40)),
    "aegiochusmon": dict(skin=(196, 64, 52), body=(196, 64, 52), hair=(240, 240, 244), horn=(70, 66, 74),
                         fur=(170, 132, 90), fur_dark=(120, 90, 60), armour=(232, 234, 240), armour_dark=(160, 164, 176),
                         accent=(130, 24, 30), eye=(250, 220, 90)),
    "aegiochusmonblue": dict(skin=(240, 210, 190), body=(236, 238, 244), hair=(220, 226, 240), horn=(70, 80, 120),
                             fur=(220, 224, 236), fur_dark=(150, 160, 190), armour=(40, 90, 210), armour_dark=(24, 54, 140),
                             accent=(40, 90, 210), eye=(240, 60, 60)),
    "aegiochusmondark": dict(skin=(60, 56, 66), body=(34, 32, 40), hair=(30, 28, 34), horn=(40, 38, 46),
                             fur=(44, 42, 50), fur_dark=(26, 24, 30), armour=(70, 68, 78), armour_dark=(40, 38, 46),
                             accent=(220, 40, 60), eye=(255, 50, 50)),
    "aegiochusmongreen": dict(skin=(230, 220, 180), body=(90, 160, 60), hair=(170, 220, 120), horn=(60, 90, 50),
                              fur=(110, 120, 60), fur_dark=(70, 80, 40), armour=(232, 234, 230), armour_dark=(150, 170, 140),
                              accent=(230, 80, 150), eye=(250, 220, 90)),
    "aegiochusmonholy": dict(skin=(250, 226, 200), body=(240, 236, 226), hair=(240, 232, 210), horn=(200, 160, 60),
                             fur=(236, 228, 210), fur_dark=(190, 180, 160), armour=(232, 186, 60), armour_dark=(170, 126, 30),
                             accent=(232, 186, 60), eye=(90, 160, 240)),
}


def palette(kind):
    base = dict(LOOKS[kind], hoof=(30, 28, 32), white=(250, 250, 250), pupil=(20, 18, 22), gold=(232, 186, 60),
                vine=(70, 150, 50), pod=(230, 90, 150), blade=(200, 30, 50), glow=(255, 220, 120))
    shiny = {"body": tuple(min(255, int(c * 0.6 + 60)) for c in base["body"]),
             "armour": tuple(255 - c // 2 for c in base["armour"]), "fur": (210, 210, 220), "accent": (60, 200, 220),
             "skin": tuple(min(255, int(c * 0.85 + 30)) for c in base["skin"])}

    def P(v):
        return pal(base, shiny, v)
    return P


def build_goat(name, kind, height=34) -> Model:
    P = palette(kind)

    def solid(key, glow=False):
        def s(x, y, z, face, variant, **k):
            p = P(variant)
            return tone(p[key], face), (p[key] if glow else None)
        return s

    def furf(x, y, z, face, variant, **k):
        p = P(variant)
        return tone(p["fur_dark"] if (x * 2 + y * 3 + z) % 4 < 1 else p["fur"], face), None

    def thighf(x, y, z, face, variant, **k):
        p = P(variant)
        if face != "up" and face != "down" and (abs(y - 12.5) < 0.4 or abs(y - 10.5) < 0.4):
            return tone(p["armour_dark"], face), None                  # straps
        return tone(p["armour"], face), None

    def torsof(x, y, z, face, variant, **k):
        p = P(variant)
        if kind == "aegiomon":
            if face == "north" and abs(x) < 1.6 and y < 22.5:
                return tone(p["skin"], face), None                     # bare midriff under the open vest
            return tone(p["body"], face), None
        if kind == "aegiochusmon" and face == "north" and abs(abs(x) - 1.8 - 0.4 * math.sin(y)) < 0.35:
            return tone(p["accent"], face), None                       # tattoo lines
        return tone(p["body"], face), None

    def headf(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                if abs(x - sx * 1.2) < 0.7 and abs(y - 29.4) < 0.45:
                    return p["eye"], None
            if y > 30.6:
                return tone(p["hair"], face), None
            return tone(p["skin"], face), None
        if y > 29.6 or face in ("up", "south"):
            return tone(p["hair"], face), None
        return tone(p["skin"], face), None

    big = kind != "aegiomon"
    w = 1.4 if big else 1.15                                           # Aegiochusmon is broader
    m = Model(name)
    top = m.bone(name, None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    m.round_box(bd, 0, 0.5, 2.6 * w, 1.8 * w, 14.5, 18.0, solid("armour_dark"), cut=0.6)   # belt/hips
    m.round_box(bd, 0, 0.3, 3.0 * w, 2.0 * w, 17.8, 25.5, torsof, cut=0.8)               # torso
    if big:
        m.round_box(bd, 0, 0.6, 4.6, 2.8, 24.0, 26.5, furf if kind != "aegiochusmonholy" else solid("armour"), cut=1.0)
    hd = m.bone("head", bd, (0, 26, 0))
    m.round_box(hd, 0, 0, 2.2, 2.3, 26.0, 31.8, headf, cut=0.7)
    m.box(hd, -2.6, 30.8, -1.8, 2.6, 32.6, 2.6, solid("hair"))                           # spiky hair
    for i, (dx, dz) in enumerate(((0, 2.4), (-1.4, 1.8), (1.4, 1.8), (0, 3.4))):
        spike(m, hd, (dx, 31.5, dz), (dx * 0.3, 0.4 if i < 3 else -0.6, 1), 1.2, 3.0 if big and i == 3 else 1.8,
              solid("hair"), tip=0.4)
    if big:                                                                              # long white mane down its back
        rod(m, hd, (0, 30.0, 1.6), (0, 20.0, 4.0), 3.2, solid("hair"), extend=0.3, t2=1.0)
    for sx in (-1, 1):                                                                   # curled goat horns
        rod(m, hd, (sx * 1.6, 31.6, 0.2), (sx * 2.6, 33.6, 1.4), 1.1, solid("horn"), extend=0.2)
        spike(m, hd, (sx * 2.6, 33.6, 1.4), (sx * 0.5, -0.2, 1), 1.0, 2.4, solid("horn"), tip=0.3)
    if kind == "aegiomon":                                                               # the red scarf
        m.box(hd, -2.0, 25.6, -2.0, 2.0, 26.8, 2.0, solid("accent"))
        rod(m, hd, (1.2, 26.0, 1.8), (2.6, 23.0, 5.0), 1.2, solid("accent"), extend=0.2, t2=0.4)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        a = m.bone(nm, bd, (sx * 3.2 * w, 24.5, 0.3))
        rod(m, a, (sx * 3.2 * w, 24.5, 0.3), (sx * 3.8 * w, 20.0, 0.0), 1.4 * w, solid("skin"), extend=0.3)
        rod(m, a, (sx * 3.8 * w, 20.0, 0.0), (sx * 4.0 * w, 16.2, -0.8), 1.6 * w,
            solid("armour" if kind in ("aegiochusmonblue", "aegiochusmonholy") else "skin"), extend=0.3)
        if kind == "aegiomon" and sx == -1:                                              # its big white glove
            m.round_box(a, sx * 4.0, -0.9, 1.6, 1.6, 13.8, 17.0, solid("white"), cut=0.5)
        elif kind == "aegiochusmonholy":                                                 # a golden gear on each fist
            gear(m, a, (sx * 4.6 * w, 15.6, -0.8), 3.0, solid("gold"))
        else:
            m.round_box(a, sx * 4.0 * w, -0.8, 1.0 * w, 1.1 * w, 14.6, 16.4, solid("skin"), cut=0.3)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.6 * w, 15.0, 0.4))
        m.round_box(lg, sx * 1.8 * w, 0.4, 1.6 * w, 1.7 * w, 9.0, 15.2, thighf, cut=0.5)  # armoured thigh-guard
        rod(m, lg, (sx * 1.9 * w, 9.4, 0.4), (sx * 2.0 * w, 4.6, 2.2), 2.0 * w, furf, extend=0.4)   # goat shin
        rod(m, lg, (sx * 2.0 * w, 4.6, 2.2), (sx * 2.0 * w, 1.2, 0.6), 1.6 * w, furf, extend=0.3)
        m.box(lg, sx * 2.0 * w - 1.0 * w, 0.0, -0.6, sx * 2.0 * w + 1.0 * w, 1.4, 1.4, solid("hoof"))
    tl = m.bone("tail", bd, (0, 15.5, 1.8))
    spike(m, tl, (0, 15.5, 1.8), (0, 0.4, 1), 1.0, 2.4, furf, tip=0.4)
    # the forms' own parts
    if kind == "aegiochusmonblue":                                                       # the giant floating gauntlet
        g = m.bone("gauntlet", bd, (-11, 26, -2))
        m.round_box(g, -11, -2, 4.0, 3.4, 20.0, 29.0, solid("armour"), cut=1.2)
        for i in range(4):
            rod(m, g, (-13.2 + i * 1.5, 29.0, -3.0), (-13.4 + i * 1.6, 34.5, -4.5), 1.3, solid("armour_dark"), extend=0.2)
        rod(m, g, (-8.0, 25.0, -3.0), (-6.0, 29.0, -5.0), 1.4, solid("armour_dark"), extend=0.2)
        m.box(g, -12.0, 23.5, -5.5, -10.0, 25.5, -5.3, solid("accent", glow=True))
    if kind == "aegiochusmondark":
        for sx, nm in ((1, "wing_left"), (-1, "wing_right")):                           # black wings
            wb = m.bone(nm, bd, (sx * 1.5, 24.5, 2.0))
            for i in range(5):
                ang = math.radians(20 + i * 18)
                tip = (sx * (2 + 9 * math.cos(ang)), 24.5 + 9 * math.sin(ang), 2.0 + 3.0 + i * 0.6)
                rod(m, wb, (sx * 1.5, 24.5, 2.0), tip, 1.4, solid("body"), extend=0.2, t2=0.5)
        s = m.bone("scythe", bd, (5.0, 16.0, -1.0))                                     # the scythe
        rod(m, s, (5.0, 6.0, -1.0), (5.0, 34.0, -1.0), 0.8, solid("armour"), extend=0.0)
        rod(m, s, (5.0, 34.0, -1.0), (5.0, 31.0, -8.0), 1.6, solid("blade", glow=True), extend=0.0, t2=0.4)
    if kind == "aegiochusmongreen":                                                      # vine whips with seed-pods
        for sx in (-1, 1):
            vb = m.bone(f"vine_{'left' if sx > 0 else 'right'}", bd, (sx * 5.0, 16.0, -1.0))
            pts = [(sx * 5.0, 16.0, -1.0), (sx * 8.0, 12.0, -4.0), (sx * 11.0, 14.0, -6.0), (sx * 13.0, 18.0, -6.0)]
            for a1, b1 in zip(pts, pts[1:]):
                rod(m, vb, a1, b1, 0.8, solid("vine"), extend=0.2)
            m.round_box(vb, sx * 13.0, -6.0, 1.4, 1.4, 17.0, 19.8, solid("pod"), cut=0.5)
            for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1)):
                spike(m, vb, (sx * 13.0, 18.4, -6.0), d, 0.6, 1.4, solid("pod"), tip=0.2)
    if kind == "aegiochusmonholy":                                                       # halo + sun of spikes
        m.box(hd, -1.8, 34.6, -1.8, 1.8, 35.0, 1.8, solid("blade", glow=True))
        m.box(hd, -1.2, 34.6, -1.2, 1.2, 35.1, 1.2, solid("pupil"))
        sb = m.bone("sun", bd, (0, 24, 4.5))
        for i in range(10):
            ang = math.radians(i * 36)
            spike(m, sb, (0, 24, 4.5), (math.cos(ang), math.sin(ang), 0.15), 1.4, 6.0, solid("gold", glow=True), tip=0.3)
    return m


def gear(m, bone, c, r, shader):
    """A golden gear facing forward: a disc of crossed boxes with teeth."""
    x, y, z = c
    for i in range(3):
        a = math.radians(i * 30)
        m.box(bone, x - r, y - r * 0.5, z - 0.5, x + r, y + r * 0.5, z + 0.5, shader, rotation=(0, 0, i * 60),
              pivot=(x, y, z))
    for i in range(8):
        ang = math.radians(i * 45)
        spike(m, bone, (x + r * math.cos(ang), y + r * math.sin(ang), z), (math.cos(ang), math.sin(ang), 0), 0.8, 0.9,
              shader, tip=0.6)
