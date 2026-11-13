"""Writes CobbleEffort: Fusion's assets and data: item textures (original pixel art), item models, the mod icon, the
English lang file and crafting recipes. Run from anywhere: python3 fusion/tools/make_assets.py"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1] / "common" / "src" / "main" / "resources"
NS = "cobbleeffort_fusion"
ASSETS = ROOT / "assets" / NS
DATA = ROOT / "data" / NS

# 16x16 maps: '.' clear, the rest from each item's palette
SPLICER = [
    "................",
    "..aa........aa..",
    ".abba......abba.",
    ".abba......abba.",
    "..abba....abba..",
    "..abbaccccabba..",
    "...abcdeedcba...",
    "...abceddecba...",
    "....bcdeedcb....",
    "....bceddecb....",
    "....acdeedca....",
    ".....accccca....",
    "......affa......",
    "......affa......",
    "......aggа......".replace("а", "a"),
    ".......aa.......",
]
REVERSER = [
    "................",
    "....aaaaaa......",
    "...abbbbbba.....",
    "..ab......ba..c.",
    "..ab.......bacc.",
    "..ab........bcc.",
    ".cab.......cccc.",
    ".ccb............",
    "............bcc.",
    ".ccccc.......ba.",
    ".ccb........ba..",
    ".cca.......ba...",
    ".c..ab....ba....",
    ".....abbbba.....",
    "......aaaa......",
    "................",
]
PALETTES = {
    "dna_splicers": {"a": (60, 64, 76), "b": (196, 202, 214), "c": (120, 126, 140), "d": (60, 230, 250),
                     "e": (250, 250, 255), "f": (150, 156, 170), "g": (90, 96, 110)},
    "super_splicers": {"a": (90, 56, 10), "b": (250, 210, 80), "c": (200, 150, 40), "d": (240, 70, 200),
                       "e": (255, 230, 250), "f": (220, 170, 60), "g": (150, 100, 20)},
    "infinite_splicers": {"a": (20, 12, 30), "b": (110, 70, 170), "c": (60, 36, 100), "d": (255, 120, 60),
                          "e": (120, 255, 200), "f": (90, 60, 140), "g": (40, 24, 60)},
    "dna_reversers": {"a": (110, 50, 10), "b": (250, 150, 40), "c": (60, 230, 250)},
}
RAINBOW = [(255, 80, 80), (255, 170, 60), (250, 240, 80), (80, 230, 120), (80, 180, 255), (190, 110, 255)]


def draw(rows, pal, rainbow=False):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in pal:
                c = pal[ch]
                if rainbow and ch in "de":
                    c = RAINBOW[(x + y) % len(RAINBOW)]
                img.putpixel((x, y), c + (255,))
    return img


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def main():
    tex = ASSETS / "textures" / "item"
    tex.mkdir(parents=True, exist_ok=True)
    for name, pal in PALETTES.items():
        rows = REVERSER if name == "dna_reversers" else SPLICER
        img = draw(rows, pal, rainbow=name == "infinite_splicers")
        img.save(tex / f"{name}.png")
        write_json(ASSETS / "models" / "item" / f"{name}.json",
                   {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/{name}"}})
        if name == "dna_splicers":
            img.resize((128, 128), Image.NEAREST).save(ASSETS / "icon.png")

    write_json(ASSETS / "lang" / "en_us.json", {
        f"itemGroup.{NS}": "CobbleEffort: Fusion",
        f"item.{NS}.dna_splicers": "DNA Splicers",
        f"item.{NS}.dna_splicers.tooltip": "Fuse two party Pokémon (head, then body), or unfuse a fusion. Used up by fusing.",
        f"item.{NS}.super_splicers": "Super Splicers",
        f"item.{NS}.super_splicers.tooltip": "Like DNA Splicers, but the fusion takes the higher of the two levels.",
        f"item.{NS}.infinite_splicers": "Infinite Splicers",
        f"item.{NS}.infinite_splicers.tooltip": "DNA Splicers that are never used up.",
        f"item.{NS}.dna_reversers": "DNA Reversers",
        f"item.{NS}.dna_reversers.tooltip": "Swap a fusion's head and body. Used up.",
        f"{NS}.pick.head": "Choose the HEAD (or a fusion to unfuse)",
        f"{NS}.pick.body": "Choose the BODY for %s",
        f"{NS}.pick.reverse": "Choose a fusion to reverse",
        f"{NS}.fused": "%s was born from the fusion!",
        f"{NS}.unfused": "The fusion came apart: both Pokémon are back.",
        f"{NS}.unfused_pc": "Your party is full: %s went to your PC.",
        f"{NS}.ability_choice": "Ability: ",
        f"{NS}.ability_body": "Keep the body's ability",
        f"{NS}.ability_head": "Use the head's ability",
        f"{NS}.ability_set": "%s now has %s.",
        f"{NS}.info": "%s: head %s, body %s; %s; base stats %s",
        f"{NS}.info.none": "No fusions in your party.",
        f"{NS}.error.same": "A Pokémon can't be fused with itself.",
        f"{NS}.error.already": "A fusion can't be fused again: unfuse it first.",
        f"{NS}.error.party": "Both Pokémon must be in your party.",
        f"{NS}.error.not_fused": "That Pokémon isn't a fusion.",
        f"{NS}.error.no_head": "This fusion's head couldn't be found.",
        f"{NS}.error.battle": "You can't splice DNA during a battle.",
        f"{NS}.error.ability": "That ability couldn't be set.",
    })

    def shaped(name, pattern, key, count=1):
        write_json(DATA / "recipe" / f"{name}.json", {
            "type": "minecraft:crafting_shaped", "category": "misc", "pattern": pattern,
            "key": {k: {"item": v} for k, v in key.items()}, "result": {"id": f"{NS}:{name}", "count": count}})

    shaped("dna_splicers", [" A ", "IRI", " I "], {"A": "minecraft:amethyst_shard", "I": "minecraft:iron_ingot", "R": "minecraft:redstone"})
    shaped("super_splicers", [" D ", "GSG", " G "], {"D": "minecraft:diamond", "G": "minecraft:gold_ingot", "S": f"{NS}:dna_splicers"})
    shaped("infinite_splicers", [" N ", "ESE", " E "], {"N": "minecraft:nether_star", "E": "minecraft:echo_shard", "S": f"{NS}:super_splicers"})
    shaped("dna_reversers", ["LQL", " R "], {"L": "minecraft:lapis_lazuli", "Q": "minecraft:quartz", "R": "minecraft:redstone"})
    print("wrote", sorted(p.name for p in tex.iterdir()))


if __name__ == "__main__":
    main()
