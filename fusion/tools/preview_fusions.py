"""Preview fusions in 3D as the Fusion add-on draws them: dex sprite | plain head-on-body | with the design's colours.

usage: preview_fusions.py <cobblemon resources> <dex dir> <out.png> <head>/<body> [<head>/<body> ...]
  Pokémon by Infinite Dex name, e.g. Bulbasaur/Charmander (head first). Needs tools/preview served on 127.0.0.1:8765
  (python3 -m http.server 8765 --bind 127.0.0.1, in tools/preview). The sprite is fetched only to show beside it.
"""
import io
import json
import os
import subprocess
import sys
import tempfile
import urllib.request

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fusion_palette as fp  # noqa: E402
import fusion_species  # noqa: E402

PREVIEW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools", "preview")


def model_file(res, species_folder, form):
    for v in fusion_species.resolver_variations(res, species_folder)[::-1]:
        aspects = set(v.get("aspects", []))
        if v.get("model") and aspects <= ({form} if form else set()) | {"male"}:
            name = v["model"].split(":")[1] + ".json"
            for root, _, files in os.walk(os.path.join(res, "assets/cobblemon/bedrock/pokemon/models")):
                if name in files:
                    return os.path.join(root, name)
    return None


def main():
    res, dex, out = sys.argv[1:4]
    pairs = [p.split("/") for p in sys.argv[4:]]
    dropdown = json.load(open(os.path.join(dex, "dropdown.json")))
    by_name = {p["real_name"].lower(): p["pokemon_id"] for p in dropdown["pokemon"]}
    mapping = fusion_species.mapping(res, dropdown)
    folders = {}
    for d in os.listdir(os.path.join(res, "assets/cobblemon/bedrock/pokemon/resolvers")):
        folders[int(d.split("_")[0])] = d
    nat = {p["pokemon_id"]: p["nat_id"] for p in dropdown["pokemon"]}
    tmp = tempfile.mkdtemp()
    jobs, rows = [], []
    for hn, bn in pairs:
        h, b = by_name[hn.lower()], by_name[bn.lower()]
        rid = f"{h}.{b}"
        rows_h = json.load(open(os.path.join(dex, "heads", f"{h}.json")))
        row = next((r for r in rows_h if r["id"] == rid), None)
        if row is None:
            print("no custom sprite for", hn, bn)
            continue
        spr = Image.open(io.BytesIO(urllib.request.urlopen(
            f"https://ifd-spaces.sfo2.cdn.digitaloceanspaces.com/custom/{rid}{row['ext']}.png", timeout=30).read())).convert("RGBA")
        hm, bm = mapping[h], mapping[b]
        htex, btex = Image.open(hm["texture"]).convert("RGBA"), Image.open(bm["texture"]).convert("RGBA")
        hp, bp, sp = fp.palette(htex), fp.palette(btex), fp.sprite_palette(fp.sprite_hist(spr))
        ht, bt = fp.assign(hp, bp, sp)
        hfile, bfile = os.path.join(tmp, rid + "_h.png"), os.path.join(tmp, rid + "_b.png")
        fp.recolour(htex, hp[0], ht).save(hfile)
        fp.recolour(btex, bp[0], bt).save(bfile)
        hg = model_file(res, folders[nat[h]], hm["form"])
        bg = model_file(res, folders[nat[b]], bm["form"])
        plain, designed = os.path.join(tmp, rid + "_plain.png"), os.path.join(tmp, rid + "_design.png")
        jobs.append({"body_geo": bg, "body_tex": bm["texture"], "head_geo": hg, "head_tex": hm["texture"], "out": plain})
        jobs.append({"body_geo": bg, "body_tex": bfile, "head_geo": hg, "head_tex": hfile, "out": designed})
        rows.append((f"{row['name']} ({hn}/{bn}) by {' & '.join(row['artists'])}", spr, plain, designed))
    jf = os.path.join(tmp, "jobs.json")
    json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(PREVIEW, "render_fusion.js"), jf], check=True, cwd=PREVIEW)
    cell = 256
    sheet = Image.new("RGBA", (cell * 3 + 24, len(rows) * (cell + 22) + 6), (30, 30, 34, 255))
    draw = ImageDraw.Draw(sheet)
    for i, (label, spr, plain, designed) in enumerate(rows):
        y = 6 + i * (cell + 22)
        draw.text((8, y), label, fill=(230, 230, 230, 255))
        for k, im in enumerate((spr.resize((cell, cell), Image.NEAREST), Image.open(plain), Image.open(designed))):
            sheet.alpha_composite(im.convert("RGBA").resize((cell, cell)), (6 + k * (cell + 6), y + 16))
    sheet.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
