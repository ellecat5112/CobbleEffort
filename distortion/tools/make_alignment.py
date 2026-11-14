#!/usr/bin/env python3
"""
The Shadow and Crystal types (the user's design: every Pokémon has a Shadow and a Crystal counterpart).

Shadow is Pokémon XD's: a Shadow Pokémon's heart is closed, its moves are Shadow moves (2x on every Pokémon that
isn't a Shadow Pokémon, 0.5x on Shadow Pokémon), and the DNA Purifier opens its heart again. Crystal is the Crystal
Onix's: a glassy, see-through body that refracts special attacks (3/4 damage), weak to blows that shatter it.

Writes: the moves (Cobblemon datapack moves, data/<mod>/moves/<id>.js), the global species features (flags
`shadow_pokemon` and `crystal_pokemon` on every species), the two items' textures, models and recipes, the type icons
(assets/<mod>/textures/gui/alignment_types.png: Shadow then Crystal at 36 px, alignment_types_small.png at 18 px) and
the English names (merged into en_us.json). The battle engine side is data/<mod>/distortion/alignment_engine.js.
Run alone or from make_assets.py.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
RES = HERE.parent / "common" / "src" / "main" / "resources"
MOD = "cobbleeffort_distortion"
A = RES / "assets" / MOD
D = RES / "data" / MOD


def _move(num, name, type_, category, power, acc, pp, target="normal", flags=None, extra="", desc="", short=""):
    fl = flags if flags is not None else ({"protect": 1, "mirror": 1} if target != "self" else {"snatch": 1})
    acc_js = "true" if acc is True else str(acc)
    body = [f"num: {num}", f"accuracy: {acc_js}", f"basePower: {power}", f'category: "{category}"', f'name: "{name}"',
            f"pp: {pp}", "priority: 0", "flags: {" + ", ".join(f"{k}: {v}" for k, v in fl.items()) + "}"]
    if extra:
        body.append(extra.strip().rstrip(","))
    if "secondary" not in extra:
        body.append("secondary: null")
    body += [f'target: "{target}"', f'type: "{type_}"', f"desc: {json.dumps(desc)}", f"shortDesc: {json.dumps(short or desc)}"]
    return "{\n" + ",\n".join(body) + "\n}\n"


C = {"protect": 1, "mirror": 1, "contact": 1}
N = {"protect": 1, "mirror": 1}
SH = "Super effective on every Pokémon that isn't a Shadow Pokémon; not very effective on Shadow Pokémon."

# Pokémon Colosseum / XD's Shadow moves (powers from XD)
SHADOW_MOVES = {
    "shadowblitz": _move(-4001, "Shadow Blitz", "Shadow", "Physical", 40, 100, 20, flags=C,
                         desc="The user lunges at the target with a shadowy tackle. " + SH),
    "shadowrush": _move(-4002, "Shadow Rush", "Shadow", "Physical", 55, 100, 20, flags=C,
                        desc="The user charges at the target with dark, menacing force. " + SH),
    "shadowbreak": _move(-4003, "Shadow Break", "Shadow", "Physical", 75, 100, 15, flags=C,
                         desc="The user tackles the target with all of its shadowed might. " + SH),
    "shadowend": _move(-4004, "Shadow End", "Shadow", "Physical", 120, 60, 5, flags=C, extra="recoil: [1, 2],",
                       desc="A reckless charge of shadow power: the user takes half the damage it deals. " + SH,
                       short="Hits hard; the user takes 1/2 of the damage dealt."),
    "shadowwave": _move(-4005, "Shadow Wave", "Shadow", "Special", 50, 100, 20, "allAdjacentFoes", N,
                        desc="A wave of shadow washes over the foes. " + SH, short="Hits all foes."),
    "shadowrave": _move(-4006, "Shadow Rave", "Shadow", "Special", 70, 100, 15, "allAdjacentFoes", N,
                        desc="A rave of shadow energy batters the foes. " + SH, short="Hits all foes."),
    "shadowstorm": _move(-4007, "Shadow Storm", "Shadow", "Special", 95, 100, 10, "allAdjacentFoes", N,
                         desc="A raging storm of shadow engulfs the foes. " + SH, short="Hits all foes."),
    "shadowfire": _move(-4008, "Shadow Fire", "Shadow", "Special", 75, 100, 15, flags=N,
                        extra='secondary: {chance: 10, status: "brn"},',
                        desc="Black flames scorch the target; 10% chance to burn. " + SH, short="10% chance to burn."),
    "shadowbolt": _move(-4009, "Shadow Bolt", "Shadow", "Special", 75, 100, 15, flags=N,
                        extra='secondary: {chance: 10, status: "par"},',
                        desc="Dark lightning strikes the target; 10% chance to paralyse. " + SH, short="10% chance to paralyse."),
    "shadowchill": _move(-4010, "Shadow Chill", "Shadow", "Special", 75, 100, 15, flags=N,
                         extra='secondary: {chance: 10, status: "frz"},',
                         desc="A freezing shadow chills the target; 10% chance to freeze. " + SH, short="10% chance to freeze."),
    "shadowblast": _move(-4011, "Shadow Blast", "Shadow", "Special", 80, 100, 15, flags=N, extra="critRatio: 2,",
                         desc="A blade of shadow slashes the target; critical hits land more easily. " + SH,
                         short="High critical hit ratio."),
    "shadowhold": _move(-4012, "Shadow Hold", "Shadow", "Status", 0, 80, 10, "allAdjacentFoes",
                        {"protect": 1, "reflectable": 1, "mirror": 1}, extra="""
