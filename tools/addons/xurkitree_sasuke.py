"""
Addon line: Xurkitree as Sasuke Uchiha (Naruto collection).

Cobblemon 1.8.4 has no Xurkitree model. Cobblemon: AllTheMons x Mega Showdown ships one (cobblemon:xurkitree.geo),
and so does Cobblemon Ultra-Beasts; ATM's is Ultra-Beasts' model plus small glow bulbs, on the same UV map. This
builder paints an ORIGINAL texture onto the union of both UV layouts (tools/addons/atm_xurkitree_layout.json and
ultrabeasts_xurkitree_layout.json, extracted with extract_layout.py; no pixels of either mod's textures are used), so
it fits whichever of the two is installed. The resolver only swaps the texture and layers.

Design:
* head ball: the face on the front plate, pale, with glowing Sharingan eyes (red, black pupil, tomoe);
  the star spikes and other plates are Sasuke's spiky blue-black hair; the Uchiha crest (red fan over white)
  on the back
* the wire arms and tail are navy sleeves with grey wraps
* legs are navy trousers with white shin wraps, a twisted purple rope belt on top and dark shinobi sandals
* the claws and the tail plug crackle with Chidori: blue-white lightning that glows and flickers (4 frames)
* shiny: Rinnegan / Susanoo purple, with purple-black lightning
"""
from __future__ import annotations

import json
import random
from pathlib import Path

from PIL import Image

LAYOUTS = [Path(__file__).resolve().parent / n for n in ("atm_xurkitree_layout.json", "ultrabeasts_xurkitree_layout.json")]
SPECIES = "xurkitree"
FOLDER = "addon_xurkitree"

PALETTES = {
    False: {"hair": (24, 26, 44), "hair_hi": (52, 64, 110), "skin": (240, 214, 190), "skin_sh": (206, 176, 152),
            "navy": (30, 34, 62), "navy_hi": (52, 58, 96), "wrap": (226, 222, 214), "rope": [(120, 70, 170), (90, 46, 130)],
            "sandal": (36, 36, 44), "bolt": [(240, 250, 255), (150, 210, 255), (90, 160, 250)], "eye": (220, 20, 30)},
    True: {"hair": (34, 18, 50), "hair_hi": (96, 52, 140), "skin": (232, 214, 236), "skin_sh": (196, 170, 206),
           "navy": (54, 28, 80), "navy_hi": (92, 54, 130), "wrap": (220, 210, 232), "rope": [(170, 90, 210), (120, 60, 170)],
           "sandal": (40, 26, 52), "bolt": [(250, 230, 255), (200, 120, 255), (90, 30, 140)], "eye": (190, 110, 255)},
}


def faces(c):
    u, v = c["uv"]
    w, h, d = c["size"]
    return {"top": (u + d, v, w, d), "bottom": (u + d + w, v, w, d), "right": (u, v + d, d, h),
            "front": (u + d, v + d, w, h), "left": (u + d + w, v + d, d, h), "back": (u + 2 * d + w, v + d, w, h)}


def kind(c):
    a, bone = c["ancestry"], c["bone"]
    if bone.startswith("glow_"):
        return "hand"        # ATM's little glow bulbs crackle with Chidori too
    if "realhead" in a:
        return "head"
    if any(x.endswith("_hand") or "finger" in x or x == "tip_plug" for x in a):
        return "hand"
    if any(x.startswith("arm") or x.startswith("tail") for x in a):
        return "arm"
    if "legs" in a:
        if "foot" in bone or "feet" in bone:
            return "sandal"
        if bone.endswith("sec_1"):
            return "belt"
        if bone.endswith(("sec_5", "sec_6")):
            return "wrap"
        return "leg"
    return "arm"


def load_layout():
    """The union of the layouts: every cube of either model, once."""
    layouts = [json.loads(p.read_text()) for p in LAYOUTS]
    assert len({(l["texture_width"], l["texture_height"]) for l in layouts}) == 1
    cubes, seen = [], set()
    for l in layouts:
        for c in l["cubes"]:
            key = (tuple(c["uv"]), tuple(c["size"]), tuple(c["origin"]))
            if key not in seen:
                seen.add(key)
                cubes.append(c)
    return {"texture_width": layouts[0]["texture_width"], "texture_height": layouts[0]["texture_height"], "cubes": cubes}


