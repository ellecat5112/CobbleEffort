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

from kotlin_poser import convert as kotlin_convert, find_model_class
from painter import paint_layout
from stack import Stack, poser_groups, rename_groups

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
RES = ROOT / "src" / "main" / "resources"
COLLECTIONS = TOOLS / "collections"
MOD_ID = "cobbleeffort"
RESOLVER_ORDER = 9000


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
    """Cobblemon's data as the whole mod stack sees it (tools/stack.py): species files merged top-down with
    species_additions applied (so other mods' new pre-evolutions/evolutions join the families), resolvers in two
    views, and every cosmetic-item aspect from every mod.

    resolvers[name]  = (folder, variations) from DERIVATIVE layers only: what our retextured copies mirror
    effective[name]  = [(variation, layer)] from every layer: what the game would actually merge
    """

    def __init__(self, root: Path, use_compat: bool = True):
        self.root = root
        self.stack = Stack(root, use_compat)
        self.species = self._load_species()
        self.resolvers, self.var_layer = self._load_resolvers(derivative_only=True)
        effective, layer_of = self._load_resolvers(derivative_only=False)
        self.effective = {n: [(v, layer_of[id(v)]) for v in vs] for n, (_, vs) in effective.items()}
        self.effective_folder = {n: f for n, (f, _) in effective.items()}
        self.cosmetic_aspects = self._load_cosmetic_aspects()

    def _load_species(self) -> dict[str, dict]:
        species = {}
        for rel, layer in self.stack.files(r"data/cobblemon/species/.+\.json").items():
            species[Path(rel).stem] = layer.json(rel)
        if not species:
            raise SystemExit(f"No species data under {self.root}/data/cobblemon/species")
        for rel, layer in self.stack.files(r"data/[^/]+/species_additions/.+\.json").items():
            add = layer.json(rel)
            target = species.get(str(add.get("target", "")).split(":")[-1])
            if target is None:
                continue
            if add.get("preEvolution"):
                target.setdefault("_added_pre", []).append(add["preEvolution"])
            target.setdefault("_added_evolutions", []).extend(add.get("evolutions", []))
        return species

    def _load_resolvers(self, derivative_only: bool):
        """species -> (resolver folder, merged variations in load order), and variation id -> layer."""
        sets: dict[str, list] = {}
        layer_of = {}
        files = self.stack.files(r"assets/[^/]+/bedrock/pokemon/resolvers/.+\.json", derivative_only)
        for rel, layer in files.items():
            data = layer.json(rel)
            name = data.get("species", data.get("name", "")).split(":")[-1]
            for v in data.get("variations", []):
                layer_of[id(v)] = layer
            sets.setdefault(name, []).append((data.get("order", 0), rel.split("/")[-2], data))
        out = {}
        for name, entries in sets.items():
            entries.sort(key=lambda e: e[0])
            folder = entries[0][1] if entries[0][1] != "resolvers" else name
            out[name] = (folder, [v for e in entries for v in e[2].get("variations", [])])
        return out, layer_of

    def _load_cosmetic_aspects(self) -> set[str]:
        """Aspects that only ever come from another cosmetic item (any mod's). A Pokémon wearing ours can't have them."""
        aspects = set()
        for rel, layer in self.stack.files(r"data/[^/]+/cosmetic_items/.+\.json").items():
            for item in layer.json(rel).get("cosmeticItems", []):
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
            for pre in data.get("_added_pre", []):
                link(name, self.species_id(pre))
            for evo in data.get("_added_evolutions", []):
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

    def __init__(self, stack: Stack):
        self.stack = stack
        self.cache: dict[tuple, dict | None] = {}

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

    def hints(self, model_id: str | None, derivative_only: bool = True):
        """Hints for a model, read from the top-most derivative layer (or, for a painted member, the foreign
        model's UV layout: only cube positions are read, never its textures)."""
        if not model_id:
            return None
        key = (model_id, derivative_only)
        if key not in self.cache:
            g = self.stack.geometry(model_id, derivative_only)
            self.cache[key] = self.from_geo(g) if g else None
        return self.cache[key]

    def from_geo(self, g):
        head = self._best(g["bones"], ("head",))
        torso = self._best(g["bones"], ("torso", "body", "chest", "belly"))
        d = g["description"]
        return {
            "tex_size": (d["texture_width"], d["texture_height"]),
            "head_front": head["front"] if head else None,
            "head_top": head["top"] if head else None,
            "torso_front": torso["front"] if torso else None,
            "ears": [self._net(c) for b in g["bones"] if "ear" in b["name"] and not b["name"].startswith("locator")
                     and "eye" not in b["name"] for c in b.get("cubes", []) if isinstance(c.get("uv"), list)],
        }


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

    Sources come from the top-most DERIVATIVE layer of the stack. Outputs adapted from a mod other than Cobblemon
    go under <aspect>/compat/<mod id>/ (so their licence can be stated per folder). "Virtual" sources (painted
    bases for members modelled by a mod whose art can't be adapted) are registered with add_virtual() and written
    under <aspect>/painted/.
    """

    def __init__(self, stack: Stack, aspect: str, out_root: Path):
        self.stack = stack
        self.aspect = aspect
        self.out_root = out_root
        self.done: dict[tuple, str] = {}
        self.virtual: dict[str, Image.Image] = {}
        self.hints = None   # geometry hints for the variation being mirrored (styles opt in with WANTS_HINTS)

    def add_virtual(self, src_id: str, img: Image.Image):
        self.virtual[src_id] = img

    def _hint_kw(self, style):
        return {"hints": self.hints} if getattr(style, "WANTS_HINTS", False) else {}

    def _source(self, src_id: str):
        """(image, output rel path without the aspect suffix)."""
        ns, path = src_id.split(":", 1)
        rel = Path(path).relative_to("textures/pokemon") if path.startswith("textures/pokemon/") else Path(ns) / path
        if src_id in self.virtual:
            return self.virtual[src_id], rel
        hit = self.stack.image(src_id)
        if hit is None:
            raise SystemExit(f"Missing source texture {src_id} (not in any layer whose licence allows adaptations)")
        img, layer = hit
        return img, (rel if layer.id == "cobblemon" else Path("compat") / layer.id / rel)

    def _eyes(self, eyes_id, base):
        if not eyes_id:
            return None
        if eyes_id in self.virtual:
            eyes = self.virtual[eyes_id]
        else:
            hit = self.stack.image(eyes_id)
            if hit is None:
                return None
            eyes = hit[0]
        # only trust the eye mask when it was painted for the same UV layout
        return eyes if eyes.width * base.height == eyes.height * base.width else None

    def __call__(self, src_id: str, eyes_id: str | None, seed: int, style, layer: str | bool = False,
                 frame: int = 0, suffix: str = "") -> str:
        key = (src_id, eyes_id or "", style.__name__, layer, frame, suffix, repr(self._hint_kw(style)))
        if key in self.done:
            return self.done[key]
        base, rel = self._source(src_id)
        out_rel = rel.with_name(f"{rel.stem}_{self.aspect}{suffix}.png")
        eyes = self._eyes(eyes_id, base)
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
                base, rel = self._source(src_id)
                eyes = self._eyes(eyes_id, base)
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


def eye_mask_for(variation_aspects: set[str], model: str | None, alpha_layers: list[tuple[set[str], str, str]],
                 same_model_only: bool = False) -> str | None:
    """Pick the alpha-eyes texture Cobblemon would overlay on this variation (most specific match). For other mods'
    forms (same_model_only) only a mask made for the same model counts: a mega with its own model has a different
    UV layout from the base's eye mask."""
    wanted = variation_aspects - {"shiny"}
    best = None
    for aspects, tex, alpha_model in alpha_layers:
        if same_model_only and alpha_model != model:
            continue
        if aspects <= wanted and (best is None or len(aspects) > len(best[0])):
            best = (aspects, tex)
    return best[1] if best else None


def resolved(variations: list[dict], index: int, prop: str):
    """The value Cobblemon would use for `prop` on variation[index]: the last variation up to it, among those
    whose aspects it has, that sets it."""
    want = set(variations[index].get("aspects", []))
    value = None
    for v in variations[:index + 1]:
        if prop in v and set(v.get("aspects", [])) <= want:
            value = v[prop]
    return value


def model_for(variations: list[dict], index: int) -> str | None:
    return resolved(variations, index, "model")


class Vendor:
    """Keeps the cosmetic on the model its texture was painted for.

    Every mirrored copy pins the model and poser of the variation it copies. When a mod whose art can't be adapted
    overwrites one of those files (same model file name / poser id / animation group in a higher layer), a pinned
    'cobblemon:x.geo' would load their geometry instead. Then the top-most derivative version is vendored into our
    namespace (cobbleeffort:x.geo, cobbleeffort:x; animation groups renamed ce_<group>, since groups are global
    by file name) and the copy pins that instead."""

    def __init__(self, stack: Stack, aspect: str):
        self.stack = stack
        self.aspect = aspect
        self.base = RES / "assets" / MOD_ID / "bedrock" / "pokemon"
        self.done: dict[str, str] = {}
        self.vendored: list[tuple[str, str]] = []   # (kind, name) for the summary / credits
        # Cobblemon's Kotlin sources, when --cobblemon is a checkout's common/src/main/resources
        kotlin = stack.layers[0].path.parent / "kotlin"
        self.kotlin = kotlin if kotlin.is_dir() else None

    def wipe(self):
        for kind in ("models", "posers", "animations"):
            d = self.base / kind / self.aspect
            if d.exists():
                shutil.rmtree(d)

    def _write(self, kind: str, filename: str, data: bytes):
        dest = self.base / kind / self.aspect / filename
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)

    def model(self, model_id: str | None) -> str | None:
        if not model_id or model_id in self.done:
            return self.done.get(model_id, model_id)
        ns, name = model_id.split(":", 1)
        entries = self.stack.models.get((ns, name))
        new = model_id
        if self.stack.overwritten(entries):
            layer, rel = self.stack.model(model_id)
            self._write("models", f"{name}.json", layer.read(rel))
            new = f"{MOD_ID}:{name}"
            self.vendored.append(("model", f"{model_id} ({layer.name})"))
        self.done[model_id] = new
        return new

    def poser(self, poser_id: str | None, model_id: str | None) -> str | None:
        """The poser goes with the model: vendored (with its overwritten animation groups) only when the model it
        animates was vendored. A mod that re-ships a poser for an unchanged model keeps its version."""
        if not poser_id or self.model(model_id) == model_id:
            return poser_id
        if poser_id in self.done:
            return self.done[poser_id]
        ns, name = poser_id.split(":", 1)
        new = poser_id
        hit = self.stack.poser(poser_id)
        text = source = None
        if hit is not None:
            layer, rel = hit
            text, source = layer.read(rel).decode("utf-8-sig"), layer.name
        elif ns == "cobblemon" and self.kotlin and (kt := find_model_class(self.kotlin, name)):
            # Cobblemon's poser is Kotlin code: write the equivalent JSON poser
            data, warnings = kotlin_convert(kt.read_text())
            for w in warnings:
                print(f"    ! {poser_id}: {w}")
            text, source = json.dumps(data, indent=2) + "\n", f"Cobblemon ({kt.name}, converted to JSON)"
        if text is None:
            print(f"    ! {model_id} was vendored but poser {poser_id} has no JSON or Kotlin source to vendor; left as is")
        else:
            groups = {g for g in poser_groups(text) if self.stack.overwritten(self.stack.anims.get(g))}
            renames = {g: f"ce_{g}" for g in groups}
            for g in sorted(groups):
                alayer, arel = self.stack.anim(g)
                data = alayer.json(arel)
                data["animations"] = {k.replace(f"animation.{g}.", f"animation.ce_{g}.", 1): v
                                      for k, v in data.get("animations", {}).items()}
                self._write("animations", f"ce_{g}.animation.json", (json.dumps(data, indent=1) + "\n").encode())
                self.vendored.append(("animations", f"{g} ({alayer.name})"))
            self._write("posers", f"{name}.json", rename_groups(text, renames).encode())
            new = f"{MOD_ID}:{name}"
            self.vendored.append(("poser", f"{poser_id} ({source})"))
        self.done[poser_id] = new
        return new


