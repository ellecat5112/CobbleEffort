"""Assets and data for CobbleEffort: Digital: the Digiball's textures (recoloured from Cobblemon's Poké Ball, CC BY-NC),
its thrown-ball resolver, item models, the Digitama sprite (drawn here), lang and recipes; make_tamer.py adds the
tamer items, blocks and Digiball tiers.

    python3 digital/tools/make_assets.py <Cobblemon jar>
"""
from __future__ import annotations

import colorsys
import io
import json
import sys
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1] / "common" / "src" / "main" / "resources"
NS = "cobbleeffort_digital"
A = ROOT / "assets" / NS
D = ROOT / "data" / NS

ORANGE, ORANGE_DARK = (244, 128, 32), (196, 84, 20)
CIRCUIT = (28, 64, 150)
BAND = (24, 28, 48)
BUTTON = (90, 230, 255)


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def digiball(im: Image.Image) -> Image.Image:
    """Poké Ball -> Digiball: the red top turns orange traced with blue circuit dots, the band navy, the white button
    cyan; the white bottom stays."""
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            hh, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if s > 0.45 and (hh < 0.06 or hh > 0.92):                     # the red top
                base = ORANGE if v > 0.7 else ORANGE_DARK
                c = CIRCUIT if (x * 3 + y * 5) % 11 == 0 else tuple(int(k * (0.75 + 0.25 * v)) for k in base)
                px[x, y] = (*c, a)
            elif v < 0.25:                                                 # the black band
                px[x, y] = (*BAND, a)
    return im


def button(im: Image.Image, ref: Image.Image) -> Image.Image:
    """Turn the white button cyan: white pixels of the 2D sprite with the band (dark) beside them on the same row."""
    px, rp = im.load(), ref.convert("RGBA").load()
    w, h = im.size
    for y in range(h):
        for x in range(1, w - 1):
            r, g, b, a = rp[x, y]
            if a and min(r, g, b) > 200 and any(max(rp[x + d, y][:3]) < 60 for d in (-1, 1)):
                px[x, y] = (*BUTTON, a)
    return im


def digitama() -> Image.Image:
    """A 16 x 16 Digi-Egg: cream, with an orange zigzag band and blue spots (an original egg pattern)."""
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = im.load()
    for y in range(16):
        for x in range(16):
            u, v = (x - 7.5) / 5.6, (y - 8.6) / 7.0
            v *= 1.0 + 0.18 * (v < 0)                                         # narrower at the top
            d = u * u + v * v
            if d > 1:
                continue
            c = (246, 238, 214)
            zig = 9.0 + (1.2 if x % 4 < 2 else -0.2)
            if abs(y - zig) < 1.0:
                c = (240, 120, 40)
            elif (x, y) in ((5, 4), (9, 3), (10, 6), (4, 13), (9, 13), (11, 11)):
                c = (60, 120, 210)
            shade = 0.82 + 0.18 * (1 - (u + 0.3) ** 2) if d < 0.75 else 0.72
            c = tuple(min(255, int(k * shade)) for k in c)
            if d > 0.82:
                c = tuple(int(k * 0.55) for k in c)                           # outline
            px[x, y] = (*c, 255)
    return im


def main():
    jar = zipfile.ZipFile(sys.argv[1])

    def img(path):
        return Image.open(io.BytesIO(jar.read("assets/cobblemon/" + path)))

    sprite = img("textures/item/poke_balls/poke_ball.png")
    out = {
        "textures/item/poke_balls/digiball.png": button(digiball(sprite), sprite),
        "textures/item/poke_balls/models/digiball.png": digiball(img("textures/item/poke_balls/models/poke_ball.png")),
        "textures/poke_balls/digiball.png": digiball(img("textures/poke_balls/poke_ball.png")),
        "textures/gui/ball/digiball.png": digiball(img("textures/gui/ball/poke_ball.png")),
        "textures/item/digitama.png": digitama(),
    }
    for rel, im in out.items():
        p = A / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        im.save(p)

    write_json(A / "models/item/digiball.json",
               {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/poke_balls/digiball"}})
    write_json(A / "models/item/digiball_model.json",
               {"parent": "cobblemon:item/poke_ball_model", "textures": {"layer0": f"{NS}:item/poke_balls/models/digiball"}})
    write_json(A / "models/item/digitama.json",
               {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/digitama"}})
    write_json(A / "bedrock/poke_balls/variations/0_digiball_base.json",
               {"order": 0, "pokeball": f"{NS}:digiball", "variations": [
                   {"aspects": [], "layers": [], "model": "cobblemon:poke_ball.geo", "poser": "cobblemon:poke_ball",
                    "texture": f"{NS}:textures/poke_balls/digiball.png"}]})
    lang_file = A / "lang/en_us.json"
    lang = json.loads(lang_file.read_text()) if lang_file.exists() else {}   # newmons build.py adds the Digimon here
    lang.update({
        f"itemGroup.{NS}": "CobbleEffort: Digital",
        f"item.{NS}.digiball": "Digiball",
        f"item.{NS}.digiball.tooltip": "Three times as good as a Poké Ball on Digimon.",
        f"item.{NS}.digitama": "Digitama",
        f"{NS}.digitama.warming": "Warming up: %s%%. Keep it in your inventory.",
        f"{NS}.digitama.ready": "It's moving! Use it to hatch.",
        f"{NS}.digitama.not_ready": "The Digitama is still warming up (%s%%).",
        f"{NS}.digitama.hatched": "The Digitama hatched into %s!",
        f"{NS}.digitama.dropped": "The %s left a Digitama behind!",
    })
    import make_tamer                                                      # 0.13.0: tamer basics
    lang.update(make_tamer.build(jar))
    import make_world                                                      # 0.14.0: the Digital World
    lang.update(make_world.build())
    write_json(lang_file, dict(sorted(lang.items())))
    write_json(D / "recipe/digiball.json", {
        "type": "minecraft:crafting_shapeless", "category": "misc",
        "ingredients": [{"item": "cobblemon:poke_ball"}, {"item": "minecraft:redstone"},
                        {"item": "minecraft:lapis_lazuli"}, {"item": "minecraft:copper_ingot"}],
        "result": {"id": f"{NS}:digiball", "count": 1}})
    write_json(D / "recipe/digiball_x4.json", {
        "type": "minecraft:crafting_shaped", "category": "misc",
        "pattern": ["RCR", "LBL", "RCR"],
        "key": {"R": {"item": "minecraft:redstone"}, "C": {"item": "minecraft:copper_ingot"},
                "L": {"item": "minecraft:lapis_lazuli"}, "B": {"item": "cobblemon:great_ball"}},
        "result": {"id": f"{NS}:digiball", "count": 4}})
    # Cobblemon's own tags, so it counts as a Poké Ball wherever Cobblemon checks (e.g. dispensers, the PC)
    write_json(ROOT / "data/cobblemon/tags/item/poke_balls.json", {"replace": False, "values": [f"{NS}:digiball"]})
    print("wrote", len(out), "textures")


if __name__ == "__main__":
    main()
