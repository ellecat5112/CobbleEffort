"""Borrow heads from other Pokémon's models for our own models (the imitator crabs' head-claws).

  python3 tools/newmons/borrow_heads.py --cobblemon <cobblemon>/common/src/main/resources --msd <mega showdown jar>

For each SOURCE: the head bone's subtree (minus glow, eyelid, closed-eye, open-mouth and locator bones), its ancestors
as empty bones (so their rotations, i.e. the pose, are kept), and every copied cube's box-UV footprint packed into a
small texture, plain, shiny and emissive. Written to tools/newmons/borrowed/<name>.json + .png files, committed, so the
build doesn't need the sources. build.py's write_model_assets mounts them (a model module's BORROW list).

Licences: Tyrunt and Aggron are Cobblemon's models (CC BY-NC); Groudon and Kyogre are Mega Showdown's (CC BY-NC-SA
4.0): models that borrow them are shared under the same terms (see CREDITS.md).
"""
from __future__ import annotations

import argparse
import io
import json
import math
import re
import zipfile
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE / "borrowed"

SKIP = re.compile(r"glow|eyelid|closed|mouth_open|locator")
SOURCES = {
    "tyrunt": {"from": "cobblemon", "folder": "0696_tyrunt", "geo": "tyrunt.geo.json", "tex": "tyrunt",
               "head": "head", "stop": "torso", "credit": "Cobblemon (Tyrunt's head)"},
    "aggron": {"from": "cobblemon", "folder": "0306_aggron", "geo": "aggron.geo.json", "tex": "aggron",
               "head": "head", "stop": "torso2", "credit": "Cobblemon (Aggron's head)"},
    "groudon": {"from": "msd", "folder": "0383_groudon", "geo": "groudon.geo.json", "tex": "groudon",
                "head": "head", "stop": "tophalf", "credit": "Mega Showdown (Groudon's head)"},
    # Kyogre's "head" bone is only the front of its body, so its whole body comes along (minus the tail and fins)
    "kyogre": {"from": "msd", "folder": "0382_kyogre", "geo": "kyogre.geo.json", "tex": "kyogre",
               "emissive": "kyogre_emissive", "head": "torso", "stop": "body", "skip": r"tail|fin",
               "credit": "Mega Showdown (Kyogre's head and body)"},
}


def footprint(cube):
    w, h, d = (math.ceil(v - 1e-6) for v in cube["size"])
    return 2 * (d + w), d + h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cobblemon", type=Path, required=True)
    ap.add_argument("--msd", type=Path, required=True)
    a = ap.parse_args()
    msd = zipfile.ZipFile(a.msd)

    def read(src, rel):
        if src["from"] == "cobblemon":
            p = a.cobblemon / "assets" / "cobblemon" / rel
            return p.read_bytes() if p.exists() else None
        try:
            return msd.read(f"assets/cobblemon/{rel}")
        except KeyError:
            return None

    OUT.mkdir(parents=True, exist_ok=True)
    for name, src in SOURCES.items():
        geo = json.loads(read(src, f"bedrock/pokemon/models/{src['folder']}/{src['geo']}"))["minecraft:geometry"][0]
        bones = {b["name"]: b for b in geo["bones"]}
        kids = {}
        for b in geo["bones"]:
            kids.setdefault(b.get("parent"), []).append(b["name"])
        # ancestors of the head up to (not including) `stop`, as empty bones keeping their pivots and rotations
        chain, n = [], bones[src["head"]].get("parent")
        while n and n != src["stop"]:
            chain.append(n)
            n = bones[n].get("parent")
        chain.reverse()
        keep = []
        for c in chain:
            keep.append({"name": c, "parent": bones[c].get("parent") if c != chain[0] else None,
                         "pivot": bones[c]["pivot"], "rotation": bones[c].get("rotation"), "cubes": []})

        extra = re.compile(src["skip"]) if src.get("skip") else None

        def walk(bn, parent):
            if SKIP.search(bn) or (extra and extra.search(bn)):
                return
            b = bones[bn]
            keep.append({"name": bn, "parent": parent, "pivot": b["pivot"], "rotation": b.get("rotation"),
                         "cubes": [dict(c) for c in b.get("cubes", [])]})
            for ch in kids.get(bn, []):
                walk(ch, bn)
        walk(src["head"], chain[-1] if chain else None)
        anchor = bones[src["head"]]["pivot"]                 # the head bone's own pivot (its ancestors keep the pose)

        # pack every cube's box-UV footprint into a small texture (shelves 256 wide), for each texture variant
        tw = geo["description"]["texture_width"]
        texs = {"": read(src, f"textures/pokemon/{src['folder']}/{src['tex']}.png"),
                "_shiny": read(src, f"textures/pokemon/{src['folder']}/{src['tex']}_shiny.png")}
        if src.get("emissive"):
            texs["_emissive"] = read(src, f"textures/pokemon/{src['folder']}/{src['emissive']}.png")
            texs["_emissive_shiny"] = read(src, f"textures/pokemon/{src['folder']}/{src['emissive']}_shiny.png")
        imgs = {k: Image.open(io.BytesIO(v)).convert("RGBA") for k, v in texs.items() if v}
        dens = imgs[""].size[0] / tw
        cubes = [c for b in keep for c in b["cubes"]]
        order = sorted(range(len(cubes)), key=lambda i: -footprint(cubes[i])[1])
        W, x, y, shelf, pos = 256, 0, 0, 0, {}
        for i in order:
            fw, fh = footprint(cubes[i])
            if x + fw > W:
                x, y, shelf = 0, y + shelf, 0
            pos[i] = (x, y)
            x += fw
            shelf = max(shelf, fh)
        H = y + shelf
        for key, img in imgs.items():
            out = Image.new("RGBA", (W, H))
            for i, c in enumerate(cubes):
                u, v = c["uv"]
                fw, fh = footprint(c)
                crop = img.crop((round(u * dens), round(v * dens), round((u + fw) * dens), round((v + fh) * dens)))
                out.paste(crop.resize((fw, fh), Image.NEAREST), pos[i])
            out.save(OUT / f"{name}{key}.png", optimize=True)
        for i, c in enumerate(cubes):
            c["uv"] = list(pos[i])
        (OUT / f"{name}.json").write_text(json.dumps({
            "source": f"{src['from']}:{src['folder']}/{src['geo']}", "credit": src["credit"], "anchor": anchor,
            "texture": [W, H], "variants": sorted(imgs), "bones": keep}, indent=1) + "\n")
        print(f"{name}: {len(keep)} bones, {len(cubes)} cubes, footprints {W}x{H}, variants {sorted(imgs)}")


if __name__ == "__main__":
    main()
