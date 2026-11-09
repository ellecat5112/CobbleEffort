"""Mega Brute Bonnet, built by hand from boxes (Cobblemon style), after ellecat5112's model and notes: a cute lizard
carrying a towering prototaxite trunk (the giant fungus of ancient times) ringed with shelf fungi, under a huge
round cap. Bright and friendly like Brute Bonnet, Foongus and Amoonguss: a red cap with big white spots, a cream
trunk with soft pink growth rings, glowing yellow shelf fungi, a minty lizard with big yellow eyes.

Front is -z, y is up, 1 unit = 1 texel. ~69 units tall: with baseScale 1.5 it stands about 6.5 blocks high.
"""
from __future__ import annotations

import math

from _boxmodel import Model, dist, hue_shift, mix

SCALE = 1.5
HITBOX = [3.5, 6.5]
SHINY_HUE = 0.5

BASE = {
    "cap": (232, 58, 88), "cap_top": (246, 98, 120), "spot": (252, 246, 240), "gill": (252, 206, 214),
    "spark": (255, 226, 92),
    "trunk": (246, 234, 214), "ring": (242, 194, 204), "bark": (230, 214, 192),
    "shelf": (255, 194, 70), "shelf_glow": (255, 236, 120),
    "lizard": (112, 210, 150), "lizard_dark": (84, 182, 128), "belly": (238, 246, 204), "spike": (246, 118, 150),
    "claw": (255, 255, 250), "eye": (255, 212, 60), "pupil": (34, 30, 40), "shine": (255, 255, 255),
    "mouth": (120, 50, 70),
}
SHIFTED = {"cap", "cap_top", "gill", "lizard", "lizard_dark", "spike", "shelf", "shelf_glow", "spark", "ring"}


def palette(variant):
    if variant != "shiny":
        return BASE
    return {k: (hue_shift(v, SHINY_HUE) if k in SHIFTED else v) for k, v in BASE.items()}


# --- the cap's spots, on its dome -------------------------------------------------------------------------------

CAP_C = (0.0, 57.0, 2.0)
CAP_R = (17.0, 12.0, 17.0)


def _on_dome(az, el):
    a, e = math.radians(az), math.radians(el)
    return (CAP_C[0] + CAP_R[0] * math.cos(e) * math.sin(a), CAP_C[1] + CAP_R[1] * math.sin(e),
            CAP_C[2] - CAP_R[2] * math.cos(e) * math.cos(a))


SPOTS = [_on_dome(az, el) for az, el in
         [(0, 15), (60, 20), (120, 12), (180, 18), (240, 14), (300, 22), (30, 50), (150, 48), (270, 52), (90, 78),
          (210, 40), (330, 45)]]
SPARKS = [_on_dome(az, el) for az, el in
          [(20, 32), (95, 35), (165, 30), (235, 33), (310, 8), (40, 5), (200, 5), (130, 62), (350, 70), (270, 25)]]


