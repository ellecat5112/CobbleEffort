#!/usr/bin/env python3
"""
Writes CobbleEffort: Distortion's assets and data into common/src/main/resources (deterministic; rerun after changes):

  items      the Distortion Band and the Distortion Crystal: textures, item models, names
  slot       the "distortion_slot" accessory slot (Accessories reads slots, entity bindings, groups and slot tags
             from data), its icon, the band in its slot tag
  forms      Distorted forms for every DISTORTABLE Pokémon (incl. Origin and plate forms; not megas or Gigantamax):
             types turned into their weaknesses (TYPE_CHART); a "distorted" flag feature (aspect) for them
  looks      resolvers (order 9100) mirroring every variation Cobblemon and Mega Showdown give them, with "distorted"
             added and textures recoloured: every hue turned to its complement (orange -> blue), greys kept; parts
             where they fit (tools/parts/: one module per line, on the part kit)
  chart      data/cobbleeffort_distortion/distortion/type_chart.json, for the battle code

The Pokémon's models and textures come from Cobblemon (its jar: COBBLEMON_JAR) and Mega Showdown (CC BY-NC-SA 4.0,
../tools/compat/jars/mega_showdown-*.jar); the recoloured textures and part models are adaptations.

Usage: python3 tools/make_assets.py
"""
from __future__ import annotations

import colorsys
import copy
import glob
import io
import json
import math
import sys
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
# the distortable Pokémon (curated): the Distortion World's champion and the creation trio, then the Charmander line
# every starter's evolutionary line (Gen 1-9): water types distort into plant-inspired forms, grass types into natural
# disasters, fire types into sea life (looks and parts: tools/parts/<first stage>.py)
STARTER_LINES = [
    ["bulbasaur", "ivysaur", "venusaur"], ["charmander", "charmeleon", "charizard"], ["squirtle", "wartortle", "blastoise"],
    ["chikorita", "bayleef", "meganium"], ["cyndaquil", "quilava", "typhlosion"], ["totodile", "croconaw", "feraligatr"],
    ["treecko", "grovyle", "sceptile"], ["torchic", "combusken", "blaziken"], ["mudkip", "marshtomp", "swampert"],
    ["turtwig", "grotle", "torterra"], ["chimchar", "monferno", "infernape"], ["piplup", "prinplup", "empoleon"],
    ["snivy", "servine", "serperior"], ["tepig", "pignite", "emboar"], ["oshawott", "dewott", "samurott"],
    ["chespin", "quilladin", "chesnaught"], ["fennekin", "braixen", "delphox"], ["froakie", "frogadier", "greninja"],
    ["rowlet", "dartrix", "decidueye"], ["litten", "torracat", "incineroar"], ["popplio", "brionne", "primarina"],
    ["grookey", "thwackey", "rillaboom"], ["scorbunny", "raboot", "cinderace"], ["sobble", "drizzile", "inteleon"],
    ["sprigatito", "floragato", "meowscarada"], ["fuecoco", "crocalor", "skeledirge"], ["quaxly", "quaxwell", "quaquaval"],
]
STARTER_NUMS = [1, 4, 7, 152, 155, 158, 252, 255, 258, 387, 390, 393, 495, 498, 501, 650, 653, 656, 722, 725, 728,
                810, 813, 816, 906, 909, 912]
# the distortable Pokémon (curated): the Distortion World's champion and the creation trio, the Gen 1 legendary and
# mythical Pokémon, then every starter line
DISTORTABLE = {"giratina": "0487_giratina", "dialga": "0483_dialga", "palkia": "0484_palkia", "arceus": "0493_arceus",
               "articuno": "0144_articuno", "zapdos": "0145_zapdos", "moltres": "0146_moltres",
               "mewtwo": "0150_mewtwo", "mew": "0151_mew",
               "raikou": "0243_raikou", "entei": "0244_entei", "suicune": "0245_suicune",
               "lugia": "0249_lugia", "hooh": "0250_hooh", "celebi": "0251_celebi"}
# specialised distortions (the user's designs): these don't follow the chart; every form gets these types
TYPE_OVERRIDES = {"mew": ["normal", "fighting"], "mewtwo": ["normal", "fighting"]}
for _line, _num in zip(STARTER_LINES, STARTER_NUMS):
    for _i, _sp in enumerate(_line):
        DISTORTABLE[_sp] = f"{_num + _i:04d}_{_sp}"


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


