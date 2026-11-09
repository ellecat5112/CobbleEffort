"""Celebi (Psychic/Grass -> Dark/Fire): an ember sprite of a burnt forest. Celebi is modelled only by AllTheMons x
Mega Showdown (no derivatives), so this is an original texture painted onto that model's UV layout (extracted with
tools/addons/extract_layout.py; none of its art is read): charcoal skin with an ash-pale face, glowing ember eyes,
a smouldering crest, ember wings and burning antenna tips."""
from __future__ import annotations

import math

from PIL import Image

from _kit import faces, shade
from _materials import LIGHT

LINE = ["celebi"]
ADDON = {"layout": "layouts/atm_celebi_layout.json", "source": "AllTheMons x Mega Showdown"}

PAL = {False: {"skin": (58, 42, 48), "face": (168, 150, 146), "crest": (150, 44, 30), "wing": (214, 96, 40),
               "glow": [(255, 240, 180), (255, 170, 60), (230, 80, 30)], "iris": (255, 150, 40), "mouth": (110, 30, 30)},
       True: {"skin": (44, 40, 62), "face": (160, 154, 184), "crest": (90, 50, 150), "wing": (150, 90, 220),
              "glow": [(240, 230, 255), (190, 130, 255), (120, 70, 220)], "iris": (180, 120, 255), "mouth": (80, 30, 90)}}


def paint(layout, shiny):
    W, H = layout["texture_width"], layout["texture_height"]
    body = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    b, g = body.load(), glow.load()
    P = PAL[shiny]
    for cube in layout["cubes"]:
        bone = cube["bone"]
        for face, (u, v, w, h) in faces(cube["uv"], cube["size"]).items():
            for y in range(h):
                for x in range(w):
                    X, Y = u + x, v + y
                    if not (0 <= X < W and 0 <= Y < H):
                        continue
                    s, t = (x + 0.5) / w, (y + 0.5) / h
                    lit = LIGHT[face] * (1.05 - 0.12 * t if face not in ("up", "down") else 1)
                    if bone == "head" and face == "north":
                        c = eye(P, x, y, w, h, g, X, Y) or shade(P["face"], lit)
                    elif bone.startswith("mouth"):
                        c = P["mouth"]
                    elif bone.startswith("bone"):                      # the crest, smouldering
                        c = shade(P["crest"], lit * (0.85 + 0.3 * ((x * 7 + y * 3) % 5) / 5))
                        if (x * 5 + y * 3) % 7 == 0:
                            g[X, Y] = P["glow"][1] + (255,)
                    elif bone.startswith("wing"):                      # ember wings, veined
                        c = shade(P["wing"], 0.85 + 0.3 * (1 - t))
                        if abs(math.sin(s * 9 + t * 2)) < 0.25:
                            g[X, Y] = P["glow"][2] + (255,)
                            c = shade(P["wing"], 1.2)
                    elif bone.startswith("anthena"):
                        c = shade(P["skin"], lit)
                        if bone.endswith("_3"):                       # burning tips
                            c = P["glow"][2]
                            g[X, Y] = P["glow"][0 if (x + y) % 2 else 1] + (255,)
                    else:
                        c = shade(P["skin"], lit)
                    b[X, Y] = c + (255,)
    return body, glow


def eye(P, x, y, w, h, g, X, Y):
    """Big eyes on the face (the head's front): dark rims, glowing ember irises, a pale glint."""
    for cx in (1.5, w - 2.5):
        dx, dy = x - cx, y - 3.2
        if abs(dx) <= 1.3 and abs(dy) <= 1.9:
            if (abs(dx) > 0.9 and abs(dy) > 0.6) or abs(dy) > 1.5:
                return (40, 22, 24)
            if dx < -0.4 and dy < -0.9:
                return (255, 250, 240)
            g[X, Y] = P["iris"] + (255,)
            return P["iris"]
    return None


def build(kit):
    raise KeyError("celebi is painted on its addon layout")
