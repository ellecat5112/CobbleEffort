"""Iron Blast (Psychic/Dark), the future paradox Mewtwo, built from boxes after Elesteva076's art (the art's own name;
the art calls it "Mewthree").

A sleek armoured Mewtwo in black: a helmeted head swept back into a blade-like crest, a glowing pink visor and a pink
line running up its crest, a white collar over a glowing pink core at its throat, white shoulder pads dripping with
glowing pink plasma, white forearms, great round white thigh plates, long black legs on white claws, and a long
black tail whose end glows pink. Its right fist is sheathed in a white ring round a pink orb.

Shiny: white armour turned gold, and cyan plasma.

Front is -z, y is up. 67 units tall; about 1.7 blocks.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _mewtwo import mewtwo
from _pgen1 import stars
from _regi import ellipsoid, lit
from _route import pal, tone

HEIGHT = 67
SCALE = round(1.7 * 16 / HEIGHT, 3)
HITBOX = [1.0, HEIGHT / 16]
KIND = "biped"
K = 3
LOOK = ("a sleek black armoured Mewtwo with a blade-crested helmet and pink visor, white shoulder pads dripping "
        "glowing pink plasma, round white thigh plates, a pink-orb fist and a black tail glowing pink at its end")

BASE = {"black": (38, 38, 46), "black_light": (66, 66, 78), "grey": (96, 98, 110), "white": (232, 234, 240),
        "white_dark": (186, 190, 204), "pink": (255, 96, 196), "pink_light": (255, 186, 232), "star": (255, 255, 255)}
SHINY = {"white": (240, 206, 110), "white_dark": (196, 156, 70), "pink": (80, 226, 255), "pink_light": (190, 246, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def blackf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["black_light"] if face == "up" else p["black"], face), None


def chestf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(x) < 0.3 and y > 36:
        return p["pink"], p["pink"]
    if face == "north" and y > 44:
        return tone(p["grey"], face), None
    return blackf(x, y, z, face, variant)


def hipf(x, y, z, face, variant, **k):
    """White thigh plates below, the black belly above."""
    p = P(variant)
    if y < 30.8:
        return lit(p["white"] if face != "south" else p["white_dark"], face, y, 25.5, 5.6), None
    return blackf(x, y, z, face, variant)


def deltf(x, y, z, face, variant, **k):
    """White shoulder pads under a glowing pink plasma cap that drips down their front."""
    p = P(variant)
    drip = 50.6 - 1.6 * ((int(abs(x) * 2.2) % 3) / 2.0)
    if face == "up" or y > drip:
        c = p["pink_light"] if stars(x, y, z, face, cell=1.2, r=0.25, prob=0.3) else p["pink"]
        return c, c
    return tone(p["white"], face), None


def forearmf(x, y, z, face, variant, **k):
    p = P(variant)
    if (z % 2.2) < 0.35:
        return tone(p["white_dark"], face), None
    return tone(p["white"], face), None


def headf(x, y, z, face, variant, **k):
    """A black helmet: a glowing pink visor across the face and a pink line up the middle."""
    p = P(variant)
    if face == "north" and 58.2 < y < 59.4 and abs(x) < 2.6:
        return p["pink"], p["pink"]
    if face in ("east", "west") and 58.2 < y < 59.2 and z < -1.4:
        return p["pink"], p["pink"]
    if face in ("north", "up") and abs(x) < 0.3 and y > 59:
        return p["pink"], p["pink"]
    return lit(p["black"], face, y, 58.6, 3.4), None


def crestf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up" and abs(x - 0.0) < 0.35:
        return p["pink"], p["pink"]
    return blackf(x, y, z, face, variant)


def plasmaf(x, y, z, face, variant, **k):
    p = P(variant)
    c = p["pink_light"] if stars(x, y, z, face, cell=1.2, r=0.25, prob=0.35) else p["pink"]
    return c, c


def tailtipf(x, y, z, face, variant, **k):
    p = P(variant)
    if (z % 3.0) < 0.6:
        return tone(p["black"], face), None
    c = p["pink_light"] if stars(x, y, z, face, cell=1.3, r=0.26, prob=0.4) else p["pink"]
    return c, c


def build() -> Model:
    m = Model("ironblast")
    mats = {"skin": blackf, "chest": chestf, "abs": blackf, "pelvis": blackf, "neck": blackf, "deltoid": deltf,
            "upper_arm": blackf, "forearm": forearmf, "hand": blackf, "finger": blackf, "thigh": blackf,
            "knee": solid("white"), "shin": blackf, "foot": solid("white"), "toe": solid("white"),
            "head": headf, "muzzle": blackf, "tube": blackf, "tail": blackf, "tail_tip": tailtipf, "hip": hipf}
    a = mewtwo(m, mats, "ironblast", horns=False, tail_w=(4.4, 2.0))
    hd, bd = a["head"], a["body"]
    for p0, p1, w in (((0, 60.6, -1.6), (0, 64.0, 1.0), 2.6), ((0, 63.8, 0.8), (0, 66.4, 4.6), 1.8),
                      ((0, 66.2, 4.4), (0, 66.8, 6.4), 1.0)):
        rod(m, hd, p0, p1, w, crestf, extend=0.6, t2=2.2)                            # the blade crest
    for sx in (-1, 1):                                                              # swept side fins of the helmet
        rod(m, hd, (sx * 2.4, 60.0, 0.2), (sx * 3.0, 62.4, 3.6), 1.2, blackf, extend=0.4)
    for i, y in enumerate((50.6, 51.8, 53.0)):                                     # white collar rings
        m.round_box(bd, 0, 0.6, 2.6 - 0.2 * i, 2.4 - 0.2 * i, y, y + 0.8, solid("white"), cut=1)
    ellipsoid(m, bd, 0, 49.6, -2.4, 1.2, 1.2, 1.0, solid("pink", True), step=1)    # the glowing core at its throat
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):                         # pink plasma heaped on the shoulders
        ellipsoid(m, a[nm]["bone"], sx * 5.8, 51.4, 0.0, 2.8, 1.8, 2.8, plasmaf, step=1)
        spike(m, a[nm]["bone"], (sx * 7.6, 51.6, 0.0), (sx, 0.6, 0.2), 1.4, 3.0, plasmaf, tip=0.7)
    for i, nm in enumerate(("arm_left", "arm_right")):
        arm = a[nm]
        h = arm["hand"]
        if nm == "arm_right":                                                      # the wrist cannon
            rod(m, arm["bone"], (h[0], h[1] + 1.4, h[2]), (h[0], h[1] - 0.8, h[2] - 0.4), 3.8, solid("white"),
                extend=0.2)
            ellipsoid(m, arm["bone"], h[0], h[1] - 2.4, h[2] - 0.4, 1.7, 1.7, 1.7, solid("pink", True), step=1)
        else:                                                                       # plasma round the forearm
            w = arm["wrist"]
            ellipsoid(m, arm["bone"], w[0], w[1] + 2.0, w[2], 2.4, 2.2, 2.4, plasmaf, step=1)
            spike(m, arm["bone"], (w[0] + 1.6, w[1] + 2.6, w[2]), (1, 0.4, 0), 1.2, 2.8, plasmaf, tip=0.6)
    return m