def mirror_variations(variations: list[dict], aspect: str, seed: int, skip: set[str],
                      retex: Retexturer, style, geometry: "Geometry | None" = None,
                      vendor: "Vendor | None" = None) -> list[dict]:
    """Mirror every variation (Cobblemon's and those of mods whose art may be adapted) with the collection aspect added.

    Cobblemon picks the last matching variation for each property, so copying the list in order, each with the
    aspect added, keeps its logic (shiny, gender, regional forms, megas, model swaps) while every texture is swapped
    for the collection's version. Model and poser are copied too (and so pinned): other mods' base replacements at
    a lower order can't put our texture on a model it wasn't painted for.
    """
    alpha_layers = [
        (set(v.get("aspects", [])) - {"alpha_eyes"}, layer["texture"], model_for(variations, i))
        for i, v in enumerate(variations) if "alpha_eyes" in v.get("aspects", [])
        for layer in v.get("layers", []) if isinstance(layer.get("texture"), str)
    ]
    out = []
    for index, v in enumerate(variations):
        model = model_for(variations, index)
        retex.hints = geometry.hints(model) if geometry else None
        aspects = list(v.get("aspects", []))
        if "alpha_eyes" in aspects or skip.intersection(aspects):
            continue
        if "texture" not in v and not v.get("layers") and "model" not in v and "poser" not in v:
            continue
        copy = {"aspects": aspects + [aspect]}
        if "condition" in v:
            copy["condition"] = v["condition"]
        if "poser" in v:
            copy["poser"] = vendor.poser(v["poser"], model) if vendor else v["poser"]
        if "model" in v:
            copy["model"] = vendor.model(v["model"]) if vendor else v["model"]
            if vendor and copy["model"] != v["model"] and "poser" not in v:
                # the model is vendored but its poser is inherited: pin the vendored poser too
                copy["poser"] = vendor.poser(resolved(variations, index, "poser"), model)
        layer_of = getattr(retex, "layer_of", None)
        other_mod = layer_of is not None and layer_of(v) != "cobblemon"
        eyes = eye_mask_for(set(aspects), model, alpha_layers, same_model_only=other_mod)
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


