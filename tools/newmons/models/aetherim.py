"""Aetherim, the Energy Golem Pokémon (Normal), built from boxes after the fakemon art by @LMRTRAINER that the user
shared (the art's own name): a tiny golem of energy. A round pale head under a crest of three big curved cream plates,
big blue eyes, a glowing pearl on its forehead, a small rounded body ending in a pointed spike, and two big floating
stone fists with dark knuckles, a pearl set in one of them.

It takes the type of the tuft of hair it holds (its cosmetic slot): each type form (FORM_VARIANTS) turns its pearls
and eyes that type's colour, glowing, and tints its crest a little.

Shiny: a pale gold crest and bronze fists.

Front is -z, y is up. 20 units tall to the crest; baseScale 0.5 (0.5 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, mix, rod
from _route import tone

SCALE = 0.5
HITBOX = [1.2, 1.4]
KIND = "floater"
K = 6
HEIGHT = 20
LOOK = ("a tiny energy golem with a crest of three curved cream plates, big blue eyes, a glowing pearl on its forehead "
        "and two big floating stone fists")

TYPE_COLOURS = {"fire": (240, 128, 48), "water": (104, 144, 240), "grass": (120, 200, 80), "electric": (248, 208, 48),
                "ice": (152, 216, 216), "fighting": (192, 48, 40), "poison": (160, 64, 160), "ground": (224, 192, 104),
                "flying": (168, 144, 240), "psychic": (248, 88, 136), "bug": (168, 184, 32), "rock": (184, 160, 56),
                "ghost": (112, 88, 152), "dragon": (112, 56, 248), "dark": (112, 88, 72), "steel": (184, 184, 208),
                "fairy": (238, 153, 172)}
FORM_VARIANTS = [(f"{t}-tuft", t) for t in TYPE_COLOURS]

BASE = {"crest": (232, 230, 216), "crest_shade": (196, 198, 188), "head": (222, 224, 220), "stone": (150, 160, 170),
        "stone_dark": (112, 122, 134), "knuckle": (78, 90, 104), "eye": (52, 72, 150), "eye_light": (110, 140, 214),
        "glint": (240, 244, 255), "pearl": (246, 246, 250), "pearl_shade": (206, 212, 222)}
SHINY = {"crest": (232, 214, 150), "crest_shade": (200, 178, 112), "stone": (180, 140, 100), "stone_dark": (140, 104, 72),
         "knuckle": (104, 76, 54)}


def P(variant):
    """Palette for a variant: None, "shiny", "<type>" or "<type>_shiny"."""
    v = variant or ""
    shiny = v.endswith("shiny")
    t = v.removesuffix("_shiny").removesuffix("shiny")
    p = {**BASE, **(SHINY if shiny else {})}
    if t in TYPE_COLOURS:
        c = TYPE_COLOURS[t]
        p.update({"pearl": mix(c, (255, 255, 255), 0.35), "pearl_shade": c, "eye": mix(c, (0, 0, 0), 0.35),
                  "eye_light": mix(c, (255, 255, 255), 0.25), "crest": mix(p["crest"], c, 0.14),
                  "crest_shade": mix(p["crest_shade"], c, 0.14)})
        p["typed"] = True
    return p


def crestf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["crest"] if face in ("up", "north", "south") else p["crest_shade"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            ex, ey = sx * 1.6, 11.2
            d = math.hypot((x - ex) / 1.15, (y - ey) / 1.35)
            if d < 1:
                if math.hypot(x - ex + 0.35, y - ey - 0.45) < 0.32:
                    return p["glint"], None
                return (p["eye_light"] if d > 0.62 else p["eye"]), (p["eye_light"] if p.get("typed") else None)
    return tone(p["head"], face), None


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["head"] if y > 6 else p["crest_shade"], face), None


def pearlf(x, y, z, face, variant, **k):
    p = P(variant)
    c = p["pearl"] if face in ("north", "up") else p["pearl_shade"]
    return c, c


def stonef(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["stone"] if face != "down" else p["stone_dark"], face), None


def knucklef(x, y, z, face, variant, **k):
    return tone(P(variant)["knuckle"], face), None


def build() -> Model:
    m = Model("aetherim")
    top = m.bone("aetherim", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    m.round_box(bd, 0, 0.2, 1.8, 1.6, 5, 8.2, bodyf, cut=0.6)                       # small rounded body
    rod(m, bd, (0, 5.5, 0.2), (0, 1.5, 0.6), 1.4, bodyf, extend=0.2)               # pointed spike below
    rod(m, bd, (0, 2.6, 0.5), (0, 0.6, 0.7), 0.8, bodyf, extend=0.1)
    hd = m.bone("head", bd, (0, 9, 0))
    m.round_box(hd, 0, 0, 3.2, 2.8, 7.8, 14, headf, cut=1.1)                        # round head
    m.box(hd, -0.9, 13, -3.4, 0.9, 14.8, -2.6, pearlf)                              # forehead pearl
    # the crest: three big curved plates, the middle one tall, the side ones sweeping out
    m.box(hd, -1.6, 13.4, -2.6, 1.6, 20, 2.4, crestf, rotation=(-24, 0, 0), pivot=(0, 13.5, 0))
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.2, sx * 4.8), 13, -2.4, max(sx * 1.2, sx * 4.8), 18, 2.2, crestf,
              rotation=(-18, 0, sx * 30), pivot=(sx * 1.2, 13.4, 0))
        m.box(hd, min(sx * 4, sx * 7.6), 12.6, -1.6, max(sx * 4, sx * 7.6), 14.6, 1.8, crestf,
              rotation=(0, 0, sx * 38), pivot=(sx * 4.2, 14.4, 0))                  # the plates' curled tips
    # two big floating stone fists with dark knuckles; a pearl in the right one
    for nm, sx in (("arm_left", -1), ("arm_right", 1)):
        ar = m.bone(nm, bd, (sx * 6, 7, -1))
        m.round_box(ar, sx * 6.5, -1, 2.8, 2.8, 4.4, 10, stonef, cut=1)
        for dx in (-1.5, 0, 1.5):                                                    # dark knuckles on top, at the front
            m.box(ar, sx * 6.5 + dx - 0.65, 9.4, -3.9, sx * 6.5 + dx + 0.65, 10.8, -2.5, knucklef)
        m.box(ar, sx * 6.5 + sx * 2.4, 6, -3.2, sx * 6.5 + sx * 3.4, 7.6, -1.8, knucklef)   # thumb
        if sx > 0:
            m.box(ar, sx * 6.5 - 1.1, 6.2, -4, sx * 6.5 + 1.1, 8.4, -3.4, pearlf)      # pearl in the fist
    return m