def cap(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "down":                                  # gills: pale with radial lines
        ang = math.atan2(x - CAP_C[0], z - CAP_C[2])
        return mix(P["gill"], P["cap"], 0.25) if int((ang + math.pi) * 24 / math.pi) % 2 == 0 else P["gill"]
    p = (x, y, z)
    if min(dist(p, s) for s in SPOTS) < 3.3:
        return P["spot"]
    if min(dist(p, s) for s in SPARKS) < 1.0:
        return P["spark"], P["spark"]
    return P["cap_top"] if face == "up" and y > 63 else P["cap"]


def gills(x, y, z, face, variant, **k):
    P = palette(variant)
    ang = math.atan2(x - CAP_C[0], z - CAP_C[2])
    return P["gill"] if int((ang + math.pi) * 24 / math.pi) % 2 else mix(P["gill"], P["cap"], 0.25)


def trunk(x, y, z, face, variant, **k):
    P = palette(variant)
    if face in ("up", "down"):
        return P["bark"]
    if int(y) % 6 == 0:                                 # growth rings, like a prototaxite's trunk
        return P["ring"]
    # soft vertical fibres
    return P["bark"] if int(x * 1.7 + z * 1.3) % 5 == 0 else P["trunk"]


def shelf(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "down":
        return P["shelf_glow"], P["shelf_glow"]
    if face == "up":
        return mix(P["shelf"], P["spot"], 0.25)
    return P["shelf"]


def mini_cap(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "down":
        return P["shelf_glow"], P["shelf_glow"]
    return P["spark"]


def lizard(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "down" or y < 6.2:
        return P["belly"]
    if face == "up" and abs(x) < 3 and int(z) % 4 == 0:  # a darker stripe of scales down the back
        return P["lizard_dark"]
    return P["lizard"]


def spike(x, y, z, face, variant, **k):
    return palette(variant)["spike"]


def claw_foot(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "north" and k["r"] == k["rows"] - 1 and k["c"] % 2 == 0:
        return P["claw"]                                 # three little white claws
    return P["belly"] if face == "down" else P["lizard"]


def white(x, y, z, face, variant, **k):
    return palette(variant)["claw"]


def skull(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "north" and 10.5 <= y <= 15:
        for side in (-1, 1):                             # big round yellow eyes with a highlight
            dx = x - side * 3.5
            if abs(dx) <= 2.1:
                corner = abs(dx) > 1.6 and (y > 14.4 or y < 11)
                if corner:
                    break                                # round the eye's corners
                if dx * side < 0.2 and y < 13.2:         # pupil, towards the middle
                    return P["pupil"], (40, 30, 10)
                if dx * side > 0.6 and y > 13.4:
                    return P["shine"], (255, 255, 255)
                return P["eye"], P["eye"]
    if face in ("east", "west") and 8 <= y <= 10 and z < -16:
        return mix(P["lizard"], P["spike"], 0.55)        # rosy cheeks
    return lizard(x, y, z, face, variant)


def snout(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "north":
        if 5.8 < y < 6.8 and abs(x) < 3.6:               # a little smile
            return P["mouth"]
        if 8.4 < y < 9.4 and abs(abs(x) - 2) < 0.6:      # nostrils
            return P["lizard_dark"]
    return lizard(x, y, z, face, variant)


def build() -> Model:
    m = Model("brutebonnet_mega")
    root = m.bone("brutebonnet_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 10, 2))

    # the lizard
    m.box(body, -7, 5, -9, 7, 15, 13, lizard)                       # torso
    m.box(body, -6, 4, -7, 6, 5, 11, lizard)                         # belly
    for zz in (-6, 10):
        m.mirror_x(body, 4, 15, zz, 6, 17, zz + 2, spike)            # shoulder and hip spikes
    # the prototaxite trunk: rounded, tapering, with a flared root
    m.round_box(body, 0, 2, 8, 8, 15, 18, trunk, cut=3)
    m.round_box(body, 0, 2, 6, 6, 18, 31, trunk, cut=2)
    m.round_box(body, 0, 2, 5, 5, 31, 44, trunk, cut=2)
    m.round_box(body, 0, 2, 4, 4, 44, 56, trunk, cut=1)
    # shelf fungi round the trunk, and little glowing mushrooms
    m.box(body, 6, 22, -2, 11, 24, 5, shelf)
    m.box(body, -11, 31, -1, -5, 33, 6, shelf)
    m.box(body, 5, 38, 0, 9, 40, 6, shelf)
    m.box(body, -3, 26, -8, 3, 28, -4, shelf)
    m.box(body, -8, 46, 0, -4, 48, 5, shelf)
    m.box(body, -2, 36, -6, 2, 37, -3, shelf)
    for (sx, sy, sz) in ((7, 30, 3), (-7, 40, 4), (3, 49, -3)):
        m.box(body, sx - 0.5, sy, sz - 0.5, sx + 0.5, sy + 2, sz + 0.5, white)       # stem
        m.box(body, sx - 1.5, sy + 2, sz - 1.5, sx + 1.5, sy + 3, sz + 1.5, mini_cap)

    # the cap
    capb = m.bone("cap", body, (0, 57, 2))
    m.round_box(capb, 0, 2, 12, 12, 56, 57, gills, cut=4)
    for r, y0, y1 in ((17, 57, 59), (16, 59, 61), (14, 61, 63), (12, 63, 65), (9, 65, 67), (5, 67, 68)):
        m.round_box(capb, 0, 2, r, r, y0, y1, cap, cut=max(1, round(r * 0.32)))

    # the head
    head = m.bone("head", body, (0, 11, -9))
    m.box(head, -7, 5, -20, 7, 16, -9, skull)
    m.box(head, -6, 5, -24, 6, 10, -20, snout)
    m.box(head, -6, 3, -23, 6, 5, -12, lizard)                       # lower jaw
    m.mirror_x(head, 3, 3, -24, 4, 5, -23, white)                    # fangs
    m.mirror_x(head, 2, 16, -17, 4, 18, -15, spike)                  # little horns

    # legs (left = +x)
    for name, zf, zb in (("leg_front_left", -8, -4), ("leg_back_left", 7, 11)):
        for sgn, nm in ((1, name), (-1, name.replace("left", "right"))):
            leg = m.bone(nm, root, (sgn * 7, 8, (zf + zb) / 2))
            x0, x1 = (5, 9) if sgn > 0 else (-9, -5)
            m.box(leg, x0, 2, zf, x1, 8, zb, lizard)
            fx0, fx1 = (5, 10) if sgn > 0 else (-10, -5)
            m.box(leg, fx0, 0, zf - 2, fx1, 2, zb, claw_foot)

    # the tail
    tail = m.bone("tail", body, (0, 10, 13))
    m.box(tail, -4, 6, 13, 4, 13, 22, lizard)
    m.box(tail, -3, 7, 22, 3, 11, 31, lizard)
    m.box(tail, -2, 8, 31, 2, 10, 40, lizard)
    m.box(tail, -1, 8.5, 40, 1, 9.5, 45, lizard)
    for zz in (15, 24, 33):
        m.box(tail, -1, 13 if zz < 22 else (11 if zz < 31 else 10), zz, 1, (13 if zz < 22 else (11 if zz < 31 else 10)) + 2, zz + 2, spike)
    return m
