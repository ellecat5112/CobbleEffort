#!/usr/bin/env python3
"""
Writes CobbleEffort: Distortion's assets and data into common/src/main/resources (deterministic; rerun after changes):

  items      the Distortion Band and 18 Distortion Crystals: textures, item models, names
  slot       the "distortion_slot" accessory slot (Accessories reads slots, entity bindings, groups and slot tags
             from data), its icon, the band in its slot tag
  forms      Distorted forms for the first set (Giratina, Dialga, Palkia, Arceus, incl. Origin and plate forms):
             types turned into their weaknesses (TYPE_CHART); a "distorted" flag feature (aspect) for them
  looks      resolvers (order 9100) mirroring every variation Mega Showdown gives them, with "distorted" added and
             textures recoloured: every hue turned to its complement (orange -> blue), greys kept
  chart      data/cobbleeffort_distortion/distortion/type_chart.json, for the battle code

The Pokémon's models and textures come from Mega Showdown (CC BY-NC-SA 4.0), read from
../tools/compat/jars/mega_showdown-*.jar; the recoloured textures are adaptations under the same licence.

Usage: python3 tools/make_assets.py
"""
from __future__ import annotations

import colorsys
import copy
import glob
import io
import json
import math
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parent
RES = ROOT / "common" / "src" / "main" / "resources"
MOD = "cobbleeffort_distortion"

TYPES = ["normal", "fire", "water", "grass", "electric", "ice", "fighting", "poison", "ground", "flying", "psychic",
         "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"]
# each type becomes one of its weaknesses (the user's choice: "becomes its weakness")
TYPE_CHART = {"normal": "fighting", "fire": "water", "water": "grass", "grass": "fire", "electric": "ground",
              "ice": "fire", "fighting": "psychic", "poison": "ground", "ground": "water", "flying": "electric",
              "psychic": "dark", "bug": "flying", "rock": "fighting", "ghost": "dark", "dragon": "fairy",
              "dark": "fairy", "steel": "ground", "fairy": "steel"}
TYPE_COLOUR = {"normal": (168, 167, 122), "fire": (238, 129, 48), "water": (99, 144, 240), "grass": (122, 199, 76),
               "electric": (247, 208, 44), "ice": (150, 217, 214), "fighting": (194, 46, 40), "poison": (163, 62, 161),
               "ground": (226, 191, 101), "flying": (169, 143, 243), "psychic": (249, 85, 135), "bug": (166, 185, 26),
               "rock": (182, 161, 54), "ghost": (115, 87, 151), "dragon": (111, 53, 252), "dark": (112, 87, 70),
               "steel": (183, 183, 206), "fairy": (214, 133, 173)}
FIRST_SET = {"giratina": "0487_giratina", "dialga": "0483_dialga", "palkia": "0484_palkia", "arceus": "0493_arceus"}


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def save_png(path: Path, img: Image.Image):
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, optimize=True)


def shade(c, f):
    return tuple(max(0, min(255, int(round(v * f)))) for v in c[:3])


# --- items -----------------------------------------------------------------------------------------------------------

def crystal_icon(type_):
    """A 16x16 crystal: a tall rhombus in the type's colour, lit from the top left, a dark swirl of distortion inside."""
    col = TYPE_COLOUR[type_]
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    cx, cy = 7.5, 7.5
    for y in range(16):
        for x in range(16):
            d = abs(x - cx) / 5.2 + abs(y - cy) / 7.4
            if d > 1.0:
                continue
            if d > 0.86:
                c = shade(col, 0.45)                                  # outline
            else:
                light = 1.25 - 0.35 * ((x - 3) + (y - 2)) / 20           # lit from the top left
                c = shade(col, light)
                if x < cx and y < cy and (x + y) % 5 == 0:
                    c = shade(col, 1.55)                              # facet glints
                r = math.hypot(x - cx, (y - cy) * 0.75)
                ang = math.atan2(y - cy, x - cx)
                if r < 3.2 and int((ang * 2 + r * 1.3) * 1.2) % 3 == 0:
                    c = (40, 20, 50)                                  # the distortion swirl
            px[x, y] = c + (255,)
    for (x, y) in ((5, 4), (5, 5), (6, 3)):
        px[x, y] = (255, 255, 255, 255)
    return img


