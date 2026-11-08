#!/usr/bin/env python3
"""
Builds the CobbleEffort creatures: new models / forms for Pokémon that Cobblemon doesn't model (or new forms of
ones it does). Writes, for each creature module in this folder:

  assets/cobbleeffort/bedrock/pokemon/models/<folder>/<name>.geo.json
  assets/cobbleeffort/textures/pokemon/<folder>/<name>[_shiny][_emissive].png
  assets/cobbleeffort/bedrock/pokemon/posers/<folder>/<name>.json
  assets/cobbleeffort/bedrock/pokemon/animations/<folder>/<group>.animation.json
  assets/cobbleeffort/bedrock/pokemon/resolvers/creatures/<folder>/<order>_<name>.json

and the gameplay data (species/forms, features, interactions, fossil recipe, spawns, lang) from data.py.

Usage: python3 tools/creatures/build.py --cobblemon <cobblemon>/common/src/main/resources [creature ...]
(the Cobblemon checkout is needed for the creatures built on Cobblemon's own models: Armored Mewtwo, Shadow Lugia).
"""
from __future__ import annotations

import argparse
import importlib
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parent.parent
RES = ROOT / "src" / "main" / "resources"
A = RES / "assets" / "cobbleeffort"
NS = "cobbleeffort"

NEW_MODELS = ["ironboulder", "celesteela", "origindragon"]
FORMS = ["armored_mewtwo", "shadow_lugia"]


def recolour(img: Image.Image, fn) -> Image.Image:
    img = img.convert("RGBA")
    out = img.copy()
    px = out.load()
    memo = {}
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a:
                if (r, g, b) not in memo:
                    memo[(r, g, b)] = tuple(int(v) for v in fn((r, g, b)))
                px[x, y] = memo[(r, g, b)] + (a,)
    return out


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n")


def build_new_model(mod) -> dict:
    """A brand-new model (no Cobblemon model exists): base + shiny + glow, poser, animations, base resolver."""
    from modelkit import write_animations, write_poser
    name, folder, group = mod.SPECIES, mod.DEX_FOLDER, mod.GROUP
    model = mod.build()
    tex_dir = A / "textures" / "pokemon" / folder
    geo, img, glow = model.export(A / "bedrock" / "pokemon" / "models" / folder / f"{name}.geo.json",
                                  tex_dir / f"{name}.png", tex_dir / f"{name}_emissive.png")
    recolour(img, mod.shiny_recolour).save(tex_dir / f"{name}_shiny.png", optimize=True)
    if glow is not None:
        recolour(glow, mod.shiny_recolour).save(tex_dir / f"{name}_emissive_shiny.png", optimize=True)
    write_animations(A / "bedrock" / "pokemon" / "animations" / folder / f"{group}.animation.json", group, mod.animations())
    head_y = next(b.pivot[1] for b in model.bones.values() if b.name == "head")
    write_poser(A / "bedrock" / "pokemon" / "posers" / folder / f"{name}.json", root=name, group=group,
                head="head", height_px=model.height(), head_y=head_y, walk=getattr(mod, "WALK", None),
                flies=getattr(mod, "FLIES", False))

    def tex(n):
        return f"{NS}:textures/pokemon/{folder}/{n}.png"
    glow_layer = lambda shiny: [{"name": "emissive", "texture": tex(f"{name}_emissive{'_shiny' if shiny else ''}"),
                                 "emissive": True, "translucent": False}] if glow is not None else []
    write_json(A / "bedrock" / "pokemon" / "resolvers" / "creatures" / folder / f"0_{name}_base.json", {
        "species": f"cobblemon:{name}",
        "order": 0,
        "variations": [
            {"aspects": [], "poser": f"{NS}:{name}", "model": f"{NS}:{name}.geo", "texture": tex(name),
             "layers": glow_layer(False)},
            {"aspects": ["shiny"], "texture": tex(f"{name}_shiny"), "layers": glow_layer(True)},
        ],
    })
    return {"species": name, "folder": folder, "model": f"{NS}:{name}.geo", "original": None,
            "retextured": tex(name), "layers": [{"original": None, "retextured": tex(f"{name}_emissive"), "emissive": True}]
            if glow is not None else []}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cobblemon", required=True, type=Path)
    ap.add_argument("only", nargs="*")
    args = ap.parse_args()
    manifest = []
    for name in NEW_MODELS + FORMS:
        if args.only and name not in args.only:
            continue
        mod = importlib.import_module(name)
        print(f"building {name}")
        if name in NEW_MODELS:
            manifest.append(build_new_model(mod))
        else:
            manifest.extend(mod.build_form(args.cobblemon, A, NS))
    if not args.only:
        import data
        data.build(args.cobblemon, RES)
    out = ROOT / "tools" / "preview" / "manifest_creatures.json"
    old = json.loads(out.read_text()) if out.exists() and args.only else []
    keep = [e for e in old if e["species"] not in {m["species"] for m in manifest}]
    write_json(out, keep + manifest)


if __name__ == "__main__":
    main()