def distortion_crystal_icon():
    """The one Distortion Crystal: a rhombus whose halves are complementary (violet over gold), split by a dark
    swirl of distortion, so it reads as 'inversion'."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    cx, cy = 7.5, 7.5
    top, bottom = (150, 90, 220), (240, 190, 60)
    for y in range(16):
        for x in range(16):
            d = abs(x - cx) / 5.2 + abs(y - cy) / 7.4
            if d > 1.0:
                continue
            split = (y - cy) + (x - cx) * 0.45                    # a slanted line between the two halves
            col = top if split < 0 else bottom
            if d > 0.86:
                c = shade(col, 0.45)
            else:
                c = shade(col, 1.25 - 0.35 * ((x - 3) + (y - 2)) / 20)
                if abs(split) < 0.9:
                    c = (40, 20, 50)                              # the rift between them
                elif x < cx and y < cy and (x + y) % 5 == 0:
                    c = shade(col, 1.55)
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
    save_png(tex / "distortion_crystal.png", distortion_crystal_icon())
    write_json(mdl / "distortion_crystal.json",
               {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/distortion_crystal"}})
    # the mod's icon: the band over a fan of crystals
    icon = Image.new("RGBA", (64, 64), (24, 16, 34, 255))
    icon.alpha_composite(distortion_crystal_icon().resize((32, 32), Image.NEAREST), (16, 0))
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


def cobblemon_jar():
    """Cobblemon's jar (COBBLEMON_JAR, or one found next to the repository or in a scratch dist_deps folder)."""
    import os
    jars = ([os.environ["COBBLEMON_JAR"]] if os.environ.get("COBBLEMON_JAR") else []) + \
        sorted(glob.glob(str(REPO.parent / "**" / "Cobblemon-fabric-1.8.4*.jar"), recursive=True)) + \
        sorted(glob.glob("/tmp/claude-0/**/dist_deps/Cobblemon-fabric-1.8.4*.jar", recursive=True))
    if not jars:
        raise SystemExit("Cobblemon 1.8.4's jar is missing (set COBBLEMON_JAR)")
    return zipfile.ZipFile(jars[0])


def cobblemon_species(sp):
    """Cobblemon's species data."""
    z = cobblemon_jar()
    for n in z.namelist():
        if n.startswith("data/cobblemon/species/") and n.endswith(f"/{sp}.json"):
            return json.loads(z.read(n))
    raise SystemExit(f"no Cobblemon species data for {sp}")


# distorting needs the Pokémon to hold the Distortion Crystal, so forms that need another held item can't distort:
# stone megas and primals. Everything else can (Gigantamax, Battle Bond's Ash-Greninja, a move-triggered mega).
ITEMLESS_MEGAS = {"rayquaza"}                                  # Dragon Ascent, no stone
SKIPPED_ASPECTS = {"mega", "mega_x", "mega_y", "primal"}


def skipped(sp, aspects):
    return bool(set(aspects) & SKIPPED_ASPECTS) and not (sp in ITEMLESS_MEGAS and "primal" not in aspects)


def invert(t):
    return TYPE_CHART[t]


def forms():
    feature = RES / "data" / MOD / "species_features" / "distorted.json"
    write_json(feature, {"keys": ["distorted"], "type": "flag", "isAspect": True, "default": False})
    write_json(RES / "data" / MOD / "species_feature_assignments" / "distorted.json",
               {"pokemon": list(DISTORTABLE), "features": ["distorted"]})
    for sp in DISTORTABLE:
        d = cobblemon_species(sp)
        new = []
        base = {"name": "Distorted", "primaryType": invert(d["primaryType"]), "aspects": ["distorted"],
                "battleOnly": False}
        if d.get("secondaryType"):
            base["secondaryType"] = invert(d["secondaryType"])
        if sp in TYPE_OVERRIDES:
            base["primaryType"], base["secondaryType"] = TYPE_OVERRIDES[sp]
        new.append(base)
        for f in d.get("forms", []):
            if skipped(sp, f.get("aspects", [])):
                continue
            g = copy.deepcopy(f)                                   # keep the form's stats, abilities, size
            g["name"] = f"{f['name']}-Distorted"
            g["primaryType"] = invert(f.get("primaryType", d["primaryType"]))
            sec = f.get("secondaryType", d.get("secondaryType") if "primaryType" not in f else None)
            if sec:
                g["secondaryType"] = invert(sec)
            else:
                g.pop("secondaryType", None)
            g["aspects"] = list(f.get("aspects", [])) + ["distorted"]
            g["battleOnly"] = bool(f.get("battleOnly"))           # Gigantamax/Ash stay battle forms
            if sp in TYPE_OVERRIDES:
                g["primaryType"], g["secondaryType"] = TYPE_OVERRIDES[sp]
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


