#!/usr/bin/env python3
"""
Extract the UV layout (no art) of another mod's Bedrock model, for addon-line builders.

    python3 -I tools/addons/extract_layout.py <model.geo.json> <out.json>

Writes the texture size and, for every box-UV cube, its bone, its bone's ancestry, uv, size, origin and rotation. That's all a
builder needs to paint an original texture onto the model's UV map; none of the other mod's texture pixels are read.
"""
import json
import sys
from pathlib import Path


def main(src, dst):
    g = json.loads(Path(src).read_text())["minecraft:geometry"][0]
    parent = {b["name"]: b.get("parent") for b in g["bones"]}

    def chain(name):
        out = []
        while name:
            out.append(name)
            name = parent.get(name)
        return out

    cubes = []
    for b in g["bones"]:
        for c in b.get("cubes", []):
            if isinstance(c.get("uv"), list):
                cubes.append({"bone": b["name"], "ancestry": chain(b["name"]), "uv": c["uv"],
                              "size": [abs(int(round(v))) for v in c["size"]], "origin": c["origin"],
                              "rotation": c.get("rotation")})
    d = g["description"]
    Path(dst).write_text(json.dumps({"source": Path(src).name, "texture_width": d["texture_width"],
                                     "texture_height": d["texture_height"], "cubes": cubes}, indent=1) + "\n")
    print(f"{len(cubes)} cubes -> {dst}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
