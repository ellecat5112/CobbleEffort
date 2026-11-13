"""Shared colours and parts for the whip crab line (Whippersnap, Karkuttle), after the Zorneo region commission art by
@RedmondJake (names kept; Zorneo region designs are used with the creators' permission): low teal-shelled crabs like
whip spiders, with sleepy yellow eyes, white fangs, very long whip antennae and thin legs, their front legs grown into
long teal arms ending in hooked tan claws.

Shiny: a violet shell and arms, slate legs and red eyes.
"""
from __future__ import annotations

from _boxmodel import rod, spike
from _route import along, pal, tone

BASE = {"teal": (98, 212, 188), "teal_dark": (50, 148, 134), "teal_light": (152, 236, 214), "stripe": (34, 98, 94),
        "tan": (214, 192, 168), "tan_dark": (176, 152, 128), "cream": (238, 228, 210), "eye": (238, 212, 70),
        "pupil": (64, 52, 28), "white": (246, 244, 236), "orange": (238, 136, 58)}
SHINY = {"teal": (176, 124, 214), "teal_dark": (122, 78, 164), "teal_light": (212, 172, 240), "stripe": (70, 40, 104),
         "tan": (170, 172, 186), "tan_dark": (132, 134, 150), "cream": (214, 216, 226), "eye": (236, 70, 70),
         "pupil": (70, 20, 24)}


def P(v):
    return pal(BASE, SHINY, v)


def solid(key):
    def s(x, y, z, face, variant, **k):
        return tone(P(variant)[key], face), None
    return s


def tipped(base_key, tip_key, frac):
    """A rod coloured base_key, its last `frac` coloured tip_key (orange-tipped fangs and claws)."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        return tone(p[tip_key] if along(z, box) > 1 - frac else p[base_key], face), None
    return s


def sleepy_eye(p, dx, dy, rx, ry):
    """A heavy-lidded yellow eye: the top part hidden under a lid, a dark pupil low down. -> colour or None."""
    if (dx / rx) ** 2 + (dy / ry) ** 2 > 1:
        return None
    if dy > ry * 0.15:
        return p["teal_dark"]
    if (dx / (rx * 0.32)) ** 2 + ((dy + ry * 0.35) / (ry * 0.4)) ** 2 < 1:
        return p["pupil"]
    return p["eye"]


def antenna(m, bone, pts, t=1.0):
    """A long whip antenna through pts: tan, a darker hooked end."""
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        rod(m, bone, a, b, t, solid("tan_dark" if i == len(pts) - 2 else "tan"), extend=0.6)


def leg(m, bone, pts, ts, keys, claw=None):
    """A jointed leg through pts (thicknesses ts, colour keys per segment), with a claw spike at the foot."""
    for a, b, t, key in zip(pts, pts[1:], ts, keys):
        rod(m, bone, a, b, t, solid(key), extend=0.4)
    if claw:
        d, w, h, key = claw
        spike(m, bone, pts[-1], d, w, h, solid(key))