def band_icon():
    """A 16x16 band: a black-and-purple wrist band with gold trim and a red-gold griseous gem."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for y in range(16):
        for x in range(16):
            r = math.hypot((x - 7.5) / 7.2, (y - 7.5) / 5.6)
            if 0.62 <= r <= 1.0:
                c = (46, 30, 64) if r > 0.72 else (98, 60, 130)
                if 0.94 < r <= 1.0 or 0.62 <= r < 0.66:
                    c = (214, 170, 60)                                # gold trim
                px[x, y] = c + (255,)
    for y in range(5, 11):
        for x in range(5, 11):
            d = abs(x - 7.5) + abs(y - 7.5)
            if d <= 3.2:
                c = (200, 40, 50) if d > 1.4 else (250, 210, 90)
                if d > 2.6:
                    c = (110, 20, 30)
                px[x, y] = c + (255,)
    px[6, 6] = (255, 255, 255, 255)
    return img


def items():
    tex = RES / "assets" / MOD / "textures" / "item"
    mdl = RES / "assets" / MOD / "models" / "item"
    save_png(tex / "distortion_band.png", band_icon())
    write_json(mdl / "distortion_band.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/distortion_band"}})
    for t in TYPES:
        save_png(tex / f"{t}_distortion_crystal.png", crystal_icon(t))
        write_json(mdl / f"{t}_distortion_crystal.json",
                   {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/{t}_distortion_crystal"}})
    # the mod's icon: the band over a fan of crystals
    icon = Image.new("RGBA", (64, 64), (24, 16, 34, 255))
    for n, t in enumerate(("ghost", "dragon", "dark", "fairy", "steel", "water")):
        c = crystal_icon(t).resize((28, 28), Image.NEAREST)
        icon.alpha_composite(c, (2 + n * 6, 4 + (n % 2) * 4))
    icon.alpha_composite(band_icon().resize((40, 40), Image.NEAREST), (12, 20))
    save_png(RES / "assets" / MOD / "icon.png", icon)


# --- accessory slot --------------------------------------------------------------------------------------------------

def slot():
    data = RES / "data" / MOD / "accessories"
    write_json(data / "slot" / "distortion_slot.json",
               {"replace": False, "amount": 1, "operation": "set", "order": 2, "icon": f"{MOD}:gui/slot/distortion_slot"})
    write_json(data / "entity" / "entities.json", {"replace": False, "entities": ["minecraft:player"], "slots": ["distortion_slot"]})
    write_json(data / "group" / "distortion_group.json",
               {"replace": False, "order": 2, "slots": ["distortion_slot"], "icon": f"{MOD}:gui/group/distortion"})
    write_json(RES / "data" / "accessories" / "tags" / "item" / "distortion_slot.json",
               {"replace": False, "values": [f"{MOD}:distortion_band"]})
    # icons: a faint band outline (slot), the band (group)
    outline = band_icon().convert("RGBA")
    a = np.array(outline)
    a[..., :3] = 120
    a[..., 3] = (a[..., 3] > 0) * 110
    save_png(RES / "assets" / MOD / "textures" / "gui" / "slot" / "distortion_slot.png", Image.fromarray(a))
    save_png(RES / "assets" / MOD / "textures" / "gui" / "group" / "distortion.png", band_icon())


# --- forms and looks ----------------------------------------------------------------------------------------------

def msd_jar():
    jars = sorted(glob.glob(str(REPO / "tools" / "compat" / "jars" / "mega_showdown-*.jar")))
    if not jars:
        raise SystemExit("Mega Showdown's jar is missing from tools/compat/jars/")
    return zipfile.ZipFile(jars[-1])


def cobblemon_species(sp):
    """Cobblemon's species data (from the jar tools/compat lists, or the reference checkout)."""
    for j in sorted(glob.glob(str(REPO.parent / "**" / "Cobblemon-fabric-1.8.4*.jar"), recursive=True)) + \
            sorted(glob.glob("/tmp/claude-0/**/dist_deps/Cobblemon-fabric-1.8.4*.jar", recursive=True)):
        z = zipfile.ZipFile(j)
        for n in z.namelist():
            if n.startswith("data/cobblemon/species/") and n.endswith(f"/{sp}.json"):
                return json.loads(z.read(n))
    raise SystemExit(f"no Cobblemon species data for {sp}")


def invert(t):
    return TYPE_CHART[t]


def forms():
    feature = RES / "data" / MOD / "species_features" / "distorted.json"
    write_json(feature, {"keys": ["distorted"], "type": "flag", "isAspect": True, "default": False})
    write_json(RES / "data" / MOD / "species_feature_assignments" / "distorted.json",
               {"pokemon": list(FIRST_SET), "features": ["distorted"]})
    for sp in FIRST_SET:
        d = cobblemon_species(sp)
        new = []
        base = {"name": "Distorted", "primaryType": invert(d["primaryType"]), "aspects": ["distorted"],
                "battleOnly": False}
        if d.get("secondaryType"):
            base["secondaryType"] = invert(d["secondaryType"])
        new.append(base)
        for f in d.get("forms", []):
            g = copy.deepcopy(f)                                   # keep the form's stats, abilities, size
            g["name"] = f"{f['name']}-Distorted"
            g["primaryType"] = invert(f.get("primaryType", d["primaryType"]))
            sec = f.get("secondaryType", d.get("secondaryType") if "primaryType" not in f else None)
            if sec:
                g["secondaryType"] = invert(sec)
            else:
                g.pop("secondaryType", None)
            g["aspects"] = list(f.get("aspects", [])) + ["distorted"]
            g["battleOnly"] = False
            for k in ("evolutions", "preEvolution", "drops", "moves"):
                g.pop(k, None)
            new.append(g)
        write_json(RES / "data" / MOD / "species_additions" / f"{sp}_distorted.json", {"target": f"cobblemon:{sp}", "forms": new})


