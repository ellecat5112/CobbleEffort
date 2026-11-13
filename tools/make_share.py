"""Shareable packages: every CobbleEffort mod for one loader, in zips under a size limit (e.g. Discord's).

usage: make_share.py --out <dir> --base <cobbleeffort jar> [--distortion <jar>] [--kanto <jar>] [--fusion <jar>]
                     [--readme Name=<file> ...] [--limit 19.5] [--loader Fabric] [--cache <dir>]

1. Each jar is repacked smaller without changing what the game sees in practice: PNGs re-encoded losslessly by oxipng,
   textures with more than 256 colours reduced to their best 256 (median cut; invisible on Cobblemon's textures),
   JSON minified, maximum deflate. Repacks are cached by the source jar's hash.
2. A jar can't be split across zips, and CobbleEffort's own jar (all collections' textures) is bigger than the limit,
   so it's split into a core jar (code, data, models, resolvers, lang: everything but the collection texture
   folders) and texture-only jars ("CobbleEffort Textures N"), each a tiny mod of its own for both loaders (Fabric:
   no entrypoint; NeoForge: lowcodefml), whole texture folders each. Install all of them: a missing part only means
   that part's cosmetics show Minecraft's missing texture.
3. The jars are packed into as few zips as fit the limit (first fit, biggest first), each with an INSTALL.txt that
   lists every zip and what's in it, plus the READMEs and licences of the mods it carries.
"""
import argparse
import hashlib
import io
import json
import os
import shutil
import sys
import zipfile
from concurrent.futures import ProcessPoolExecutor

MB = 1_000_000
TEX = "assets/cobbleeffort/textures/pokemon/"


# ---- repack ----------------------------------------------------------------------------------------------------------

def _palettize(data):
    from PIL import Image
    im = Image.open(io.BytesIO(data)).convert("RGBA")
    if im.getcolors(256) is not None:
        return data
    q = im.quantize(256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).convert("RGBA")
    buf = io.BytesIO()
    q.save(buf, "PNG")
    return buf.getvalue()


def _shrink(item):
    import oxipng
    name, data = item
    try:
        if name.endswith(".png"):
            out = oxipng.optimize_from_memory(_palettize(data), level=4, strip=oxipng.StripChunks.safe())
            return name, out if len(out) < len(data) else data
        if name.endswith(".json") or name.endswith(".mcmeta"):
            out = json.dumps(json.loads(data), separators=(",", ":"), ensure_ascii=False).encode()
            return name, out if len(out) < len(data) else data
    except Exception:
        pass
    return name, data


def repack(src, cache):
    h = hashlib.sha1(open(src, "rb").read()).hexdigest()[:16]
    dst = os.path.join(cache, f"{os.path.basename(src)[:-4]}-{h}.jar")
    if os.path.exists(dst):
        return dst
    zin = zipfile.ZipFile(src)
    items = [(i.filename, zin.read(i.filename)) for i in zin.infolist()]
    with ProcessPoolExecutor() as ex:
        done = dict(ex.map(_shrink, items, chunksize=64))
    write_jar(dst + ".tmp", [(i.filename, done[i.filename], i.date_time) for i in zin.infolist()])
    os.replace(dst + ".tmp", dst)
    return dst


def write_jar(path, entries):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data, dt in entries:
            zi = zipfile.ZipInfo(name, date_time=dt)
            zi.compress_type = zipfile.ZIP_STORED if name.endswith("/") else zipfile.ZIP_DEFLATED
            z.writestr(zi, data, compresslevel=9)


# ---- split CobbleEffort ----------------------------------------------------------------------------------------------