def paint(shiny: bool, out_root: Path, aspect: str, mod_id: str):
    lay = load_layout()
    W, H = lay["texture_width"], lay["texture_height"]
    P = PALETTES[shiny]
    rng = random.Random(f"{mod_id}:{aspect}:{SPECIES}:{shiny}")
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = img.load()
    bolt_cells, eye_cells = [], []

    def put(x, y, c, a=255):
        if 0 <= x < W and 0 <= y < H:
            px[x, y] = tuple(int(v) for v in c[:3]) + (a,)

    def jitter(c, amt=0.06):
        f = 1 + rng.uniform(-amt, amt)
        return tuple(max(0, min(255, int(v * f))) for v in c)

    # which ball cube is which: core (14^3), front plate (lowest z, unrotated), back plate (highest z, unrotated)
    balls = {}
    for c in lay["cubes"]:
        if c["bone"].startswith("ball"):
            balls.setdefault(c["bone"], []).append(c)
    front_plates = {id(min((q for q in g if q["size"] == [12, 12, 2] and not q["rotation"]), key=lambda q: q["origin"][2]))
                    for g in balls.values()}
    back_plates = {id(max((q for q in g if q["size"] == [12, 12, 2] and not q["rotation"]), key=lambda q: q["origin"][2]))
                   for g in balls.values()}

    for c in lay["cubes"]:
        k = kind(c)
        glowup = any(x.startswith("head_glowup") for x in c["ancestry"])
        for face, (fx, fy, fw, fh) in faces(c).items():
            if fw <= 0 or fh <= 0:
                continue
            shadefac = {"top": 1.1, "bottom": 0.75, "back": 0.9}.get(face, 1.0)
            for j in range(fh):
                for i in range(fw):
                    x, y = fx + i, fy + j
                    a = 255
                    if k == "head":
                        if 0 in c["size"]:
                            # a star spike of hair: a diamond, the rest transparent
                            dx, dy = abs(i - (fw - 1) / 2) / (fw / 2), abs(j - (fh - 1) / 2) / (fh / 2)
                            if dx + dy > 1.0:
                                continue
                            col = P["hair_hi"] if (i + 2 * j) % 7 == 0 else P["hair"]
                        elif id(c) in front_plates and face == "front":
                            col = P["skin"] if j > 1 else P["hair"]          # a fringe of hair over the face
                            for ex in (3, fw - 4):                           # Sharingan eyes
                                ddx, ddy = i - ex, j - 5
                                if abs(ddx) + abs(ddy) <= 2:
                                    col = P["eye"]
                                    eye_cells.append((x, y))
                                    if (ddx, ddy) == (0, 0) or (abs(ddx), abs(ddy)) in ((2, 0), (0, 2)) and (ddx + ddy) % 3 == 0:
                                        col = (10, 6, 8)                     # pupil and tomoe
                            if j == fh - 3 and fw // 2 - 1 <= i <= fw // 2:
                                col = P["skin_sh"]                           # mouth
                        elif id(c) in back_plates and face == "back":
                            # the Uchiha crest: a red fan over white, with a handle below
                            cx, cy = (fw - 1) / 2, fh * 0.42
                            r = ((i - cx) ** 2 + (j - cy) ** 2) ** 0.5
                            if r <= fw * 0.36:
                                col = (210, 30, 40) if j < cy else (244, 242, 236)
                            elif abs(i - cx) <= 0.6 and cy < j < fh - 1:
                                col = (244, 242, 236)
                            else:
                                col = P["hair"]
                        else:
                            col = P["hair_hi"] if (i * 3 + j) % 9 == 0 else P["hair"]
                        if glowup:
                            col = tuple(min(255, int(v * 1.25 + 12)) for v in col)
                    elif k == "hand":
                        col = P["bolt"][rng.randrange(3)]
                        bolt_cells.append((x, y))
                    elif k == "arm":
                        col = P["wrap"] if (i // 2) % 5 == 0 and face != "bottom" else (P["navy_hi"] if j == 0 else P["navy"])
                    elif k == "belt":
                        col = P["rope"][((i + j) // 2) % 2] if j < 3 else P["navy"]
                    elif k == "wrap":
                        col = P["wrap"] if (i + j) % 3 else (180, 176, 168)
                    elif k == "sandal":
                        col = P["sandal"]
                    else:
                        col = P["navy_hi"] if i == 0 else P["navy"]
                    put(x, y, jitter(tuple(v * shadefac for v in col)), a)
    return img, bolt_cells, eye_cells, (W, H), P, rng


def build(out_tex_root: Path, aspect: str, mod_id: str):
    out_dir = out_tex_root / FOLDER
    out_dir.mkdir(parents=True, exist_ok=True)
    tex = lambda n: f"{mod_id}:textures/pokemon/{aspect}/{FOLDER}/{n}.png"
    variations = []
    for shiny in (False, True):
        sfx = "_shiny" if shiny else ""
        img, bolts, eyes, (W, H), P, rng = paint(shiny, out_tex_root, aspect, mod_id)
        img.save(out_dir / f"xurkitree_sasuke{sfx}.png", optimize=True)
        frames = []
        for f in range(4):    # Chidori: a different scatter of crackling bright pixels every frame, eyes always lit
            frng = random.Random(f"{mod_id}:{aspect}:chidori:{shiny}:{f}")
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            lp = layer.load()
            for x, y in bolts:
                if frng.random() < 0.42:
                    lp[x, y] = P["bolt"][0 if frng.random() < 0.5 else 1] + (255,)
            for x, y in eyes:
                lp[x, y] = P["eye"] + (255,)
            name = f"xurkitree_sasuke{sfx}_chidori_{f}"
            layer.save(out_dir / f"{name}.png", optimize=True)
            frames.append(tex(name))
        variations.append({
            "aspects": [aspect, "shiny"] if shiny else [aspect],
            "texture": tex(f"xurkitree_sasuke{sfx}"),
            "layers": [
                {"name": "glow", "enabled": False},     # Ultra-Beasts' own glow layer belongs to its own texture
                {"name": f"{mod_id}_chidori", "texture": {"frames": frames, "fps": 8, "loop": True},
                 "emissive": True, "translucent": True},
            ],
        })
    entry = {"species": SPECIES, "folder": FOLDER, "model": "cobblemon:xurkitree.geo", "original": None,
             "retextured": tex("xurkitree_sasuke"),
             "layers": [{"original": None, "retextured": variations[0]["layers"][1]["texture"]["frames"][0], "emissive": True}],
             "addon": "Cobblemon: AllTheMons x Mega Showdown / Cobblemon Ultra-Beasts"}
    return variations, entry