def resolved_state(pairs: list[tuple[dict, object]], aspects: set[str]) -> dict:
    """Everything Cobblemon would resolve for a Pokémon with exactly these aspects from the merged variations."""
    state, layers = {}, {}
    for v, _ in pairs:
        if set(v.get("aspects", [])) <= aspects:
            for prop in ("model", "poser", "texture"):
                if prop in v:
                    state[prop] = v[prop]
            for layer in v.get("layers") or []:
                layers[layer.get("name", "")] = layer
    state["layers"] = list(layers.values())
    return state


def passthrough_variations(pairs: list[tuple[dict, object]], mirrored_sets: set[frozenset], aspect: str,
                           skip: set[str], touched_layers: set[str]) -> list[dict]:
    """Forms added by mods whose art can't be adapted (a Lost Lore clone, an AllTheMons form...). Our texture can't
    fit their model and we may not recolour their texture, so the cosmetic steps aside: for each such aspect set a
    copy with our aspect restores exactly what the game shows without it."""
    out = []
    seen = set()
    for v, layer in pairs:
        aspects = frozenset(v.get("aspects", []))
        if layer.derivatives or aspects in mirrored_sets or aspects in seen or "alpha_eyes" in aspects or skip & aspects:
            continue
        seen.add(aspects)
        state = resolved_state(pairs, set(aspects))
        names = {l.get("name", "") for l in state["layers"]}
        copy = {"aspects": sorted(aspects) + [aspect], **{k: state[k] for k in ("model", "poser", "texture") if k in state}}
        layers = state["layers"] + [{"name": n, "enabled": False} for n in sorted(touched_layers - names)]
        if layers:
            copy["layers"] = layers
        out.append(copy)
    return sorted(out, key=lambda c: len(c["aspects"]))


