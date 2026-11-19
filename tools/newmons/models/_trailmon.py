"""Shared builder for the Trailmon (CobbleEffort: Digital; hand-built after the art on wikimon.net, mostly anime
stills): living locomotives: a long rounded train body on heavy wheels with a face in the nose. Looks (`make(name,
look)`): angler (teal with an orange skirt, a lure on a stalk and a tail fin), battle (grey armour, a sharp eye and
gatling barrels), buffalo (slate with golden horns and a spiked snow-plough), c89 (navy steam engine with a whale-like
white jaw, a red eye, smokestacks and gold pipes), franken (maroon diesel with a grey grille face and green eyes),
kettle (yellow with an orange skirt, grey side pipes and a red lamp), mole (pink with a big pale snout, whiskers and
yellow digging claws), darkness (black segmented body with three glowing red eyes joined by green lines), raccoon
(mint bullet-train nose with a red-brown mask), next1/next2/next3 (the unnamed bullet trains of Digimon Next: white with a
huge eye, white with blade fins, grey ribbed with a long beak nose), worm (copper segmented worm with four yellow eyes and huge fangs).
Shiny: each look's colours turned round the hue wheel."""
from __future__ import annotations

import colorsys
import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, slab_z
from _digidetail import armour, metal, plane, riveted, solid
from _route import pal, tone

LOOKS = {
    "angler": {"body": (80, 170, 170), "body_dark": (30, 100, 110), "lower": (220, 120, 70), "eye": (220, 40, 40),
               "accent": (250, 240, 170)},
    "battle": {"body": (180, 184, 196), "body_dark": (80, 84, 96), "lower": (120, 124, 136), "eye": (250, 200, 60),
               "accent": (90, 94, 106)},
    "buffalo": {"body": (80, 76, 100), "body_dark": (30, 28, 44), "lower": (150, 150, 160), "eye": (130, 230, 80),
                "accent": (230, 190, 60)},
    "c89": {"body": (40, 60, 80), "body_dark": (14, 24, 34), "lower": (40, 44, 50), "eye": (220, 30, 40),
            "accent": (230, 190, 90)},
    "franken": {"body": (160, 50, 70), "body_dark": (90, 20, 34), "lower": (170, 170, 176), "eye": (120, 220, 70),
                "accent": (250, 160, 50)},
    "kettle": {"body": (250, 220, 50), "body_dark": (200, 160, 20), "lower": (250, 140, 50), "eye": (60, 160, 230),
               "accent": (210, 50, 40)},
    "mole": {"body": (220, 120, 190), "body_dark": (150, 60, 130), "lower": (90, 90, 100), "eye": (120, 220, 60),
             "accent": (250, 210, 80)},
    "darkness": {"body": (50, 50, 56), "body_dark": (16, 16, 20), "lower": (40, 40, 46), "eye": (250, 40, 40),
                 "accent": (120, 230, 80)},
    "raccoon": {"body": (120, 200, 160), "body_dark": (60, 130, 100), "lower": (236, 236, 236), "eye": (230, 220, 60),
                "accent": (150, 60, 40)},
    "next1": {"body": (236, 238, 244), "body_dark": (150, 156, 170), "lower": (90, 120, 200), "eye": (30, 30, 40),
              "accent": (60, 60, 70)},
    "next2": {"body": (240, 242, 248), "body_dark": (160, 166, 180), "lower": (200, 60, 60), "eye": (40, 40, 60),
              "accent": (180, 186, 200)},
    "next3": {"body": (110, 116, 130), "body_dark": (50, 54, 66), "lower": (70, 74, 86), "eye": (240, 240, 250),
              "accent": (40, 44, 56)},
    "worm": {"body": (190, 110, 80), "body_dark": (110, 54, 34), "lower": (60, 56, 60), "eye": (250, 220, 40),
             "accent": (250, 250, 240)},
}
COMMON = {"wheel": (50, 50, 56), "hub": (180, 180, 190), "black": (24, 24, 28), "white": (250, 250, 250),
          "pupil": (20, 16, 16), "grille": (60, 60, 66), "tooth": (250, 250, 244), "snout": (250, 200, 190),
          "glow": (255, 250, 200)}


def _hue(c, d):
    h, s, v = colorsys.rgb_to_hsv(*(x / 255 for x in c[:3]))
    r, g, b = colorsys.hsv_to_rgb((h + d) % 1.0, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))