def _hsv(rgb):
    mx, mn = rgb.max(-1), rgb.min(-1)
    d = mx - mn
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    h = np.where(mx == r, (g - b) / np.maximum(d, 1e-9), np.where(mx == g, 2 + (b - r) / np.maximum(d, 1e-9), 4 + (r - g) / np.maximum(d, 1e-9)))
    h = np.where(d > 0, (h / 6.0) % 1.0, 0)
    s = np.where(mx > 0, d / np.maximum(mx, 1e-9), 0)
    return h, s, mx


def _rgb(h, s, v):
    i = np.floor(h * 6).astype(int) % 6
    f = h * 6 - np.floor(h * 6)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    out = np.zeros(h.shape + (3,))
    for k, (r, g, b) in enumerate([(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)]):
        m = i == k
        out[m] = np.stack([r[m], g[m], b[m]], -1)
    return out


def dominant_hue(img, near=None, within=50.0):
    """The hue most of the texture's colour is (weighted by saturation), in degrees; only hues within `within` of
    `near` count, if given (the old type's colour: Blastoise's skin, not its bigger brown shell)."""
    a = np.array(img.convert("RGBA")).astype(np.float64) / 255.0
    h, s, v = _hsv(a[..., :3])
    w = s * v * (a[..., 3] > 0) * (s > 0.15)
    if near is not None:
        w = w * (np.abs(((h * 360 - near) + 180) % 360 - 180) < within)
    hist, _ = np.histogram(h * 360, bins=36, range=(0, 360), weights=w)
    hist = hist + 0.5 * (np.roll(hist, 1) + np.roll(hist, -1))
    return float(np.argmax(hist) * 10 + 5)


def recolour_shift(img, dst, src=None, width=55.0, sat=1.0, val=1.0, near=None):
    """The type colour moved to the new type's: hues within `width` degrees of `src` (the texture's dominant hue unless
    given) turn towards `dst` (fading out at the edge of the range); other colours stay (Squirtle's shell stays brown)."""
    if src is None:
        src = dominant_hue(img, near)
    a = np.array(img.convert("RGBA")).astype(np.float64) / 255.0
    h, s, v = _hsv(a[..., :3])
    d = np.abs(((h * 360 - src) + 180) % 360 - 180)
    k = np.clip((width - d) / (width * 0.4), 0, 1) * (s > 0.08)
    shift = (((dst - src) + 180) % 360 - 180) / 360.0
    h2 = (h + shift * k) % 1.0
    s2 = np.clip(s * (1 + (sat - 1) * k), 0, 1)
    v2 = np.clip(v * (1 + (val - 1) * k), 0, 1)
    a[..., :3] = _rgb(h2, s2, v2)
    return Image.fromarray((a * 255).round().astype(np.uint8), "RGBA")


