"""Shared builders for Shoutmon and its Digi-Xros forms (CobbleEffort: Digital; hand-built after the official art on
wikimon.net).

`small(name, look)`: Shoutmon itself: a little red dragon with a white belly and face, a big yellow beak-like mouth
full of teeth, golden headphones with a green lens, a spiked crest of red horns, white-and-black clawed feet, and a
yellow microphone stand in one hand. Looks: "red", "black", "blue", "yellow" (the game recolours) and "king" (King
Ver.: a red cape-like ring of golden flame round it and a fireball in its fist).

`mech(name, **parts)`: the Xros mechs built round Shoutmon's head and V crest. Parts: robot (X2: a chunky red-and-blue
Ballistamon body with big fists), axe (Plus M: a huge yellow-and-silver axe), drill (Dorulumon's white legs with
orange flame marks and drill knees), star_sword (the red serrated Star Sword with a gold star guard), lance (a blue
drill lance), shield (a white shield with a red crest), flame_wings, feather_mane (a great orange feather mane and a
red spear), jet (Sparrowmon's yellow jet on the arm), biker (black exhaust-piped legs), light_wings (cream feather
wings and red rings), colours "red" (default), "gold" (gold-and-black), "dark" (black-and-gold).
Shiny: blue for the red ones, silver for the gold ones.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, feather_wing
from _digibody import humanoid
from _digidetail import armour, cutout, feathers, flame_inside, metal, skin, solid, strands
from _route import pal, tone

LOOKS = {"red": {"red": (220, 50, 40), "red_dark": (130, 20, 14)},
         "black": {"red": (50, 50, 60), "red_dark": (16, 16, 22)},
         "blue": {"red": (50, 90, 210), "red_dark": (18, 36, 130)},
         "yellow": {"red": (240, 190, 40), "red_dark": (170, 110, 10)},
         "king": {"red": (220, 50, 40), "red_dark": (130, 20, 14)}}
COMMON = {"white": (240, 240, 246), "white_dark": (170, 172, 190), "yellow": (250, 210, 50), "gold": (236, 196, 70),
          "gold_dark": (150, 110, 20), "green": (70, 200, 90), "black": (28, 26, 32), "eye": (60, 120, 220),
          "steel": (200, 204, 216), "steel_dark": (100, 104, 120), "beak": (250, 200, 50), "tooth": (250, 250, 240),
          "blue": (50, 70, 190), "blue_dark": (18, 28, 110), "orange": (250, 130, 40), "flame": (255, 150, 40, 220),
          "sword": (240, 40, 70), "lance": (120, 200, 250), "cream": (250, 240, 214), "ring": (250, 90, 90, 170)}


def small(name, look="red"):
    base = dict(COMMON, **LOOKS[look])
    shiny = dict(base, red=(70, 110, 210), red_dark=(24, 50, 140)) if look in ("red", "king") else \
        dict(base, red=(220, 50, 40), red_dark=(130, 20, 14))

    def P(v):
        return pal(base, shiny, v)

    RED = skin(P, "red", dark="red_dark")
    WHITE = skin(P, "white", dark="white_dark")

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 8, 0))
        m.round_box(bd, 0, 0, 3.4, 2.8, 8.0, 17.0, RED, cut=1)
        m.round_box(bd, 0, -1.6, 2.4, 1.6, 9.0, 15.6, WHITE, cut=0)
        hd = m.bone("head", bd, (0, 17, 0))
        ball(m, hd, (0, 21.0, -0.4), 3.8, RED, layers=4, ry=3.4)
        m.round_box(hd, 0, -3.0, 2.6, 1.0, 19.0, 22.6, WHITE, cut=0)
        m.round_box(hd, 0, -4.2, 2.8, 1.6, 17.6, 19.8, solid(P, "beak"), cut=0)             # big yellow mouth
        for j in range(4):
            spike(m, hd, (-1.8 + j * 1.2, 19.8, -5.4), (0, -1, 0), 0.8, 1.0, solid(P, "tooth"), tip=0.8)
        for sx in (-1, 1):
            m.box(hd, sx * 1.4 - 0.6, 21.0, -3.6, sx * 1.4 + 0.6, 22.2, -3.4, solid(P, "eye"))
            m.round_box(hd, sx * 3.8, 0, 0.8, 1.4, 20.0, 22.4, metal(P, "gold", dark="gold_dark"), cut=0)  # headphones
            m.box(hd, min(sx * 4.4, sx * 4.8), 20.6, -0.6, max(sx * 4.4, sx * 4.8), 21.8, 0.6, solid(P, "green"))
        for j in range(4):                                                               # crest of red horns
            spike(m, hd, (-1.5 + j, 24.0, -0.6 + j * 0.6), ((j - 1.5) * 0.3, 1, 0.4), 1.2, 4.0 + (j % 2) * 1.6, RED,
                  tip=0.8)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 3.6, 15.0, 0))
            rod(m, ab, (sx * 3.6, 15.0, 0), (sx * 4.6, 11.0, -1.0), 2, WHITE, extend=0.3)
            ball(m, ab, (sx * 4.8, 10.4, -1.2), 1.4, solid(P, "black"), layers=2)
        rod(m, "arm_left", (4.8, 2.0, -1.2), (4.8, 22.0, -1.2), 1, solid(P, "yellow"), extend=0.2)   # mic stand
        ball(m, "arm_left", (4.8, 23.0, -1.2), 1.2, metal(P, "steel"), layers=2)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 1.8, 8.0, 0))
            rod(m, lg, (sx * 1.8, 8.0, 0), (sx * 2.2, 1.6, 0), 2, WHITE, extend=0.3)
            m.round_box(lg, sx * 2.2, -0.8, 1.6, 2.2, 0.0, 1.8, WHITE, cut=0)
            for f in range(3):
                spike(m, lg, (sx * 2.2 + (f - 1) * 1.0, 0.6, -2.8), (0, -0.2, -1), 0.8, 1.6, solid(P, "black"), tip=0.8)
        tl = m.bone("tail", bd, (0, 9, 3))
        rod(m, tl, (0, 9.0, 3.0), (0, 6.0, 8.0), 2, RED, extend=0.3)
        spike(m, tl, (0, 6.0, 8.0), (0, -0.2, 1), 1.4, 2.6, RED, tip=0.8)
        if look == "king":                                                               # ring of golden flame
            FIRE = cutout(flame_inside(tongues=3), solid(P, "flame", glow=True))
            rb = m.bone("ring_flame", bd, (0, 14, 0))
            for i in range(14):
                ang = 2 * math.pi * i / 14
                m.box(rb, 12.0 * math.cos(ang) - 1.6, 14.0 + 12.0 * math.sin(ang) - 1.6, 1.0,
                      12.0 * math.cos(ang) + 1.6, 14.0 + 12.0 * math.sin(ang) + 1.6, 1.0, FIRE)
            ball(m, "arm_right", (-4.8, 12.6, -2.6), 2.0, solid(P, "flame", glow=True), layers=2)
        return m

    return build


def mech(name, colour="red", robot=False, axe=False, drill=False, star_sword=False, lance=False, shield=False,
         flame_wings=False, feather_mane=False, jet=False, biker=False, light_wings=False):
    base = dict(COMMON, **LOOKS["red"])
    if colour == "gold":
        base.update({"red": (236, 196, 70), "red_dark": (150, 110, 20), "blue": (40, 38, 46), "blue_dark": (14, 14, 18),
                     "white": (60, 58, 66), "white_dark": (24, 22, 28)})
    elif colour == "dark":
        base.update({"red": (40, 38, 46), "red_dark": (14, 14, 18), "blue": (236, 196, 70), "blue_dark": (150, 110, 20),
                     "white": (60, 58, 66), "white_dark": (24, 22, 28)})
    shiny = dict(base, red=(70, 110, 210), red_dark=(24, 50, 140)) if colour == "red" else \
        dict(base, red=(210, 214, 226), red_dark=(110, 114, 130))

    def P(v):
        return pal(base, shiny, v)

    RED = armour(P, "red", "red_dark", trim="gold", trim_w=0.2)
    BLUE = armour(P, "blue", "blue_dark", trim="steel", trim_w=0.2)
    WHITE = armour(P, "white", "white_dark")
    STEEL = metal(P, "steel", dark="steel_dark")
    GOLD = metal(P, "gold", dark="gold_dark")

    def legf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if drill and face in ("north", "east", "west") and abs(math.sin(y * 0.8 + abs(x))) > 0.9 and y < 14.0:
            return tone(p["orange"], face), None
        return WHITE(x, y, z, face, variant, box=box, **k)

    def drillf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        return tone(p["gold"] if (y * 2.0) % 2.0 < 1.0 else p["black"], face), None

    def build():
        m = Model(name)
        bulk = 1.25 if robot else 1.0
        mats = {"skin": RED, "chest": BLUE if robot else RED, "deltoid": BLUE, "upper_arm": BLUE if robot else STEEL,
                "forearm": RED, "hand": RED, "finger": RED, "thigh": legf, "knee": legf, "shin": legf, "calf": legf,
                "foot": legf, "talon": STEEL, "claw": STEEL,
                "pelvis": solid(P, "black") if biker else RED}
        if biker:
            mats.update({"thigh": metal(P, "black"), "shin": metal(P, "black"), "calf": metal(P, "black"),
                         "foot": metal(P, "black")})
        a = humanoid(m, mats, bulk=bulk, arm_bulk=1.3 if robot else 1.0, leg_bulk=1.2 if robot else 1.0,
                     talons=not robot, digitigrade=drill, name=name)
        bd = a["body"]
        for sx in (-1, 1):                                                               # V crest on the chest
            m.box(bd, min(sx * 0.4, sx * 5.0), 47.0, -5.4, max(sx * 0.4, sx * 5.0), 49.0, -4.8, solid(P, "red"),
                  rotation=(0, 0, sx * 40), pivot=(0, 42.0, -5.0))
        for sx in (-1, 1):                                                               # shoulder blocks
            m.round_box(bd, sx * 8.6, 0, 3.6, 3.8, 45.0, 52.0, BLUE if robot or colour != "red" else RED, cut=1)
        rod(m, bd, (2.0, 50.0, 4.0), (6.0, 62.0, 6.0), 2, BLUE, extend=0.4)               # Ballistamon's "7" bracket
        rod(m, bd, (6.0, 62.0, 6.0), (1.0, 64.0, 6.0), 2, BLUE, extend=0.4)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.8, 2.8, 3.2, 54.0, 60.0, RED, cut=1)
        m.round_box(hd, 0, -3.4, 2.4, 0.8, 55.0, 58.6, WHITE, cut=0)                        # white face-guard
        m.box(hd, -1.8, 57.0, -4.3, 1.8, 57.8, -4.1, solid(P, "green", glow=True))
        for sx in (-1, 1):
            spike(m, hd, (sx * 1.6, 60.0, -1.0), (sx * 0.6, 1, -0.2), 1.4, 7.0, RED, tip=0.8)   # V horns
        if drill:                                                                        # drill knees + tail
            for side in ("leg_left", "leg_right"):
                k_ = a[side]["knee"]
                spike(m, a[side]["bone"], (k_[0], k_[1] + 1.0, k_[2] - 1.0), (0, 0.3, -1), 1.6, 5.0, drillf, tip=0.8)
            tl = m.bone("tail", bd, (0, 32, 4))
            rod(m, tl, (0, 32.0, 4.0), (0, 22.0, 14.0), 2, WHITE, extend=0.4)
            spike(m, tl, (0, 22.0, 14.0), (0, -0.4, 1), 1.6, 5.0, drillf, tip=0.8)
        wr, wl = a["arm_right"], a["arm_left"]
        if robot:                                                                        # big fists
            for side in (wr, wl):
                ball(m, side["bone"], side["hand"], 3.4, RED, layers=3)
        if axe:                                                                          # huge axe
            w = wr["wrist"]
            rod(m, wr["bone"], (w[0], 2.0, w[2] - 2.0), (w[0], 72.0, w[2] - 2.0), 1, STEEL, extend=0.2)
            m.box(wr["bone"], w[0] - 0.6, 52.0, w[2] - 18.0, w[0] + 0.6, 76.0, w[2] - 2.0, solid(P, "yellow"))
            m.box(wr["bone"], w[0] - 0.4, 50.0, w[2] - 22.0, w[0] + 0.4, 78.0, w[2] - 17.0, STEEL)
        if star_sword:                                                                   # Star Sword
            w = wr["wrist"]
            for j in range(5):
                ang = math.radians(90 + j * 72)
                spike(m, wr["bone"], (w[0], w[1] - 1.0, w[2] - 2.0), (0, math.sin(ang), math.cos(ang)), 1.0, 2.4, GOLD,
                      tip=0.8)
            for j in range(8):
                y0 = w[1] + 2.0 + j * 3.6
                m.box(wr["bone"], w[0] - 0.6, y0, w[2] - 3.4, w[0] + 0.6, y0 + 3.0, w[2] - 0.6, solid(P, "sword", glow=True),
                      rotation=(-35, 0, 0), pivot=(w[0], w[1], w[2] - 2.0))
        if lance:                                                                        # blue drill lance
            w = wl["wrist"]
            spike(m, wl["bone"], (w[0], w[1], w[2] - 2.0), (0.2, -0.3, -1), 2.4, 30.0, solid(P, "lance"), tip=0.8)
        if shield:
            w = wl["wrist"]
            m.box(wl["bone"], w[0] + 1.0, w[1] - 10.0, w[2] - 7.0, w[0] + 2.0, w[1] + 8.0, w[2] + 5.0,
                  armour(P, "cream", "white_dark", trim="red", trim_w=0.4, trim_edges=("top", "bottom", "sides")))
        if jet:                                                                          # Sparrowmon's yellow jet
            e = wl["elbow"]
            rod(m, wl["bone"], (e[0] + 3.0, e[1], e[2] + 8.0), (e[0] + 3.0, e[1], e[2] - 12.0), 4, armour(P, "yellow", "gold_dark"),
                extend=0.4)
            spike(m, wl["bone"], (e[0] + 3.0, e[1], e[2] - 12.4), (0, 0, -1), 2.0, 4.0, STEEL, tip=0.8)
        if flame_wings:
            FIRE = cutout(flame_inside(tongues=4), solid(P, "flame", glow=True))
            for sx in (-1, 1):
                x0, x1 = sorted((sx * 4.0, sx * 30.0))
                m.box(bd, x0, 44.0, 5.0, x1, 58.0, 5.0, FIRE, rotation=(0, -sx * 10, sx * 10), pivot=(sx * 4.0, 50.0, 5.0))
        if feather_mane:
            for j in range(12):
                ang = math.radians(-100 + j * 18)
                spike(m, hd, (2.6 * math.sin(ang), 58.0, 1.6), (math.sin(ang), math.cos(ang) * 0.5 + 0.4, 1), 1.8, 16.0,
                      feathers(P, "orange", "red_dark"), tip=0.8)
            w = wl["wrist"]
            rod(m, wl["bone"], (w[0], w[1] - 20.0, w[2] + 6.0), (w[0], w[1] + 16.0, w[2] - 8.0), 1, STEEL, extend=0.2)
            spike(m, wl["bone"], (w[0], w[1] - 20.0, w[2] + 6.0), (0, -0.85, 0.4), 2.0, 8.0, solid(P, "red"), tip=0.8)
        if light_wings:
            for sx in (-1, 1):
                feather_wing(m, bd, (sx * 3.0, 50.0, 4.0), 26.0, 14.0, 5, feathers(P, "cream", "gold"), side=sx, sweep=20,
                             droop=-10.0)
            rb = m.bone("ring_light", bd, (0, 40, 0))
            for i in range(20):
                ang = 2 * math.pi * i / 20
                m.box(rb, 22.0 * math.cos(ang) - 1.0, 40.0 + 22.0 * math.sin(ang) - 1.0, -0.4, 22.0 * math.cos(ang) + 1.0,
                      40.0 + 22.0 * math.sin(ang) + 1.0, 0.4, solid(P, "ring", glow=True),
                      rotation=(0, 40, 20), pivot=(0, 40.0, 0))
        if biker:                                                                        # exhaust pipes
            for side in ("leg_left", "leg_right"):
                k_ = a[side]["knee"]
                rod(m, a[side]["bone"], (k_[0], k_[1] + 2.0, k_[2] + 2.0), (k_[0], k_[1] - 8.0, k_[2] + 4.0), 2, STEEL,
                    extend=0.2)
        return m

    return build
