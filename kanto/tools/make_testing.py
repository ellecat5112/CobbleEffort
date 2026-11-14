#!/usr/bin/env python3
"""
Creative testing tools (0.9.0, the user's request): the Biome Wand and Structure Wand (TestTools.java), the Pokémon
Spawner and Trainer Spawner (Spawners.java + client/SpawnerScreen). This writes their textures, models, blockstates
and lang, plus the spawned trainers' NPC class (no party of its own, so the spawner's team is used), its look
(Cobblemon's standard trainer) and its "Battle!" dialogue. Run by make_assets.py.
"""
from __future__ import annotations

from PIL import Image

from make_ashtray import A, D, MOD, clamp, write_json

LANG: dict[str, str] = {}


def px(img, x, y, c):
    if 0 <= x < img.width and 0 <= y < img.height:
        img.putpixel((x, y), clamp(c) + (255,))


def wand(rod, gem, glow):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for i in range(2, 13):                                         # the shaft, bottom-left to top-right
        px(img, i, 15 - i, rod)
        px(img, i + 1, 15 - i, tuple(v * 0.7 for v in rod))
    for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (2, 1), (1, 2)):
        px(img, 12 + dx, 2 + dy, gem)                              # the gem at its tip
    px(img, 12, 2, glow)
    px(img, 14, 0, glow)
    px(img, 10, 1, glow)
    return img


def spawner(frame, face):
    """A command-block-like frame round a picture: `face(x, y) -> colour or None`."""
    img = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            edge = x in (0, 15) or y in (0, 15)
            inner = x in (1, 14) or y in (1, 14)
            c = tuple(v * 0.6 for v in frame) if edge else frame if inner else (48, 48, 56)
            f = None if edge or inner else face(x, y)
            px(img, x, y, f if f else c)
    return img


def ball(x, y):
    dx, dy = x - 7.5, y - 7.5
    d = (dx * dx + dy * dy) ** 0.5
    if d > 5.6:
        return None
    if abs(dy) < 0.8 or d > 5.0:
        return (30, 30, 34)
    if d < 1.6:
        return (240, 240, 240)
    return (220, 50, 50) if dy < 0 else (240, 240, 240)


def trainer(x, y):
    if (x - 7.5) ** 2 + (y - 5) ** 2 < 5:                          # head
        return (232, 198, 164)
    if 3 <= y <= 4 and 5 <= x <= 10:                                # cap
        return (210, 50, 44)
    if 7 <= y <= 12 and 5 <= x <= 10:                               # body
        return (60, 120, 220)
    if 12 < y <= 13 and x in (6, 9):
        return (40, 40, 60)
    return None


