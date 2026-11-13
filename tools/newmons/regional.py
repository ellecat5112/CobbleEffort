"""CobbleEffort regional forms: existing Pokémon lines with a form of our own (like Cobblemon's Alolan or Galarian
forms), on Cobblemon's own models with new textures, types, abilities, moves and Pokédex entries.

usage: python3 tools/newmons/regional.py --cobblemon <cobblemon>/common/src/main/resources

The aspect is "cobbleeffortian" (a flag species feature, so "caterpie cobbleeffortian" works in spawns, commands and
evolution results), the form is called "CobbleEffort". Writes:
  data/cobbleeffort/species_features/cobbleeffortian.json + species_feature_assignments/cobbleeffortian.json
  data/cobbleeffort/species_additions/<species>_cobbleeffortian.json      the form (appended to the species' forms)
  data/cobbleeffort/spawn_pool_world/regional_<line>.json                   wild spawns of the form
  assets/cobbleeffort/bedrock/pokemon/resolvers/regional/<species>.json    texture swap, order 5 (model from below)
  assets/cobbleeffort/textures/pokemon/regional/<species>/...             recoloured from Cobblemon's textures
  assets/cobbleeffort/lang/en_us.json (merged)                             Pokédex entries
  tools/readme/_new_<species>_cobbleeffortian.json                          player guide entries
  tools/preview/manifest_regional.json                                      preview manifest

Lines so far: Caterpie, Metapod, Butterfree (Bug/Poison; after the CobbleEffort Caterpie art by @MerphISC, the user's
idea: purple, poisonous, vibrant warning colours like real toxic caterpillars).
"""
from __future__ import annotations

import argparse
import colorsys
import json
import random
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
RES = TOOLS.parent / "src" / "main" / "resources"
MOD = "cobbleeffort"
ASPECT = "cobbleeffortian"
FORM = "CobbleEffort"


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


# ---- textures ----------------------------------------------------------------------------------------------------------

def hsv_img(a):
    rgb = a[..., :3].astype(np.float64) / 255
    mx, mn = rgb.max(-1), rgb.min(-1)
    v = mx
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-9), 0)
    d = np.maximum(mx - mn, 1e-9)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) / 6
    h = np.where(mx == mn, 0, h)
    return h * 360, s, v


def from_hsv(h, s, v):
    out = np.zeros(h.shape + (3,))
    for idx in np.ndindex(h.shape):
        out[idx] = colorsys.hsv_to_rgb((h[idx] / 360) % 1, min(1, max(0, s[idx])), min(1, max(0, v[idx])))
    return (out * 255).round().astype(np.uint8)


def recolour(a, rules):
    """rules: list of (mask function(h, s, v) -> bool array, (hue, sat_mul, val_mul)); the first match wins."""
    h, s, v = hsv_img(a)
    nh, ns, nv = h.copy(), s.copy(), v.copy()
    done = np.zeros(h.shape, bool) | (a[..., 3] == 0)
    for test, (hue, sm, vm) in rules:
        m = test(h, s, v) & ~done
        nh[m] = hue
        ns[m] = s[m] * sm if sm > 0 else -sm
        nv[m] = v[m] * vm
        done |= m
    out = a.copy()
    out[..., :3] = from_hsv(nh, ns, nv)
    return out


def spots(a, mask, colour, seed, density, size=2, rim=None):
    """Warning spots: size x size blobs of `colour` on texels where mask is true, a little apart."""
    rnd = random.Random(seed)
    ys, xs = np.nonzero(mask)
    taken = np.zeros(mask.shape, bool)
    n = int(len(xs) * density / (size * size))
    for _ in range(n * 6):
        if n <= 0 or len(xs) == 0:
            break
        i = rnd.randrange(len(xs))
        y, x = ys[i], xs[i]
        y0, x0 = y - (size - 1) // 2, x - (size - 1) // 2
        sl = (slice(max(0, y0 - 1), y0 + size + 1), slice(max(0, x0 - 1), x0 + size + 1))
        if taken[sl].any():
            continue
        blob = (slice(max(0, y0), y0 + size), slice(max(0, x0), x0 + size))
        if not mask[blob].all():
            continue
        a[blob][..., :3] = colour
        if rim is not None:
            ring = np.zeros(mask.shape, bool)
            ring[sl] = True
            ring[blob] = False
            ring &= mask
            a[ring, :3] = rim
        taken[sl] = True
        n -= 1
    return a