def make(name, look):
    base = dict(COMMON, **LOOKS[look])
    shiny = dict(base, **{k: _hue(v, 0.45) for k, v in LOOKS[look].items() if k in ("body", "body_dark", "lower")})

    def P(v):
        return pal(base, shiny, v)

    L0, L1 = -24.0, 26.0                                     # body length along z (front = -z)

    def bodyf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        a, b = plane(x, y, z, face)
        seg = look in ("darkness", "worm")
        if seg and (z % 7.0) < 0.6:
            return tone(p["body_dark"], face), None
        if face in ("east", "west"):
            if look == "darkness":                                               # three red eyes joined by lines
                for j, cz in enumerate((-16.0, -6.0, 4.0)):
                    d = math.hypot(z - cz, y - 11.0)
                    if d < 2.4:
                        return (p["eye"] if d < 1.8 else p["black"]), p["eye"]
                if abs(y - 11.0) < 0.35 and -16.0 < z < 4.0:
                    return p["accent"], p["accent"]
                if abs(y - 6.0) < 0.6 and int(z) % 4 == 0:
                    return p["white"], p["white"]
            if look in ("franken", "raccoon", "c89", "battle") and 12.5 < y < 14.5 and z > -8.0 and int(z) % 5 != 0:
                return tone(p["black"], face), None                              # window band
            if look == "c89" and z > -10.0 and 9.0 < y < 11.0 and int(z * 1.4) % 3 == 0:
                return tone(p["accent"], face), None                             # gold lettering
            if y < 8.0 and look not in ("darkness",):
                return tone(p["lower"], face), None
        if face == "up" and look in ("angler", "battle", "c89") and (int(z * 0.5) % 3 == 0) and abs(x) > 3.0:
            return tone(p["body_dark"], face), None
        return metal(P, "body", dark="body_dark")(x, y, z, face, variant, box=box, **k)

    def wheelf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face in ("east", "west") and box is not None:
            cy = box.lo[1] + box.size[1] / 2
            cz = box.lo[2] + box.size[2] / 2
            if math.hypot(y - cy, z - cz) < 0.9:
                return p["hub"], None
        return tone(p["wheel"], face), None

    def facef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            a, b = plane(x, y, z, face)
            if look in ("angler", "c89", "worm", "mole"):
                return tone(p["tooth"] if look != "mole" else p["snout"], face), None
            if look in ("franken",) and b < 10.0 and (abs(a) * 1.2 + (10.0 - b)) % 2.4 < 0.6:
                return tone(p["grille"], face), None
            if look == "raccoon":
                return tone(p["lower"], face), None
        return bodyf(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 10, 0))
        n = 8
        for i in range(n):                                                         # main body
            z0 = L0 + i * (L1 - L0) / n
            ry = 7.0 if look != "worm" else 7.6 - 0.6 * (i % 2)
            slab_z(m, bd, 0, 11.0, z0 - 0.2, z0 + (L1 - L0) / n + 0.2, 6.2, ry, bodyf)
        hd = m.bone("head", bd, (0, 10, L0))
        for j in range(4):                                                         # rounded nose
            t = (j + 1) / 4
            ry = 7.0 * math.cos(t * 1.1)
            rx = 6.2 * math.cos(t * 0.9)
            slab_z(m, hd, 0, 11.0 - (7.0 - ry) * 0.6, L0 - (j + 1) * 1.6, L0 - j * 1.6 + 0.2, rx, ry,
                   facef if j >= 2 else bodyf)
        zf = L0 - 6.4
        for sx in (-1, 1):                                                         # wheels
            for j in range(6):
                z = L0 + 4.0 + j * 7.6
                m.box(top, sx * 6.0 - 0.6 if sx > 0 else -6.6, 0.0, z - 2.4, sx * 6.0 + 0.6 if sx > 0 else -5.4, 4.8,
                      z + 2.4, wheelf)
        if look not in ("darkness",):                                              # eyes on the nose
            for sx in (-1, 1):
                ex = sx * 4.4
                ball(m, hd, (ex, 14.0 if look != "worm" else 15.6, L0 - 2.0), 1.6, solid(P, "white"), layers=1)
                ball(m, hd, (ex * 1.04, 14.0 if look != "worm" else 15.6, L0 - 3.2), 0.9, solid(P, "eye", glow=True),
                     layers=1)
                if look == "worm":
                    ball(m, hd, (ex, 10.6, L0 - 3.4), 1.4, solid(P, "eye", glow=True), layers=1)
        if look == "angler":
            pts = [(0, 18.0, L0 + 2.0), (0, 22.0, L0 + 1.0), (0, 23.0, L0 - 3.0), (0, 21.0, L0 - 6.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, hd, p0, p1, 1, solid(P, "lower"), extend=0.3)
            ball(m, hd, (0, 20.0, L0 - 7.0), 1.6, solid(P, "accent", glow=True), layers=2)
            m.box(bd, -0.6, 17.0, L1 - 8.0, 0.6, 24.0, L1, solid(P, "body"), rotation=(-20, 0, 0),
                  pivot=(0, 17.0, L1 - 4.0))
        elif look == "battle":
            for sx in (-1, 1):
                for j in range(4):
                    rod(m, bd, (sx * 6.6, 13.0 + (j % 2) * 1.6, L0 + 10.0 + (j // 2) * 1.6),
                        (sx * 6.6, 13.0 + (j % 2) * 1.6, L0 - 6.0 + (j // 2) * 1.6), 1, metal(P, "accent"), extend=0.0)
            m.round_box(hd, 0, L0 - 3.0, 5.0, 2.0, 15.0, 18.6, armour(P, "body", "body_dark"), cut=1)
        elif look == "buffalo":
            for sx in (-1, 1):
                pts = [(sx * 4.0, 17.0, L0 + 2.0), (sx * 9.0, 20.0, L0 + 1.0), (sx * 11.0, 24.0, L0 - 1.0)]
                for p0, p1 in zip(pts, pts[1:]):
                    rod(m, hd, p0, p1, 2, metal(P, "accent"), extend=0.4)
            m.box(hd, -7.0, 0.6, L0 - 9.0, 7.0, 6.0, L0 - 6.0, armour(P, "lower", "body_dark"), rotation=(-30, 0, 0),
                  pivot=(0, 3.0, L0 - 7.0))
            for sx in (-1, 1):
                spike(m, hd, (sx * 5.6, 3.0, L0 - 8.6), (sx * 0.4, 0, -1), 1.6, 4.0, metal(P, "accent"), tip=0.8)
        elif look == "c89":
            for j, z in enumerate((L0 + 4.0, L0 + 9.0)):
                m.round_box(bd, 0, z, 1.6, 1.6, 17.0, 22.0, metal(P, "body_dark"), cut=0)
            for sx in (-1, 1):
                rod(m, bd, (sx * 6.4, 8.0, L0 + 2.0), (sx * 6.4, 8.0, L1 - 4.0), 1, metal(P, "accent"), extend=0.0)
                rod(m, top, (sx * 6.8, 2.4, L0 + 4.0), (sx * 6.8, 2.4, L0 + 26.0), 1, solid(P, "eye"), extend=0.0)
            m.box(hd, -6.0, 0.4, L0 - 9.0, 6.0, 3.6, L0 - 6.0, metal(P, "accent"), rotation=(-35, 0, 0),
                  pivot=(0, 2.0, L0 - 7.0))
        elif look == "franken":
            ball(m, hd, (0, 18.4, L0 + 1.0), 1.4, solid(P, "accent", glow=True), layers=1)
        elif look == "kettle":
            ball(m, bd, (0, 18.6, L0 + 6.0), 1.8, solid(P, "accent", glow=True), layers=1)
            for sx in (-1, 1):
                for j in range(3):
                    rod(m, bd, (sx * 6.6, 9.0 + j * 2.0, L0 + 8.0), (sx * 6.6, 9.0 + j * 2.0, L1 - 6.0), 1,
                        metal(P, "hub"), extend=0.0)
        elif look == "mole":
            ball(m, hd, (0, 8.0, L0 - 8.0), 4.2, solid(P, "snout"), layers=3, squash=0.7)
            for sx in (-1, 1):
                for j in range(4):
                    spike(m, bd, (sx * 6.0, 6.0, L0 + 4.0 + j * 1.6), (sx, -0.6, -0.4), 1.0, 5.0, solid(P, "accent"),
                          tip=0.8)
                for j in range(3):
                    m.box(hd, min(sx * 3.0, sx * 5.6), 9.0 + j * 0.8, L0 - 11.0, max(sx * 3.0, sx * 5.6), 9.3 + j * 0.8,
                          L0 - 10.4, solid(P, "black"))
        elif look == "raccoon":
            for sx in (-1, 1):
                m.box(hd, min(sx * 1.0, sx * 6.0), 13.0, L0 - 2.6, max(sx * 1.0, sx * 6.0), 15.4, L0 - 1.0,
                      solid(P, "accent"))
        elif look == "next2":
            for sx in (-1, 1):
                m.box(bd, min(sx * 6.0, sx * 11.0), 14.0, L0 + 8.0, max(sx * 6.0, sx * 11.0), 14.8, L0 + 18.0,
                      solid(P, "accent"), rotation=(0, 0, sx * 15), pivot=(sx * 6.0, 14.4, L0 + 13.0))
            m.box(bd, -0.5, 17.0, L1 - 10.0, 0.5, 23.0, L1 - 2.0, solid(P, "accent"), rotation=(-25, 0, 0),
                  pivot=(0, 17.0, L1 - 6.0))
        elif look == "next3":
            spike(m, hd, (0, 9.0, L0 - 5.0), (0, 0, -1), 4.0, 12.0, metal(P, "body", dark="body_dark"), tip=0.8)
            for j in range(6):
                m.round_box(bd, 0, L0 + 4.0 + j * 7.0, 6.6, 1.0, 16.0, 18.4, metal(P, "body_dark"), cut=1)
        elif look == "worm":
            for j in range(9):
                spike(m, bd, (0, 17.6, L0 + 2.0 + j * 5.0), (0, 1, 0.3), 1.2, 2.6, solid(P, "body_dark"), tip=0.8)
            for j in range(7):                                                     # huge fangs
                a = (j - 3) * 0.42
                spike(m, hd, (math.sin(a) * 5.4, 8.6, L0 - 6.0 + abs(a)), (0, -1, -0.2), 1.4, 4.4 - abs(j - 3) * 0.4,
                      solid(P, "tooth"), tip=0.8)
        return m
    return build
