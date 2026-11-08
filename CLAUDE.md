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
5. Generated textures are adaptations of Cobblemon assets (CC BY-NC 3.0): keep `CREDITS.md` accurate; non-commercial.

## Workflow

- Collections: `tools/collections/<name>.json` (aspect, feature, style, cosmetic_items, lines, optional `line_styles`)
  + `tools/styles/<style>.py` (`retexture(base, eyes, seed, shiny, frame=0, layer=False)`, `EMISSIVE`, optional
  `FRAMES`/`FPS`). `layer` is False for body textures, "emissive" or "plain" for layers.
- Regenerate: `python3 tools/generate.py --cobblemon <cobblemon>/common/src/main/resources build [collection]`
  (needs `assets/cobblemon` + `data/cobblemon/species` + `data/cobblemon/cosmetic_items`).
- New lines: `python3 tools/generate.py --cobblemon ... pick --count 18 --seed <text>`.
- Build and check: `./gradlew build` (runs `validateData`). Bump `mod_version` in `gradle.properties` per update.
- Preview renders: `tools/preview/` (three.js in headless Chromium; `node render.js <cobblemon-res> ../../src/main/resources out manifest_<aspect>.json`).