onHit(target, source, move) {
  return target.addVolatile('trapped', source, move, 'trapper');
},""", desc="Shadowy bonds hold every foe so they can't flee or switch out.", short="Foes can't switch out."),
    "shadowmist": _move(-4013, "Shadow Mist", "Shadow", "Status", 0, 100, 10, "allAdjacentFoes",
                        {"protect": 1, "reflectable": 1, "mirror": 1}, extra="boosts: {evasion: -2},",
                        desc="A shadowy mist harshly lowers every foe's evasiveness.", short="Lowers foes' evasion by 2."),
    "shadowdown": _move(-4014, "Shadow Down", "Shadow", "Status", 0, 100, 10, "allAdjacentFoes",
                        {"protect": 1, "reflectable": 1, "mirror": 1}, extra="boosts: {def: -2},",
                        desc="A dark aura harshly lowers every foe's Defense.", short="Lowers foes' Defense by 2."),
    "shadowpanic": _move(-4015, "Shadow Panic", "Shadow", "Status", 0, 60, 10, "allAdjacentFoes",
                         {"protect": 1, "reflectable": 1, "mirror": 1}, extra='volatileStatus: "confusion",',
                         desc="Terrifying shadows confuse every foe.", short="Confuses all foes."),
    "shadowshed": _move(-4016, "Shadow Shed", "Shadow", "Status", 0, True, 10, "all", {}, extra="""
onHitField(target, source) {
  let removed = false;
  for (const side of this.sides) {
    for (const c of ['reflect', 'lightscreen', 'auroraveil', 'safeguard', 'mist']) {
      if (side.removeSideCondition(c)) removed = true;
    }
  }
  this.add('-activate', source, 'move: Shadow Shed');
  return removed || undefined;
},""", desc="The user sheds shadow over the field, shattering Reflect, Light Screen, Aurora Veil, Safeguard and Mist on both sides.",
                        short="Removes screens, Safeguard and Mist from both sides."),
    "shadowhalf": _move(-4017, "Shadow Half", "Shadow", "Status", 0, True, 5, "all", {}, extra="""