def recolour(img: Image.Image) -> Image.Image:
    """Every hue to its complement (orange -> blue, red -> cyan, gold -> blue-violet); greys and blacks stay."""
    a = np.array(img.convert("RGBA")).astype(np.float64) / 255.0
    rgb = a[..., :3]
    mx, mn = rgb.max(-1), rgb.min(-1)
    l = (mx + mn) / 2
    d = mx - mn
    s = np.where(d == 0, 0, d / np.maximum(1e-9, 1 - np.abs(2 * l - 1)))
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    h = np.zeros_like(l)
    nz = d > 0
    rc = np.where(nz, (mx - r) / np.maximum(d, 1e-9), 0)
    gc = np.where(nz, (mx - g) / np.maximum(d, 1e-9), 0)
    bc = np.where(nz, (mx - b) / np.maximum(d, 1e-9), 0)
    h = np.where(mx == r, bc - gc, np.where(mx == g, 2 + rc - bc, 4 + gc - rc))
    h = np.where(nz, (h / 6.0) % 1.0, 0)
    h = np.where(s > 0.08, (h + 0.5) % 1.0, h)                    # the complement, only where there's colour
    c = (1 - np.abs(2 * l - 1)) * s
    hp = h * 6
    x = c * (1 - np.abs(hp % 2 - 1))
    z = np.zeros_like(c)
    sel = [(hp < 1), (hp < 2), (hp < 3), (hp < 4), (hp < 5), (hp >= 5)]
    out = np.zeros_like(rgb)
    choices = [(c, x, z), (x, c, z), (z, c, x), (z, x, c), (x, z, c), (c, z, x)]
    done = np.zeros(l.shape, bool)
    for m, (rr, gg, bb) in zip(sel, choices):
        m = m & ~done
        out[m] = np.stack([rr[m], gg[m], bb[m]], -1)
        done |= m
    out += (l - c / 2)[..., None]
    a[..., :3] = np.clip(out, 0, 1)
    return Image.fromarray((a * 255).round().astype(np.uint8), "RGBA")


def looks():
    z = msd_jar()
    names = z.namelist()
    for sp, folder in FIRST_SET.items():
        resolvers = sorted(n for n in names if n.startswith(f"assets/cobblemon/bedrock/pokemon/resolvers/{folder}/") and n.endswith(".json"))
        out = []
        done_tex = {}

        def tex(path):
            if path not in done_tex:
                ns, p = path.split(":", 1)
                src = f"assets/{ns}/{p}"
                img = Image.open(io.BytesIO(z.read(src)))
                dst = p.replace(f"textures/pokemon/{folder}/", f"textures/pokemon/{folder}/distorted_")
                save_png(RES / "assets" / MOD / dst, recolour(img))
                done_tex[path] = f"{MOD}:{dst}"
            return done_tex[path]

        for n in resolvers:
            d = json.loads(z.read(n))
            for v in d["variations"]:
                w = {"aspects": list(v.get("aspects", [])) + ["distorted"]}
                if isinstance(v.get("texture"), str):
                    w["texture"] = tex(v["texture"])
                if "layers" in v:
                    layers = []
                    for lay in v["layers"]:
                        lay = dict(lay)
                        if isinstance(lay.get("texture"), str):
                            lay["texture"] = tex(lay["texture"])
                        layers.append(lay)
                    w["layers"] = layers
                out.append(w)
        write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "resolvers" / folder / f"9100_{sp}_distorted.json",
                   {"species": f"cobblemon:{sp}", "order": 9100, "variations": out})
        print(f"{sp}: {len(out)} variations, {len(done_tex)} textures recoloured")


def chart():
    write_json(RES / "data" / MOD / "distortion" / "type_chart.json", TYPE_CHART)


def lang():
    names = {f"item.{MOD}.distortion_band": "Distortion Band",
             f"item.{MOD}.distortion_band.tooltip": "Wear it in the Distortion slot to let a Pokémon holding the Distortion Crystal of its type distort in battle.",
             f"itemGroup.{MOD}": "Distortion"}
    for t in TYPES:
        names[f"item.{MOD}.{t}_distortion_crystal"] = f"{t.title()} Distortion Crystal"
    names["slot.accessories.distortion_slot"] = "Distortion"
    names[f"accessories.group.{MOD}.distortion_group"] = "Distortion"
    write_json(RES / "assets" / MOD / "lang" / "en_us.json", dict(sorted(names.items())))


def main():
    items()
    slot()
    forms()
    looks()
    chart()
    lang()


if __name__ == "__main__":
    main()
