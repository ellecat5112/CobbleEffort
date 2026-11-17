"""Shared builder for Cherubimon, one of the Three Great Angels (CobbleEffort: Digital; hand-built after the official art
on wikimon.net). A long-eared holy beast with a pointed face, a slender torso, huge arms ending in great hands and a
tapering lower body.

"virtue": white-and-pink, feathered wings and long ears, a golden face guard, delicate hands.
"vice": the fallen form: dark violet hide, a green belly, a crest of blue spikes round the face, horned ears and
monstrous clawed arms.
"virtue_x" / "vice_x": the X-Antibody forms: a great sphere at the core (white light / black void), feathered wings
above, and enormous armoured hands (pink with gold studs / violet with copper plating).
Shiny: gold for Virtue, crimson for Vice.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import armour, cutout, feathers, fur, gem, local, metal, skin, solid
from _route import pal, tone

VIRTUE = {"hide": (250, 230, 236), "hide_dark": (220, 170, 190), "accent": (240, 170, 200), "accent_dark": (190, 110, 150),
          "gold": (240, 200, 80), "gold_dark": (170, 130, 30), "orb": (250, 250, 255), "orb_light": (210, 230, 255),
          "wing": (250, 220, 236), "wing_dark": (220, 170, 200), "eye": (90, 150, 240), "spike": (250, 240, 200),
          "claw": (250, 250, 250), "line": (120, 210, 230)}
VICE = {"hide": (70, 50, 120), "hide_dark": (30, 20, 60), "accent": (40, 140, 110), "accent_dark": (16, 80, 60),
        "gold": (180, 110, 60), "gold_dark": (110, 60, 30), "orb": (20, 18, 26), "orb_light": (90, 40, 110),
        "wing": (110, 70, 170), "wing_dark": (50, 30, 90), "eye": (250, 60, 60), "spike": (80, 190, 250),
        "claw": (230, 230, 240), "line": (240, 60, 140)}
SHINY_VIRTUE = {"hide": (250, 236, 180), "hide_dark": (220, 190, 110), "accent": (240, 200, 90), "wing": (255, 240, 190)}
SHINY_VICE = {"hide": (130, 20, 30), "hide_dark": (60, 8, 14), "accent": (40, 40, 48), "wing": (160, 30, 40)}


def make(name, variant="virtue"):
    vice = variant.startswith("vice")
    x = variant.endswith("_x")
    base = VICE if vice else VIRTUE
    shiny = dict(base, **(SHINY_VICE if vice else SHINY_VIRTUE))

    def P(v):
        return pal(base, shiny, v)

    HIDE = fur(P, "hide", "hide_dark", length=1.0) if not vice else skin(P, "hide", dark="hide_dark", var=0.05)
    ACC = skin(P, "accent", dark="accent_dark", var=0.04)
    GOLD = metal(P, "gold", dark="gold_dark")
    WING = feathers(P, "wing", "wing_dark", size=(1.6, 3.0), flow=(0, 1))
    HAND = armour(P, "accent" if x else "hide", "accent_dark" if x else "hide_dark", trim="gold" if x else None,
                  rivets=x)

    def headf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                if abs(xx - sx * 1.2) < 0.6 and abs(y - 60.4) < 0.35:
                    return p["eye"], p["eye"]
        return HIDE(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 30, 0))
        # a slender torso tapering down into a pointed lower body (it floats)
        for i, (r, y0, y1) in enumerate(((1.0, 6.0, 12.0), (2.0, 12.0, 20.0), (3.0, 20.0, 30.0), (4.2, 30.0, 42.0),
                                         (5.0, 42.0, 52.0))):
            m.round_box(bd, 0, 0, r * (1.3 if i > 2 else 1.0), r, y0, y1, ACC if i < 4 else HIDE,
                        cut=max(1, round(r * 0.3)))
        if x:                                                             # the great sphere at the core
            ball(m, bd, (0, 38.0, -1.0), 7.4, gem(P, "orb", "orb_light", glow=not vice), layers=6)
            for sx in (-1, 1):
                rod(m, bd, (sx * 3.0, 32.0, 0), (sx * 4.6, 6.0, 0), 3, solid(P, "line"), extend=0.4)
        hd = m.bone("head", bd, (0, 54, 0))
        m.round_box(hd, 0, -0.6, 2.6, 3.0, 54.0, 62.0, headf, cut=1)
        m.box(hd, -1.4, 55.0, -4.6, 1.4, 58.0, -3.0, HIDE)                  # pointed muzzle
        m.box(hd, -2.0, 58.6, -3.8, 2.0, 59.6, -3.4, GOLD)                  # face guard
        for sx in (-1, 1):                                                  # long ears / horned ears
            pts = [(sx * 1.6, 61.0, 0), (sx * 2.6, 68.0, 0.6), (sx * 3.0, 75.0, 1.6), (sx * (5.0 if vice else 2.6), 80.0, 2.6)]
            for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
                rod(m, hd, p0, p1, 2 if j < 2 else 1, HIDE, extend=0.3, t2=3 if not vice else 2)
        crest = solid(P, "spike")
        for i in range(12):                                                 # the crest round the face
            ang = math.radians(i * 30)
            spike(m, hd, (2.4 * math.cos(ang), 58.0 + 2.4 * math.sin(ang), -1.0),
                  (math.cos(ang), math.sin(ang), 0.3), 1.2, 4.4 if vice else 2.0, crest, tip=0.3)
        # the arms: huge hands (claws for Vice)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 6.0, 50.0, 0))
            sh = (sx * 6.0, 50.0, 0)
            el = (sx * (16.0 if x else 12.0), 46.0 if x else 40.0, -1.0)
            hand = (sx * (18.0 if x else 13.0), 24.0 if x else 26.0, -3.0)
            rod(m, ab, sh, el, 5 if x else 4, HAND if x else HIDE, extend=0.8)
            rod(m, ab, el, hand, 6 if x else 4, HAND if x else HIDE, extend=0.8)
            hs = 2.6 if x else 1.6 if not vice else 2.0
            m.round_box(ab, hand[0], hand[2], 3.0 * hs / 1.6, 2.6 * hs / 1.6, hand[1] - 4.0 * hs / 1.6,
                        hand[1] + 1.0, HAND, cut=1)
            for f in range(4):
                fx = hand[0] + (f - 1.5) * 1.6 * hs / 1.6
                if vice:
                    spike(m, ab, (fx, hand[1] - 4.0 * hs / 1.6, hand[2] - 1.0), (0, -1, -0.4), 1.4, 6.0,
                          solid(P, "claw"), tip=0.4)
                else:
                    rod(m, ab, (fx, hand[1] - 4.0 * hs / 1.6, hand[2]), (fx, hand[1] - 9.0 * hs / 1.6, hand[2] - 1.6),
                        max(1, round(hs)), HAND, extend=0.3)
            if x:
                for j in range(3):
                    m.round_box(ab, el[0] + (hand[0] - el[0]) * (0.3 + 0.25 * j), -4.0,
                                1.2, 1.2, el[1] + (hand[1] - el[1]) * (0.3 + 0.25 * j) - 1.0,
                                el[1] + (hand[1] - el[1]) * (0.3 + 0.25 * j) + 1.0, GOLD, cut=1)
        # wings (feathered for Virtue and both X forms; Vice has none)
        if not vice or x:
            wb = m.bone("wings", bd, (0, 50, 3))
            for sx in (-1, 1):
                x0, x1 = sorted((sx * 2.0, sx * 26.0))
                for j, (ang, y0) in enumerate(((30, 48.0), (10, 44.0), (-12, 40.0))):
                    m.box(wb, x0, y0, 3.0 + j, x1, y0 + 8.0, 3.0 + j, WING,
                          rotation=(0, sx * 15, sx * ang), pivot=(sx * 2.0, y0 + 4.0, 3.0 + j))
        return m
    return build
