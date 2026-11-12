#!/usr/bin/env python3
"""
The leagues of Johto to Paldea (CobbleEffort: Kanto 0.4.0): each region's dimension gets its own eight gyms and Elite
Four hall, built around its centre the first time someone arrives (KantoGyms reads sites_<region>.json), with its own
badges (one per gym) and Champion Ribbon. Leaders and Elite Four are original characters with teams from that
generation's Pokédex (tools/league_teams.json, from make_league_teams.py). Gym buildings are Kanto's design with the
gym type's blocks. Run by make_assets.py.
"""
from __future__ import annotations

import colorsys
import json
import math
from pathlib import Path

from PIL import Image

import make_assets as ma
from make_assets import A, D, MOD, Nbt, save, write_json

HERE = Path(__file__).resolve().parent
LANG: dict[str, str] = {}
REGIONS = ["johto", "hoenn", "sinnoh", "unova", "kalos", "alola", "galar", "paldea"]
# original names (8 gym leaders, then the Elite Four), none of them the games' characters
NAMES = {
    "johto": ["Wren", "Sable", "Corin", "Hollis", "Brannock", "Ferris", "Aster", "Draven", "Mireille", "Thorne", "Kestrel", "Vesper"],
    "hoenn": ["Marisol", "Cobalt", "Rhea", "Pell", "Tasman", "Cirrus", "Lumen", "Halia", "Sorrel", "Nerine", "Basalt", "Corvina"],
    "sinnoh": ["Linnea", "Gerd", "Holm", "Frida", "Torvald", "Isak", "Saga", "Embla", "Runa", "Valdis", "Eir", "Brage"],
    "unova": ["Jett", "Marlow", "Ceci", "Dorian", "Tamsin", "Rook", "Indigo", "Halcyon", "Vale", "Odessa", "Cyprus", "Nyx"],
    "kalos": ["Amelie", "Bastien", "Coralie", "Fleur", "Gaspard", "Lucien", "Margaux", "Sylvain", "Odile", "Thibault", "Celeste", "Aurelien"],
    "alola": ["Kalani", "Makoa", "Leilani", "Nalu", "Keoni", "Mahina", "Ikaika", "Pua", "Kaimana", "Nohea", "Lani", "Akoni"],
    "galar": ["Bryony", "Rowan", "Imogen", "Ewan", "Morwenna", "Callum", "Heddwyn", "Fenella", "Gareth", "Isolde", "Lachlan", "Rhiannon"],
    "paldea": ["Ines", "Mateo", "Lucia", "Rafael", "Carmen", "Joaquin", "Pilar", "Tomas", "Alba", "Ignacio", "Rocio", "Esteban"],
}
REGION_COLOUR = {"johto": (200, 160, 60), "hoenn": (40, 140, 200), "sinnoh": (120, 120, 210), "unova": (60, 60, 70),
                 "kalos": (60, 90, 200), "alola": (240, 130, 60), "galar": (200, 40, 60), "paldea": (230, 120, 30)}
