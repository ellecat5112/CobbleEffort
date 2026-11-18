"""Shared builder for Omegamon and its forms (CobbleEffort: Digital; hand-built after the official art on wikimon.net):
the Royal Knight born of War Greymon and Metal Garurumon: a towering knight in white plate trimmed blue and gold on
long digitigrade legs with golden talons, a horned crested helm with a red visor, a great cape white without and red
within, its left arm the golden War Greymon head with the Grey Sword sliding out of the mouth, its right arm the blue
Metal Garurumon head with the Garuru Cannon. Looks: "base"; "x" (X-Antibody: blue-violet plate, more gold spikes, a
rune-engraved sword); "merciful" (Merciful Mode: silver-white plate and great feathered wings of ice-blue light, the
sword a blade of blue light); "shuangwu" (Shuang Wu: two great cannons and a crimson dragon gauntlet); "zwart" (black
plate, a black cape lined red); "zwartdefeat" (Zwart Defeat: black, tattered and broken, a red-lit blade).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, feather_wing
from _digibody import cape, humanoid
from _digidetail import armour, fabric, feathers, local, metal, solid
from _route import pal, tone

LOOKS = {"base": {"plate": (240, 242, 248), "plate_dark": (150, 156, 180), "trim": (60, 90, 200)},
         "x": {"plate": (120, 130, 210), "plate_dark": (50, 56, 130), "trim": (230, 190, 70)},
         "merciful": {"plate": (236, 240, 250), "plate_dark": (170, 186, 210), "trim": (120, 200, 250)},
         "shuangwu": {"plate": (230, 232, 240), "plate_dark": (140, 146, 170), "trim": (90, 80, 190)},
         "zwart": {"plate": (40, 40, 48), "plate_dark": (12, 12, 16), "trim": (230, 190, 70)},
         "zwartdefeat": {"plate": (34, 32, 38), "plate_dark": (10, 10, 12), "trim": (120, 30, 30)}}
COMMON = {"gold": (236, 196, 70), "gold_dark": (160, 120, 20), "orange": (240, 140, 40), "blue": (70, 110, 210),
          "blue_dark": (24, 44, 130), "red": (200, 30, 40), "red_dark": (110, 10, 16), "steel": (220, 224, 236),
          "steel_dark": (110, 114, 126), "visor": (220, 40, 50), "cape_out": (246, 246, 250), "black": (30, 30, 36),
          "light": (130, 210, 255, 190), "redglow": (255, 60, 60)}


def make(name, look="base"):
    base = dict(COMMON, **LOOKS[look])
    if look in ("zwart", "zwartdefeat"):
        base["cape_out"] = (36, 34, 40)
    shiny = dict(base, plate=(250, 220, 120), plate_dark=(170, 130, 40)) if look not in ("zwart", "zwartdefeat") \
        else dict(base, plate=(230, 230, 240), plate_dark=(150, 150, 170))

    def P(v):
        return pal(base, shiny, v)

    PLATE = armour(P, "plate", "plate_dark", trim="trim", trim_w=0.3)
    GOLD = metal(P, "gold", dark="gold_dark")
    STEEL = metal(P, "steel", dark="steel_dark")

    def capef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        return tone(p["red"] if face == "north" else p["cape_out"], face), None

    def runef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if look == "zwartdefeat":
            return p["redglow"], p["redglow"]
        if look == "merciful":
            return p["light"], p["light"][:3]
        if look == "x" and face not in ("up", "down") and int(y * 1.3) % 3 == 0:
            return tone(p["gold"], face), None
        return STEEL(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": PLATE, "neck": STEEL, "upper_arm": PLATE, "thigh": PLATE, "knee": GOLD, "talon": GOLD,
                "foot": PLATE}
        a = humanoid(m, mats, bulk=1.1, arm_bulk=1.1, leg_bulk=1.05, talons=True, digitigrade=True, name=name)
        bd = a["body"]
        for sx in (-1, 1):                                                             # spiked pauldrons
            m.round_box(bd, sx * 8.4, 0.0, 3.4, 3.6, 46.0, 53.0, PLATE, cut=1)
            for j in range(2 if look != "x" else 4):
                spike(m, bd, (sx * 10.0, 52.0 - j, -1.0 + j * 1.4), (sx * 0.6, 1, 0.2), 1.4, 5.0, GOLD, tip=0.8)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.0, 60.0, PLATE, cut=1)                    # crested helm
        m.box(hd, -1.8, 57.2, -3.3, 1.8, 58.0, -3.1, solid(P, "visor", glow=True))
        for sx in (-1, 1):
            spike(m, hd, (sx * 1.8, 60.0, -0.6), (sx * 0.5, 1, 0.6), 1.4, 7.0, PLATE, tip=0.8)
            spike(m, hd, (sx * 2.6, 57.0, 0.6), (sx * 1, 0.3, 0.4), 1.0, 4.0, GOLD, tip=0.8)
        spike(m, hd, (0, 60.0, -2.0), (0, 1, -0.3), 1.2, 4.0, GOLD, tip=0.8)
        if look == "merciful":                                                          # feathered wings of light
            wb = m.bone("wings", bd, (0, 49, 3))
            for side in (1, -1):
                feather_wing(m, wb, (side * 3.0, 49.0, 3.0), 26.0, 16.0, 6, feathers(P, "plate", "trim"), side=side,
                             sweep=25, droop=-12.0)
        else:
            cs = capef
            cape(m, bd, 52.0, 20.0, 46.0 if look != "zwartdefeat" else 40.0, cs, z=4.0,
                 flare=1.2 if look != "zwartdefeat" else 1.8, panels=7, seed=11 if look != "zwartdefeat" else 13)
        al = a["arm_left"]                                                             # War Greymon head + sword
        w = al["wrist"]
        head_key = "red" if look == "shuangwu" else ("black" if look.startswith("zwart") else "orange")
        m.round_box(al["bone"], w[0], w[2] - 2.0, 2.8, 4.4, w[1] - 3.0, w[1] + 2.0,
                    armour(P, head_key, "red_dark", trim="gold", trim_w=0.25), cut=1)
        for sx in (-1, 1):
            spike(m, al["bone"], (w[0] + sx * 1.6, w[1] + 2.0, w[2] - 1.0), (sx * 0.3, 0.6, 0.8), 1.0, 4.0, GOLD, tip=0.8)
        m.box(al["bone"], w[0] - 1.0, w[1] - 30.0, w[2] - 7.0, w[0] + 1.0, w[1] - 1.0, w[2] - 5.6, runef,
              rotation=(-12, 0, 0), pivot=(w[0], w[1] - 1.0, w[2] - 6.0))
        spike(m, al["bone"], (w[0], w[1] - 30.0, w[2] - 13.0), (0, -1, -0.2), 1.6, 3.0, runef, tip=0.8)
        ar = a["arm_right"]                                                            # Metal Garurumon head + cannon
        w = ar["wrist"]
        wolf_key = "black" if look.startswith("zwart") else "blue"
        m.round_box(ar["bone"], w[0], w[2] - 2.0, 2.8, 4.6, w[1] - 3.0, w[1] + 2.0,
                    armour(P, wolf_key, "blue_dark", trim="gold", trim_w=0.25), cut=1)
        r = 3 if look != "shuangwu" else 5
        rod(m, ar["bone"], (w[0], w[1] - 1.0, w[2] - 5.0), (w[0], w[1] - 1.0, w[2] - 14.0), r, STEEL, extend=0.4)
        m.round_box(ar["bone"], w[0], w[2] - 14.2, r * 0.4, r * 0.4, w[1] - 1.0 - r * 0.4, w[1] - 1.0 + r * 0.4,
                    solid(P, "black"), cut=0)
        if look == "shuangwu":                                                          # the second great cannon
            rod(m, bd, (6.0, 54.0, 3.0), (14.0, 60.0, -10.0), 4, STEEL, extend=0.4)
        if look == "zwartdefeat":                                                       # broken spikes, scorch
            for i in range(5):
                spike(m, bd, ((i - 2) * 3.0, 40.0 + i, 4.0), ((i - 2) * 0.3, 0.4, 1), 1.0, 5.0, solid(P, "black"),
                      tip=0.8)
        return m

    return build
