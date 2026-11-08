#!/usr/bin/env python3
"""
CobbleEffort collection generator.

Every collection lives in tools/collections/<name>.json and has a texture style in
tools/styles/<style>.py. For each collection this script writes:

  * retextured PNGs for every species in each listed species' WHOLE evolutionary line
    (pre-evolutions, evolutions and branches)
  * an order-9000 resolver per species that mirrors every vanilla variation with the
    collection's aspect added
  * the cosmetic-item, item-tag, species-feature and species-feature-assignment data files
  * tools/preview/manifest_<aspect>.json for the preview renderer

Usage:
    python3 tools/generate.py --cobblemon <resources-root> build [collection ...]
    python3 tools/generate.py --cobblemon <resources-root> pick --count 18 --seed <text>

<resources-root> contains assets/cobblemon and data/cobblemon (a Cobblemon source checkout's
common/src/main/resources, or an extracted Cobblemon jar). Output is deterministic: every
species has a fixed seed per collection, so reruns are byte-identical.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import random
import shutil
from pathlib import Path

from PIL import Image

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
RES = ROOT / "src" / "main" / "resources"
COLLECTIONS = TOOLS / "collections"
MOD_ID = "cobbleeffort"
RESOLVER_ORDER = 9000


def resolve_path(assets_root: Path, identifier: str) -> Path:
    ns, path = identifier.split(":", 1)
    return assets_root / "assets" / ns / path


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n")


def load_collection(name: str) -> dict:
    cfg = json.loads((COLLECTIONS / f"{name}.json").read_text())
    cfg.setdefault("extra_links", [])
    cfg["name"] = name
    return cfg


def all_collections() -> list[str]:
    return sorted(p.stem for p in COLLECTIONS.glob("*.json"))


# ---------------------------------------------------------------------------------------------
# Cobblemon data
# ---------------------------------------------------------------------------------------------

class Cobblemon:
    def __init__(self, root: Path):
        self.root = root
        self.species = self._load_species()
        self.resolvers = self._load_resolvers()
        self.cosmetic_aspects = self._load_cosmetic_aspects()

    def _load_species(self) -> dict[str, dict]:
        species = {}
        for f in (self.root / "data" / "cobblemon" / "species").glob("*/*.json"):
            species[f.stem] = json.loads(f.read_text())
        if not species:
            raise SystemExit(f"No species data under {self.root}/data/cobblemon/species")
        return species

    def _load_resolvers(self) -> dict[str, tuple[str, list[dict]]]:
        """species -> (resolver folder, merged variations in Cobblemon's load order)."""
        sets: dict[str, list[tuple[int, str, dict]]] = {}
        root = self.root / "assets" / "cobblemon" / "bedrock" / "pokemon" / "resolvers"
        for f in sorted(root.rglob("*.json")):
            data = json.loads(f.read_text())
            name = data.get("species", data.get("name", "")).split(":")[-1]
            sets.setdefault(name, []).append((data.get("order", 0), f.parent.name, data))
        out = {}
        for name, entries in sets.items():
            entries.sort(key=lambda e: e[0])
            out[name] = (entries[0][1], [v for e in entries for v in e[2].get("variations", [])])
        return out

    def _load_cosmetic_aspects(self) -> set[str]:
        """Aspects that only ever come from another cosmetic item. A Pokémon wearing ours can't have them."""
        aspects = set()
        for f in (self.root / "data" / "cobblemon" / "cosmetic_items").glob("*.json"):
            for item in json.loads(f.read_text()).get("cosmeticItems", []):
                aspects.update(item.get("aspects", []))
        return aspects

    def dex(self, name: str) -> int:
        return self.species[name]["nationalPokedexNumber"]

    # -----------------------------------------------------------------------------------------
    # Evolutionary lines
    #
    # Collection rule: a cosmetic never covers just one stage. A family is the connected group of
    # species linked by "preEvolution"/"evolutions" (forms included), plus a collection's extra_links.
    # -----------------------------------------------------------------------------------------

    @staticmethod
    def species_id(ref: str) -> str:
        """'cobblemon:rattata alolan' / 'rattata form=alolan' -> 'rattata'."""
        return ref.split()[0].split(":")[-1].lower()

    def families(self, extra_links: list[list[str]]) -> dict[str, frozenset[str]]:
        adj: dict[str, set[str]] = {n: set() for n in self.species}

        def link(a: str, b: str):
            if a in adj and b in adj:
                adj[a].add(b)
                adj[b].add(a)

        for name, data in self.species.items():
            for block in [data] + data.get("forms", []):
                if block.get("preEvolution"):
                    link(name, self.species_id(block["preEvolution"]))
                for evo in block.get("evolutions", []):
                    if evo.get("result"):
                        link(name, self.species_id(evo["result"]))
        for a, b in extra_links:
            link(a, b)

        families: dict[str, frozenset[str]] = {}
        for name in self.species:
            if name in families:
                continue
            seen, stack = set(), [name]
            while stack:
                cur = stack.pop()
                if cur not in seen:
                    seen.add(cur)
                    stack.extend(adj[cur])
            fam = frozenset(seen)
            for member in fam:
                families[member] = fam
        return families

    def retexturable(self, family) -> bool:
        return all(
            n in self.resolvers and self.species[n].get("implemented", True)
            and any(not v.get("aspects") and "model" in v and "texture" in v for v in self.resolvers[n][1])
            for n in family
        )


# ---------------------------------------------------------------------------------------------
# Geometry hints: where a model's head and torso faces sit in its texture
# ---------------------------------------------------------------------------------------------

class Geometry:
    """Reads Cobblemon .geo.json models to tell styles where the head's front/top faces and the torso's
    front face are in the texture (in geo UV units; styles scale to the real texture size via tex_size).
    Many Cobblemon models have their eyes as separate little cubes, so a face can't be found from the eyes."""

    def __init__(self, root: Path):
        self.root = root
        self.cache: dict[str, dict | None] = {}
        self.files = {f.name[:-len(".json")]: f for f in
                      (root / "assets" / "cobblemon" / "bedrock" / "pokemon" / "models").rglob("*.geo.json")}

    @staticmethod
    def _box(cube):
        uv = cube.get("uv")
        if not isinstance(uv, list):
            return None
        w, h, d = (abs(int(round(v))) for v in cube["size"])
        u, v = uv
        return {"front": (u + d, v + d, w, h), "top": (u + d, v, w, d), "area": w * h}

    @staticmethod
    def _net(cube):
        """The whole box-UV net of a cube: (u, v, width, height)."""
        w, h, d = (abs(int(round(v))) for v in cube["size"])
        return (cube["uv"][0], cube["uv"][1], 2 * (w + d), d + h)

    def _best(self, bones, words):
        best = None
        for b in bones:
            name = b["name"]
            if name.startswith("locator") or not any(wd in name for wd in words):
                continue
            for c in b.get("cubes", []):
                box = self._box(c)
                if box and (best is None or box["area"] > best["area"]):
                    best = box
        return best

    def hints(self, model_id: str | None):
        if not model_id:
            return None
        if model_id not in self.cache:
            f = self.files.get(model_id.split(":")[-1])
            if f is None:
                self.cache[model_id] = None
            else:
                g = json.loads(f.read_text())["minecraft:geometry"][0]
                head = self._best(g["bones"], ("head",))
                torso = self._best(g["bones"], ("torso", "body", "chest", "belly"))
                d = g["description"]
                self.cache[model_id] = {
                    "tex_size": (d["texture_width"], d["texture_height"]),
                    "head_front": head["front"] if head else None,
                    "head_top": head["top"] if head else None,
                    "torso_front": torso["front"] if torso else None,
                    "ears": [self._net(c) for b in g["bones"] if "ear" in b["name"] and not b["name"].startswith("locator")
                             and "eye" not in b["name"] for c in b.get("cubes", []) if isinstance(c.get("uv"), list)],
                }
        return self.cache[model_id]


# ---------------------------------------------------------------------------------------------
# Texturing and resolvers
# ---------------------------------------------------------------------------------------------

class Retexturer:
    """Writes retextured PNGs. Styles expose:

    retexture(base, eyes, seed, shiny, frame=0, layer=False) -> Image
              layer is False for a body texture, "emissive" for a glowing layer, "plain" for any other layer
    EMISSIVE  "disable" | "retexture"
    FRAMES    optional, >1 turns every static texture into an animation of that many frames
    FPS       optional, frames per second for those animations
    """

    def __init__(self, cobblemon: Path, aspect: str, out_root: Path):
        self.cobblemon = cobblemon
        self.aspect = aspect
        self.out_root = out_root
        self.done: dict[tuple, str] = {}
        self.hints = None   # geometry hints for the variation being mirrored (styles opt in with WANTS_HINTS)

    def _hint_kw(self, style):
        return {"hints": self.hints} if getattr(style, "WANTS_HINTS", False) else {}

    def __call__(self, src_id: str, eyes_id: str | None, seed: int, style, layer: str | bool = False,
                 frame: int = 0, suffix: str = "") -> str:
        key = (src_id, eyes_id or "", style.__name__, layer, frame, suffix, repr(self._hint_kw(style)))
        if key in self.done:
            return self.done[key]
        ns, path = src_id.split(":", 1)
        rel = Path(path).relative_to("textures/pokemon") if path.startswith("textures/pokemon/") else Path(ns) / path
        out_rel = rel.with_name(f"{rel.stem}_{self.aspect}{suffix}.png")
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
        shiny = "shiny" in rel.stem
        if frame or layer:
            img = style.retexture(base, eyes, seed, shiny, frame=frame, layer=layer, **self._hint_kw(style))
        else:
            img = style.retexture(base, eyes, seed, shiny, **self._hint_kw(style))
        dest = self.out_root / out_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        img.save(dest, optimize=True)
        new_id = f"{MOD_ID}:textures/pokemon/{self.aspect}/{out_rel.as_posix()}"
        self.done[key] = new_id
        return new_id

    def extra(self, src_tex, eyes_id: str | None, seed: int, style, spec: dict):
        """A layer the style adds on top of the body (spec from style.EXTRA_LAYERS), or None if it has nothing to draw.

        style.extra_layer(name, base, eyes, seed, shiny, frame) -> Image | None
        """
        src_id = src_tex["frames"][0] if isinstance(src_tex, dict) else src_tex
        frames = spec.get("frames", 1)
        ids = []
        for i in range(frames):
            key = ("extra", src_id, eyes_id or "", style.__name__, spec["name"], i, repr(self._hint_kw(style)))
            if key not in self.done:
                ns, path = src_id.split(":", 1)
                rel = Path(path).relative_to("textures/pokemon") if path.startswith("textures/pokemon/") else Path(ns) / path
                base = Image.open(resolve_path(self.cobblemon, src_id))
                eyes = None
                if eyes_id and resolve_path(self.cobblemon, eyes_id).exists():
                    eyes = Image.open(resolve_path(self.cobblemon, eyes_id))
                    if eyes.width * base.height != eyes.height * base.width:
                        eyes = None
                img = style.extra_layer(spec["name"], base, eyes, seed, "shiny" in rel.stem, i, **self._hint_kw(style))
                if img is None:
                    self.done[key] = None
                else:
                    out_rel = rel.with_name(f"{rel.stem}_{self.aspect}_{spec['name']}" + (f"_{i}" if frames > 1 else "") + ".png")
                    dest = self.out_root / out_rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    img.save(dest, optimize=True)
                    self.done[key] = f"{MOD_ID}:textures/pokemon/{self.aspect}/{out_rel.as_posix()}"
            if self.done[key] is None:
                return None
            ids.append(self.done[key])
        return ids[0] if frames == 1 else {"frames": ids, "fps": spec.get("fps", 6), "loop": True}

    @property
    def count(self) -> int:
        return sum(1 for v in self.done.values() if v)

    def supplier(self, tex, eyes_id: str | None, seed: int, style, layer: str | bool = False):
        """Static texture id, or an animated supplier {"frames": [...], ...}."""
        frames = getattr(style, "FRAMES", 1)
        if isinstance(tex, str):
            if frames <= 1:
                return self(tex, eyes_id, seed, style, layer)
            return {"frames": [self(tex, eyes_id, seed, style, layer, i, f"_{i}") for i in range(frames)],
                    "fps": getattr(style, "FPS", 6), "loop": True}
        if isinstance(tex, dict) and "frames" in tex:
            return {**tex, "frames": [self(f, eyes_id, seed, style, layer, i % max(1, frames))
                                      for i, f in enumerate(tex["frames"])]}
        return tex


def eye_mask_for(variation_aspects: set[str], alpha_layers: list[tuple[set[str], str]]) -> str | None:
    """Pick the alpha-eyes texture Cobblemon would overlay on this variation (most specific match)."""
    wanted = variation_aspects - {"shiny"}
    best = None
    for aspects, tex in alpha_layers:
        if aspects <= wanted and (best is None or len(aspects) > len(best[0])):
            best = (aspects, tex)
    return best[1] if best else None


def model_for(variations: list[dict], index: int) -> str | None:
    """The model Cobblemon would use for variation[index]: the last variation up to it whose aspects it has."""
    want = set(variations[index].get("aspects", []))
    model = None
    for v in variations[:index + 1]:
        if "model" in v and set(v.get("aspects", [])) <= want:
            model = v["model"]
    return model


def mirror_variations(variations: list[dict], aspect: str, seed: int, skip: set[str],
                      retex: Retexturer, style, geometry: "Geometry | None" = None) -> list[dict]:
    """Mirror every vanilla variation with the collection aspect added.

    Cobblemon picks the last matching variation for each property, so copying the vanilla list in order,
    each with the aspect added, keeps the vanilla logic (shiny, gender, regional forms, model swaps) while
    every texture is swapped for the collection's version.
    """
    alpha_layers = [
        (set(v.get("aspects", [])) - {"alpha_eyes"}, layer["texture"])
        for v in variations if "alpha_eyes" in v.get("aspects", [])
        for layer in v.get("layers", []) if isinstance(layer.get("texture"), str)
    ]
    out = []
    for index, v in enumerate(variations):
        retex.hints = geometry.hints(model_for(variations, index)) if geometry else None
        aspects = list(v.get("aspects", []))
        if "alpha_eyes" in aspects or skip.intersection(aspects):
            continue
        if "texture" not in v and not v.get("layers"):
            continue
        copy = {"aspects": aspects + [aspect]}
        if "condition" in v:
            copy["condition"] = v["condition"]
        eyes = eye_mask_for(set(aspects), alpha_layers)
        if "texture" in v:
            copy["texture"] = retex.supplier(v["texture"], eyes, seed, style)
        layers = []
        for layer in v.get("layers") or []:
            if layer.get("emissive") and style.EMISSIVE == "disable":
                layers.append({"name": layer.get("name", ""), "enabled": False})   # Cobblemon defaults a missing name to ""
            elif "texture" in layer:
                kind = "emissive" if layer.get("emissive") else "plain"
                layers.append({**layer, "texture": retex.supplier(layer["texture"], None, seed, style, layer=kind)})
        if "texture" in v:
            for spec in getattr(style, "EXTRA_LAYERS", []):
                tex = retex.extra(v["texture"], eyes, seed, style, spec)
                # the layer is always declared, so a variation without lights also switches off inherited ones
                layers.append({"name": f"{MOD_ID}_{spec['name']}", "texture": tex, "emissive": spec.get("emissive", False),
                               "translucent": spec.get("translucent", True)} if tex else
                              {"name": f"{MOD_ID}_{spec['name']}", "enabled": False})
        if layers:
            copy["layers"] = layers
        out.append(copy)
    return out


# ---------------------------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------------------------

def build_collection(cob: Cobblemon, cfg: dict):
    aspect, feature = cfg["aspect"], cfg["feature"]
    default_style = importlib.import_module(f"styles.{cfg['style']}")
    families = cob.families(cfg["extra_links"])
    # optional per-line looks, e.g. {"charmander": "halloween_skeleton"}; applies to the whole line
    style_of: dict[str, object] = {}
    for pick, name in cfg.get("line_styles", {}).items():
        if pick not in cfg["lines"]:
            raise SystemExit(f"{cfg['name']}: line_styles names {pick}, which is not in lines")
        for member in families[pick]:
            style_of[member] = importlib.import_module(f"styles.{name}")

    members: set[str] = set()
    print(f"[{cfg['name']}] evolutionary lines:")
    for pick in cfg["lines"]:
        if pick not in cob.species:
            raise SystemExit(f"Unknown species in {cfg['name']}: {pick}")
        family = sorted(families[pick], key=cob.dex)
        missing = [n for n in family if n not in cob.resolvers]
        if missing:
            raise SystemExit(f"{pick}: no Cobblemon model for {missing}. The whole line must be retexturable.")
        look = cfg.get("line_styles", {}).get(pick)
        print(f"  {pick:12s} -> {', '.join(family)}" + (f"  [{look}]" if look else ""))
        members.update(family)
    ordered = sorted(members, key=cob.dex)
    addons = cfg.get("addon_lines", [])
    for a in addons:
        print(f"  {a['species']:12s} -> {a['species']}  [addon: {a['builder']}; needs {a['requires']}]")

    out_tex_root = RES / "assets" / MOD_ID / "textures" / "pokemon" / aspect
    out_res_root = RES / "assets" / MOD_ID / "bedrock" / "pokemon" / "resolvers" / aspect
    for generated in (out_tex_root, out_res_root):
        if generated.exists():
            shutil.rmtree(generated)   # this collection's outputs are fully regenerated: no stale files
    retex = Retexturer(cob.root, aspect, out_tex_root)
    geometry = Geometry(cob.root)
    manifest = []
    for name in ordered:
        folder, variations = cob.resolvers[name]
        seed = int(hashlib.sha256(f"{MOD_ID}:{aspect}:{name}".encode()).hexdigest()[:12], 16)
        style = style_of.get(name, default_style)
        mirrored = mirror_variations(variations, aspect, seed, cob.cosmetic_aspects, retex, style, geometry)
        write_json(out_res_root / folder / f"{RESOLVER_ORDER}_{name}_{aspect}.json", {
            "species": f"cobblemon:{name}",
            # Cobblemon sorts resolver files by "order" and the last matching variation wins,
            # so a high order keeps this collection's textures on top of every vanilla variation.
            "order": RESOLVER_ORDER,
            "variations": mirrored,
        })
        base = next(v for v in variations if not v.get("aspects") and "model" in v)
        first = lambda t: t["frames"][0] if isinstance(t, dict) else t
        mirrored_base = mirrored[0]
        layers = []
        vanilla_layers = {l.get("name", ""): l for l in base.get("layers") or []}
        for new in mirrored_base.get("layers") or []:
            orig = vanilla_layers.get(new.get("name", ""), {})
            if new.get("enabled", True) and "texture" in new or "texture" in orig:
                layers.append({"original": first(orig["texture"]) if "texture" in orig else None,
                               "retextured": first(new["texture"]) if new.get("enabled", True) and "texture" in new else None,
                               "emissive": bool(new.get("emissive", orig.get("emissive")))})
        manifest.append({"species": name, "folder": folder, "model": base["model"],
                         "original": first(base["texture"]), "retextured": first(mirrored_base["texture"]),
                         "layers": layers})
    # addon lines: the model comes from another mod; the builder paints our texture from scratch onto its UV layout
    for a in addons:
        builder = importlib.import_module(f"addons.{a['builder']}")
        variations, entry = builder.build(out_tex_root, aspect, MOD_ID)
        write_json(out_res_root / f"addon_{a['species']}" / f"{RESOLVER_ORDER}_{a['species']}_{aspect}.json", {
            "species": f"cobblemon:{a['species']}", "order": RESOLVER_ORDER, "variations": variations,
        })
        manifest.append(entry)
        ordered.append(a["species"])
    write_json(TOOLS / "preview" / f"manifest_{aspect}.json", manifest)

    data = RES / "data" / MOD_ID
    write_json(data / "species_features" / f"{feature}.json", {
        "keys": [aspect], "type": "flag", "isAspect": True, "default": False,
    })
    write_json(data / "species_feature_assignments" / f"{feature}.json", {
        "pokemon": ordered, "features": [feature],
    })
    write_json(data / "cosmetic_items" / f"{aspect}.json", {
        "pokemon": ordered,
        "cosmeticItems": [{"consumedItem": f"#{MOD_ID}:{aspect}_cosmetics", "aspects": [aspect]}],
    })
    write_json(data / "tags" / "item" / f"{aspect}_cosmetics.json", {
        "replace": False, "values": cfg["cosmetic_items"],
    })
    print(f"[{cfg['name']}] {len(ordered)} Pokémon from {len(cfg['lines']) + len(addons)} lines, {retex.count} textures"
          + (f" (+ {len(addons)} addon line)" if addons else "") + ".")


def check_no_overlap(cob: Cobblemon, cfgs: list[dict]):
    """Collections must not share species or cosmetic items."""
    owner: dict[str, str] = {}
    items: dict[str, str] = {}
    for cfg in cfgs:
        fam = cob.families(cfg["extra_links"])
        for pick in cfg["lines"]:
            for n in fam[pick]:
                if owner.setdefault(n, cfg["name"]) != cfg["name"]:
                    raise SystemExit(f"{n} is in both {owner[n]} and {cfg['name']}")
        for a in cfg.get("addon_lines", []):
            if owner.setdefault(a["species"], cfg["name"]) != cfg["name"]:
                raise SystemExit(f"{a['species']} is in both {owner[a['species']]} and {cfg['name']}")
        for item in cfg["cosmetic_items"]:
            if items.setdefault(item, cfg["name"]) != cfg["name"]:
                raise SystemExit(f"{item} is the cosmetic item of both {items[item]} and {cfg['name']}")


def cmd_build(cob: Cobblemon, names: list[str]):
    every = [load_collection(n) for n in all_collections()]
    check_no_overlap(cob, every)
    for cfg in every:
        if not names or cfg["name"] in names:
            build_collection(cob, cfg)


def cmd_pick(cob: Cobblemon, count: int, seed: str):
    """Randomly pick `count` new evolutionary lines that no collection uses yet."""
    families = cob.families([])
    taken = set()
    for name in all_collections():
        cfg = load_collection(name)
        fam = cob.families(cfg["extra_links"])
        for pick in cfg["lines"]:
            taken |= fam[pick]
    pool = sorted({fam for fam in families.values() if not fam & taken and cob.retexturable(fam)},
                  key=lambda f: min(cob.dex(n) for n in f))
    rng = random.Random(seed)
    chosen = rng.sample(pool, count)
    for fam in sorted(chosen, key=lambda f: min(cob.dex(n) for n in f)):
        family = sorted(fam, key=cob.dex)
        print(f"{family[0]:12s} {', '.join(family)}")
    print(f"(picked {count} of {len(pool)} eligible lines with seed {seed!r})")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cobblemon", required=True, type=Path,
                    help="Cobblemon resources root containing assets/cobblemon and data/cobblemon")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="generate collections (all by default)")
    b.add_argument("collections", nargs="*")
    p = sub.add_parser("pick", help="randomly pick new evolutionary lines no collection uses yet")
    p.add_argument("--count", type=int, default=18)
    p.add_argument("--seed", required=True)
    args = ap.parse_args()
    cob = Cobblemon(args.cobblemon)
    if args.cmd == "build":
        cmd_build(cob, args.collections)
    else:
        cmd_pick(cob, args.count, args.seed)


if __name__ == "__main__":
    main()
