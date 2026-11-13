"""Writhing Rot, the Paradox Pokémon (Bug/Dragon), the ancient paradox of Sudowoodo, built from boxes after the concept
art the user shared ("Writhing Rot (Infestower)"; artist not named).

A hollow, rotting log on four gnarled root legs: dark brown bark split with grain lines and pink wounds, Sudowoodo's
orange zigzag markings, a pink ringed hollow at the front, and pink-and-orange zigzag ankles over white claws. Out of
the hollow writhes a long, white, segmented grub of a neck in an S-curve, ending in a skull-like head with slanted
glowing yellow eyes, a pink cheek, a small orange horn and two curved orange-tipped mandibles. Four white segmented
feelers curl back from the top of the log, and a long white segmented tail with small orange spikes trails behind.

Shiny: a pale birch log with mint wounds and lime markings, and a creamy yellow grub.

Front is -z, y is up. 54 units tall to the top of the head; baseScale 0.72 (2.4 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, mix, rod, spike
from _route import pal, tone

SCALE = 0.72
HITBOX = [1.6, 2.4]
KIND = "quadruped"
K = 4
HEIGHT = 54
LOOK = ("a hollow rotting log on gnarled root legs with Sudowoodo's orange zigzags, a long white segmented grub neck "
        "writhing out of the hollow to a skull-like head with glowing yellow eyes and orange mandibles, white feelers "
        "and a segmented tail")

BASE = {"bark": (118, 104, 86), "bark_dark": (74, 64, 52), "bark_light": (150, 136, 112), "wound": (220, 116, 112),
        "wound_dark": (176, 80, 80), "hollow": (222, 124, 120), "zig": (240, 176, 92), "grub": (238, 236, 232),
        "grub_shade": (198, 198, 204), "seam": (120, 118, 126), "tip": (238, 140, 90), "tip_light": (248, 214, 160),
        "claw": (246, 246, 240), "eye": (226, 210, 70), "eye_glow": (232, 220, 80), "pupil": (70, 60, 20),
        "cheek": (230, 140, 140), "dark": (40, 34, 30)}
SHINY = {"bark": (176, 168, 150), "bark_dark": (118, 110, 96), "bark_light": (212, 206, 190), "wound": (130, 210, 170),
         "wound_dark": (80, 160, 120), "hollow": (140, 214, 176), "zig": (186, 226, 96), "grub": (244, 236, 190),
         "grub_shade": (210, 200, 150), "tip": (150, 210, 90), "tip_light": (220, 240, 170), "cheek": (150, 214, 170)}


def P(v):
    return pal(BASE, SHINY, v)


def zigzag(u, v, u0, v0, length, h):
    """Inside an orange zigzag band (a lightning stroke) running along u from u0, v0."""
    if not u0 <= u <= u0 + length:
        return False
    t = (u - u0) / 2.4
    centre = v0 + h * (1 - 2 * abs((t % 1) - 0.5) * 2) * 0.5
    return abs(v - centre) < 0.9 + 0.8 * (1 - (u - u0) / length)


def barkf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        if zigzag(z, y, -7, 21.5, 15, 4.5):
            return p["zig"], None                                        # Sudowoodo's orange zigzags
        if math.hypot((z - 2.5) / 2.6, (y - 18) / 0.6) < 1 or math.hypot((z - 4) / 2, (y - 16.2) / 0.5) < 1:
            return p["wound"], None                                      # split pink wounds
    if face == "up" and zigzag(z, abs(x), -7, 2.5, 14, 3):
        return p["zig"], None
    if (abs((y + math.sin(z * 0.5) * 0.8) % 3.3) < 0.35) and face in ("east", "west"):
        return tone(p["bark_dark"], face), None                          # grain lines along the log
    return tone(mix(p["bark"], p["bark_light"], 0.25) if y > 23 else p["bark"], face), None


def hollowf(x, y, z, face, variant, **k):
    """The log's front: a pink ringed hollow with a dark hole the neck comes out of."""
    p = P(variant)
    if face == "north":
        r = math.hypot(x, y - 20.5)
        if r < 3:
            return p["dark"], None
        rings = int(r * 1.4) % 2
        return (p["hollow"] if rings else p["wound_dark"]), None
    return barkf(x, y, z, face, variant)


