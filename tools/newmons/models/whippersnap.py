"""Whippersnap, the Whip Crab Pokémon (Bug), after the Zorneo region commission art by @RedmondJake (the art's own
name): a low, flat crab with a smooth teal shell over a tan face, heavy-lidded sleepy yellow eyes and two little white
fangs. Two very long tan whip antennae sweep forward and back over it; three pairs of thin tan legs hold it up, and
its front legs are short teal arms ending in hooked tan claws.

Shiny: a violet shell, slate legs, red eyes.

Front is -z, y is up. 13 units tall to the top of its antennae; baseScale 0.5 (0.4 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _route import tone
from _whip import P, antenna, leg, sleepy_eye, solid, tipped

SCALE = 0.5
HITBOX = [1.0, 0.8]
KIND = "quadruped"
K = 5
HEIGHT = 13
LOOK = ("a low flat crab with a teal shell over a tan face, sleepy yellow eyes, white fangs, very long whip antennae, "
        "thin tan legs and short teal arms with hooked tan claws")


def shellf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "down" or (face != "up" and y < 4.8):
        return tone(p["tan"], face), None                                    # the pale underside
    if face == "up" and abs(x) < 0.3 and z > -2:
        return p["teal_dark"], None                                          # the groove down its back
    return tone(p["teal_light"] if face == "up" else p["teal"], face), None


def facef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = sleepy_eye(p, x - sx * 1.7, y - 5.5, 1.15, 0.85)
            if e:
                return e, None
    return tone(p["tan"], face), None


def build() -> Model:
    m = Model("whippersnap")
    top = m.bone("whippersnap", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    m.round_box(bd, 0, 0.5, 5.0, 4.6, 4.0, 7.6, shellf, cut=1.8)              # the flat shell
    m.round_box(bd, 0, 0.8, 3.6, 3.4, 7.4, 8.6, shellf, cut=1.4)

    hd = m.bone("head", bd, (0, 5.5, -4))
    m.box(hd, -3.2, 3.6, -6.4, 3.2, 7.0, -3.6, facef)                         # its tan face
    m.box(hd, -3.6, 6.6, -6.8, 3.6, 7.8, -3.4, shellf)                        # the shell's brim over its eyes
    for sx in (-1, 1):
        spike(m, hd, (sx * 0.8, 3.9, -6.2), (0, -1, -0.2), 1.0, 2.0, solid("white"))          # little fangs
        antenna(m, hd, [(sx * 1.2, 7.0, -6.4), (sx * 2.4, 9.4, -8.6), (sx * 4.0, 11.8, -8.0), (sx * 6.0, 12.8, -4.0),
                        (sx * 8.0, 12.4, 1.0), (sx * 10.0, 10.4, 6.0), (sx * 11.0, 8.0, 10.0), (sx * 10.6, 7.0, 11.6)])

    for sx, side in ((-1, "left"), (1, "right")):
        for role, z in (("front", -1.5), ("mid", 1.5), ("back", 4.2)):         # thin tan walking legs
            lb = m.bone(f"leg_{role}_{side}", top, (sx * 4.2, 4.6, z))
            leg(m, lb, [(sx * 4.2, 4.6, z), (sx * 8.0, 8.0, z * 1.2), (sx * 11.0, 0.4, z * 1.6)], [1.0, 1.0],
                ["tan", "tan"])
        ar = m.bone(f"arm_{side}", bd, (sx * 3.0, 5.0, -4.0))                   # short teal arms, hooked claws
        rod(m, ar, (sx * 3.0, 5.0, -4.0), (sx * 7.0, 6.6, -7.0), 1.8, solid("teal"), extend=0.4)
        rod(m, ar, (sx * 7.0, 6.6, -7.0), (sx * 8.4, 3.2, -9.0), 1.8, solid("teal"), extend=0.4)
        rod(m, ar, (sx * 8.4, 3.2, -9.0), (sx * 7.4, 0.8, -11.4), 1.8, solid("tan"), extend=0.4)
        rod(m, ar, (sx * 7.4, 0.8, -11.4), (sx * 5.2, 0.8, -12.2), 1.2, tipped("tan", "cream", 0.4), extend=0.2)
        spike(m, ar, (sx * 8.6, 2.0, -9.6), (sx * 0.2, -0.6, -1), 1.0, 1.8, solid("cream"))      # a little thumb
    return m
