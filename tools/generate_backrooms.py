#!/usr/bin/env python3
"""
CobbleEffort - "Backrooms" collection generator.

Turns existing Cobblemon textures into "Still Life" versions inspired by the
Kane Pixels Backrooms series. A Still Life is an imperfect copy that the
Backrooms makes from memory. It looks moulded and assembled, with a sallow
plaster/clay finish, drained colour, smeared features and extra eyes.

The script reads the original textures from a Cobblemon source checkout (or an
extracted Cobblemon jar) and writes:

  * the retextured PNGs for every species in each listed species' WHOLE
    evolutionary line (pre-evolutions, evolutions and branches)
  * a resolver per species (assets/cobbleeffort/bedrock/pokemon/resolvers)
  * the cosmetic-item, species-feature and species-feature-assignment data files

Usage:
    python3 tools/generate_backrooms.py --cobblemon <path-to-cobblemon-assets-root>

where <path> is the directory that contains `assets/cobblemon/...` and
`data/cobblemon/...` (for a
Cobblemon source checkout: common/src/main/resources; for a jar: the folder
you extracted it into).

Every species gets its own seed, so the output can be reproduced exactly.
"""
from __future__ import annotations

import argparse
import colorsys
import hashlib
import json
import random
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "src" / "main" / "resources"
MOD_ID = "cobbleeffort"
ASPECT = "backrooms"
FEATURE_NAME = "backrooms_still_life"
CONFIG = Path(__file__).resolve().parent / "backrooms_species.json"

# Level 0 / Still Life palette: dark umber -> wet clay -> sallow plaster -> fluorescent-lit highlight
PALETTE = [
    (0.00, (34, 28, 18)),
    (0.25, (88, 72, 46)),
    (0.50, (150, 128, 86)),
    (0.75, (201, 183, 128)),
    (1.00, (236, 226, 178)),
]
EYE_COLOUR = (22, 17, 11)  # flat, matte, "painted-on" eyes


def lerp(a, b, t):
    return a + (b - a) * t


def palette_lookup(lum: float):
    lum = max(0.0, min(1.0, lum))
    for (p0, c0), (p1, c1) in zip(PALETTE, PALETTE[1:]):
        if lum <= p1:
            t = (lum - p0) / (p1 - p0) if p1 > p0 else 0
            return tuple(lerp(c0[i], c1[i], t) for i in range(3))
    return PALETTE[-1][1]


def seed_for(name: str) -> int:
    return int(hashlib.sha256(f"{MOD_ID}:{ASPECT}:{name}".encode()).hexdigest()[:12], 16)


def value_noise(w: int, h: int, cell: int, rng: random.Random):
    """Cheap smooth value noise (bilinear), values 0..1."""
    gw, gh = w // cell + 2, h // cell + 2
    grid = [[rng.random() for _ in range(gw)] for _ in range(gh)]
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        gy, fy = divmod(y / cell, 1)
        gy = int(gy)
        for x in range(w):
            gx, fx = divmod(x / cell, 1)
            gx = int(gx)
            a = lerp(grid[gy][gx], grid[gy][gx + 1], fx)
            b = lerp(grid[gy + 1][gx], grid[gy + 1][gx + 1], fx)
            out[y][x] = lerp(a, b, fy)
    return out