HAIRS = [(40, 28, 20), (200, 170, 90), (150, 60, 30), (30, 30, 36), (230, 230, 235), (90, 50, 120), (60, 110, 160), (180, 90, 60)]
# per type: building accents (wall stripe, floor accent, pillar, light), shirt hue, badge colours (dark, mid, light)
TYPES = {
    "normal": (("minecraft:smooth_stone", "minecraft:birch_planks", "minecraft:quartz_pillar", "minecraft:lantern"), 40,
               ((90, 80, 70), (190, 180, 160), (240, 236, 224))),
    "fire": (("minecraft:nether_bricks", "minecraft:red_terracotta", "minecraft:red_nether_bricks", "minecraft:shroomlight"), 12,
             ((130, 30, 10), (240, 100, 30), (255, 220, 120))),
    "water": (("minecraft:prismarine_bricks", "minecraft:water", "minecraft:dark_prismarine", "minecraft:sea_lantern"), 205,
              ((20, 50, 120), (50, 120, 220), (170, 220, 255))),
    "grass": (("minecraft:moss_block", "minecraft:moss_block", "minecraft:oak_leaves", "minecraft:shroomlight"), 110,
              ((20, 80, 30), (70, 170, 60), (180, 240, 150))),
    "electric": (("minecraft:waxed_copper_block", "minecraft:waxed_cut_copper", "minecraft:waxed_exposed_copper", "minecraft:redstone_lamp"), 52,
                 ((120, 90, 0), (240, 200, 30), (255, 250, 170))),
    "ice": (("minecraft:packed_ice", "minecraft:snow_block", "minecraft:blue_ice", "minecraft:sea_lantern"), 190,
            ((40, 90, 140), (120, 200, 240), (230, 250, 255))),
    "fighting": (("minecraft:stripped_spruce_log", "minecraft:red_wool", "minecraft:spruce_planks", "minecraft:lantern"), 0,
                 ((100, 20, 20), (190, 60, 40), (250, 160, 120))),
    "poison": (("minecraft:purple_terracotta", "minecraft:purple_stained_glass", "minecraft:purpur_pillar", "minecraft:pearlescent_froglight"), 285,
               ((60, 20, 80), (150, 70, 190), (230, 170, 250))),
    "ground": (("minecraft:terracotta", "minecraft:coarse_dirt", "minecraft:smooth_sandstone", "minecraft:lantern"), 38,
               ((90, 60, 30), (190, 140, 80), (240, 210, 150))),
    "flying": (("minecraft:light_blue_terracotta", "minecraft:white_concrete", "minecraft:smooth_quartz", "minecraft:end_rod"), 200,
               ((60, 100, 160), (140, 190, 240), (240, 248, 255))),
    "psychic": (("minecraft:amethyst_block", "minecraft:pink_stained_glass", "minecraft:purpur_block", "minecraft:end_rod"), 330,
                ((120, 30, 80), (240, 100, 170), (255, 200, 230))),
    "bug": (("minecraft:lime_terracotta", "minecraft:moss_block", "minecraft:jungle_planks", "minecraft:ochre_froglight"), 80,
            ((60, 90, 10), (150, 190, 40), (220, 240, 140))),
    "rock": (("minecraft:polished_andesite", "minecraft:cobblestone", "minecraft:stone", "minecraft:lantern"), 30,
             ((70, 60, 50), (140, 124, 104), (210, 196, 170))),
    "ghost": (("minecraft:deepslate_tiles", "minecraft:polished_blackstone", "minecraft:chiseled_deepslate", "minecraft:soul_lantern"), 270,
              ((40, 20, 70), (100, 70, 160), (190, 170, 230))),
    "dragon": (("minecraft:purpur_block", "minecraft:end_stone_bricks", "minecraft:obsidian", "minecraft:end_rod"), 250,
               ((30, 30, 110), (90, 80, 210), (190, 180, 255))),
    "dark": (("minecraft:blackstone", "minecraft:black_concrete", "minecraft:polished_blackstone_bricks", "minecraft:soul_lantern"), 280,
             ((14, 12, 16), (60, 50, 60), (140, 120, 130))),
    "steel": (("minecraft:iron_block", "minecraft:smooth_stone", "minecraft:polished_andesite", "minecraft:sea_lantern"), 210,
              ((70, 76, 90), (160, 170, 185), (230, 236, 245))),
    "fairy": (("minecraft:pink_terracotta", "minecraft:pink_concrete", "minecraft:stripped_cherry_log", "minecraft:pearlescent_froglight"), 320,
              ((150, 60, 110), (240, 140, 190), (255, 220, 240))),
}
# badge emblems (16x16, centre 7.5): Kanto's eight plus the other types
c = 7.5
SHAPES = dict(ma.BADGE_SHAPES)
SHAPES.update({
    "normal": lambda x, y: 3.2 <= math.hypot(x - c, y - c) <= 6.8,                                            # a ring
    "fighting": lambda x, y: abs(x - c) <= 5.5 and abs(y - c - 1) <= 4.5 or (2 <= y <= 4 and abs(x - c) <= 5 and (x % 3) != 0),  # a fist
    "flying": lambda x, y: ((x - c) / 7) ** 2 + ((y - c) / 4.5) ** 2 <= 1 and not ((x - c + 1) / 6) ** 2 + ((y - c + 2.5) / 4) ** 2 <= 1,  # a wing
    "bug": lambda x, y: ((x - c) / 5) ** 2 + ((y - c - 1) / 6) ** 2 <= 1 or (abs(x - c) in (2.5, 3.5) and y <= 3),   # a beetle
    "ghost": lambda x, y: (math.hypot(x - c, y - 6) <= 5.5 and y <= 6) or (abs(x - c) <= 5.5 and 6 < y <= 12 + (int(x) % 3 == 0)),  # a ghost
    "steel": lambda x, y: abs(x - c) <= 6.5 and abs(y - c) <= 6.5 - abs(x - c) * 0.45 + 2.5,                   # a hexagon-ish
    "ice": lambda x, y: abs(x - c) <= 1 or abs(y - c) <= 1 or abs(abs(x - c) - abs(y - c)) <= 0.9 and math.hypot(x - c, y - c) <= 7,  # a snowflake
    "dragon": lambda x, y: abs(x - c) <= 6.8 - abs(y - c) * 0.95 or abs(y - c) <= 6.8 - abs(x - c) * 0.95,     # a four-point star
    "dark": lambda x, y: math.hypot(x - c, y - c) <= 6.5 and math.hypot(x - c - 3, y - c + 2) > 5,            # a crescent
    "fairy": lambda x, y: ((x - c) * 1.1 / 6) ** 2 + ((-(y - c) + 1) / 6 - math.sqrt(abs((x - c) * 1.1 / 6))) ** 2 <= 1.0,  # a heart
})


