# CobbleEffort: project rules

Content-only Cobblemon sidemod (no code; one jar for Fabric and NeoForge) adding cosmetic forms via Cobblemon's
cosmetic slot and aspects. Built against Cobblemon 1.8.4 / Minecraft 1.21.1.

## Rules that always apply

1. **Cosmetics cover whole evolutionary lines.** Never give a cosmetic to a single stage. Collection configs
   (e.g. `tools/backrooms_species.json`) list one species per line in `lines`. The generator expands each one to its
   full family (pre-evolutions, evolutions, branches) from Cobblemon's species data, and fails if any member can't be
   retextured. Don't hand-edit generated species lists; change the config and rerun the generator.
2. **Mirror every vanilla resolver variation** (shiny, female, regional, model swaps, layers) with the cosmetic aspect
   added, in Cobblemon's order, in an `order: 9000` resolver. Emissive layers are disabled for Still Lifes.
3. **Every jar produced is delivered as a zip containing the .jar.** `./gradlew build` → `build/libs/<name>.zip`;
   the bare jar is only an intermediate in `build/tmp/jar/`. Hand users the zip, never a loose jar.
4. Generated textures are adaptations of Cobblemon assets (CC BY-NC 3.0): keep `CREDITS.md` accurate; non-commercial.

## Workflow

- Regenerate: `python3 tools/generate_backrooms.py --cobblemon <cobblemon>/common/src/main/resources`
  (needs `assets/cobblemon` + `data/cobblemon/species` + `data/cobblemon/cosmetic_items`).
- Build and check: `./gradlew build` (runs `validateData`).
- Preview renders: `tools/preview/` (three.js in headless Chromium; reads `tools/preview/manifest.json`).
