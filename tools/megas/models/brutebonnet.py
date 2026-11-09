"""Mega Brute Bonnet, hand-built from boxes in Cobblemon's style.

Brute Bonnet (official art: a brown cap with a grey and a red panel, each with spikes; long green moss hanging from
the rim; a pale grey body with a fanged pink mouth and a yellow eye; Poké-Ball-like mushroom caps held as fists; a
dark brown base and tail), grown into a prototaxite: its body is a tall pale trunk with brown growth rings and shelf
fungi, under a huge cap with long moss. Taller and angrier: two glaring eyes, a wide fanged mouth, stubby legs
and stubby arms gripping big mushroom-cap shields.

Front is -z, y is up, 1 unit = 1 texel. ~64 units tall; baseScale 1.6 makes it about 6.4 blocks high.
"""
from __future__ import annotations

import math

from _boxmodel import Model, hue_shift, mix

SCALE = 1.6
HITBOX = [3.2, 6.4]
LOOK = "a towering prototaxite: a pale ringed trunk with glowing shelf fungi, stubby root legs and arms gripping mushroom-cap shields, two glaring eyes and a fanged mouth, under a huge brown cap with red and grey spiked panels and long hanging moss"
KIND = "biped"
SHINY_HUE = 0.3

BASE = {
    "cap": (112, 64, 44), "cap_dark": (84, 46, 32), "panel_grey": (196, 198, 190), "panel_red": (200, 52, 48),
    "spike_grey": (176, 178, 170), "spike_red": (176, 40, 40), "gill": (150, 104, 76),
    "moss": (150, 214, 110), "moss_dark": (102, 170, 78), "moss_light": (190, 236, 140),
    "trunk": (216, 218, 208), "trunk_shade": (196, 198, 188), "ring": (168, 150, 132),
    "root": (96, 56, 40), "root_dark": (72, 40, 30),
    "eye": (236, 210, 40), "pupil": (40, 30, 20), "brow": (90, 70, 60),
    "mouth": (120, 40, 70), "tongue": (236, 150, 186), "tooth": (252, 252, 246),
    "ball_red": (206, 54, 50), "ball_white": (232, 232, 226), "ball_rim": (100, 58, 42),
    "shelf": (148, 92, 60), "shelf_top": (176, 116, 78), "shelf_glow": (210, 255, 160), "spore": (220, 255, 170),
}
# shiny: lavender moss, a plum cap with a pink panel, teal shelf glow
SHINY = {"cap": (92, 58, 92), "cap_dark": (68, 40, 70), "panel_red": (226, 96, 150), "spike_red": (200, 76, 130),
         "gill": (140, 100, 140), "moss": (190, 160, 236), "moss_dark": (146, 116, 200), "moss_light": (222, 200, 250),
         "ball_red": (226, 96, 150), "ring": (120, 86, 120), "root": (86, 56, 84), "root_dark": (64, 40, 64),
         "ball_rim": (92, 58, 92), "shelf": (130, 90, 130), "shelf_top": (160, 116, 160), "shelf_glow": (150, 255, 230),
         "spore": (170, 255, 240)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def _h(*v):
    n = 0
    for x in v:
        n = (n * 1000003 + int(round(x * 7919))) & 0xFFFFFFFF
    n ^= n >> 13
    n = (n * 0x5BD1E995) & 0xFFFFFFFF
    return ((n ^ (n >> 15)) & 0xFFFF) / 65536


# --- heights -------------------------------------------------------------------------------------------------------
LEG_TOP = 9
BODY = (8, 34)          # the lower trunk
HEAD = (34, 50)         # the upper trunk with the face
CAP_Y = 49              # the cap's rim


# --- shaders -------------------------------------------------------------------------------------------------------

def cap(x, y, z, face, variant, **k):
    """The cap: brown, with a grey panel at the back-left and a red panel at the front-right (as Brute Bonnet's),
    a darker band at the rim, gills underneath."""
    P = palette(variant)
    if face == "down":
        ang = math.atan2(x, z)
        return P["gill"] if int((ang + math.pi) * 20 / math.pi) % 2 else mix(P["gill"], P["cap_dark"], 0.4)
    ang = math.degrees(math.atan2(x, -z)) % 360          # 0 = front, 90 = left (+x)
    if y < CAP_Y + 1.5 and face != "up":
        return P["cap_dark"]
    if 20 <= ang <= 75:
        return P["panel_red"]
    if 200 <= ang <= 255:
        return P["panel_grey"]
    return P["cap"]


def spike_red(x, y, z, face, variant, **k):
    return palette(variant)["spike_red"]


def spike_grey(x, y, z, face, variant, **k):
    return palette(variant)["spike_grey"]


def moss(x, y, z, face, variant, r=0, c=0, rows=1, cols=1, box=None, **k):
    """Hanging moss: jagged strands of different lengths (cut out below each strand's end)."""
    P = palette(variant)
    seed = box.lo[0] * 3.1 + box.lo[2] * 1.7
    length = rows * (0.5 + 0.5 * _h(seed, c // 2))
    if c % 2 == 1:
        length -= 1.5                                   # pointed strand tips
    if r >= length:
        return (0, 0, 0, 0)
    if r < 2:
        return P["moss_dark"]
    return P["moss_light"] if (c // 2 + int(seed)) % 3 == 0 else P["moss"]


def trunk(x, y, z, face, variant, **k):
    """The prototaxite trunk: pale grey with brown growth rings."""
    P = palette(variant)
    if face in ("up", "down"):
        return P["trunk_shade"]
    if int(math.floor(y)) % 8 == 3 and y < HEAD[0] - 1:
        return P["ring"]
    return P["trunk_shade"] if int(x * 1.3 + z * 1.7) % 7 == 0 else P["trunk"]


EYE_Y = (42.0, 45.5)


def face(x, y, z, face, variant, **k):
    """The upper trunk: two glaring yellow eyes under heavy brows and a wide mouth of jagged teeth."""
    P = palette(variant)
    if face == "north":
        for side in (-1, 1):
            dx = (x - side * 3.8) * side                # + outward from the eye centre
            top = EYE_Y[1] - 0.55 * (2.4 - dx)          # slanted top edge, lower towards the middle: a glare
            if -2.4 <= dx <= 2.4 and EYE_Y[0] <= y <= top:
                if -0.9 <= dx <= 0.5 and y <= EYE_Y[0] + 2.2:
                    return P["pupil"], (50, 40, 10)
                return P["eye"], P["eye"]
            if -2.6 <= dx <= 2.6 and top < y <= top + 1.1:
                return P["brow"]
        if 35.5 <= y <= 40.5 and abs(x) <= 6.5:         # the mouth
            tri = 1.5 - abs(((x + 8) % 2.0) - 1.0) * 1.5
            if y >= 40.5 - tri - 0.3:
                return P["tooth"]
            if y <= 35.5 + tri * 0.8 + 0.3 and int(x + 8) % 2 == 1:
                return P["tooth"]
            if y < 37.2 and abs(x) < 3.2:
                return P["tongue"]
            return P["mouth"]
    return trunk(x, y, z, face, variant)


def root(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["root_dark"] if face == "down" or (face != "up" and y < 2) else P["root"]


def shelf(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "down":
        return P["shelf_glow"], P["shelf_glow"]          # softly glowing gills
    if face == "up":
        return P["shelf_top"]
    return P["shelf"]


def ball(x, y, z, face, variant, box=None, **k):
    """A mushroom-cap shield like Brute Bonnet's: red top, white bottom, brown rim, a white button."""
    P = palette(variant)
    x0, y0, z0 = box.lo
    w, h, d = box.size
    cy = y0 + h / 2
    cz = z0 + d / 2
    if face in ("east", "west"):
        rr = math.hypot(y - cy, z - cz)
        if rr < 1.6:
            return P["ball_white"]
        if rr < 2.4:
            return P["ball_rim"]
        if abs(y - cy) < 0.7:
            return P["ball_rim"]
        return P["ball_red"] if y > cy else P["ball_white"]
    return P["ball_rim"]


def tooth(x, y, z, face, variant, **k):
    return palette(variant)["tooth"]


def spore(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["spore"], P["spore"]


# --- the model -----------------------------------------------------------------------------------------------------

def build() -> Model:
    m = Model("brutebonnet_mega")
    root_b = m.bone("brutebonnet_mega", None, (0, 0, 0))
    body = m.bone("body", root_b, (0, 16, 0))

    # the brown root base, its little tail, and the lower trunk
    m.round_box(body, 0, 0, 11, 10, 7, 12, root, cut=3)
    m.box(body, -3, 7, 8, 3, 11, 16, root)
    m.box(body, -2, 7, 16, 2, 9, 21, root)
    m.round_box(body, 0, 0, 9, 8, 12, BODY[1], trunk, cut=3)
    # shelf fungi round the trunk, glowing softly underneath
    for (x0, y0, z0, x1, z1) in ((8, 18, -3, 13, 4), (-13, 24, -1, -8, 6), (-4, 15, 7, 4, 12), (5, 28, 5, 10, 10), (-11, 13, -6, -7, -1)):
        m.box(body, x0, y0, z0, x1, y0 + 2, z1, shelf)

    # stubby arms gripping mushroom-cap shields (left = +x)
    for sgn, nm in ((1, "arm_left"), (-1, "arm_right")):
        arm = m.bone(nm, body, (sgn * 9, 30, 0))
        x0, x1 = (8, 13) if sgn > 0 else (-13, -8)
        m.box(arm, x0, 22, -3, x1, 31, 3, trunk)
        bx0 = 12 if sgn > 0 else -15
        m.box(arm, bx0, 15, -7, bx0 + 3, 27, 5, ball)          # the shield, facing outwards

    # the upper trunk with the face, the cap and its moss: the head
    head = m.bone("head", body, (0, HEAD[0], 0))
    m.round_box(head, 0, 0, 8, 7, HEAD[0], HEAD[1] + 1, face, cut=3)
    m.mirror_x(head, 4.5, 39.5, -7.6, 5.5, 42, -6.6, tooth)        # two big fangs
    capb = m.bone("cap", head, (0, CAP_Y, 0))
    m.round_box(capb, 0, 0, 13, 13, CAP_Y - 1, CAP_Y, cap, cut=4)    # gills
    for r, y0, y1 in ((20, 49, 51), (19, 51, 53), (17, 53, 55), (14, 55, 57), (10, 57, 59), (6, 59, 61), (3, 61, 62)):
        m.round_box(capb, 0, 0, r, r, y0, y1, cap, cut=max(1, round(r * 0.32)))
    # spikes: red on the red panel, grey on the grey panel (as Brute Bonnet's)
    for ang, sh in ((35, spike_red), (60, spike_red), (215, spike_grey), (240, spike_grey)):
        a = math.radians(ang)
        px, pz = 11 * math.sin(a), -11 * math.cos(a)
        m.box(capb, px - 1.5, 56, pz - 1.5, px + 1.5, 59, pz + 1.5, sh)
        m.box(capb, px - 0.5, 59, pz - 0.5, px + 0.5, 61, pz + 0.5, sh)
    # long moss hanging from the rim, all the way round (shorter in front of the eyes)
    for n in range(18):
        a = 2 * math.pi * n / 18 + 0.17
        px, pz = 18 * math.sin(a), -18 * math.cos(a)
        w = 6
        h = 16 if n % 2 else 12
        if pz < -10 and abs(px) < 11:
            continue                                    # a gap in front, so its glare shows
        if pz < -6:
            h = 7
        m.box(capb, px - w / 2, CAP_Y - 1 - h, pz, px + w / 2, CAP_Y - 1, pz, moss,
              rotation=(0, -math.degrees(a), 0), pivot=(px, CAP_Y - 1, pz))
    # a few glowing spores drifting round the cap
    for (sx, sy, sz) in ((15, 60, -6), (-16, 58, 5), (6, 64, 9), (-9, 63, -11)):
        m.box(capb, sx, sy, sz, sx + 1, sy + 1, sz + 1, spore)

    # stubby root legs
    for sgn, nm in ((1, "leg_front_left"), (-1, "leg_front_right")):
        leg = m.bone(nm, root_b, (sgn * 6, LEG_TOP, 0))
        x0, x1 = (2, 10) if sgn > 0 else (-10, -2)
        m.box(leg, x0, 2, -4, x1, LEG_TOP, 4, root)
        fx0, fx1 = (1, 11) if sgn > 0 else (-11, -1)
        m.box(leg, fx0, 0, -6, fx1, 2, 5, root)
        for tx in ((2, 5, 8) if sgn > 0 else (-3, -6, -9)):
            m.box(leg, tx, 0, -8, tx + 1, 1, -6, root)              # root toes
    return m