def looks():
    """Resolvers mirroring every variation the Pokémon has (Cobblemon's, with Mega Showdown's where it replaces or adds
    them), with "distorted" added and the textures recoloured. A line with a parts module (tools/parts/) gets its
    distorted models (a copy of each model it uses, with parts) and its recolour (the type colour moved to the new
    type's); the others keep the complement recolour and Cobblemon's models."""
    sys.path.insert(0, str(HERE / "parts"))
    import parts as partlib
    cz, mz = cobblemon_jar(), msd_jar()
    zips = [mz, cz]                                             # Mega Showdown's assets win over Cobblemon's
    names = {z: set(z.namelist()) for z in zips}

    def read(path):
        z = next(z for z in zips if path in names[z])
        return z.read(path)

    def geo_path(model_id):
        want = model_id.split(":", 1)[1] + ".json"
        for z in zips:
            for n in names[z]:
                if n.startswith("assets/cobblemon/bedrock/pokemon/models/") and n.endswith("/" + want):
                    return n
        raise SystemExit(f"no model {model_id}")

    for sp, folder in DISTORTABLE.items():
        module = partlib.module_for(sp)
        if module is not None and getattr(module, "ADDON", None):
            addon_look(sp, folder, module)
            continue
        prefix = f"assets/cobblemon/bedrock/pokemon/resolvers/{folder}/"
        paths = sorted({n for z in zips for n in names[z] if n.startswith(prefix) and n.endswith(".json")})
        resolvers = sorted(((json.loads(read(n)), n) for n in paths), key=lambda r: (r[0].get("order", 0), r[1]))
        variations = [v for d, _ in resolvers for v in d["variations"] if not skipped(sp, v.get("aspects", []))]
        base = next((v for v in variations if not v.get("aspects") and v.get("model")), None)
        base_model = base["model"] if base else None
        kits, done, frames_of = {}, {}, {}

        def kit_for(model_id):
            if module is None or model_id is None:
                return None
            if model_id not in kits:
                geo = json.loads(read(geo_path(model_id)))
                kit = partlib.Kit(sp, model_id.split(":", 1)[1].removesuffix(".geo"), geo)
                try:
                    module.build(kit)
                except KeyError:                                # a model the line's parts don't fit (Gigantamax...)
                    kit = partlib.Kit(sp, model_id.split(":", 1)[1].removesuffix(".geo"), geo)
                    kit.used = True                             # recoloured, on its own model
                if kit.used and kit.geo_changed:
                    name = kit.model + "_distorted"
                    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "models" / folder / f"{name}.geo.json",
                               kit.finish_geo(f"geometry.{name}"))
                    kit.id = f"{MOD}:{name}.geo"
                elif kit.used:
                    kit.id = model_id                           # only repainted: Cobblemon's own model
                kits[model_id] = kit if kit.used else None
            return kits[model_id]

        def dst_for(p, tag):
            stem = p.rsplit("/", 1)[1][:-4]
            return p.rsplit("/", 1)[0].replace(f"textures/pokemon/{folder}", f"textures/pokemon/{folder}") + f"/distorted_{stem}{tag}.png"

        def recolour_for(img, shiny):
            rc = getattr(module, "RECOLOUR", None) if module else None
            if rc == "keep":
                return img.convert("RGBA")                      # a specialised distortion keeps its colours
            if rc == "negative":                                # a photographic negative (Lugia: white turns black)
                a = np.array(img.convert("RGBA"))
                a[..., :3] = 255 - a[..., :3]
                return Image.fromarray(a, "RGBA")
            if not rc:
                return recolour(img)
            dst = rc.get("dst_shiny", rc["dst"] + 35) if shiny else rc["dst"]
            old = cobblemon_species(sp)["primaryType"]
            near = colorsys.rgb_to_hsv(*(c / 255 for c in TYPE_COLOUR[old]))[0] * 360
            return recolour_shift(img, dst, rc.get("src_shiny" if shiny else "src"), rc.get("width", 55), rc.get("sat", 1.0),
                                  rc.get("val", 1.0), near=rc.get("near", near))

        def body(path, kit, src_layers):
            key = (path, id(kit))
            if key not in done:
                ns, p = path.split(":", 1)
                shiny = "shiny" in p
                img = recolour_for(Image.open(io.BytesIO(read(f"assets/{ns}/{p}"))), shiny)
                tag = "" if kit is None or kit.model == sp else f"_{kit.model}"
                dst = dst_for(p, tag)
                fr = {}
                if kit:
                    img, frames = kit.paint(img, shiny, src_layers)
                    for lname, ims in frames.items():
                        fr[lname] = []
                        for i, im in enumerate(ims):
                            fdst = dst_for(p, f"{tag}_{lname}{i}")
                            save_png(RES / "assets" / MOD / fdst, im)
                            fr[lname].append(f"{MOD}:{fdst}")
                save_png(RES / "assets" / MOD / dst, img)
                done[key] = (f"{MOD}:{dst}", fr)
            return done[key]

        def layer_tex(t, kit):
            def one(path):
                key = (path, id(kit), "layer")
                if key not in done:
                    ns, p = path.split(":", 1)
                    img = recolour_for(Image.open(io.BytesIO(read(f"assets/{ns}/{p}"))), "shiny" in p)
                    if module is not None and getattr(module, "GLOW_DST", None) is not None and "alpha" not in p:
                        img = recolour_shift(img, module.GLOW_DST, width=180)   # the glow's colours, all turned
                    if kit:
                        img = pad(img, kit.height_factor(), kit.TW)
                    dst = dst_for(p, "" if kit is None or kit.model == sp else f"_{kit.model}")
                    save_png(RES / "assets" / MOD / dst, img)
                    done[key] = f"{MOD}:{dst}"
                return done[key]
            if isinstance(t, str):
                return one(t)
            if isinstance(t, dict) and "frames" in t:
                return dict(t, frames=[one(f) for f in t["frames"]])
            return t

        def src_layers_of(v):
            out = {}
            for lay in v.get("layers", []) or []:
                t = lay.get("texture")
                t = t["frames"][0] if isinstance(t, dict) and t.get("frames") else t
                if isinstance(t, str):
                    ns, p = t.split(":", 1)
                    out[lay.get("name")] = Image.open(io.BytesIO(read(f"assets/{ns}/{p}"))).convert("RGBA")
            return out

        unify_on = module is not None and getattr(module, "UNIFY", False)

        def inherited(v, key, skip_swaps=False):
            """What Cobblemon would use for v's aspects: the last variation (with key) whose aspects are all v's."""
            best = None
            for u in variations:
                if set(u.get("aspects", [])) <= set(v.get("aspects", [])) and key in u:
                    if skip_swaps and u.get("model") and u.get("aspects"):
                        continue
                    best = u
            return best

        out = []
        for v in variations:
            aspects = list(v.get("aspects", []))
            swap = bool(v.get("model") and aspects)
            if unify_on and swap and not isinstance(v.get("texture"), str) and "layers" not in v:
                continue                                        # a tree variant with only a model: the base parts cover it
            mv = inherited(v, "model", skip_swaps=unify_on)
            eff = mv["model"] if mv else base_model
            kit = kit_for(eff)
            tv = inherited(v, "texture", skip_swaps=unify_on)
            lv = inherited(v, "layers", skip_swaps=unify_on)
            w = {"aspects": aspects + ["distorted"]}
            if kit and ("model" in v or not aspects or "texture" in v):
                w["model"] = kit.id
            elif module is not None and swap and not unify_on:
                w["model"] = v["model"]                         # a model swap (female, Hisuian): pinned
                if v.get("poser"):
                    w["poser"] = v["poser"]
            fr = {}
            if tv and isinstance(tv.get("texture"), str) and (("texture" in v and not (unify_on and swap)) or (kit and "model" in w)):
                tex_id, fr = body(tv["texture"], kit, src_layers_of(lv) if lv else {})
                w["texture"] = tex_id
            elif kit and tv and isinstance(tv.get("texture"), str):
                _, fr = body(tv["texture"], kit, src_layers_of(lv) if lv else {})
            if "layers" in v or (kit and kit.layers and ("texture" in w or not aspects)):
                lays = [dict(lay, texture=layer_tex(lay.get("texture"), kit)) for lay in ((lv or {}).get("layers") or [])
                        if not (kit and lay.get("name") in kit.drop_layers)]
                if kit:
                    for lname, cfg in kit.layers.items():
                        if fr.get(lname):
                            lays.append({"name": f"cobbleeffort_{lname}", "emissive": cfg["emissive"], "translucent": cfg["translucent"],
                                         "texture": {"fps": cfg["fps"], "frames": fr[lname], "loop": True}})
                w["layers"] = lays
            if len(w) > 1:
                out.append(w)
        write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "resolvers" / folder / f"9100_{sp}_distorted.json",
                   {"species": f"cobblemon:{sp}", "order": 9100, "variations": out})
        n_kits = len({k for k in kits.values() if k})
        print(f"{sp}: {len(out)} variations, {len(done)} textures" + (f", {n_kits} distorted model(s)" if n_kits else ""))