GREEN = lambda h, s, v: (h > 55) & (h < 175) & (s > 0.15)
RED = lambda h, s, v: ((h < 18) | (h > 335)) & (s > 0.35)
BLUEPURPLE = lambda h, s, v: (h > 195) & (h < 285) & (s > 0.15)
CYAN = lambda h, s, v: (h >= 160) & (h <= 195) & (s > 0.15)
PINKRED = lambda h, s, v: ((h > 300) | (h < 18)) & (s > 0.3)
WHITE = lambda h, s, v: (s < 0.18) & (v > 0.5)
DARK = lambda h, s, v: (s < 0.25) & (v <= 0.5)


def paint_caterpie(a, shiny):
    if not shiny:
        return recolour(a, [(GREEN, (286, 0.85, 0.92)), (RED, (342, -0.42, 1.18))])
    return recolour(a, [(GREEN, (222, 0.95, 0.95)), (RED, (24, -0.85, 1.15))])


def paint_metapod(a, shiny):
    base = recolour(a, [(GREEN, (284, 0.85, 0.85) if not shiny else (220, 0.95, 0.85))])
    h, s, v = hsv_img(a)
    shell = GREEN(h, s, v) & (a[..., 3] > 0)
    spot, rim = ((255, 204, 51), (214, 112, 30)) if not shiny else ((255, 150, 40), (200, 70, 20))
    return spots(base, shell, spot, 11 if not shiny else 12, 0.16, size=2)


def paint_butterfree(a, shiny):
    h, s, v = hsv_img(a)
    wing = WHITE(h, s, v) & (a[..., 3] > 0)
    if not shiny:
        rules = [(WHITE, (284, -0.55, 0.9)), (DARK, (285, -0.45, 0.55)), (BLUEPURPLE, (276, 1.1, 0.78)),
                 (CYAN, (330, -0.5, 1.05)), (PINKRED, (50, -0.85, 1.25))]
        spot = (255, 210, 60)
    else:
        rules = [(WHITE, (188, -0.6, 0.92)), (DARK, (215, -0.4, 0.5)), (BLUEPURPLE, (232, 1.1, 0.7)),
                 (CYAN, (28, -0.6, 1.05)), (PINKRED, (24, -0.85, 1.2))]
        spot = (255, 140, 40)
    out = recolour(a, rules)
    # brighter warning bands where the wing grows lighter toward its tips, then yellow spots
    return spots(out, wing & (v > 0.8), spot, 21 if not shiny else 22, 0.07, size=2)


def geo_rects(geo):
    """{bone name: [(face rects for each cube)]}; each entry {face: (x, y, w, h)} in texture pixels (box UV)."""
    g = geo["minecraft:geometry"][0]
    out = {}
    for b in g["bones"]:
        for c in b.get("cubes", []):
            if not isinstance(c.get("uv"), list):
                continue
            (u, v), (w, h, d) = c["uv"], [int(round(x)) for x in c["size"]]
            out.setdefault(b["name"], []).append({
                "up": (u + d, v, w, d), "down": (u + d + w, v, w, d), "east": (u, v + d, d, h),
                "north": (u + d, v + d, w, h), "west": (u + d + w, v + d, d, h), "south": (u + 2 * d + w, v + d, w, h)})
    return out


def fill(a, rect, colour, mask=None):
    x, y, w, h = rect
    for yy in range(max(0, y), min(a.shape[0], y + h)):
        for xx in range(max(0, x), min(a.shape[1], x + w)):
            if a[yy, xx, 3] == 0:
                continue
            if mask is None or mask(xx - x, yy - y, w, h):
                a[yy, xx, :3] = colour
    return a