def part_meta(n, total, version):
    mod_id = f"cobbleeffort_textures_{n}"
    name = f"CobbleEffort Textures {n} of {total}"
    desc = f"Part {n} of {total} of CobbleEffort's cosmetic textures (split off so the mods share in small files)."
    fabric = {"schemaVersion": 1, "id": mod_id, "version": version, "name": name, "description": desc,
              "authors": ["ellecat5112"], "license": "MPL-2.0", "environment": "*",
              "depends": {"cobbleeffort": f"={version}"}}
    neo = "\n".join([
        'modLoader = "lowcodefml"', 'loaderVersion = "[1,)"', 'license = "MPL-2.0"', "",
        "[[mods]]", f'modId = "{mod_id}"', f'version = "{version}"', f'displayName = "{name}"',
        'authors = "ellecat5112"', f"description = '''{desc}'''", "",
        f"[[dependencies.{mod_id}]]", 'modId = "cobbleeffort"', 'type = "required"',
        f'versionRange = "[{version}]"', 'ordering = "NONE"', 'side = "BOTH"', ""])
    return mod_id, json.dumps(fabric, indent=1).encode(), neo.encode()


def split_base(jar, out_dir):
    """The core jar (written now) and the collection texture folders: {folder: [ZipInfo]} with estimated sizes."""
    z = zipfile.ZipFile(jar)
    version = json.loads(z.read("fabric.mod.json"))["version"]
    folders, core = {}, []
    for i in z.infolist():
        if i.filename == "previous-compilation-data.bin":
            continue
        rest = i.filename[len(TEX):] if i.filename.startswith(TEX) else ""
        if "/" in rest:
            folders.setdefault(rest.split("/")[0], []).append(i)
        else:
            core.append(i)
    core_path = os.path.join(out_dir, f"cobbleeffort-{version}+1.21.1-core.jar")
    write_jar(core_path, [(i.filename, z.read(i.filename), i.date_time) for i in core])
    sizes = {k: sum(i.compress_size + 76 + 2 * len(i.filename) for i in v) for k, v in folders.items()}
    return z, version, core_path, folders, sizes


def texture_jar(z, version, folders, keys, n, total, out_dir):
    mod_id, fabric, neo = part_meta(n, total, version)
    t0 = (1980, 1, 1, 0, 0, 0)
    entries = [("META-INF/MANIFEST.MF", b"Manifest-Version: 1.0\r\n\r\n", t0), ("fabric.mod.json", fabric, t0),
               ("META-INF/neoforge.mods.toml", neo, t0), ("pack.mcmeta", z.read("pack.mcmeta"), t0),
               ("LICENSE_" + mod_id, z.read("LICENSE_cobbleeffort"), t0)]
    for k in sorted(keys):
        entries += [(i.filename, z.read(i.filename), i.date_time) for i in folders[k]]
    path = os.path.join(out_dir, f"cobbleeffort-textures-{n}-{version}+1.21.1.jar")
    write_jar(path, entries)
    return path


