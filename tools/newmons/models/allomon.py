"""Allomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a blue upright dinosaur. Scaly blue hide with a pale blue belly, red-and-orange tiger bands on its arms,
legs and long tail, a big head with a mouth full of white fangs and fierce yellow eyes, a headdress of red-tipped
white feathers fanning behind its skull, a gold necklace of round medallions, yellow fur cuffs and white claws.
15 blocks tall.

Front is -z, y is up. 50 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import theropod
from _digidetail import eye, feathers, fur, metal, mix, plane, scales, skin, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(15, HEIGHT, 1.8)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 14}
LOOK = ("a blue upright dinosaur with red-and-orange tiger bands, a pale belly, a fanged mouth, yellow eyes, a "
        "headdress of red-tipped white feathers, a gold medallion necklace and yellow fur cuffs")

BASE = {"blue": (52, 110, 200), "blue_dark": (24, 54, 128), "blue_light": (110, 170, 240),
        "belly": (150, 200, 246), "belly_dark": (96, 150, 214), "band": (220, 50, 40), "band2": (250, 140, 40),
        "white": (248, 248, 246), "claw": (226, 228, 240), "claw_dark": (150, 156, 186), "mouth": (150, 30, 50),
        "tongue": (220, 80, 100), "eye": (250, 214, 40), "pupil": (20, 16, 10), "feather_tip": (210, 40, 40),
        "feather_dark": (196, 196, 204), "gold": (232, 186, 60), "gold_dark": (160, 112, 30), "gold_light": (255, 236, 160),
        "cuff": (246, 214, 70), "cuff_dark": (196, 150, 30), "mantle": (140, 86, 44), "mantle_dark": (86, 50, 24),
        "mantle_light": (196, 140, 90), "bonnet_tip": (30, 30, 36)}
SHINY = {"blue": (60, 150, 90), "blue_dark": (26, 84, 46), "blue_light": (120, 210, 140), "belly": (210, 236, 170),
         "belly_dark": (160, 196, 120), "band": (120, 40, 170), "band2": (200, 90, 220), "feather_tip": (110, 40, 170)}


def make(name, base, shiny, x=False):
    """The Allomon builder; x = the X-Antibody look (brown fur mantle, war bonnet down its back, leaning pose)."""
    def P(v):
        return pal(base, shiny, v)


    HIDE = scales(P, "blue", "blue_dark", size=1.8, light="blue_light", rim_mix=0.4)
    BELLY = scales(P, "belly", "belly_dark", size=1.6, belly_key="belly", belly=lambda x, y, z, f: f == "north")


    def banded(period=3.2, offset=0.0, axis="y"):
        """Blue scales crossed by red bands with an orange inner stripe (tiger bands)."""
        def s(x, y, z, face, variant, box=None, **k):
            p = P(variant)
            t = ((y if axis == "y" else z) + offset + 0.3 * x) % period / period
            if t < 0.22:
                return tone(p["band"], face), None
            if t < 0.3:
                return tone(p["band2"], face), None
            return HIDE(x, y, z, face, variant, box=box, **k)
        return s


    ARM = banded(2.6)
    LEG = banded(3.4)
    TAIL = banded(3.6, axis="z")
    CLAW = metal(P, "claw", dark="claw_dark", light="white", streak=2.0)
    GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
    CUFF = fur(P, "cuff", "cuff_dark", length=1.0)
    BONNET = feathers(P, "white", "feather_dark", size=(1.2, 2.6), flow=(0, 1), tip="bonnet_tip")
    PLUME = feathers(P, "white", "feather_dark", size=(1.4, 3.0), flow=(0, 1), tip="feather_tip")


    def headf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face in ("east", "west"):
            c = eye(p, z + 9.2, y - 43.6, 1.2, "eye", lid="blue_dark", slit=True)
            if c is not None:
                return c, None
        return HIDE(x, y, z, face, variant, box=box, **k)


    def build_model():
        m = Model(name)
        mats = {"skin": HIDE, "belly": BELLY, "neck": HIDE, "head": headf, "snout": HIDE, "jaw": HIDE,
                "mouth": solid(P, "mouth"), "tooth": solid(P, "white"), "tongue": solid(P, "tongue"), "arm": ARM,
                "hand": HIDE, "claw": CLAW, "thigh": LEG, "shin": LEG, "foot": HIDE, "talon": CLAW, "tail": TAIL,
                "tail_tip": TAIL}
        a = theropod(m, mats, name, hip_y=19.0, hip_z=2.0, chest=(0, 33.0, -1.0), body_r=6.4, chest_r=5.8,
                     neck_top=(0, 41.0, -3.0), head_len=12.5, head_w=4.4, head_h=4.6, mouth_open=24, teeth=7,
                     arm_len=10.0, arm_bulk=1.25, leg_bulk=1.35, stance=4.8, tail=((0, 16, 9), (2, 11, 16), (5, 7, 22), (8, 5, 27), (10, 4, 31)),
                     tail_r=(4.6, 3.6, 2.6, 1.8, 1.0))
        hd = a["head"]
        z0, z1 = a["skull_z"]
        top = a["skull_top"]
        # the feather headdress: a fan of red-tipped white feathers standing up behind the skull, red base band
        m.box(hd, -4.0, top - 1.6, z1 - 1.6, 4.0, top - 0.2, z1, solid(P, "band"))
        for i in range(0 if x else 9):
            ang = -60 + i * 15
            import math
            r = math.radians(ang)
            base = (3.6 * math.sin(r), top - 0.8, z1 - 0.8)
            tipp = (base[0] + 5.5 * math.sin(r), base[1] + 3.0 * math.cos(r) + 1.5, base[2] + 7.5)
            rod(m, hd, base, tipp, 2, PLUME, extend=0.3, t2=1)
        # cheek spikes and the horn-nub on the snout
        for sx in (-1, 1):
            spike(m, hd, (sx * 4.2, a["mouth_y"] + 1.6, z0 + 2.0), (sx, 0.2, 0.4), 1.2, 2.2, HIDE)
        # gold necklace of medallions round the base of the neck
        import math
        for i in range(9):
            ang = math.radians(-100 + i * 25)
            c = (5.6 * math.sin(ang), 36.0 - 1.6 * math.cos(ang) ** 2, -1.0 - 5.0 * math.cos(ang))
            m.box(a["body"], c[0] - 0.9, c[1] - 0.9, c[2] - 0.5, c[0] + 0.9, c[1] + 0.9, c[2] + 0.5, GOLD,
                  rotation=(0, -math.degrees(ang), 0), pivot=c)
        m.box(a["body"], -1.4, 33.4, -7.2, 1.4, 35.6, -6.2, GOLD)                         # centre medallion
        for sx in (-1, 1):
            m.box(a["body"], sx * 4.0 - 0.6, 34.6, -6.4, sx * 4.0 + 0.6, 35.8, -5.6, GOLD)
        # yellow fur cuffs on the wrists
        for nm in ("arm_left", "arm_right"):
            ab = a[nm]
            rod(m, ab["bone"], ab["elbow"], tuple(e + (h - e) * 0.25 for e, h in zip(ab["elbow"], ab["hand"])), 4, CUFF,
                extend=0.2)
        if x:
            bd = a["body"]
            MANTLE = fur(P, "mantle", "mantle_dark", tip="mantle_light", length=1.4)
            # a shaggy brown fur mantle over the shoulders and chest, white fang fringe on its lower edge
            for i in range(10):
                ang = math.radians(-120 + i * 26.7)
                c = (6.8 * math.sin(ang), 33.5, -1.0 - 6.2 * math.cos(ang))
                m.box(bd, c[0] - 1.8, c[1] - 4.5, c[2] - 0.9, c[0] + 1.8, c[1] + 2.5, c[2] + 0.9, MANTLE,
                      rotation=(8, -math.degrees(ang), 0), pivot=c)
                spike(m, bd, (c[0], c[1] - 4.5, c[2]), (0, -1, 0), 1.0, 1.8, solid(P, "white"))
            # the war bonnet: white black-tipped feathers in a row from the crown down its back
            for i in range(12):
                t = i / 11
                base = (0, 46.0 - 18.0 * t, 1.0 + 7.0 * t)
                for sx in (-1, 0, 1):
                    rod(m, bd if i > 2 else a["head"], base, (sx * 2.2, base[1] + 5.0 - 1.5 * t, base[2] + 4.0),
                        2, BONNET, extend=0.2, t2=1)
        return m

    return build_model


build = make("allomon", BASE, SHINY)