# ---------------------------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------------------------

def painted_variations(cob: Cobblemon, name: str, aspect: str, seed: int, style, retex: Retexturer,
                       geometry: Geometry, skip: set[str]) -> tuple[list[dict], dict]:
    """A family member modelled only by a mod whose art can't be adapted: paint an original base on its model's UV
    layout (tools/painter.py) in its evolved form's Cobblemon colours, then style it. Their own layers are switched
    off (they belong to their texture); forms with another model get a passthrough."""
    spec = cob.stack.painted[name]
    pairs = cob.effective[name]
    base = next(v for v, _ in pairs if not v.get("aspects") and "model" in v)
    geo = cob.stack.geometry(base["model"], derivative_only=False)    # UV layout only: no texture of theirs is read
    retex.hints = geometry.from_geo(geo)
    their_layers = sorted({l.get("name", "") for v, _ in pairs for l in v.get("layers") or []})
    out = []
    for v, _ in pairs:
        aspects = set(v.get("aspects", []))
        if "alpha_eyes" in aspects or skip & aspects:
            continue
        state = resolved_state(pairs, aspects)
        if state.get("model") != base["model"]:
            continue                       # another model: passed through below
        key = next((k for k in sorted(spec["palette_from"], key=len, reverse=True) if not k or k in aspects), "")
        source = spec["palette_from"][key]
        shiny = "shiny" in aspects
        src_vars = cob.resolvers[source][1]
        # the source's plain (or shiny) texture; if a mod replaced its aspect-less base, its simplest form
        candidates = [sv for sv in src_vars if isinstance(sv.get("texture"), str) and ("shiny" in sv.get("aspects", [])) == shiny
                      and "alpha_eyes" not in sv.get("aspects", [])]
        src = min(candidates, key=lambda sv: len(sv.get("aspects", [])))["texture"]
        stem = "_".join([name] + ([key] if key else []) + (["shiny"] if shiny else []))
        tex_id = f"{MOD_ID}:textures/pokemon/painted/{name}/{stem}.png"
        if tex_id not in retex.virtual:
            img, eyes = paint_layout(geo, cob.stack.image(src)[0], seed + len(stem))
            retex.add_virtual(tex_id, img)
            retex.add_virtual(tex_id + "#eyes", eyes)
        copy = {"aspects": sorted(aspects) + [aspect], "texture": retex.supplier(tex_id, tex_id + "#eyes", seed, style)}
        layers = [{"name": n, "enabled": False} for n in their_layers]
        for spec_ in getattr(style, "EXTRA_LAYERS", []):
            tex = retex.extra(tex_id, tex_id + "#eyes", seed, style, spec_)
            layers.append({"name": f"{MOD_ID}_{spec_['name']}", "texture": tex, "emissive": spec_.get("emissive", False),
                           "translucent": spec_.get("translucent", True)} if tex else
                          {"name": f"{MOD_ID}_{spec_['name']}", "enabled": False})
        if layers:
            copy["layers"] = layers
        out.append(copy)
    touched = {l["name"] for c in out for l in c.get("layers", [])}
    out += passthrough_variations(pairs, {frozenset(c["aspects"][:-1]) for c in out}, aspect, skip, touched)
    first = lambda t: t["frames"][0] if isinstance(t, dict) else t
    entry = {"species": name, "folder": f"painted_{name}", "model": base["model"], "original": None,
             "retextured": first(out[0]["texture"]), "layers": [], "painted_from": spec["mod"]}
    return out, entry


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
        missing = [n for n in family if n not in cob.resolvers and n not in cob.stack.painted]
        if missing:
            raise SystemExit(f"{pick}: no adaptable model for {missing}. The whole line must be retexturable"
                             " (or, for a member modelled by a mod whose art can't be adapted, listed under 'painted'"
                             " in tools/compat/mods.json).")
        look = cfg.get("line_styles", {}).get(pick)
        painted = [n for n in family if n not in cob.resolvers]
        print(f"  {pick:12s} -> {', '.join(family)}" + (f"  [{look}]" if look else "")
              + (f"  (painted: {', '.join(painted)})" if painted else ""))
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
    vendor = Vendor(cob.stack, aspect)
    vendor.wipe()
    retex = Retexturer(cob.stack, aspect, out_tex_root)
    retex.layer_of = lambda v: cob.var_layer[id(v)].id
    geometry = Geometry(cob.stack)
    manifest = []
    first = lambda t: t["frames"][0] if isinstance(t, dict) else t
    stats = {"compat_forms": 0, "passthrough": 0}
    for name in ordered:
        seed = int(hashlib.sha256(f"{MOD_ID}:{aspect}:{name}".encode()).hexdigest()[:12], 16)
        style = style_of.get(name, default_style)
        if name not in cob.resolvers:
            variations, entry = painted_variations(cob, name, aspect, seed, style, retex, geometry, cob.cosmetic_aspects)
            write_json(out_res_root / entry["folder"] / f"{RESOLVER_ORDER}_{name}_{aspect}.json", {
                "species": f"cobblemon:{name}", "order": RESOLVER_ORDER, "variations": variations})
            manifest.append(entry)
            continue
        folder, variations = cob.resolvers[name]
        mirrored = mirror_variations(variations, aspect, seed, cob.cosmetic_aspects, retex, style, geometry, vendor)
        touched = {l.get("name", "") for c in mirrored for l in c.get("layers", [])}
        passthrough = passthrough_variations(cob.effective.get(name, []), {frozenset(v.get("aspects", [])) for v in variations},
                                             aspect, cob.cosmetic_aspects, touched)
        stats["passthrough"] += len(passthrough)
        write_json(out_res_root / folder / f"{RESOLVER_ORDER}_{name}_{aspect}.json", {
            "species": f"cobblemon:{name}",
            # Cobblemon sorts resolver files by "order" and the last matching variation wins,
            # so a high order keeps this collection's textures on top of every other variation.
            "order": RESOLVER_ORDER,
            "variations": mirrored + passthrough,
        })
        # preview manifest: the base form, plus every other-mod form with its own model (megas, gmax...)
        by_aspects = {frozenset(c["aspects"][:-1]): c for c in mirrored}
        # (a mod may replace the aspect-less base, e.g. Mega Showdown's Xerneas only has neutral/active modes)
        base = next((v for v in variations if not v.get("aspects") and "model" in v), next(v for v in variations if "model" in v))
        for i, v in enumerate(variations):
            aspects = frozenset(v.get("aspects", []))
            is_base = v is base
            layer = cob.var_layer[id(v)]
            if not is_base and not ("model" in v and layer.id != "cobblemon" and "shiny" not in aspects):
                continue
            if aspects not in by_aspects or "texture" not in by_aspects[aspects]:
                continue
            if not is_base:
                stats["compat_forms"] += 1
            new = by_aspects[aspects]
            state = resolved_state([(x, None) for x in variations[:i + 1]], set(aspects))
            layers = []
            vanilla_layers = {l.get("name", ""): l for l in state["layers"]}
            for nl in new.get("layers") or []:
                orig = vanilla_layers.get(nl.get("name", ""), {})
                if nl.get("enabled", True) and "texture" in nl or "texture" in orig:
                    layers.append({"original": first(orig["texture"]) if "texture" in orig else None,
                                   "retextured": first(nl["texture"]) if nl.get("enabled", True) and "texture" in nl else None,
                                   "emissive": bool(nl.get("emissive", orig.get("emissive")))})
            entry = {"species": name, "folder": folder, "model": state["model"],
                     "original": first(state["texture"]), "retextured": first(new["texture"]), "layers": layers}
            if not is_base:
                entry["form"] = "_".join(sorted(aspects))
                entry["mod"] = layer.name
            manifest.append(entry)
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
          + (f" (+ {len(addons)} addon line)" if addons else "")
          + f"; {stats['compat_forms']} other-mod forms retextured, {stats['passthrough']} passed through"
          + (f"; vendored: {', '.join(f'{k} {n}' for k, n in vendor.vendored)}" if vendor.vendored else "") + ".")


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
    # another mod in the stack must not already use one of our items as a cosmetic for one of our species
    for rel, layer in cob.stack.files(r"data/[^/]+/cosmetic_items/.+\.json").items():
        data = layer.json(rel)
        for entry in data.get("cosmeticItems", []):
            item = str(entry.get("consumedItem", ""))
            for name in data.get("pokemon", []):
                name = cob.species_id(name)
                if item in items and owner.get(name) == items[item]:
                    raise SystemExit(f"{layer.name} already uses {item} as a cosmetic for {name} ({rel})")


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
    ap.add_argument("--no-compat", action="store_true",
                    help="ignore tools/compat/mods.json (Cobblemon alone; output will differ from the release build)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="generate collections (all by default)")
    b.add_argument("collections", nargs="*")
    p = sub.add_parser("pick", help="randomly pick new evolutionary lines no collection uses yet")
    p.add_argument("--count", type=int, default=18)
    p.add_argument("--seed", required=True)
    args = ap.parse_args()
    cob = Cobblemon(args.cobblemon, not args.no_compat)
    if args.cmd == "build":
        cmd_build(cob, args.collections)
    else:
        cmd_pick(cob, args.count, args.seed)


if __name__ == "__main__":
    main()
