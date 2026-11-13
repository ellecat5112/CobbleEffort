"""Build assets/cobbleeffort_fusion/designs.bin: Infinite Fusion fusion designs (colours, names, credits).

usage: make_designs.py <cobblemon resources> <dex dir> [--preview N]
  <dex dir> holds what the Infinite Dex gave (gitignored, never committed): dropdown.json (its Pokémon list),
  heads/<head id>.json (its custom-art fusions per head: id, names, main sprite, artists) and hist.jsonl (each
  main sprite's colour histogram, fusion_palette.sprite_hist; the sprites themselves aren't kept).

Format (gzip, big-endian; FusionDesigns.java reads it):
  int 'CEFD', int 1
  int nSpecies; per species: UTF key ("species" or "species:form"), UTF head name part, UTF body name part,
                byte K, K x (short L*100, short a*100, short b*100)   (its Cobblemon texture's colour clusters)
  int nArtists; UTF each (a fusion sprite's credit line)
  int nFusions; per fusion: ushort head, ushort body, int artist (-1 none),
                head targets, body targets: byte mask (bit j = cluster j changed), then 3 bytes per set bit (L*2.55, a+128, b+128)
"""
import collections
import gzip
import io
import json
import os
import struct
import sys
from multiprocessing import Pool

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fusion_palette as fp  # noqa: E402
import fusion_species  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "common", "src", "main", "resources", "assets", "cobbleeffort_fusion", "designs.bin")


def name_parts(rows):
    """Each Pokémon's head part and body part of Infinite Fusion's fusion names (name = head part + body part)."""
    by_head, by_body = collections.defaultdict(list), collections.defaultdict(list)
    for r in rows:
        by_head[r["head"]].append(r)
        by_body[r["body"]].append(r)
    pre = {h: os.path.commonprefix([r["name"] for r in rs]) for h, rs in by_head.items()}
    suf = {}
    for _ in range(6):
        for b, rs in by_body.items():
            c = collections.Counter(r["name"][len(pre[r["head"]]):] for r in rs if r["name"].startswith(pre[r["head"]]))
            if c:
                suf[b] = c.most_common(1)[0][0]
        for h, rs in by_head.items():
            c = collections.Counter(r["name"][:len(r["name"]) - len(suf[r["body"]])] for r in rs
                                    if r["body"] in suf and r["name"].endswith(suf[r["body"]]) and len(r["name"]) > len(suf[r["body"]]))
            if c:
                pre[h] = c.most_common(1)[0][0]
    ok = sum(1 for r in rows if pre.get(r["head"], "") + suf.get(r["body"], "") == r["name"])
    print(f"names: {ok} of {len(rows)} custom fusions' names rebuilt from parts", flush=True)
    return pre, suf


SPECIES_PAL = {}


def pack_lab(c):
    """A Lab colour in three bytes: L * 2.55, a + 128, b + 128 (FusionDesigns.targets unpacks it)."""
    L, a, b = (float(v) for v in c)
    return (int(np.clip(round(L * 2.55), 0, 255)), int(np.clip(round(a + 128), 0, 255)), int(np.clip(round(b + 128), 0, 255)))


def _init(pals):
    SPECIES_PAL.update(pals)


def _design(job):
    fid, h, b, hist = job
    sp = fp.sprite_palette(hist)
    ht, bt = fp.assign(SPECIES_PAL[h], SPECIES_PAL[b], sp)
    return fid, ht, bt


