"""
Shadow Lugia (from Pokémon XD): Cobblemon's own Lugia model, retextured.

Design (after the reference): the white body turns a deep indigo-navy, the blue dorsal plates, eye mask and
tail fins go near-black purple, the belly (front of the torso) becomes pale lavender-grey, and the eyes burn
red. Two extra layers: the eyes glow red in the dark, and a faint purple glow over the whole body stands in
for the Shadow aura. Shiny Shadow Lugia keeps the same idea in crimson.
"""
from __future__ import annotations

import colorsys
import json
from pathlib import Path

from PIL import Image

NAVY = [(0.0, (14, 12, 34)), (0.5, (38, 36, 86)), (1.0, (86, 84, 150))]
CRIMSON = [(0.0, (30, 6, 18)), (0.5, (78, 22, 52)), (1.0, (140, 64, 104))]
ACCENT = (34, 18, 56)
ACCENT_SHINY = (64, 8, 30)
BELLY = [(0.0, (96, 98, 122)), (1.0, (178, 180, 204))]
EYE_RED = (255, 40, 40)
AURA = (140, 70, 230)


def ramp(stops, v):
    v = max(0.0, min(1.0, v))
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        if v <= p1:
            t = (v - p0) / (p1 - p0)
            return tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3))
    return stops[-1][1]


def belly_rects(geo):
    """Texture rectangles of the front faces of Lugia's torso cubes (its belly)."""
    rects = []
    for b in geo["minecraft:geometry"][0]["bones"]:
        if b["name"] in ("torso", "torso2"):
            for c in b.get("cubes", []):
                u, v = c["uv"]
                w, h, d = (abs(int(round(s))) for s in c["size"])
                rects.append((u + d, v + d, w, h))
    return rects


def shadowify(img, rects, shiny):
    img = img.convert("RGBA")
    out = img.copy()
    px = out.load()
    in_belly = lambda x, y: any(rx <= x < rx + rw and ry <= y < ry + rh for rx, ry, rw, rh in rects)
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if not a:
                continue
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            if r > 100 and r > g * 1.6 and r > b * 1.4 and l < 0.55:          # red eyes
                c = EYE_RED
            elif in_belly(x, y):                                             # belly first: it's blue in the original
                c = ramp(BELLY, l * 1.3 - 0.2)
            elif s > 0.35 and l < 0.72:                                     # blue (or shiny red) accents
                c = tuple(int(v * (0.6 + l)) for v in (ACCENT_SHINY if shiny else ACCENT))
            else:
                c = ramp(CRIMSON if shiny else NAVY, (l - 0.45) * 1.8)
            px[x, y] = tuple(int(v) for v in c) + (a,)
    return out


def build_form(cob_root: Path, A: Path, NS: str):
    folder = "0249_lugia"
    src = cob_root / "assets" / "cobblemon"
    geo = json.loads((src / "bedrock" / "pokemon" / "models" / folder / "lugia.geo.json").read_text())
    rects = belly_rects(geo)
    tex_dir = A / "textures" / "pokemon" / folder
    tex_dir.mkdir(parents=True, exist_ok=True)
    for suffix, shiny in (("", False), ("_shiny", True)):
        base = Image.open(src / "textures" / "pokemon" / folder / f"lugia{suffix}.png")
        shadowify(base, rects, shiny).save(tex_dir / f"lugia_shadow{suffix}.png", optimize=True)
        # aura: a faint purple copy of the whole body, drawn glowing and translucent on top
        a_src = base.convert("RGBA")
        aura = Image.new("RGBA", a_src.size, (0, 0, 0, 0))
        sp, ap = a_src.load(), aura.load()
        tint = (230, 60, 110) if shiny else AURA
        for y in range(a_src.height):
            for x in range(a_src.width):
                if sp[x, y][3]:
                    ap[x, y] = tint + (46,)
        aura.save(tex_dir / f"lugia_shadow_aura{suffix}.png", optimize=True)
    # glowing red eyes: Cobblemon's alpha-eyes mask, recoloured
    mask = Image.open(src / "textures" / "pokemon" / folder / "lugia_alpha.png").convert("RGBA")
    eyes = Image.new("RGBA", mask.size, (0, 0, 0, 0))
    mp, ep = mask.load(), eyes.load()
    for y in range(mask.height):
        for x in range(mask.width):
            if mp[x, y][3]:
                ep[x, y] = EYE_RED + (255,)
    eyes.save(tex_dir / "lugia_shadow_eyes.png", optimize=True)

    tex = lambda n: f"{NS}:textures/pokemon/{folder}/{n}.png"
    layers = lambda sfx: [
        {"name": "cobbleeffort_shadow_aura", "texture": tex(f"lugia_shadow_aura{sfx}"), "emissive": True, "translucent": True},
        {"name": "cobbleeffort_shadow_eyes", "texture": tex("lugia_shadow_eyes"), "emissive": True, "translucent": True},
    ]
    resolver = {
        "species": "cobblemon:lugia",
        "order": 9000,
        "variations": [
            {"aspects": ["shadow"], "texture": tex("lugia_shadow"), "layers": layers("")},
            {"aspects": ["shadow", "shiny"], "texture": tex("lugia_shadow_shiny"), "layers": layers("_shiny")},
        ],
    }
    out_res = A / "bedrock" / "pokemon" / "resolvers" / "creatures" / folder / "9000_lugia_shadow.json"
    out_res.parent.mkdir(parents=True, exist_ok=True)
    out_res.write_text(json.dumps(resolver, indent=2) + "\n")
    return [{"species": "lugia_shadow", "folder": folder, "model": "cobblemon:lugia.geo",
             "original": "cobblemon:textures/pokemon/0249_lugia/lugia.png", "retextured": tex("lugia_shadow"),
             "layers": [{"original": None, "retextured": tex("lugia_shadow_eyes"), "emissive": True}]}]