# ---- packages --------------------------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--distortion")
    ap.add_argument("--kanto")
    ap.add_argument("--fusion")
    ap.add_argument("--readme", action="append", default=[], help="Mod=path (README/LICENSE files to include)")
    ap.add_argument("--limit", type=float, default=19.5)
    ap.add_argument("--loader", default="Fabric")
    ap.add_argument("--cache", default=None)
    a = ap.parse_args()
    limit = int(a.limit * MB)
    cache = a.cache or os.path.join(a.out, "cache")
    work = os.path.join(a.out, "jars")
    for d in (cache, work):
        os.makedirs(d, exist_ok=True)

    z, version, core_path, folders, fsizes = split_base(repack(a.base, cache), work)
    mods = {"CobbleEffort": [("CobbleEffort (core)", core_path)]}
    for key, label in (("distortion", "CobbleEffort: Distortion"), ("kanto", "CobbleEffort: Kanto"),
                       ("fusion", "CobbleEffort: Fusion")):
        src = getattr(a, key)
        if src:
            dst = os.path.join(work, os.path.basename(src))
            shutil.copy(repack(src, cache), dst)
            mods[label] = [(label, dst)]
    docs = {}
    for r in a.readme:
        mod, path = r.split("=", 1)
        docs.setdefault(mod, []).append(path)
    doc_size = {m: sum(os.path.getsize(p) // 3 for p in ps) for m, ps in docs.items()}   # text deflates ~3x

    for safety in (0.25, 0.5, 0.8, 1.2, 1.8):
        cap = limit - int(safety * MB)
        # whole jars first (biggest first, first fit), then texture folders into the room left (best fit)
        items = sorted([(label, path, mod) for mod, js in mods.items() for label, path in js], key=lambda t: -os.path.getsize(t[1]))
        zips = []
        for label, path, mod in items:
            size = os.path.getsize(path) + doc_size.get(mod, 0)
            for zp in zips:
                if zp["size"] + size <= cap:
                    zp["items"].append((label, path, mod)); zp["size"] += size
                    break
            else:
                if size > cap:
                    sys.exit(f"{os.path.basename(path)} alone is over the limit")
                zips.append({"items": [(label, path, mod)], "size": size, "tex": []})
        for k in sorted(fsizes, key=lambda k: -fsizes[k]):
            fit = [zp for zp in zips if zp["size"] + fsizes[k] + (0 if zp["tex"] else 20_000) <= cap]
            if fit:
                zp = min(fit, key=lambda zp: cap - zp["size"])
            else:
                zp = {"items": [], "size": 0, "tex": []}
                zips.append(zp)
            zp["size"] += fsizes[k] + (0 if zp["tex"] else 20_000)
            zp["tex"].append(k)
        total = sum(1 for zp in zips if zp["tex"])
        n = 0
        for zp in zips:
            if zp["tex"]:
                n += 1
                path = texture_jar(z, version, folders, zp["tex"], n, total, work)
                label = f"CobbleEffort Textures {n} of {total} ({len(zp['tex'])} texture folders)"
                zp["items"].append((label, path, "CobbleEffort"))
        real = [sum(os.path.getsize(p) for _, p, _ in zp["items"]) + sum(doc_size.get(m, 0) for m in {m for _, _, m in zp["items"]})
                for zp in zips]
        if max(real) + 60_000 <= limit:
            break
        for f in os.listdir(work):
            if f.startswith("cobbleeffort-textures-"):
                os.remove(os.path.join(work, f))

    names = [f"CobbleEffort-{a.loader}-{version}-part{n}of{len(zips)}.zip" for n in range(1, len(zips) + 1)]
    lines = [f"CobbleEffort mods for {a.loader.upper()} (Minecraft 1.21.1, Cobblemon 1.8.4)",
             "=" * 64, f"{len(zips)} downloads, each under {a.limit:g} MB:"]
    for name, zp in zip(names, zips):
        lines.append(f"  {name}")
        for label, path, _ in zp["items"]:
            lines.append(f"      {os.path.basename(path):55s} {label}")
    lines += ["",
              "Unzip them all and put every .jar in your mods folder (and on the server). CobbleEffort is the core jar",
              "plus its texture jars: install all of them together (a missing texture jar shows some cosmetics with",
              "Minecraft's missing texture). Distortion, Kanto and Fusion are add-ons; Kanto needs Distortion.",
              "",
              f"Also needed (download separately): {a.loader} Loader" + (", Fabric API" if a.loader == "Fabric" else "") +
              ", Cobblemon 1.8.4, Architectury API; for Distortion and Kanto also Mega Showdown 1.3.3+ and Accessories.",
              "",
              "These jars are packed smaller for sharing: the same files, with textures that had more than 256 colours",
              "reduced to their best 256 (an invisible change). Each mod's README and licence are included.",
              "Non-commercial (CC BY-NC / CC BY-NC-SA); not affiliated with Nintendo, Game Freak, The Pokémon Company,",
              "the Cobblemon team or the Infinite Fusion team.", ""]
    install = "\n".join(lines).encode()
    for name, zp in zip(names, zips):
        path = os.path.join(a.out, name)
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("INSTALL.txt", install)
            done = set()
            for label, jar, mod in zp["items"]:
                z.write(jar, os.path.basename(jar), compress_type=zipfile.ZIP_STORED)
                for d in docs.get(mod, []):
                    arc = f"{os.path.splitext(os.path.basename(d))[0]}-{mod.split(': ')[-1]}.txt"
                    if arc not in done:
                        z.write(d, arc)
                        done.add(arc)
        print(f"{name}: {os.path.getsize(path) / MB:.2f} MB")
        for label, jar, _ in zp["items"]:
            print(f"    {os.path.getsize(jar) / MB:6.2f} MB  {os.path.basename(jar)}")


if __name__ == "__main__":
    main()