def addon_look(sp, folder, module):
    """A Pokémon modelled only by another mod whose art can't be adapted (no-derivatives): an original texture painted
    onto that model's UV layout (extracted with tools/addons/extract_layout.py, no art read), set by texture alone, so
    the resolver names no model (it's launch-safe without that mod; with it, the distorted look shows)."""
    layout = json.loads((HERE / "parts" / module.ADDON["layout"]).read_text())
    out = []
    for shiny in (False, True):
        body, glow = module.paint(layout, shiny)
        stem = f"textures/pokemon/{folder}/distorted_{sp}{'_shiny' if shiny else ''}"
        save_png(RES / "assets" / MOD / f"{stem}.png", body)
        w = {"aspects": (["shiny"] if shiny else []) + ["distorted"], "texture": f"{MOD}:{stem}.png"}
        if glow is not None:
            save_png(RES / "assets" / MOD / f"{stem}_glow.png", glow)
            w["layers"] = [{"name": "cobbleeffort_glow", "emissive": True, "texture": f"{MOD}:{stem}_glow.png"}]
        out.append(w)
    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "resolvers" / folder / f"9100_{sp}_distorted.json",
               {"species": f"cobblemon:{sp}", "order": 9100, "variations": out})
    print(f"{sp}: {len(out)} variations, painted on {module.ADDON['source']}'s UV layout")


