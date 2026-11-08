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
* **Five Nights at Freddy's** (`tools/styles/fnaf_*.py`, `_animatronic.py`; textures under `.../pokemon/animatronic/`):
  colours remapped per look (classic, withered, toy, springtrap, nightmare, funtime, scrap); felt, seams, rivets,
  grime, endoskeleton tears, teeth and glowing eyes added; the Teddiursa, Torchic and Sandile lines repainted after
  Freddy, Chica and Foxy.
* **Ice Sculptures** (`tools/styles/ice_sculpture.py`; textures under `.../pokemon/ice_sculpture/`): colours remapped
  to an ice palette by lightness; facets, refraction streaks, cracks, bubbles and a frosted rim added; eyes darkened;
  an extra emissive layer of twinkling glints; shinies tinted teal-to-violet.
* **Stone Statues** (`tools/styles/stone_statue.py`; textures under `.../pokemon/stone_statue/`): colours remapped to
  stone by lightness; grain, speckles, chisel strokes, weathered edges, cracks, moss and lichen added; shinies remapped
  to veined white marble with gilded eyes.
* **Naruto** (`tools/styles/naruto_*.py`, `_shinobi.py`; textures under `.../pokemon/shinobi/`): colours remapped per
  look; clouds, flak vests, forehead protectors, masks, sage pigment, flame hems, whiskers, swirls, veins, Karma
  seals and glowing eyes added; the Vulpix line repainted as Kurama with a flickering chakra layer.

Cobblemon ships many of its Pokémon models and textures under the **Creative Commons
Attribution-NonCommercial 3.0** licence (see the `license` files next to the models in Cobblemon's repository,
e.g. `assets/cobblemon/bedrock/pokemon/models/0082_magneton/license`):
<https://creativecommons.org/licenses/by-nc/3.0/>.
The adapted textures are shared under those same terms. **No commercial use.**

The `docs/*_preview.png` images show Cobblemon models rendered with both the original and the adapted
textures, and are covered by the same terms.

## Other mods' models (addon lines)

* **Xurkitree as Sasuke** is made for the Xurkitree model from **Cobblemon Ultra-Beasts** by BileulDevs
  (<https://github.com/BileulDevs/cobblemon-ultra-beasts>). That model and its textures are **not** included in
  CobbleEffort. Only its UV layout (cube positions, no art) is stored in `tools/addons/ultrabeasts_xurkitree_layout.json`
  so an original texture can be painted to fit it. The cosmetic works only with Ultra-Beasts installed.

## Code and data

The build scripts, generator, data and resolver JSON are licensed under the
[Mozilla Public License 2.0](LICENSE), the same licence Cobblemon's code uses.

## Inspiration

* **CobblemonMoreCosmetics** (Archaeus) set the "more cosmetic forms through the cosmetic slot" model this mod follows.
* **The Backrooms** by Kane Parsons (Kane Pixels) is the source of the Still Lifes and the Level 0 look. This is fan
  work; no footage or art from the series is used.

* **Five Nights at Freddy's** by Scott Cawthon inspired collection #6 (fan work; no art or assets from the games
  are used).

* **Naruto**, **Naruto Shippuden** and **Boruto** by Masashi Kishimoto (and Mikio Ikemoto / Ukyo Kodachi) inspired
  collection #9 (fan work; no art from the series is used).

Pokémon and all related names are trademarks of Nintendo, Game Freak and The Pokémon Company.
CobbleEffort is not affiliated with or endorsed by them, the Cobblemon team, or Kane Parsons / A24.