def paint_mudbray(a, shiny, geo):
    """The emo CobbleEffort Mudbray: a near-black body with white skeleton markings (ribs, leg bones), a white skull
    face, a black side-swept fringe with a purple streak, grey hooves and a black tail with red X marks."""
    dark_h = 238 if not shiny else 330
    out = recolour(a, [(lambda h, s, v: s < 0.16, (270, -0.14, 0.3)),                        # grey mane/hooves: black
                       (lambda h, s, v: s >= 0.16, (dark_h, -0.3, 0.3))])                   # the rest: navy-black
    r = geo_rects(geo)
    bone, grey = (236, 234, 228), (110, 110, 120)
    red = (214, 52, 52) if not shiny else (60, 150, 230)
    streak = (120, 70, 170) if not shiny else (230, 80, 140)
    for cube in r.get("torso", []):                                                   # ribs on both flanks
        for f in ("east", "west"):
            fill(out, cube[f], bone, lambda x, y, w, h: 2 <= x <= w - 3 and x % 2 == 1 and 0 < y < h - 1)
        fill(out, cube["up"], bone, lambda x, y, w, h: x == w // 2 and y % 2 == 0)     # spine
    for cube in r.get("torso", []):
        fill(out, cube["north"], bone, lambda x, y, w, h: x == w // 2)                # breastbone
    for name in ("ear_left", "ear_right", "ear_left2", "ear_right2"):
        for cube in r.get(name, []):
            fill(out, cube["north"], streak, lambda x, y, w, h: x == w // 2)          # purple inner ears
    for cube in r.get("head", [])[:1]:
        fill(out, cube["north"], bone)                                                # white skull face
        for f in ("east", "west"):
            fill(out, cube[f], bone, lambda x, y, w, h: y >= h // 2)
    for name in ("muzzle",):
        for cube in r.get(name, []):
            for f in cube:
                fill(out, cube[f], bone)
    for name in ("eye_left", "eye_right", "pupil_left", "pupil_right"):
        for cube in r.get(name, []):
            for f in cube:
                fill(out, cube[f], (16, 14, 20) if "eye_" in name else red)           # hollow eyes, red pupils
    for name in ("hair_left", "hair_right", "hair_left2", "hair_right2", "head_mane_left", "head_mane_left2"):
        for cube in r.get(name, []):
            for f in cube:
                fill(out, cube[f], streak, lambda x, y, w, h: x == w // 2)            # purple streak in the fringe
    for leg in ("front_left", "front_right", "back_left", "back_right"):
        for cube in r.get(f"leg_{leg}", []):
            fill(out, cube["north"], bone, lambda x, y, w, h: x == w // 2)            # bone down the upper leg
        for cube in r.get(f"leg_{leg}2", []):
            for f in cube:
                fill(out, cube[f], bone)                                              # white lower leg bones
        for cube in r.get(f"leg_{leg}3", []):
            for f in cube:
                fill(out, cube[f], grey)                                              # grey hooves
    for name in ("tail2", "tail3"):
        for cube in r.get(name, []):
            for f in ("up", "down"):
                fill(out, cube[f], red, lambda x, y, w, h: abs((x % 3) - 1) == abs(y - h // 2) % 2 and x % 3 != 2)
    return out


# ---- forms ------------------------------------------------------------------------------------------------------------

LINE = {
    "caterpie": {
        "folder": "0010_caterpie", "paint": paint_caterpie, "types": ("bug", "poison"),
        "abilities": ["poisonpoint", "h:runaway"],
        "moves_add": ["5:poisonsting", "tm:toxic", "tm:venoshock", "tm:acidspray"],
        "evolve": ("metapod", 7, ["acidarmor"]),
        "entry": ("Its purple body warns every bird Pokémon away: it is laced with poison from the toxic leaves it "
                  "eats. When something comes too close it rears up and flicks out its pink, forked feeler, "
                  "which oozes a stinging, foul-smelling liquid."),
        "look": "purple with a pink forked feeler, a cream belly and a curled yellow tail tip",
        "spawn": ("common", "2-10", 5.0, ["#cobblemon:is_jungle", "#cobblemon:is_swamp", "minecraft:flower_forest",
                                          "minecraft:dark_forest"]),
        "how_where": "jungles, swamps, flower forests and dark forests",
    },
    "metapod": {
        "folder": "0011_metapod", "paint": paint_metapod, "types": ("bug", "poison"),
        "abilities": ["poisonpoint", "h:shedskin"],
        "moves_add": ["1:acidarmor", "1:poisonsting", "tm:toxic", "tm:venoshock"],
        "evolve": ("butterfree", 10, ["acidspray"]),
        "entry": ("Its shell is studded with bright yellow spots that shout poison to anything that would eat it. "
                  "Inside, the toxins it gathered as a Caterpie are being brewed into wing scales."),
        "look": "a purple shell studded with bright yellow warning spots",
        "spawn": ("uncommon", "7-15", 2.0, ["#cobblemon:is_jungle", "#cobblemon:is_swamp", "minecraft:flower_forest"]),
        "how_where": "jungles, swamps and flower forests",
    },
    "butterfree": {
        "folder": "0012_butterfree", "paint": paint_butterfree, "types": ("bug", "poison"),
        "abilities": ["poisontouch", "h:tintedlens"],
        "moves_replace": {"gust": "acidspray", "confusion": "acid", "psybeam": "venoshock", "airslash": "sludgebomb",
                          "whirlwind": "toxic", "tailwind": "toxicspikes"},
        "moves_add": ["tm:sludgebomb", "tm:venoshock", "tm:toxic", "tm:toxicspikes", "tm:sludgewave", "tm:acidspray"],
        "evolve": None,
        "entry": ("Its wings shine violet and gold so no predator forgets them: one taste of their scales leaves a "
                  "bird Pokémon numb for days. Flocks of them drift over jungle canopies, and the trees they rest in "
                  "turn faintly purple."),
        "look": "violet wings with dark veins and yellow warning spots, a plum body and yellow eyes",
        "spawn": ("rare", "10-30", 0.8, ["#cobblemon:is_jungle", "minecraft:flower_forest"]),
        "how_where": "jungles and flower forests", "model": "cobblemon:butterfree_male.geo",
    },
    "mudbray": {
        "folder": "0749_mudbray", "paint": paint_mudbray, "geo": "0749_mudbray/mudbray.geo.json", "generation": 7,
        "model": "cobblemon:mudbray.geo",
        "types": ("dark",), "abilities": ["moody", "stamina", "h:innerfocus"],
        "moves_replace": {"mudslap": "bite", "mudsport": "faketears", "rototiller": "leer", "bulldoze": "assurance",
                          "strength": "nightslash", "highhorsepower": "suckerpunch", "earthquake": "darkpulse",
                          "megakick": "foulplay"},
        "moves_add": ["tm:darkpulse", "tm:nightslash", "tm:foulplay", "tm:snarl", "tm:taunt", "tm:faketears",
                      "tm:willowisp", "tm:flamecharge", "tm:firefang"],
        "evolve": ("cobbleeffort:ignitemare", 30, ["flamecharge"]),
        "entry": ("It dyes its mane black, lets its fringe fall over its eyes and wears the pattern of a skeleton on "
                  "its hide. It sulks in the shadows and kicks at anyone who calls it a phase."),
        "look": "near-black with white skeleton markings, a white skull face, a black side-swept fringe with a purple "
                "streak and a black tail with red X marks",
        "spawn": ("uncommon", "5-28", 2.0, ["minecraft:dark_forest", "#cobblemon:is_badlands", "#cobblemon:is_spooky"]),
        "how_where": "dark forests, badlands and spooky biomes",
        "shiny_note": "Shiny: crimson-black with blue marks.",
    },
}
SHINY_NOTE = "Shiny: electric blue with orange (feeler, spots and eyes) and teal wings."
ABILITY_NAMES = {"poisonpoint": "Poison Point", "runaway": "Run Away", "shedskin": "Shed Skin",
                 "poisontouch": "Poison Touch", "tintedlens": "Tinted Lens", "innerfocus": "Inner Focus"}


def form_json(sp, species, c):
    moves = list(species["moves"])
    rep = c.get("moves_replace", {})
    moves = [m.split(":")[0] + ":" + rep.get(m.split(":", 1)[1], m.split(":", 1)[1]) for m in moves]
    for m in c.get("moves_add", []):
        if m not in moves:
            moves.append(m)
    seen, out = set(), []
    for m in moves:
        if m not in seen:
            seen.add(m)
            out.append(m)
    f = {"name": FORM, "primaryType": c["types"][0], "aspects": [ASPECT],
         "labels": [f"gen{c.get('generation', 1)}", "cobbleeffort_regional"], "abilities": c["abilities"], "moves": out,
         "pokedex": [f"{MOD}.species.{sp}-{ASPECT}.desc"], "battleOnly": False}
    if len(c["types"]) > 1:
        f["secondaryType"] = c["types"][1]
    if c["evolve"]:
        res, lvl, learn = c["evolve"]
        # into the next CobbleEffort form, or (a namespaced id) into a species of its own, like Sirfetch'd
        result = res if ":" in res else f"{res} {ASPECT}"
        f["evolutions"] = [{"id": f"{sp}_{res.split(':')[-1]}_{ASPECT}", "variant": "level_up", "result": result,
                            "consumeHeldItem": False, "learnableMoves": learn,
                            "requirements": [{"variant": "level", "minLevel": lvl}]}]
    else:
        f["evolutions"] = []
    return f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cobblemon", type=Path, required=True)
    a = ap.parse_args()
    cob = a.cobblemon
    data = RES / "data" / MOD
    lang_path = RES / "assets" / MOD / "lang" / "en_us.json"
    lang = json.loads(lang_path.read_text())
    write_json(data / "species_features" / f"{ASPECT}.json",
               {"keys": [ASPECT], "type": "flag", "isAspect": True, "default": False})
    write_json(data / "species_feature_assignments" / f"{ASPECT}.json", {"pokemon": list(LINE), "features": [ASPECT]})
    manifest, spawns = [], []
    for sp, c in LINE.items():
        species = json.loads((cob / "data" / "cobblemon" / "species" / f"generation{c.get('generation', 1)}" /
                              f"{sp}.json").read_text())
        geo = json.loads((cob / "assets" / "cobblemon" / "bedrock" / "pokemon" / "models" / c["geo"]).read_text()) \
            if c.get("geo") else None
        write_json(data / "species_additions" / f"{sp}_{ASPECT}.json",
                   {"target": f"cobblemon:{sp}", "forms": [form_json(sp, species, c)]})
        lang[f"{MOD}.species.{sp}-{ASPECT}.desc"] = c["entry"]
        tex_dir = RES / "assets" / MOD / "textures" / "pokemon" / "regional" / c["folder"]
        tex_dir.mkdir(parents=True, exist_ok=True)
        src = cob / "assets" / "cobblemon" / "textures" / "pokemon" / c["folder"]
        for shiny, sfx in ((False, ""), (True, "_shiny")):
            img = np.array(Image.open(src / f"{sp}.png").convert("RGBA"))
            out = c["paint"](img, shiny, geo) if geo else c["paint"](img, shiny)
            Image.fromarray(out, "RGBA").save(tex_dir / f"{sp}_{ASPECT}{sfx}.png", optimize=True)
        tex = lambda sfx: f"{MOD}:textures/pokemon/regional/{c['folder']}/{sp}_{ASPECT}{sfx}.png"
        write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "resolvers" / "regional" / f"{sp}_{ASPECT}.json", {
            "species": f"cobblemon:{sp}", "order": 5,
            "variations": [{"aspects": [ASPECT], "texture": tex("")},
                           {"aspects": [ASPECT, "shiny"], "texture": tex("_shiny")}]})
        bucket, level, weight, biomes = c["spawn"]
        spawns.append({"id": f"{sp}-{ASPECT}", "pokemon": f"{sp} {ASPECT}", "presets": ["natural"], "type": "pokemon",
                       "spawnablePositionType": "grounded", "bucket": bucket, "level": level, "weight": weight,
                       "condition": {"canSeeSky": True, "biomes": biomes}})
        dex = species["nationalPokedexNumber"]
        s = species["baseStats"]
        write_json(TOOLS / "readme" / f"_new_{sp}_{ASPECT}.json", {
            "dex": dex, "name": f"{species['name']} (CobbleEffort form)", "types": " / ".join(t.title() for t in c["types"]),
            "ability": " / ".join(ABILITY_NAMES.get(x.removeprefix("h:"), x.removeprefix("h:").title())
                                  + (" (hidden)" if x.startswith("h:") else "") for x in c["abilities"]),
            "look": c["look"], "entry": c["entry"],
            "how": [f"Wild: {bucket} in {c['how_where']}."] +
                   ([(f"Evolves into {c['evolve'][0].split(':')[1].title()} at level {c['evolve'][1]}." if ":" in c["evolve"][0]
                      else f"Evolves into the CobbleEffort {c['evolve'][0].title()} at level {c['evolve'][1]}.")]
                    if c["evolve"] else []),
            "stats": [s["hp"], s["attack"], s["defence"], s["special_attack"], s["special_defence"], s["speed"]]})
        model = c.get("model", f"cobblemon:{sp}.geo")
        manifest.append({"species": f"{sp}_{ASPECT}", "folder": c["folder"], "model": model,
                         "original": f"cobblemon:textures/pokemon/{c['folder']}/{sp}.png", "retextured": tex(""), "layers": []})
        manifest.append({"species": f"{sp}_{ASPECT}_shiny", "folder": c["folder"], "model": model,
                         "original": f"cobblemon:textures/pokemon/{c['folder']}/{sp}_shiny.png", "retextured": tex("_shiny"),
                         "layers": []})
    old = data / "spawn_pool_world" / "regional_caterpie.json"
    if old.exists():
        old.unlink()
    write_json(data / "spawn_pool_world" / "regional.json",
               {"enabled": True, "neededInstalledMods": [], "neededUninstalledMods": [], "spawns": spawns})
    lang_path.write_text(json.dumps(lang, indent=2, ensure_ascii=False) + "\n")
    write_json(TOOLS / "preview" / "manifest_regional.json", manifest)
    print(f"regional forms: {', '.join(LINE)} ({ASPECT})")


if __name__ == "__main__":
    main()