def main():
    res, dex = sys.argv[1], sys.argv[2]
    preview = int(sys.argv[sys.argv.index("--preview") + 1]) if "--preview" in sys.argv else 0
    dropdown = json.load(open(os.path.join(dex, "dropdown.json")))
    mapping = fusion_species.mapping(res, dropdown)
    rows = []
    for n in sorted(os.listdir(os.path.join(dex, "heads")), key=lambda s: int(s.split(".")[0])):
        rows += json.load(open(os.path.join(dex, "heads", n)))
    pre, suf = name_parts(rows)
    palettes = {}
    for line in open(os.path.join(dex, "hist.jsonl")):
        d = json.loads(line)
        if not d.get("missing"):
            palettes[d["id"]] = d["c"]

    # species table: one entry per key (an Infinite Fusion Pokémon Cobblemon models)
    ids = sorted(mapping)
    index = {}
    species = []
    for i in ids:
        key = mapping[i]["key"]
        if key in index:
            continue
        index[key] = len(species)
        species.append((key, i, fp.palette(Image.open(mapping[i]["texture"]))))
    by_if = {i: index[mapping[i]["key"]] for i in ids}
    pals = {s: (p[0], p[1]) for s, (_, _, p) in enumerate(species)}

    jobs, meta = [], {}
    for r in rows:
        if r["custom"] and r["head"] in by_if and r["body"] in by_if and r["id"] in palettes:
            h, b = by_if[r["head"]], by_if[r["body"]]
            if (h, b) in meta:
                continue
            meta[(h, b)] = r
            jobs.append(((h, b), h, b, palettes[r["id"]]))
    print(f"designs: {len(jobs)} fusions with a custom sprite and both Pokémon in Cobblemon", flush=True)
    with Pool(os.cpu_count(), initializer=_init, initargs=(pals,)) as pool:
        results = pool.map(_design, jobs, chunksize=256)

    artists, artist_index = [], {}
    buf = io.BytesIO()
    w = buf.write
    w(struct.pack(">ii", 0x43454644, 1))
    w(struct.pack(">i", len(species)))

    def utf(s):
        b = s.encode("utf-8")
        w(struct.pack(">H", len(b)) + b)

    for key, i, (c, _) in species:
        utf(key)
        utf(pre.get(i, ""))
        utf(suf.get(i, ""))
        w(struct.pack(">B", len(c)))
        for col in c:
            w(struct.pack(">hhh", *[int(round(v * 100)) for v in col]))
    lines = []
    for (h, b), _, _ in results:
        credit = " & ".join(meta[(h, b)]["artists"])
        if credit not in artist_index:
            artist_index[credit] = len(artists)
            artists.append(credit)
    w(struct.pack(">i", len(artists)))
    for a in artists:
        utf(a)
    w(struct.pack(">i", len(results)))
    changed = 0
    for (h, b), ht, bt in sorted(results, key=lambda t: t[0]):
        w(struct.pack(">HHi", h, b, artist_index[" & ".join(meta[(h, b)]["artists"])]))
        for src, tgt in ((pals[h][0], ht), (pals[b][0], bt)):
            mask, body = 0, b""
            for j, (s, t) in enumerate(zip(src, tgt)):
                if np.abs(np.asarray(s) - np.asarray(t)).max() > 0.5:
                    mask |= 1 << j
                    body += struct.pack(">BBB", *pack_lab(t))
                    changed += 1
            w(struct.pack(">B", mask) + body)
    raw = buf.getvalue()
    with gzip.GzipFile(OUT, "wb", mtime=0, compresslevel=9) as f:
        f.write(raw)
    print(f"wrote {OUT}: {len(species)} species, {len(artists)} credits, {len(results)} designs, "
          f"{len(raw) / 1e6:.1f} MB raw, {os.path.getsize(OUT) / 1e6:.1f} MB gzip", flush=True)

    # credits: every artist whose sprite gave a design (each fusion's own credit is in the data, shown in game)
    counts = collections.Counter()
    for (h, b), _, _ in results:
        for a in meta[(h, b)]["artists"]:
            counts[a] += 1
    root = os.path.join(HERE, "..")
    with open(os.path.join(root, "CREDITS.txt"), "w") as f:
        f.write("CobbleEffort: Fusion - fusion colour credits\n"
                "==============================================\n\n"
                f"The colours of {len(results)} fusions follow Pokémon Infinite Fusion's custom sprites, by the artists of\n"
                "its community (as credited on the Infinite Dex, infinitefusiondex.com). Only the colours they chose are\n"
                "used; the sprites themselves are not included. In game, /fusion info names the artist of each fusion.\n\n"
                "Artists (fusions coloured after their sprites):\n")
        for a, n in sorted(counts.items(), key=lambda t: t[0].lower()):
            f.write(f"  {a} ({n})\n")
    with open(os.path.join(root, "designs_count.txt"), "w") as f:
        f.write(f"{len(results):,}\n")

    if preview:
        sheet(res, mapping, species, pals, results, meta, preview, os.path.join(dex, "preview.png"))


def sheet(res, mapping, species, pals, results, meta, n, out):
    """Sprite | head texture -> recoloured | body texture -> recoloured, for n evenly spaced designs."""
    import urllib.request
    rows = []
    step = max(1, len(results) // n)
    tex = {s: Image.open(mapping[i]["texture"]).convert("RGBA") for s, (_, i, _) in enumerate(species)}
    for (h, b), ht, bt in sorted(results, key=lambda t: t[0])[::step][:n]:
        r = meta[(h, b)]
        url = f"https://ifd-spaces.sfo2.cdn.digitaloceanspaces.com/custom/{r['id']}{r['ext']}.png"
        try:
            spr = Image.open(io.BytesIO(urllib.request.urlopen(url, timeout=30).read())).convert("RGBA")
        except Exception:
            continue
        cells = [spr.resize((144, 144), Image.NEAREST)]
        for s, t in ((h, ht), (b, bt)):
            im = tex[s]
            sc = 144 / max(im.size)
            for img in (im, fp.recolour(im, pals[s][0], t)):
                cells.append(img.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.NEAREST))
        rows.append(cells)
    W = 6 + sum(c.width + 6 for c in rows[0]) if rows else 10
    img = Image.new("RGBA", (W + 300, len(rows) * 150 + 6), (36, 36, 40, 255))
    for y, cells in enumerate(rows):
        x = 6
        for c in cells:
            img.alpha_composite(c, (x, 6 + y * 150))
            x += c.width + 6
    img.save(out)
    print("preview", out)


if __name__ == "__main__":
    main()