def segf(az):
    """White grub segments: dark seams across the rod every 2.2 units (rods run along -z from z = az)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face in ("east", "west", "up", "down") and ((az - z) % 2.2) < 0.3:
            return p["seam"], None
        return tone(p["grub"] if face in ("up", "north", "east", "west") else p["grub_shade"], face), None
    return s


def tipf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["tip"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        dz, dy = z + 17.5, y - 51.3
        if -1.6 < dz < 1.6 and abs(dy + 0.35 * dz) < 0.75:
            return (p["pupil"] if abs(dz) < 0.25 else p["eye"]), p["eye_glow"]   # slanted glowing yellow eyes
        if math.hypot(dz - 1.8, dy + 1.3) < 0.8:
            return p["cheek"], None
        if abs(y - 49.3) < 0.2 and z < -17:
            return p["dark"], None                                       # mouth line
    if face == "north" and 50.4 < y < 52 and abs(abs(x) - 1.5) < 0.9:
        return p["eye"], p["eye_glow"]
    return tone(p["grub"] if face != "down" else p["grub_shade"], face), None


def legf(x, y, z, face, variant, **k):
    p = P(variant)
    if y < 6.5:
        if y < 4.2 or zigzag(x * 0 + y, (x if face in ("north", "south") else z), 3.8, 0, 2.7, 1.5):
            return tone(p["wound"] if y > 2.4 else p["zig"], face), None   # pink-and-orange zigzag ankles
    if (abs((x + z) % 2.6) < 0.3) and y > 8:
        return tone(p["bark_dark"], face), None
    return tone(p["bark"], face), None


def clawf(x, y, z, face, variant, **k):
    return tone(P(variant)["claw"], face), None


def segment_chain(m, bone, pts, ts, tip_len=0.0):
    """White segmented rods through pts; an orange tip on the last one if tip_len > 0."""
    for a, b, t in zip(pts, pts[1:], ts):
        rod(m, bone, a, b, t, segf(a[2]))
    if tip_len:
        a, b = pts[-2], pts[-1]
        d = [bb - aa for aa, bb in zip(a, b)]
        n = math.sqrt(sum(v * v for v in d))
        spike(m, bone, b, d, max(1, ts[-1] * 0.8), tip_len, tipf)


def build() -> Model:
    m = Model("writhingrot")
    top = m.bone("writhingrot", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    # the hollow log, lying along z, rounded by a cross of boxes
    m.box(bd, -6, 15, -7, 6, 27, 9, barkf)
    m.box(bd, -7, 16.5, -6.8, 7, 25.5, 8.8, barkf)
    m.box(bd, -4.5, 13.8, -6.9, 4.5, 28.2, 8.9, barkf)
    m.box(bd, -6.4, 14.6, -8.2, 6.4, 26.4, -7, hollowf)                     # the pink ringed hollow at the front

    # the grub neck: out of the hollow, down and forward, then rearing up in an S to the head
    nk = m.bone("neck", bd, (0, 20.5, -8))
    pts = [(0, 20.5, -7.5), (0, 18.5, -12), (0, 20, -16), (0, 26, -18.5), (0, 33, -18), (0, 40, -15.5),
           (0, 45.5, -14), (0, 49, -15.5)]
    segment_chain(m, nk, pts, (5, 4.6, 4.4, 4.2, 4, 3.8, 3.6))
    for a in pts[2:7]:
        spike(m, nk, (0, a[1] + 1.6, a[2] + 1.4), (0, 0.6, 1), 1, 1.8, tipf)   # small orange spikes down its back

    hd = m.bone("head", nk, (0, 49, -15.5))
    m.round_box(hd, 0, -17.2, 2.6, 3.4, 47.6, 53, headf, cut=1)               # skull-like head
    spike(m, hd, (0, 52.6, -15), (0, 0.6, 1), 1.4, 2.6, tipf, tip=0.8)        # small horn at the back of the head
    for sx in (-1, 1):                                                       # curved orange-tipped mandibles
        segment_chain(m, hd, [(sx * 1.6, 49.5, -19.5), (sx * 2.6, 49.5, -23), (sx * 3, 48, -25.5)], (2, 1.8))
        spike(m, hd, (sx * 3, 48.2, -25.5), (-sx * 0.3, -1, -0.5), 1.6, 3.4, tipf, tip=0.9)

    # four white feelers curling back from the top of the log
    fl = m.bone("mane", bd, (0, 27, 2))
    for i, (sx, z0, h) in enumerate(((-2.5, -2, 9), (1.5, 1, 10), (-1, 4, 8), (2.5, 6.5, 6))):
        pts = [(sx, 27, z0), (sx * 1.1, 27 + h * 0.5, z0 + 1.5), (sx * 1.2, 27 + h * 0.85, z0 + 4), (sx * 1.2, 27 + h, z0 + 7)]
        segment_chain(m, fl, pts, (2.4, 2, 1.6), tip_len=2.4)

    # the long segmented tail
    tl = m.bone("tail", bd, (0, 19, 9))
    pts = [(0, 19, 8.5), (0, 15, 13), (0, 11, 18), (0, 8, 23), (0, 6.5, 28)]
    segment_chain(m, tl, pts, (3.6, 3, 2.4, 1.6))
    for a in pts[1:4]:
        spike(m, tl, (0, a[1] + 1.2, a[2]), (0, 1, 0.5), 1, 1.6, tipf)

    # gnarled root legs: a thick trunk, splayed, with a root branching off, zigzag ankle and white claws
    for nm, lx, lz in (("leg_front_left", -5, -4.5), ("leg_front_right", 5, -4.5),
                       ("leg_back_left", -5, 5.5), ("leg_back_right", 5, 5.5)):
        lg = m.bone(nm, top, (lx, 16, lz))
        sx = 1 if lx > 0 else -1
        foot = (lx + sx * 3, 0, lz + (-1.5 if lz < 0 else 1.5))
        rod(m, lg, (lx, 17, lz), (foot[0] - sx * 0.5, 6, foot[2]), 3.4, legf)
        m.box(lg, foot[0] - 1.9, 0, foot[2] - 1.9, foot[0] + 1.9, 6.5, foot[2] + 1.9, legf)   # ankle
        rod(m, lg, (lx + sx * 0.5, 13, lz), (lx - sx * 0.6, 6, lz + (1.5 if lz < 0 else -1.5)), 1.6, legf)  # root
        for dx in (-1.2, 0, 1.2):
            spike(m, lg, (foot[0] + dx, 0.6, foot[2] - 1.8), (0, -0.2, -1), 1, 1.8, clawf)
    return m