def build():
    tex_i, tex_b = A / "textures" / "item", A / "textures" / "block"
    tex_i.mkdir(parents=True, exist_ok=True)
    tex_b.mkdir(parents=True, exist_ok=True)
    wand((120, 84, 50), (90, 210, 90), (220, 255, 200)).save(tex_i / "biome_wand.png")
    wand((140, 140, 150), (230, 180, 60), (255, 240, 180)).save(tex_i / "structure_wand.png")
    for name in ("biome_wand", "structure_wand"):
        write_json(A / "models" / "item" / f"{name}.json", {"parent": "minecraft:item/handheld",
                                                           "textures": {"layer0": f"{MOD}:item/{name}"}})
    spawner((200, 70, 70), ball).save(tex_b / "pokemon_spawner.png")
    spawner((70, 110, 200), trainer).save(tex_b / "trainer_spawner.png")
    for b in ("pokemon_spawner", "trainer_spawner"):
        write_json(A / "blockstates" / f"{b}.json", {"variants": {"": {"model": f"{MOD}:block/{b}"}}})
        write_json(A / "models" / "block" / f"{b}.json", {"parent": "minecraft:block/cube_all",
                                                         "textures": {"all": f"{MOD}:block/{b}"}})
        write_json(A / "models" / "item" / f"{b}.json", {"parent": f"{MOD}:block/{b}"})
    # the spawned trainers: an NPC class with no party (Cobblemon then battles with the party we give it)
    write_json(D / "npcs" / "spawner_trainer.json", {
        "names": ["Trainer"], "hitbox": "player", "canDespawn": False, "autoHealParty": True,
        "battleConfiguration": {"canChallenge": True},
        "interaction": {"type": "dialogue", "dialogue": f"{MOD}:spawner_trainer"}, "skill": 3, "presets": []})
    write_json(A / "bedrock" / "npcs" / "variations" / "spawner_trainer.json", {
        "name": f"{MOD}:spawner_trainer", "order": 0, "variations": [{
            "aspects": [], "layers": [], "model": "cobblemon:trainer.geo", "poser": "cobblemon:standard",
            "texture": "cobblemon:textures/npcs/standard/trainer.png"}]})
    write_json(D / "dialogues" / "spawner_trainer.json", {
        "pages": [{"id": "intro", "speaker": "npc", "lines": ["You've found me. Ready to battle?"],
                   "input": {"type": "option", "vertical": False, "options": [
                       {"value": "battle", "text": "Battle!",
                        "action": ["q.dialogue.close();", "q.npc.start_battle(q.player, 'singles');"]},
                       {"value": "later", "text": "Not yet", "action": ["q.dialogue.close();"]}]}}],
        "speakers": {"npc": {"face": "q.npc.face(false);", "name": {"type": "expression", "expression": "q.npc.name"}}}})
    k = f"{MOD}."
    LANG.update({
        f"item.{MOD}.biome_wand": "Biome Wand", f"item.{MOD}.structure_wand": "Structure Wand",
        f"block.{MOD}.pokemon_spawner": "Pokémon Spawner", f"block.{MOD}.trainer_spawner": "Trainer Spawner",
        k + "wand.biome.tip1": "Use: locate the nearest Ashtray Wastes or Liquor Meadows",
        k + "wand.biome.tip2": "Use on a block: turn the 65 x 65 area round it into that biome, with its features",
        k + "wand.structure.tip1": "Use: locate the nearest CobbleEffort or Kanto structure of its kind",
        k + "wand.structure.tip2": "Use on a block: place that structure there",
        k + "wand.tip3": "Sneak + use: change the target (creative operators only)",
        k + "wand.target": "Target: %s",
        k + "wand.none": "Nothing to target here",
        k + "wand.not_allowed": "Creative mode and operator permission are needed for this",
        k + "wand.forced": "%s painted over %s x %s blocks (%s features placed). Rejoin if the grass colour lags.",
        k + "spawner.saved": "Spawner saved",
        k + "spawner.pokemon.title": "Pokémon Spawner",
        k + "spawner.pokemon.help": "A redstone signal spawns this Pokémon (once per signal)",
        k + "spawner.trainer.title": "Trainer Spawner",
        k + "spawner.trainer.help": "A redstone signal spawns this trainer (once per signal)",
        k + "spawner.pokemon": "Pokémon (Cobblemon properties, e.g. mewtwo level=70 shiny=yes moves=psychic,recover)",
        k + "spawner.name": "Name tag (optional)",
        k + "spawner.level": "Level",
        k + "spawner.scale": "Size",
        k + "spawner.skin": "Skin (player)",
        k + "spawner.skill": "Skill 0-5",
        k + "spawner.team": "Team: one Pokémon per line (properties; no level= uses Level)",
        k + "spawner.team.hint": "charizard level=55 moves=flamethrower,airslash\ngarchomp shiny=yes",
        k + "spawner.uncatchable": "Uncatchable",
        k + "spawner.glowing": "Glowing",
        k + "spawner.battle": "Battle nearest player",
        k + "spawner.one": "One at a time",
        k + "spawner.doubles": "Double battle",
        k + "spawner.despawn": "Leave after losing",
    })


if __name__ == "__main__":
    build()
