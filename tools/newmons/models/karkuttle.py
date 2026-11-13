"""Karkuttle, the Whip Crab Pokémon (Bug), Whippersnap evolved, after the Zorneo region commission art by @RedmondJake
(the art's own name): a big teal crab-spider striped with dark zigzags, a tan hood with a pointed brim over its
heavy-lidded yellow eyes and a mouth full of white fangs with orange tips. Its whip antennae arch far back over it; it
stands high on three pairs of very long legs, tan above and teal below, and its front legs are huge spiked teal arms
ending in hooked tan claws tipped with orange.

Shiny: a violet shell and arms, slate legs, red eyes.

Front is -z, y is up. 26 units tall to the top of its antennae; baseScale 0.9 (1.5 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _route import tone
from _whip import P, antenna, leg, sleepy_eye, solid, tipped

SCALE = 0.9
HITBOX = [2.0, 1.6]
KIND = "quadruped"
K = 3
HEIGHT = 26
LOOK = ("a big teal crab-spider with dark zigzag stripes, a tan hood over sleepy yellow eyes, orange-tipped white fangs, "
        "long arching whip antennae, very long legs and huge spiked teal arms with hooked claws")


def shellf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "down" or (face != "up" and y < 10.8):
        return tone(p["tan"], face), None
    if face == "up" and ((z + abs(x) * 0.8) % 3.2) < 0.6:
        return p["stripe"], None                                            # zigzag stripes over its back
    if face in ("east", "west") and ((z + abs(y - 13.5) * 0.9) % 3.2) < 0.6:
        return p["stripe"], None                                            # chevrons down its sides
    if face == "south" and ((abs(x) + abs(y - 13.5) * 0.9) % 3.2) < 0.6:
        return p["stripe"], None
    return tone(p["teal_light"] if face == "up" else p["teal"], face), None


def facef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = sleepy_eye(p, x - sx * 2.2, y - 13.4, 1.4, 1.05)
            if e:
                return e, None
    if face in ("east", "west") and abs(x) > 3.8:
        e = sleepy_eye(p, z + 7.6, y - 13.4, 1.0, 0.9)
        if e:
            return e, None
    return tone(p["tan"], face), None


def build() -> Model:
    m = Model("karkuttle")
    top = m.bone("karkuttle", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 1.4, 7.4, 7.0, 9.6, 16.8, shellf, cut=2.6)            # the striped shell
    m.round_box(bd, 0, 1.8, 5.6, 5.4, 16.6, 18.4, shellf, cut=2.0)

    hd = m.bone("head", bd, (0, 13, -5))
    m.box(hd, -4.0, 10.0, -9.0, 4.0, 15.4, -4.4, facef)                       # its tan face
    m.box(hd, -4.2, 15.4, -10.0, 4.2, 17.0, -4.2, solid("tan"))                # the hood
    spike(m, hd, (0, 16.2, -9.8), (0, -0.25, -1), 2.6, 2.6, solid("tan"), tip=1.2)   # its pointed brim
    for sx in (-1, 1):
        rod(m, hd, (sx * 1.2, 10.8, -8.2), (sx * 1.7, 7.8, -9.6), 1.4, solid("white"), extend=0.3)   # big fangs
        rod(m, hd, (sx * 1.7, 8.0, -9.5), (sx * 1.0, 6.2, -9.2), 1.0, tipped("white", "orange", 0.6), extend=0.2)
        spike(m, hd, (sx * 2.8, 10.6, -8.0), (sx * 0.2, -1, -0.3), 1.0, 2.2, tipped("white", "orange", 0.45))
        antenna(m, hd, [(sx * 1.6, 15.6, -9.0), (sx * 2.0, 18.0, -11.0), (sx * 3.6, 22.0, -11.0), (sx * 5.6, 25.0, -7.0),
                        (sx * 8.0, 26.0, -1.0), (sx * 11.0, 24.6, 6.0), (sx * 13.0, 21.0, 13.0), (sx * 14.0, 17.0, 18.0),
                        (sx * 13.4, 15.4, 20.0)])

    for sx, side in ((-1, "left"), (1, "right")):
        for role, z in (("front", -2.0), ("mid", 1.6), ("back", 5.0)):         # very long legs
            lb = m.bone(f"leg_{role}_{side}", top, (sx * 6.6, 11.0, z))
            leg(m, lb, [(sx * 6.6, 11.0, z), (sx * 13.0, 20.0, z * 1.4), (sx * 19.0, 9.0, z * 2.0), (sx * 21.0, 2.0, z * 2.3)],
                [2.0, 2.0, 1.6], ["tan", "teal", "teal"], claw=((sx * 0.2, -1, 0), 1.2, 2.2, "tan"))
        ar = m.bone(f"arm_{side}", bd, (sx * 5.0, 11.0, -5.6))                  # huge spiked arms
        rod(m, ar, (sx * 5.0, 11.0, -5.6), (sx * 11.0, 15.0, -10.0), 2.6, solid("teal"), extend=0.5)
        rod(m, ar, (sx * 11.0, 15.0, -10.0), (sx * 13.0, 7.0, -15.0), 2.6, solid("teal"), extend=0.5)
        spike(m, ar, (sx * 11.2, 16.0, -10.0), (sx * 0.3, 1, 0.2), 1.4, 2.6, tipped("white", "orange", 0.45))
        spike(m, ar, (sx * 12.4, 11.0, -13.2), (sx * 1, 0.3, -0.2), 1.2, 2.2, tipped("white", "orange", 0.45))
        m.round_box(ar, sx * 13.0, -15.0, 2.0, 2.0, 4.0, 8.6, solid("tan"), cut=0.8)   # the claw's palm
        rod(m, ar, (sx * 13.0, 5.6, -15.6), (sx * 11.0, 2.0, -19.0), 2.0, solid("tan"), extend=0.4)
        rod(m, ar, (sx * 11.0, 2.0, -19.0), (sx * 8.4, 1.4, -20.6), 1.2, tipped("tan", "orange", 0.55), extend=0.2)
        spike(m, ar, (sx * 13.6, 4.6, -14.0), (-sx * 0.2, -1, -0.6), 1.0, 2.2, tipped("cream", "orange", 0.45))
    return m