def pad(img, factor, width=None):
    img = img.convert("RGBA")
    out = Image.new("RGBA", (width or img.width, img.height * factor), (0, 0, 0, 0))
    out.paste(img, (0, 0))
    return out


def distort_button():
    """The Distort battle button (36x34, normal over hovered/toggled), drawn like Cobblemon's gimmick buttons: a round
    badge with the crystal's split violet/gold and a rift through it."""
    img = Image.new("RGBA", (36, 68), (0, 0, 0, 0))
    px = img.load()
    for state in (0, 1):
        oy = state * 34
        glow = 1.25 if state else 1.0
        for y in range(34):
            for x in range(36):
                r = math.hypot(x - 17.5, y - 16.5)
                if r > 15.5:
                    continue
                if r > 13.5:
                    c = (250, 230, 140) if state else (60, 40, 80)       # rim, lit when toggled
                else:
                    split = (y - 16.5) + (x - 17.5) * 0.45
                    c = shade((150, 90, 220) if split < 0 else (240, 190, 60), glow * (1.1 - r / 40))
                    if abs(split) < 1.4:
                        c = (30, 15, 40)
                px[x, oy + y] = c + (255,)
    save_png(RES / "assets" / MOD / "textures" / "gui" / "battle" / "distort_button.png", img)


def wheel_icons():
    """The interaction-wheel icons (32x32, white on clear with half-alpha detail, like Cobblemon's):
    distort: the crystal's rhombus split by a slanted rift, one half solid, the other half hollow (inverted);
    revert: the same rhombus whole, outlined, with the rift closed."""
    for name, split_open in (("distort_wheel", True), ("revert_wheel", False)):
        img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        px = img.load()
        cx, cy = 15.5, 15.5
        for y in range(32):
            for x in range(32):
                d = abs(x - cx) / 11.0 + abs(y - cy) / 15.0
                if d > 1.0:
                    continue
                edge = d > 0.82
                if not split_open:
                    a = 255 if edge else (128 if abs((y - cy) + (x - cx) * 0.5) < 1.2 else 0)
                else:
                    split = (y - cy) + (x - cx) * 0.5
                    if abs(split) < 1.6:
                        continue                                  # the rift
                    a = 255 if split < 0 or edge else (128 if (x + y) % 4 == 0 else 0)
                if a:
                    px[x, y] = (255, 255, 255, a)
        save_png(RES / "assets" / MOD / "textures" / "gui" / "interact" / f"{name}.png", img)


def chart():
    write_json(RES / "data" / MOD / "distortion" / "type_chart.json", TYPE_CHART)


def lang():
    names = {f"item.{MOD}.distortion_band": "Distortion Band",
             f"item.{MOD}.distortion_band.tooltip": "Wear it in the Distortion slot to let a Pokémon holding the Distortion Crystal distort, in battle or from its interaction wheel.",
             f"itemGroup.{MOD}": "Distortion"}
    names[f"item.{MOD}.distortion_crystal"] = "Distortion Crystal"
    names["slot.accessories.distortion_slot"] = "Distortion"
    names[f"accessories.group.{MOD}.distortion_group"] = "Distortion"
    names[f"{MOD}.ui.distort"] = "Distort"
    names[f"{MOD}.ui.revert"] = "Revert Distortion"
    names[f"{MOD}.message.distorted"] = "%s distorted!"
    names[f"{MOD}.message.reverted"] = "%s returned to normal."
    names[f"{MOD}.message.in_battle"] = "You can't distort or revert a Pokémon while battling."
    names[f"{MOD}.message.need_band"] = "Wear the Distortion Band to distort a Pokémon."
    names[f"{MOD}.message.one_at_a_time"] = "Only one Pokémon can be distorted at a time: revert %s first."
    path = RES / "assets" / MOD / "lang" / "en_us.json"
    old = json.loads(path.read_text()) if path.exists() else {}
    names.update({k: v for k, v in old.items() if k.startswith("cobblemon.")})   # make_battle.py's move and ability names
    write_json(path, dict(sorted(names.items())))


def main():
    items()
    slot()
    forms()
    looks()
    distort_button()
    wheel_icons()
    chart()
    lang()


if __name__ == "__main__":
    main()
