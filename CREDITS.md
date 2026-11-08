# Credits & licensing

## Cobblemon assets (modified)

Every texture under `src/main/resources/assets/cobbleeffort/textures/pokemon/` is an **adaptation** of a texture
from [Cobblemon](https://gitlab.com/cable-mc/cobblemon) (tag `1.8.4`, `common/src/main/resources/assets/cobblemon/textures/pokemon/`),
made by the Cobblemon team and contributors.

**Changes made:** `tools/generate.py` transforms the originals with one style per collection:

* **Backrooms** (`tools/styles/backrooms.py`, textures under `.../pokemon/backrooms/`): colours remapped to a
  plaster/clay palette; stain, grain, seam and row-shift effects added; eyes repainted, duplicated and smeared,
  located with Cobblemon's `*_alpha.png` eye masks.
* **Thanksgiving** (`tools/styles/thanksgiving.py`, textures under `.../pokemon/thanksgiving/`): colours remapped to
  an autumn harvest palette; edge "glaze" darkening and small maple-leaf stamps added; eyes left as in the original.
* **Halloween** (`tools/styles/halloween.py`, `halloween_skeleton.py`, `_horror.py`; textures under
  `.../pokemon/halloween/`): colours darkened and mottled; wounds, stitches, lumps, blood splatters and drips,
  extra eyes and toothed mouths painted on and animated across 4 frames; the Charmander line repainted as bone,
  ribs and rotting flesh, with its flame layer recoloured pink.
* **Christmas** (`tools/styles/christmas*.py`, `_festive.py`; textures under `.../pokemon/christmas/`): colours
  remapped to a Christmas palette; snow, snowflakes and light garlands added, with an extra emissive layer of
  twinkling bulbs; the Snorlax, Turtwig, Trubbish and Phantump lines repainted as Santa Claus, Christmas trees,
  wrapped gifts and Krampus.
* **Easter** (`tools/styles/easter*.py`, `_spring.py`; textures under `.../pokemon/easter/`): colours turned
  pastel (or chocolate for shinies); painted-egg bands, zigzag ribbons, daisies and sprinkles added; the Togepi
  line repainted as Easter eggs (golden Fabergé for shinies) and the Lopunny line as the Easter Bunny (a chocolate
  bunny for shinies).

Cobblemon ships many of its Pokémon models and textures under the **Creative Commons
Attribution-NonCommercial 3.0** licence (see the `license` files next to the models in Cobblemon's repository,
e.g. `assets/cobblemon/bedrock/pokemon/models/0082_magneton/license`):
<https://creativecommons.org/licenses/by-nc/3.0/>.
The adapted textures are shared under those same terms. **No commercial use.**

The `docs/*_preview.png` images show Cobblemon models rendered with both the original and the adapted
textures, and are covered by the same terms.

## New Pokémon models (update 6)

* **Armored Mewtwo** and **Shadow Lugia** are built on Cobblemon's own Mewtwo and Lugia models and textures
  (CC BY-NC 3.0, see above). Armour pieces are added to the Mewtwo model (`tools/creatures/armored_mewtwo.py`), and the
  Lugia texture is recoloured, with glow layers added (`tools/creatures/shadow_lugia.py`). Same licence terms apply.
* **Celesteela**, **Iron Boulder** and **Origin Dragon** are new models and textures made for this mod
  (`tools/creatures/`), designed after the official Pokémon designs. The Origin Dragon is a fan concept (a fusion of
  Kyurem, Reshiram and Zekrom), not an official Pokémon.
* Species data for Celesteela and Iron Boulder is Cobblemon's own; this mod only switches them on and adds spawns.

## Code and data

The build scripts, generator, data and resolver JSON are licensed under the
[Mozilla Public License 2.0](LICENSE), the same licence Cobblemon's code uses.

## Inspiration

* **CobblemonMoreCosmetics** (Archaeus) set the "more cosmetic forms through the cosmetic slot" model this mod follows.
* **The Backrooms** by Kane Parsons (Kane Pixels) is the source of the Still Lifes and the Level 0 look. This is fan
  work; no footage or art from the series is used.

Pokémon and all related names are trademarks of Nintendo, Game Freak and The Pokémon Company.
CobbleEffort is not affiliated with or endorsed by them, the Cobblemon team, or Kane Parsons / A24.