onHitField(target, source) {
  for (const p of this.getAllActive()) {
    if (p.hp > 1) this.directDamage(Math.floor(p.hp / 2), p, source);
  }
},""", desc="A shadowy blast splits the field: every Pokémon in battle, the user too, loses half its HP.",
                        short="Every active Pokémon loses 1/2 of its HP."),
}

CRYSTAL_MOVES = {
    "prismbeam": _move(-4101, "Prism Beam", "Crystal", "Special", 80, 100, 15, flags=N,
                       extra='secondary: {chance: 10, volatileStatus: "confusion"},',
                       desc="The user splits light through its body into a dazzling beam; 10% chance to confuse.",
                       short="10% chance to confuse the target."),
    "shardvolley": _move(-4102, "Shard Volley", "Crystal", "Physical", 25, 90, 15, flags=N, extra="multihit: [2, 5],",
                         desc="The user fires sharp crystal shards at the target two to five times in a row.",
                         short="Hits 2-5 times in one turn."),
    "crystalcrash": _move(-4103, "Crystal Crash", "Crystal", "Physical", 120, 100, 15, flags=C, extra="recoil: [33, 100],",
                          desc="The user slams its crystal body into the target; it takes 1/3 of the damage it deals.",
                          short="Has 33% recoil."),
    "glassguard": _move(-4104, "Glass Guard", "Crystal", "Status", 0, True, 20, "self", extra="boosts: {def: 1, spd: 1},",
                        desc="The user hardens its crystal body, raising its Defense and Sp. Def by one stage.",
                        short="Raises the user's Defense and Sp. Def by 1."),
    "refraction": 'Object.assign({}, Dex.data.Moves["mirrorcoat"], {num: -4105, name: "Refraction", type: "Crystal", '
                  'isNonstandard: null, zMove: undefined, maxMove: undefined, desc: "The user bends the last special '
                  'attack that hit it back through its crystal body at twice the power.", shortDesc: "If hit by a '
                  'special attack, returns double damage."})\n',
}

MOVES = {**SHADOW_MOVES, **CRYSTAL_MOVES}
NAMES = {"shadowblitz": "Shadow Blitz", "shadowrush": "Shadow Rush", "shadowbreak": "Shadow Break", "shadowend": "Shadow End",
         "shadowwave": "Shadow Wave", "shadowrave": "Shadow Rave", "shadowstorm": "Shadow Storm", "shadowfire": "Shadow Fire",
         "shadowbolt": "Shadow Bolt", "shadowchill": "Shadow Chill", "shadowblast": "Shadow Blast", "shadowhold": "Shadow Hold",
         "shadowmist": "Shadow Mist", "shadowdown": "Shadow Down", "shadowpanic": "Shadow Panic", "shadowshed": "Shadow Shed",
         "shadowhalf": "Shadow Half", "prismbeam": "Prism Beam", "shardvolley": "Shard Volley", "crystalcrash": "Crystal Crash",
         "glassguard": "Glass Guard", "refraction": "Refraction"}


def _desc(js):
    i = js.find("desc:")
    if i < 0:
        return ""
    s = js[i + 5:].lstrip()
    q = s[0]
    return json.loads(s[: s.index(q, 1) + 1]) if q == '"' else ""


LANG = {
    "cobblemon.type.shadow": "Shadow",
    "cobblemon.type.crystal": "Crystal",
    f"item.{MOD}.shadow_heart": "Shadow Heart",
    f"item.{MOD}.shadow_heart.tooltip": "Use it on one of your Pokémon (sent out) to close its heart: it becomes its Shadow counterpart, Shadow-type, with Shadow moves. The DNA Purifier opens its heart again.",
    f"item.{MOD}.prism_crystal": "Prism Crystal",
    f"item.{MOD}.prism_crystal.tooltip": "Use it on one of your Pokémon (sent out) to turn its body to living crystal: it becomes its Crystal counterpart, Crystal-type, refracting special attacks. The DNA Purifier restores it.",
    f"{MOD}.align.shadowed": "%s's heart has closed! It became a Shadow Pokémon.",
    f"{MOD}.align.crystallized": "%s turned to living crystal! It became a Crystal Pokémon.",
    f"{MOD}.align.already": "%s is already a %s Pokémon.",
    f"{MOD}.align.other": "%s is a %s Pokémon: purify it in the DNA Purifier first.",
    f"{MOD}.align.not_yours": "That isn't your Pokémon.",
    f"{MOD}.align.in_battle": "Not while it's battling.",
    f"{MOD}.align.shadow": "Shadow",
    f"{MOD}.align.crystal": "Crystal",
    f"{MOD}.align.purified": "%s's heart opened! It's no longer a Shadow Pokémon, and its own moves came back.",
    f"{MOD}.align.restored": "The crystal fades: %s is back to normal, its own moves restored.",
    f"{MOD}.dna.analyzer.shadow_yes": "Shadow aura: DETECTED. Its heart is closed; sneak and use the DNA Purifier to open it.",
    f"{MOD}.dna.analyzer.crystal_yes": "Crystal lattice: DETECTED. Sneak and use the DNA Purifier to restore its body.",
    f"{MOD}.dna.purifier.aligned_inserted": "%s floats into the tank. Sneak and use the DNA Purifier to purify it.",
    f"{MOD}.dna.purifier.aligned_started": "Purifying %s... Come back in a minute.",
    f"{MOD}.dna.purifier.no_choice": "There's only one way to purify a %s Pokémon: sneak and use the Purifier to begin.",
}
for _id, _js in MOVES.items():
    LANG[f"cobblemon.move.{_id}"] = NAMES[_id]
    LANG[f"cobblemon.move.{_id}.desc"] = _desc(_js)


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


# --- art ---------------------------------------------------------------------------------------------------------------
SHADOW_RGB = ((58, 30, 84), (150, 70, 200), (236, 200, 255))     # dark, mid, light
CRYSTAL_RGB = ((60, 150, 190), (150, 230, 245), (250, 255, 255))


def _ss(draw_fn, size, scale=4):
    big = Image.new("RGBA", (size * scale, size * scale), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(big), size * scale)
    return big.resize((size, size), Image.LANCZOS)


def _shadow_symbol(d, s, col):
    """A closed heart wreathed in three flame-wisps (XD's Shadow aura)."""
    cx, cy = s / 2, s * 0.56
    r = s * 0.17
    d.ellipse((cx - 2 * r, cy - 1.6 * r, cx, cy + 0.4 * r), fill=col)
    d.ellipse((cx, cy - 1.6 * r, cx + 2 * r, cy + 0.4 * r), fill=col)
    d.polygon([(cx - 1.95 * r, cy - 0.3 * r), (cx + 1.95 * r, cy - 0.3 * r), (cx, cy + 2.0 * r)], fill=col)
    for k, (dx, h) in enumerate(((-1.7, 1.5), (0.0, 2.1), (1.7, 1.5))):
        bx = cx + dx * r
        d.polygon([(bx - 0.55 * r, cy - 1.0 * r), (bx + 0.55 * r, cy - 1.0 * r), (bx + 0.15 * r * (1 if k != 1 else 0), cy - (1.0 + h) * r)],
                  fill=col)


def _crystal_symbol(d, s, col):
    """A faceted gem: a crown of facets over a long point."""
    cx, cy = s / 2, s / 2
    w, top, mid, bot = s * 0.3, cy - s * 0.24, cy - s * 0.08, cy + s * 0.3
    d.polygon([(cx - w * 0.55, top), (cx + w * 0.55, top), (cx + w, mid), (cx, bot), (cx - w, mid)], fill=col)


def _icon(size, kind):
    dark, mid, light = SHADOW_RGB if kind == "shadow" else CRYSTAL_RGB

    def draw(d, s):
        d.ellipse((0, 0, s - 1, s - 1), fill=dark + (255,))
        d.ellipse((s * 0.07, s * 0.07, s * 0.93, s * 0.93), fill=mid + (255,))
        if kind == "shadow":
            _shadow_symbol(d, s, light + (255,))
        else:
            _crystal_symbol(d, s, light + (255,))
            cx, cy = s / 2, s / 2                                       # facet lines
            d.line((cx, cy - s * 0.24, cx, cy + s * 0.3), fill=mid + (255,), width=max(1, int(s * 0.03)))
            d.line((cx - s * 0.3, cy - s * 0.08, cx + s * 0.3, cy - s * 0.08), fill=mid + (255,), width=max(1, int(s * 0.03)))
    return _ss(draw, size)


def icons():
    for size, name in ((36, "alignment_types.png"), (18, "alignment_types_small.png")):
        sheet = Image.new("RGBA", (size * 2, size), (0, 0, 0, 0))
        sheet.paste(_icon(size, "shadow"), (0, 0))
        sheet.paste(_icon(size, "crystal"), (size, 0))
        p = A / "textures" / "gui" / name
        p.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(p, optimize=True)


def _item_shadow():
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    dark, mid, light = SHADOW_RGB
    for i in range(7):
        a = i / 7 * 2 * math.pi
        x, y = 32 + math.cos(a) * 12, 34 + math.sin(a) * 11
        d.ellipse((x - 13, y - 13, x + 13, y + 13), fill=dark + (110,))
    _shadow_symbol(d, 64, (20, 8, 30, 255))
    inner = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    _shadow_symbol(ImageDraw.Draw(inner), 64, mid + (255,))
    inner = inner.resize((52, 52), Image.LANCZOS)
    img.alpha_composite(inner, (6, 7))
    d.ellipse((22, 30, 28, 35), fill=light + (230,))                   # a glint
    return img.resize((16, 16), Image.LANCZOS)


def _item_crystal():
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    dark, mid, light = CRYSTAL_RGB
    pts = [(20, 8), (44, 8), (56, 24), (32, 58), (8, 24)]
    d.polygon(pts, fill=dark + (255,))
    d.polygon([(23, 12), (41, 12), (51, 24), (32, 52), (13, 24)], fill=mid + (235,))
    d.polygon([(23, 12), (32, 24), (13, 24)], fill=light + (255,))
    d.polygon([(41, 12), (51, 24), (32, 24)], fill=(110, 200, 230, 255))
    d.polygon([(13, 24), (32, 24), (32, 52)], fill=(200, 245, 252, 240))
    for (x, y) in ((50, 10), (12, 44)):                                 # rainbow glints
        d.line((x - 4, y, x + 4, y), fill=(255, 210, 250, 255), width=2)
        d.line((x, y - 4, x, y + 4), fill=(210, 255, 220, 255), width=2)
    return img.resize((16, 16), Image.LANCZOS)


def items():
    for name, fn in (("shadow_heart", _item_shadow), ("prism_crystal", _item_crystal)):
        p = A / "textures" / "item" / f"{name}.png"
        p.parent.mkdir(parents=True, exist_ok=True)
        fn().save(p, optimize=True)
        write_json(A / "models" / "item" / f"{name}.json", {"parent": "minecraft:item/generated",
                                                            "textures": {"layer0": f"{MOD}:item/{name}"}})
    write_json(D / "recipe" / "shadow_heart.json", {
        "type": "minecraft:crafting_shapeless", "category": "misc",
        "ingredients": [{"item": f"{MOD}:distortion_shard"}, {"item": f"{MOD}:distortion_shard"},
                        {"item": "minecraft:echo_shard"}, {"item": "minecraft:wither_rose"}],
        "result": {"id": f"{MOD}:shadow_heart", "count": 1}})
    write_json(D / "recipe" / "prism_crystal.json", {
        "type": "minecraft:crafting_shapeless", "category": "misc",
        "ingredients": [{"item": f"{MOD}:distortion_shard"}, {"item": f"{MOD}:distortion_shard"},
                        {"item": "minecraft:amethyst_shard"}, {"item": "minecraft:diamond"}, {"item": "minecraft:glass"}],
        "result": {"id": f"{MOD}:prism_crystal", "count": 1}})


def features():
    for key in ("shadow_pokemon", "crystal_pokemon"):
        write_json(D / "global_species_features" / f"{key}.json",
                   {"keys": [key], "type": "flag", "isAspect": True, "default": False})


def moves():
    out = D / "moves"
    out.mkdir(parents=True, exist_ok=True)
    for mid, js in MOVES.items():
        (out / f"{mid}.js").write_text(js)


def lang():
    path = A / "lang" / "en_us.json"
    data = json.loads(path.read_text()) if path.exists() else {}
    data.update(LANG)
    path.write_text(json.dumps(dict(sorted(data.items())), indent=2, ensure_ascii=False) + "\n")


def build():
    moves()
    features()
    icons()
    items()
    lang()


if __name__ == "__main__":
    build()
    print(f"{len(MOVES)} moves, 2 items, 2 type icons")
