#!/usr/bin/env python3
"""
Compatibility bridge for resource packs in Cobblemon's old (pre-1.5) layout, e.g. the Planeta Cobblemon free pack.

The problem: Cobblemon 1.8 still reads bedrock/models, bedrock/posers, bedrock/animations and bedrock/species, but
it loads them before bedrock/pokemon/..., into the same names (model file name, poser id, animation group), and the
later load wins. So when Cobblemon or a mod (Mega Showdown, ATM x MSD, ...) also ships a Pokémon, the pack's mesh,
poser and animations lose whatever the pack order, while its textures (same paths) still win: the pack's texture on
another mesh. Base glow / alpha-eye layers made for the other mesh also stay on.

The bridge is the same pack in the current layout, written so that it wins as a whole when it sits above the mods:
  - every model / poser / animation file at its bedrock/pokemon/... path, and also at the exact path of every file
    in the stack that shares its name (so the pack replaces each of them by pack priority);
  - its textures as they are;
  - its resolver first (a lower order than any other for that species), and every other resolver for that species
    rewritten to keep only the forms with their own mesh (megas etc.): base looks, shiny textures and base layers
    painted for the other mesh go, so nothing of it is drawn on the pack's mesh.

The pack's art is never committed or shipped in CobbleEffort: the bridge is built locally from the user's own copy
(tools/compat/jars/, gitignored) into build/bridge/, for their own use. The generator sees the stack as the bridge
makes it (tools/stack.py), so CobbleEffort's cosmetics vendor Cobblemon's model wherever the pack replaces it.

Usage: python3 tools/bridge.py --cobblemon <cobblemon>/common/src/main/resources [--out build/bridge]
"""
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

from stack import Stack, bedrock_kind

ROOT = Path(__file__).resolve().parent.parent
BASEISH = {"shiny", "alpha_eyes"}
PACK_FORMAT = 34                        # Minecraft 1.21.1


