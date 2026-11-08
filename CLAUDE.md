# CobbleEffort: project rules

Content-only Cobblemon sidemod (no code; one jar for Fabric and NeoForge) adding cosmetic forms via Cobblemon's
cosmetic slot and aspects. Built against Cobblemon 1.8.4 / Minecraft 1.21.1.

## Rules that always apply

1. **Cosmetics cover whole evolutionary lines.** Never give a cosmetic to a single stage. Collection configs
   (`tools/collections/<name>.json`) list one species per line in `lines`. The generator expands each one to its
   full family (pre-evolutions, evolutions, branches) from Cobblemon's species data, and fails if any member can't be
   retextured. Don't hand-edit generated files; change the config/style and rerun the generator.
2. **Mirror every vanilla resolver variation** (shiny, female, regional, model swaps, layers) with the cosmetic aspect
   added, in Cobblemon's order, in an `order: 9000` resolver. Each style sets `EMISSIVE` ("disable" for Backrooms,
   "retexture" for Thanksgiving/Halloween). Styles may set `FRAMES`/`FPS` for animated textures (Halloween: 4 @ 5fps).
3. **Collections don't overlap**: a species is in at most one collection, and each collection has its own cosmetic
   item. New lines come from `generate.py pick` (random, fully modelled, unused), plus any lines the user asks for
   by name (put those in `lines` first, then `pick` the rest). The generator enforces no overlap.
4. **Every jar produced is delivered as a zip containing the .jar.** `./gradlew build` → `build/libs/<name>.zip`;
   the bare jar is only an intermediate in `build/tmp/jar/`. Hand users the zip, never a loose jar.
5. Generated textures are adaptations of Cobblemon assets (CC BY-NC 3.0), plus Mega Showdown's (CC BY-NC-SA 4.0,
   under `compat/mega_showdown/`): keep `CREDITS.md` accurate; non-commercial.
6. **Always build for the user's mod stack** (`tools/compat/mods.json`): Mega Showdown (+ Extra Megas, Ores),
   Cobblemon: AllTheMons x Mega Showdown, Cobblemon Baby Legends, Cobblemon Lost Lore, Legendary Monuments, Fully
   Hisuian Starters RP, Poke Costumes DP. The generator reads their jars from `tools/compat/jars/` (gitignored; ask the
   user for any that are missing, and never commit them). It merges species data (other mods' pre-evolutions and evolutions
   join families), retextures forms from `derivatives: true` mods, passes through forms from the others, pins
   model+poser on every copy, and vendors Cobblemon's model/poser/animations when a no-derivatives mod overwrites
   them. Members modelled only by a no-derivatives mod go under `painted` in mods.json. When a mod is added to the
   stack, add it to mods.json and rebuild everything.

## Workflow

- Collections: `tools/collections/<name>.json` (aspect, feature, style, cosmetic_items, lines, optional `line_styles`)
  + `tools/styles/<style>.py` (`retexture(base, eyes, seed, shiny, frame=0, layer=False)`, `EMISSIVE`, optional
  `FRAMES`/`FPS`). `layer` is False for body textures, "emissive" or "plain" for layers. Optional
  `EXTRA_LAYERS` (list of {name, emissive, translucent, frames, fps}) + `extra_layer(name, base, eyes, seed, shiny,
  frame) -> Image | None` adds style-owned layers (named `cobbleeffort_<name>`), e.g. Christmas lights.
- Shared helpers: `styles/_horror.py` (Halloween), `styles/_festive.py` (Christmas), `styles/_spring.py` (Easter),
  `styles/_animatronic.py` (FNAF; one thin `fnaf_<look>.py` module per look).
- `WANTS_HINTS = True` on a style makes the generator pass `hints=` (from the model's `.geo.json`: `tex_size`,
  `head_front`, `head_top`, `torso_front` rects in geo UV units). Many Cobblemon models have separate eye cubes, so
  don't locate a face from the eye mask; use the hints.
- `addon_lines` in a collection config: cosmetics for Pokémon modelled by another mod (e.g. Xurkitree from ATM x MSD /
  Ultra-Beasts). Never copy or recolour another mod's art unless its licence allows it. Extract only the UV layout
  (`tools/addons/extract_layout.py`, run with `python3 -I` from outside their checkout) and paint an original texture in a
  builder (`tools/addons/<name>.py`: `build(out_tex_root, aspect, mod_id) -> (variations, manifest_entry)`).
  Disable their glow layers by name if the texture changes.
- When a requested Pokémon isn't modelled by Cobblemon, check the stack's mods first (ATM x MSD models many,
  e.g. Xurkitree), then other public mods (e.g. Cobblemon Ultra-Beasts).
- Regenerate: `python3 tools/generate.py --cobblemon <cobblemon>/common/src/main/resources build [collection]`
  (needs `assets/cobblemon` incl. posers/animations + `data/cobblemon`, the compat jars in `tools/compat/jars/`
  (Lost Lore: a directory of its `common/src/main/resources`), and Cobblemon's Kotlin sources next to the resources
  for converting Kotlin posers). The output is deterministic, so check reruns with md5.
- New lines: `python3 tools/generate.py --cobblemon ... pick --count 18 --seed <text>`.
- Build and check: `./gradlew build` (runs `validateData`). Bump `mod_version` in `gradle.properties` per update.
- Preview renders: `tools/preview/` (three.js in headless Chromium; `node render.js <cobblemon-res> ../../src/main/resources out manifest_<aspect>.json`;
  `EXTRA_ROOTS=<extracted jar>:...` for other mods' forms; manifest entries with `form` are other-mod forms).