def still_life(base: Image.Image, eyes: Image.Image | None, seed: int, shiny: bool) -> Image.Image:
    rng = random.Random(seed)
    base = base.convert("RGBA")
    w, h = base.size
    src = base.load()
    scale = max(1, w // 64)  # textures are 64..256 px; keep features proportional

    eye_mask = [[False] * w for _ in range(h)]
    if eyes is not None:
        e = eyes.convert("RGBA").resize((w, h), Image.NEAREST).load()
        for y in range(h):
            for x in range(w):
                if e[x, y][3] > 0 and src[x, y][3] > 0:
                    eye_mask[y][x] = True

    stains = value_noise(w, h, max(4, 6 * scale), rng)      # damp blotches
    fold = value_noise(w, h, max(8, 14 * scale), rng)       # big "pressed by hand" undulation
    out = Image.new("RGBA", (w, h))
    o = out.load()

    # 1. drain colour and map onto the plaster/clay palette, keep a ghost of the original hue
    ghost = 0.30 if shiny else 0.18
    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if a == 0:
                o[x, y] = (0, 0, 0, 0)
                continue
            lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            lum = 0.18 + lum * 0.74                         # flatten contrast: everything looks moulded
            lum += (fold[y][x] - 0.5) * 0.10
            lum -= max(0.0, stains[y][x] - 0.62) * 0.55     # water damage
            lum += rng.uniform(-0.035, 0.035)               # clay grain
            pr, pg, pb = palette_lookup(lum)
            hh, ll, ss = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            gr, gg, gb = colorsys.hls_to_rgb(hh, max(0.2, min(0.8, lum)), ss * 0.6)
            o[x, y] = (
                int(lerp(pr, gr * 255, ghost)),
                int(lerp(pg, gg * 255, ghost)),
                int(lerp(pb, gb * 255, ghost)),
                a,
            )

    # 2. the "copied from memory" mistake: a few rows slip sideways, like a bad scan
    for _ in range(rng.randint(2, 4) * scale):
        y0 = rng.randrange(h)
        shift = rng.choice((-1, 1)) * scale
        band = rng.randint(1, 2) * scale
        rows = {}
        for y in range(y0, min(h, y0 + band)):
            rows[y] = [o[x, y] for x in range(w)]
        for y, row in rows.items():
            for x in range(w):
                sx = x - shift
                if 0 <= sx < w and row[sx][3] > 0 and src[x, y][3] > 0:
                    o[x, y] = row[sx][:3] + (src[x, y][3],)

    # 3. seams: thin darker lines where the pieces were pressed together
    for _ in range(rng.randint(2, 3)):
        horizontal = rng.random() < 0.5
        pos = rng.randrange(h if horizontal else w)
        length = rng.randint(w // 6, w // 2) if horizontal else rng.randint(h // 6, h // 2)
        start = rng.randrange((w if horizontal else h))
        wobble = 0
        for i in range(length):
            wobble += rng.choice((-1, 0, 0, 0, 1))
            x, y = (start + i, pos + wobble) if horizontal else (pos + wobble, start + i)
            if 0 <= x < w and 0 <= y < h and o[x, y][3] > 0 and not eye_mask[y][x]:
                r, g, b, a = o[x, y]
                o[x, y] = (int(r * 0.62), int(g * 0.60), int(b * 0.55), a)

    # 4. features: matte painted eyes, a duplicated set just below, and a smear dragging down
    if any(any(row) for row in eye_mask):
        coords = [(x, y) for y in range(h) for x in range(w) if eye_mask[y][x]]
        ys = [c[1] for c in coords]
        eye_h = max(1, max(ys) - min(ys) + 1)
        eye_h = min(eye_h, 4 * scale)
        dup_dy = eye_h + scale
        smear_len = rng.randint(2, 4) * scale
        for x, y in coords:
            o[x, y] = EYE_COLOUR + (src[x, y][3],)
        for x, y in coords:
            # second, slightly misplaced set of eyes
            dx = rng.choice((0, 0, scale if x % 2 else -scale))
            nx, ny = x + dx, y + dup_dy
            if 0 <= nx < w and 0 <= ny < h and o[nx, ny][3] > 0 and not eye_mask[ny][nx]:
                r, g, b, a = o[nx, ny]
                o[nx, ny] = (int(lerp(r, EYE_COLOUR[0], 0.8)), int(lerp(g, EYE_COLOUR[1], 0.8)),
                             int(lerp(b, EYE_COLOUR[2], 0.8)), a)
            # the smear: features run downwards like wet clay
            for i in range(1, smear_len + 1):
                sy = y + i
                if sy >= h or o[x, sy][3] == 0 or eye_mask[sy][x]:
                    break
                t = 0.55 * (1 - i / (smear_len + 1))
                r, g, b, a = o[x, sy]
                o[x, sy] = (int(lerp(r, EYE_COLOUR[0], t)), int(lerp(g, EYE_COLOUR[1], t)),
                            int(lerp(b, EYE_COLOUR[2], t)), a)

    # 5. fluorescent cast: Level 0's mono-yellow light
    for y in range(h):
        for x in range(w):
            r, g, b, a = o[x, y]
            if a:
                o[x, y] = (min(255, int(r * 1.03 + 4)), min(255, int(g * 1.01 + 3)), int(b * 0.90), a)
    return out


def resolve_path(assets_root: Path, identifier: str) -> Path:
    ns, path = identifier.split(":", 1)
    return assets_root / "assets" / ns / path


# ---------------------------------------------------------------------------------------------
# Evolutionary lines
#
# Collection rule: a cosmetic never covers just one stage. Every species listed in the config
# pulls in its whole evolutionary family (pre-evolutions, evolutions and branches), read from
# Cobblemon's species data. A family is the connected group of species linked by
# "preEvolution"/"evolutions", forms included.
# ---------------------------------------------------------------------------------------------

def load_species(cobblemon: Path) -> dict[str, dict]:
    species = {}
    for f in (cobblemon / "data" / "cobblemon" / "species").glob("*/*.json"):
        species[f.stem] = json.loads(f.read_text())
    if not species:
        raise SystemExit(f"No species data under {cobblemon}/data/cobblemon/species")
    return species


def species_id(ref: str) -> str:
    """'cobblemon:rattata alolan' / 'rattata form=alolan' -> 'rattata'."""
    return ref.split()[0].split(":")[-1].lower()


def evolution_families(species: dict[str, dict], extra_links: list[list[str]]) -> dict[str, set[str]]:
    adj: dict[str, set[str]] = {n: set() for n in species}

    def link(a: str, b: str):
        if a in adj and b in adj:
            adj[a].add(b)
            adj[b].add(a)

    for name, data in species.items():
        for block in [data] + data.get("forms", []):
            if block.get("preEvolution"):
                link(name, species_id(block["preEvolution"]))
            for evo in block.get("evolutions", []):
                if evo.get("result"):
                    link(name, species_id(evo["result"]))
    for a, b in extra_links:
        link(a, b)

    families = {}
    for name in species:
        if name in families:
            continue
        seen, stack = set(), [name]
        while stack:
            cur = stack.pop()
            if cur not in seen:
                seen.add(cur)
                stack.extend(adj[cur])
        for member in seen:
            families[member] = seen
    return families


# ---------------------------------------------------------------------------------------------
# Resolvers
# ---------------------------------------------------------------------------------------------

def load_resolvers(cobblemon: Path) -> dict[str, tuple[str, list[dict]]]:
    """species -> (resolver folder, merged variations in Cobblemon's load order)."""
    sets: dict[str, list[tuple[int, str, dict]]] = {}
    root = cobblemon / "assets" / "cobblemon" / "bedrock" / "pokemon" / "resolvers"
    for f in sorted(root.rglob("*.json")):
        data = json.loads(f.read_text())
        name = data.get("species", data.get("name", "")).split(":")[-1]
        sets.setdefault(name, []).append((data.get("order", 0), f.parent.name, data))
    out = {}
    for name, entries in sets.items():
        entries.sort(key=lambda e: e[0])
        out[name] = (entries[0][1], [v for e in entries for v in e[2].get("variations", [])])
    return out


def cosmetic_aspects(cobblemon: Path) -> set[str]:
    """Aspects that only ever come from another cosmetic item. A Pokémon wearing our item can't have them."""
    aspects = set()
    for f in (cobblemon / "data" / "cobblemon" / "cosmetic_items").glob("*.json"):
        for item in json.loads(f.read_text()).get("cosmeticItems", []):
            aspects.update(item.get("aspects", []))
    return aspects


class Retexturer:
    def __init__(self, cobblemon: Path, out_root: Path):
        self.cobblemon = cobblemon
        self.out_root = out_root
        self.done: dict[tuple[str, str], str] = {}

    def __call__(self, src_id: str, eyes_id: str | None, seed: int) -> str:
        key = (src_id, eyes_id or "")
        if key in self.done:
            return self.done[key]
        ns, path = src_id.split(":", 1)
        rel = Path(path).relative_to("textures/pokemon") if path.startswith("textures/pokemon/") else Path(ns) / path
        out_rel = rel.with_name(f"{rel.stem}_{ASPECT}.png")
        src = resolve_path(self.cobblemon, src_id)
        if not src.exists():
            raise SystemExit(f"Missing source texture {src_id} ({src})")
        base = Image.open(src)
        eyes = None
        if eyes_id:
            eye_path = resolve_path(self.cobblemon, eyes_id)
            if eye_path.exists():
                eyes = Image.open(eye_path)
                # only trust the eye mask when it was painted for the same UV layout
                if eyes.width * base.height != eyes.height * base.width:
                    eyes = None
        img = still_life(base, eyes, seed, shiny="shiny" in rel.stem)
        dest = self.out_root / out_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        img.save(dest, optimize=True)
        new_id = f"{MOD_ID}:textures/pokemon/{ASPECT}/{out_rel.as_posix()}"
        self.done[key] = new_id
        return new_id

    def supplier(self, tex, eyes_id: str | None, seed: int):
        """Static texture id, or an animated supplier {"frames": [...], ...}."""
        if isinstance(tex, str):
            return self(tex, eyes_id, seed)
        if isinstance(tex, dict) and "frames" in tex:
            return {**tex, "frames": [self(f, eyes_id, seed) for f in tex["frames"]]}
        return tex


def eye_mask_for(variation_aspects: set[str], alpha_layers: list[tuple[set[str], str]]) -> str | None:
    """Pick the alpha-eyes texture Cobblemon would overlay on this variation (most specific match)."""
    wanted = variation_aspects - {"shiny"}
    best = None
    for aspects, tex in alpha_layers:
        if aspects <= wanted and (best is None or len(aspects) > len(best[0])):
            best = (aspects, tex)
    return best[1] if best else None


def still_life_variations(name: str, variations: list[dict], skip: set[str], retex: Retexturer) -> list[dict]:
    """Mirror every vanilla variation with the Still Life aspect added.

    Cobblemon picks the last matching variation for each property, so copying the vanilla list in order,
    each with "backrooms" added, keeps the vanilla logic (shiny, gender, regional forms, model swaps)
    while every texture is swapped for its Still Life version.
    """
    seed = seed_for(name)
    alpha_layers = [
        (set(v.get("aspects", [])) - {"alpha_eyes"}, layer["texture"])
        for v in variations if "alpha_eyes" in v.get("aspects", [])
        for layer in v.get("layers", []) if isinstance(layer.get("texture"), str)
    ]
    out = []
    for v in variations:
        aspects = list(v.get("aspects", []))
        if "alpha_eyes" in aspects or skip.intersection(aspects):
            continue
        if "texture" not in v and not v.get("layers"):
            continue
        copy = {"aspects": aspects + [ASPECT]}
        if "condition" in v:
            copy["condition"] = v["condition"]
        eyes = eye_mask_for(set(aspects), alpha_layers)
        if "texture" in v:
            copy["texture"] = retex.supplier(v["texture"], eyes, seed)
        layers = []
        for layer in v.get("layers") or []:
            if layer.get("emissive"):
                layers.append({"name": layer["name"], "enabled": False})   # Still Lifes do not glow
            elif "texture" in layer:
                layers.append({**layer, "texture": retex.supplier(layer["texture"], None, seed)})
        if layers:
            copy["layers"] = layers
        out.append(copy)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cobblemon", required=True, type=Path,
                    help="Cobblemon resources root, containing assets/cobblemon and data/cobblemon "
                         "(e.g. cobblemon/common/src/main/resources or an extracted Cobblemon jar)")
    args = ap.parse_args()

    config = json.loads(CONFIG.read_text())
    species = load_species(args.cobblemon)
    families = evolution_families(species, config.get("extra_links", []))
    resolvers = load_resolvers(args.cobblemon)
    skip = cosmetic_aspects(args.cobblemon)

    members: set[str] = set()
    print("Evolutionary lines:")
    for pick in config["lines"]:
        if pick not in species:
            raise SystemExit(f"Unknown species in config: {pick}")
        family = sorted(families[pick], key=lambda n: species[n]["nationalPokedexNumber"])
        missing = [n for n in family if n not in resolvers]
        if missing:
            raise SystemExit(f"{pick}: no Cobblemon model for {missing}. The whole line must be retexturable.")
        print(f"  {pick:12s} -> {', '.join(family)}")
        members.update(family)
    ordered = sorted(members, key=lambda n: species[n]["nationalPokedexNumber"])

    out_tex_root = RES / "assets" / MOD_ID / "textures" / "pokemon" / ASPECT
    out_res_root = RES / "assets" / MOD_ID / "bedrock" / "pokemon" / "resolvers"
    for generated in (out_tex_root, out_res_root):
        if generated.exists():
            shutil.rmtree(generated)   # outputs are fully regenerated, so no stale files are left behind
    retex = Retexturer(args.cobblemon, out_tex_root)
    manifest = []
    for name in ordered:
        folder, variations = resolvers[name]
        mirrored = still_life_variations(name, variations, skip, retex)
        res_dir = out_res_root / folder
        res_dir.mkdir(parents=True, exist_ok=True)
        write_json(res_dir / f"9000_{name}_{ASPECT}.json", {
            "species": f"cobblemon:{name}",
            # Cobblemon sorts resolver files by "order" and the last matching variation wins,
            # so a high order keeps the Still Life texture on top of every vanilla variation.
            "order": 9000,
            "variations": mirrored,
        })
        base = next(v for v in variations if not v.get("aspects") and "model" in v)
        manifest.append({"species": name, "folder": folder, "model": base["model"],
                         "original": base["texture"], "still_life": mirrored[0]["texture"]})
    write_json(Path(__file__).resolve().parent / "preview" / "manifest.json", manifest)

    data = RES / "data" / MOD_ID
    write_json(data / "species_features" / f"{FEATURE_NAME}.json", {
        "keys": [ASPECT],
        "type": "flag",
        "isAspect": True,
        "default": False,
    })
    write_json(data / "species_feature_assignments" / f"{FEATURE_NAME}.json", {
        "pokemon": ordered,
        "features": [FEATURE_NAME],
    })
    write_json(data / "cosmetic_items" / f"{ASPECT}.json", {
        "pokemon": ordered,
        "cosmeticItems": [{"consumedItem": f"#{MOD_ID}:{ASPECT}_cosmetics", "aspects": [ASPECT]}],
    })
    write_json(data / "tags" / "item" / f"{ASPECT}_cosmetics.json", {
        "replace": False,
        "values": config["cosmetic_items"],
    })
    print(f"Generated {len(ordered)} Still Lifes from {len(config['lines'])} lines, {len(retex.done)} textures.")


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n")


if __name__ == "__main__":
    main()