def badge(typ, gem):
    dark, mid, light = TYPES[typ][2]
    inside = SHAPES[typ]
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y in range(16):
        for x in range(16):
            if not inside(x, y):
                continue
            rim = not all(inside(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            col = dark if rim else (light if (x - c) + (y - c) < -2 else mid)
            im.putpixel((x, y), col + (255,))
    for (x, y) in ((7, 7), (8, 7), (7, 8), (8, 8)):                      # the region's gem in the middle
        if inside(x, y):
            im.putpixel((x, y), gem + (255,))
    return im


def ribbon(colour):
    """A region's Champion Ribbon: Kanto's gold rosette with tails in the region's colour."""
    im = ma.ribbon()
    px = im.load()
    for y in range(16):
        for x in range(16):
            r, g, b, a = px[x, y]
            if a and r > 100 and g < 60 and b < 60:                        # the red parts
                k = r / 200
                px[x, y] = tuple(int(min(255, v * k)) for v in colour) + (a,)
    return im


def hue_of(rgb):
    return colorsys.rgb_to_hsv(*(v / 255 for v in rgb))[0] * 360


def build():
    teams = json.loads((HERE / "league_teams.json").read_text())
    items = []
    for region in REGIONS:
        Region = region.title()
        league = teams[region]
        sites, gym_types = [], []
        leaders = []
        for k, (trainer, name) in enumerate(zip(league, NAMES[region])):
            typ = trainer["type"]
            elite = k >= 8
            lid = f"{region}_{name.lower()}"
            title = "Elite Four" if elite else f"{typ.title()} Gym Leader"
            accents, hue, _ = TYPES[typ]
            hair = HAIRS[(k * 3 + REGIONS.index(region)) % len(HAIRS)]
            leaders.append((lid, title, name, typ, accents, hue, hair, trainer["team"]))
        for lid, title, name, typ, accents, hue, hair, team in leaders:
            nid = f"{MOD}:{lid}"
            write_json(D / "npcs" / f"{lid}.json", {
                "names": [f"{title} {name}"], "hitbox": "player", "canDespawn": False, "autoHealParty": True,
                "battleConfiguration": {"canChallenge": True}, "interaction": {"type": "dialogue", "dialogue": nid},
                "party": {"type": "simple", "pokemon": team}, "skill": 5 if title == "Elite Four" else 3, "presets": []})
            intro = (f"Welcome to {Region}! I'm {name}, and this gym's trial is {typ.title()}-type. Show me your team!"
                     if title != "Elite Four" else f"You've reached {Region}'s Elite Four. I am {name}, master of {typ.title()} types. Ready?")
            write_json(D / "dialogues" / f"{lid}.json", {
                "pages": [{"id": "intro", "speaker": "npc", "lines": [intro],
                           "input": {"type": "option", "vertical": False, "options": [
                               {"value": "battle", "text": "Battle!", "action": ["q.dialogue.close();", "q.npc.start_battle(q.player, 'singles');"]},
                               {"value": "later", "text": "Not yet", "action": ["q.dialogue.close();"]}]}}],
                "speakers": {"npc": {"face": "q.npc.face(false);", "name": {"type": "expression", "expression": "q.npc.name"}}}})
            write_json(A / "bedrock" / "npcs" / "variations" / f"{lid}.json", {"name": nid, "order": 0, "variations": [
                {"aspects": [], "layers": [], "model": "cobblemon:trainer.geo", "poser": "cobblemon:standard",
                 "texture": f"{MOD}:textures/npcs/{lid}.png"}]})
            save(ma.trainer_skin(hue, hair), A / "textures" / "npcs" / f"{lid}.png")
        # the buildings: Kanto's gym design in each type's blocks, around the dimension's centre; the hall in the middle
        for i, leader in enumerate(leaders[:8]):
            typ = leader[3]
            t, pos = ma.gym(leader)
            p = D / "structure" / "gym" / f"{region}_{typ}.nbt"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(Nbt.file(t.data()))
            ang = math.radians(i * 45)
            bid = f"{region}_{typ}_badge"
            items.append(bid)
            sites.append({"id": f"{region}_{typ}", "label": f"{typ.title()} Gym", "template": f"{MOD}:gym/{region}_{typ}",
                          "size": list(t.size), "x": int(round(math.sin(ang) * 320)), "z": int(round(-math.cos(ang) * 320)),
                          "trainers": [{"npc": f"{MOD}:{leader[0]}", "pos": list(pos), "yaw": 180, "badge": bid}]})
            save(badge(typ, REGION_COLOUR[region]), A / "textures" / "item" / f"{bid}.png")
            write_json(A / "models" / "item" / f"{bid}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/{bid}"}})
            LANG[f"item.{MOD}.{bid}"] = f"{Region} {typ.title()} Badge"
        t, positions = ma.elite_hall(leaders[8:])
        p = D / "structure" / "gym" / f"{region}_elite_four.nbt"
        p.write_bytes(Nbt.file(t.data()))
        sites.append({"id": f"{region}_elite_four", "label": "Elite Four", "template": f"{MOD}:gym/{region}_elite_four",
                      "size": list(t.size), "x": 0, "z": 0,
                      "trainers": [{"npc": f"{MOD}:{m[0]}", "pos": list(pos), "yaw": -90 if pos[0] < 12 else 90, "elite": True}
                                   for m, pos in zip(leaders[8:], positions)]})
        write_json(D / "kanto" / f"sites_{region}.json", sites)
        rid = f"{region}_champion_ribbon"
        items.append(rid)
        save(ribbon(REGION_COLOUR[region]), A / "textures" / "item" / f"{rid}.png")
        write_json(A / "models" / "item" / f"{rid}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/{rid}"}})
        LANG[f"item.{MOD}.{rid}"] = f"{Region} Champion Ribbon"
    # the items Java registers (badges and ribbons for every region but Kanto, whose are in Kanto.java)
    write_json(D / "kanto" / "league_items.json", items)
    LANG.update({
        f"{MOD}.gyms.list.region": "%s's gyms and the Elite Four (x, z): %s",
        f"{MOD}.elite.locked.region": "%s's Elite Four only face trainers with all 8 of its badges (you have %s).",
        f"{MOD}.champion.region": "You defeated %s's Elite Four: you're its Champion!",
    })
    return items


if __name__ == "__main__":
    build()