def _dump(data) -> bytes:
    return (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def _new_path(rel: str, kind: str, folder: str) -> str:
    parts = rel.split("/")
    return "/".join(["assets", parts[1], "bedrock", "pokemon", kind] + ([folder] if folder else []) + [parts[-1]])


def bridge(stack: Stack, layer) -> dict[str, bytes]:
    """The bridged pack's files (rel -> bytes) for this legacy-layout layer, against the stack's other layers."""
    src = sorted(layer.files)
    out: dict[str, bytes] = {}
    report = layer.report
    report.clear()
    below = [l for l in stack.layers if not l.bridge]

    # the folder each species uses (from the pack's own resolvers/models), for posers that sit at the top level
    folders: dict[str, str] = {}
    for rel in src:
        kind = bedrock_kind(rel)
        if kind and kind[1] and kind[0] in ("models", "resolvers") and len(rel.split("/")) == 6:
            folder = rel.split("/")[4]
            folders.setdefault(folder.split("_", 1)[-1], folder)

    for rel in src:
        if not rel.startswith("assets/"):
            continue
        kind = bedrock_kind(rel)
        if kind is None:
            out[rel] = layer.read_original(rel)                     # textures, sounds, lang, ...
            continue
        what, legacy = kind
        if what == "resolvers":
            continue                                                # below
        name = rel.split("/")[-1][:-len(".json")]
        ns = rel.split("/")[1]
        sub = rel.split("/")[4:-1] if legacy else rel.split("/")[5:-1]
        folder = "/".join(sub) or folders.get(name.split(".")[0], "")
        if what == "models":
            entries = stack.models.get((ns, name), [])
        elif what == "posers":
            entries = stack.posers.get((ns, name), [])
        else:
            entries = stack.anims.get(name[:-len(".animation")], [])
        targets = {_new_path(rel, what, folder)}
        targets |= {r for l, r in entries if l in below and bedrock_kind(r) and not bedrock_kind(r)[1]}
        data = layer.read_original(rel)
        for t in sorted(targets):
            out[t] = data
        others = sorted({l.name for l, _ in entries if l in below})
        if others:
            label = f"animation group {name[:-len('.animation')]}" if what == "animations" else f"{what[:-1]} {ns}:{name}"
            report.append(f"{label} replaces {', '.join(others)}'s")

    # resolvers
    theirs: dict[str, list] = {}
    for rel, owner in stack.files(r"assets/[^/]+/bedrock/pokemon/resolvers/.+\.json").items():
        if owner.bridge:
            continue
        data = owner.json(rel)
        sp = str(data.get("species", data.get("name", ""))).split(":")[-1]
        theirs.setdefault(sp, []).append((rel, owner, data))
    for rel in src:
        kind = bedrock_kind(rel)
        if not kind or kind != ("resolvers", True):
            continue
        mine = json.loads(layer.read_original(rel).decode("utf-8-sig"))
        sp = str(mine.get("species", "")).split(":")[-1]
        others = theirs.get(sp, [])
        # forms with their own mesh stay (and their texture-only children: mega + shiny)
        form_sets = [set(v.get("aspects") or []) for _, _, d in others for v in d.get("variations", [])
                     if "model" in v and not set(v.get("aspects") or []) <= BASEISH]

        def kept(v):
            a = set(v.get("aspects") or [])
            return not a <= BASEISH and any(f <= a for f in form_sets)

        orders = []
        for orel, owner, d in others:
            vs = d.get("variations", [])
            keep = [v for v in vs if kept(v)]
            orders.append(d.get("order", 0))
            if len(keep) == len(vs):
                continue
            out[orel] = _dump({**d, "variations": keep})
            dropped = len(vs) - len(keep)
            report.append(f"resolver {orel} ({owner.name}): {dropped} base variation(s) dropped, {len(keep)} form(s) kept")
        own = _new_path(rel, "resolvers", "/".join(rel.split("/")[4:-1]))
        if any(own == o[0] for o in others):
            own = own[:-len(".json")] + "_bridge.json"
        order = min([mine.get("order", 0)] + [o - 1 for o in orders])
        out[own] = _dump({**mine, "order": order})
    return out


def write_pack(layer, files: dict[str, bytes], out_dir: Path) -> Path:
    try:
        desc = json.loads(layer.read_original("pack.mcmeta"))["pack"]["description"]
    except (KeyError, ValueError):
        desc = layer.name
    desc = desc if isinstance(desc, str) else layer.name
    meta = {"pack": {"pack_format": PACK_FORMAT, "supported_formats": {"min_inclusive": 15, "max_inclusive": PACK_FORMAT},
                     "description": f"{desc} (CobbleEffort bridge)"}}
    readme = (f"{layer.name}, rearranged by CobbleEffort's compatibility bridge (tools/bridge.py) for Cobblemon 1.8\n"
              f"and the mods it runs with. The art is {layer.name}'s, from your own copy; this file is for your own use,\n"
              "don't share it.\n\n"
              "Use it INSTEAD of the original pack (disable that one) and keep it ABOVE the other resource packs.\n\n"
              "What it changes:\n" + "".join(f"  - {line}\n" for line in layer.report))
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(layer.path.name).stem if layer.path.is_file() else layer.path.name
    dest = out_dir / f"{stem}-CobbleEffort-bridge.zip"
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in [("pack.mcmeta", _dump(meta)), ("BRIDGE.txt", readme.encode())] + sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2024, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    return dest


def build(stack: Stack, out_dir: Path) -> list[Path]:
    made = []
    for layer in stack.layers:
        if layer.bridge:
            made.append(write_pack(layer, {r: layer.read(r) for r in layer.files}, out_dir))
    return made


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cobblemon", required=True, type=Path, help="Cobblemon's common/src/main/resources")
    ap.add_argument("--out", type=Path, default=ROOT / "build" / "bridge")
    args = ap.parse_args()
    stack = Stack(args.cobblemon)
    for dest in build(stack, args.out):
        print(f"wrote {dest}")
    for layer in stack.layers:
        for line in layer.report:
            print(f"  {layer.id}: {line}")


if __name__ == "__main__":
    main()
