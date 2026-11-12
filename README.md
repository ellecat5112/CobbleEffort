# CobbleEffort

A Cobblemon sidemod that adds **extra cosmetic forms** for existing Cobblemon models, in the spirit of
[CobblemonMoreCosmetics](https://modrinth.com/resourcepack/cobblemonmorecosmetics). It changes no models:
each form is a new texture applied through Cobblemon's own cosmetic-slot and aspect system.

**Collections so far:** #1 Backrooms (41 Pokémon) · #2 Thanksgiving (37 Pokémon) · #3 Halloween (33 Pokémon) · #4 Christmas (40 Pokémon) · #5 Easter (40 Pokémon) · #6 Five Nights at Freddy's (40 Pokémon) · #7 Ice Sculptures (42 Pokémon) · #8 Stone Statues (41 Pokémon) · #9 Naruto (35 Pokémon + Xurkitree) · #10 Trans Pride (34 Pokémon) · #11 Tarot (41 Pokémon) · #12 Game Boy Sprites (33 Pokémon) · #13 Cosmic Starlight (34 Pokémon) · #14 80s Neon Cyberpunk (34 Pokémon) · #15 Bioluminescent Deep Sea (44 Pokémon) · #16 Stained Glass (37 Pokémon) · #17 Steampunk (34 Pokémon).

**Creative tab (since v0.15.1):** every collection's cosmetic items and the Paradox mega stones are in the
**CobbleEffort** tab of the creative inventory (the stones show when Mega Showdown is installed).

**House rule: every cosmetic covers whole evolutionary lines.** If one stage gets a form, every pre-evolution,
evolution and branch of that Pokémon gets it too. The generator enforces this (see [Collection rules](#collection-rules)).

**Built for a mod stack (since v0.10.0).** CobbleEffort is made to run alongside Mega Showdown (+ Extra Megas,
Ores), Cobblemon: AllTheMons x Mega Showdown, Cobblemon Baby Legends, Cobblemon Lost Lore, Legendary Monuments,
the Fully Hisuian Starters resource pack, the Poke Costumes data pack and the Planeta Cobblemon free pack (through a
bridge, see [Planeta Cobblemon](#planeta-cobblemon-free-pack-the-bridge)) (all checked against their files). Megas, Gigantamax and other new forms keep
the cosmetic, and other mods' model replacements don't break it. See [Compatibility](#compatibility).

## Collection #1: Backrooms (Still Lifes)

18 evolutionary lines (**41 Pokémon**) re-imagined as **Still Lifes** from Kane Pixels' *Backrooms*. A Still Life is an imperfect
copy of something real that the Backrooms rebuilt from memory. Here that means:

* colour drained into a sallow **plaster / wet-clay** palette, lit by Level 0's mono-yellow fluorescent light
* **damp blotches**, clay grain and wobbly **seams** where the "pieces" were pressed together
* rows that **slipped sideways**, like a bad copy
* **matte painted-on eyes** with a second, misplaced set just below and a **smear** running down from them
* no glow: emissive layers (Magnezone, Sizzlipede, Centiskorch, Nymble, Lokix) are switched off

Shiny Pokémon get their own Still Life, built from the shiny texture so a faint trace of the shiny colour shows through.

![Original vs. Still Life](docs/backrooms_preview.png)

| Line | Pokémon |
|------|---------|
| Magnemite | Magnemite → Magneton → Magnezone |
| Omanyte | Omanyte → Omastar |
| Nincada | Nincada → Ninjask / Shedinja |
| Torkoal | Torkoal |
| Anorith | Anorith → Armaldo |
| Snorunt | Snorunt → Glalie / Froslass |
| Piplup | Piplup → Prinplup → Empoleon |
| Blitzle | Blitzle → Zebstrika |
| Shelmet | Shelmet → Accelgor |
| Fletchling | Fletchling → Fletchinder → Talonflame |
| Swirlix | Swirlix → Slurpuff |
| Amaura | Amaura → Aurorus |
| Xerneas | Xerfawn (Baby Legends), Xerneas |
| Silicobra | Silicobra → Sandaconda |
| Sizzlipede | Sizzlipede → Centiskorch |
| Impidimp | Impidimp → Morgrem → Grimmsnarl |
| Nymble | Nymble → Lokix |
| Maschiff | Maschiff → Mabosstiff |

The 18 lines were picked at random (`random.Random("kane-pixels-level-0").sample(...)`) and then expanded to
their full evolutionary families from Cobblemon's species data. Torkoal has no evolutions; Xerneas' line includes Baby Legends' Xerfawn.

### How to get one

**Cosmetic slot (survival):** give a supported Pokémon one **Yellow Carpet** (Level 0's damp carpet) as its
*cosmetic item*, the same way you would put any Cobblemon cosmetic on it (open your Pokémon's interaction
menu while holding the carpet and choose the cosmetic slot). Take the carpet back to undo it.

**Commands (testing / servers):** the form is also a species feature, so it works anywhere Pokémon properties do:

```
/pokegive magnemite backrooms
/pokegive glalie backrooms shiny
/spawnpokemon slurpuff backrooms
```

**Pack makers:** the accepted items come from the item tag `#cobbleeffort:backrooms_cosmetics`. Add items to it
with a datapack (`data/cobbleeffort/tags/item/backrooms_cosmetics.json`).

## Collection #2: Thanksgiving (Harvest)

18 more evolutionary lines (**37 Pokémon**) dressed for a Thanksgiving table:

* colours moved onto a **harvest palette** that keeps the original markings readable: deep reds become cranberry,
  pinks peach, oranges pumpkin, yellows maize gold, greens sage, blues and cyans chestnut and toasted squash,
  purples plum
* greys, whites and blacks turned into warm neutrals: **pie-crust cream, cinnamon, dark roast**
* a golden-brown **roast glaze** along the edges of each painted area
* a few **fallen maple leaves** (pumpkin, amber, gold) stuck to the fur
* **eyes keep their original colours**, so every Pokémon still looks like itself
* **shiny → golden harvest**: everything pulled toward honey-gold
* glowing parts keep glowing, recoloured like candlelight

![Original vs. Harvest](docs/thanksgiving_preview.png)

| Line | Pokémon |
|------|---------|
| Squirtle | Squirtle → Wartortle → Blastoise |
| Meowth | Meowth (incl. Alolan & Galarian) → Persian / Perrserker |
| Porygon | Porygon → Porygon2 → Porygon-Z |
| Corsola | Corsola (incl. Galarian) → Cursola |
| Miltank | Miltank |
| Kecleon | Kecleon |
| Bagon | Bagon → Shelgon → Salamence |
| Croagunk | Croagunk → Toxicroak |
| Carnivine | Carnivine |
| Munna | Munna → Musharna |
| Tirtouga | Tirtouga → Carracosta |
| Ferroseed | Ferroseed → Ferrothorn |
| Mienfoo | Mienfoo → Mienshao |
| Grubbin | Grubbin → Charjabug → Vikavolt |
| Bounsweet | Bounsweet → Steenee → Tsareena |
| Pyukumuku | Pyukumuku |
| Squawkabilly | Squawkabilly (all four plumages) |
| Wiglett | Wiglett → Wugtrio |

Picked with `generate.py pick --count 18 --seed thanksgiving-2026`: 18 random lines out of the 417 that are fully
modelled in Cobblemon and not already in another collection.

### How to get one

Give a supported Pokémon one **Pumpkin Pie** as its cosmetic item. With commands: `/pokegive miltank thanksgiving`,
`/pokegive squirtle thanksgiving shiny`. Pack makers can extend the item tag `#cobbleeffort:thanksgiving_cosmetics`.

## Collection #3: Halloween (Nightmare) ⚠️ gore

> **Content warning:** this collection is deliberately horrific. It has blood, gore, rotting flesh, wounds and
> body horror. Players who don't want it simply never use the Carved Pumpkin cosmetic.

18 evolutionary lines (**33 Pokémon**) turned into nightmares. These are **animated textures** (4 frames, 5 fps):

* colour drained and darkened, mottled with **bruise-purple and rot-green**, grime along every edge
* swollen **bruised lumps**, **torn patches of raw flesh**, some crudely **stitched** shut
* **blood splatters** with drips running down, and a drop that creeps further each frame
* **lots of extra, misplaced eyes**: bloodshot, with darting pupils, some blinking, some weeping blood
* the Pokémon's own eyes turn blood red, and **misplaced copies** of them grow elsewhere on the body
* **mouths full of jagged, yellowed, bloody teeth that gnash** open and shut
* shiny → **pale corpse**: cold grey-blue skin, so the blood stands out more
* glowing parts become a sickly **ghost-green**. Full-body glow layers (Shinx line) keep only their hottest spots,
  so they don't hide the gore

**Charmander line ("Bone-Rot"):** Charmander, Charmeleon and Charizard are **skeletons with flesh rotting off the
bones**: cracked ivory bone, an exposed **rib cage** where the belly was, ragged rotting flesh with blood, ichor and
maggots, hollow eye sockets with a flickering pink ember, a gnashing skeletal grin, and the tail fire burning
**pink**. Shiny Charmanders have charred black bones.

![Original vs. Nightmare](docs/halloween_preview.png)

![Gnashing animation](docs/halloween_animation.gif)

| Line | Pokémon |
|------|---------|
| **Charmander** (Bone-Rot) | Charmander → Charmeleon → Charizard |
| Koffing | Koffing → Weezing (incl. Galarian) |
| Sentret | Sentret → Furret |
| Misdreavus | Misdreavus → Mismagius |
| Absol | Absol |
| Shinx | Shinx → Luxio → Luxray |
| Glameow | Glameow → Purugly |
| Timburr | Timburr → Gurdurr → Conkeldurr |
| Sigilyph | Sigilyph |
| Ducklett | Ducklett → Swanna |
| Pancham | Pancham → Pangoro |
| Comfey | Comfey |
| Komala | Komala |
| Dracovish | Dracovish |
| Tarountula | Tarountula → Spidops |
| Nacli | Nacli → Naclstack → Garganacl |
| Klawf | Klawf |
| Veluza | Veluza |

The Charmander line was chosen by request. The other 17 were picked with
`generate.py pick --count 17 --seed halloween-2026` from the 398 remaining eligible lines.

Models aren't changed (this mod only retextures). The deformities, extra eyes and mouths are painted onto the
existing models.

### How to get one

Give a supported Pokémon a **Carved Pumpkin** as its cosmetic item. With commands: `/pokegive charmander halloween`,
`/pokegive tarountula halloween shiny`. Pack makers can extend the item tag `#cobbleeffort:halloween_cosmetics`.

## Collection #4: Christmas

18 evolutionary lines (**40 Pokémon**). Four of them have their own costume:

| Line | Look |
|------|------|
| **Munchlax → Snorlax** | **Santa Claus**: red suit, a red coat front with white fur trim, a black belt with a gold buckle, and a white fluffy beard and cuffs. Shiny: an old-world **Father Christmas** in green |
| **Turtwig → Grotle → Torterra** | **Christmas tree**: every leafy part becomes a pine tree hung with baubles and gold tinsel, wound with **twinkling fairy lights**, and topped with snow. Shiny: a white **flocked** tree |
| **Trubbish → Garbodor** | **Christmas gift**: wrapped in candy-stripe paper with a green satin ribbon, a bow and a gift tag. Shiny: gold foil with a red ribbon |
| **Phantump → Trevenant** | **Krampus**: shaggy black goat fur, ridged ram's horns, **red eyes that glow in the dark**, a long red tongue, and iron chains hung with gold bells. Shiny: a white-furred Krampus with gold horns |

The other 14 lines get the **Festive** look: a Christmas palette (crimson, gold, pine, icy blue, berry, with snowy
whites), snow settled on top of every surface, snowflakes, and strings of **fairy lights that glow in the dark and
twinkle**. Shiny: **Frosted** (silver, ice and snow).

Weedle → Kakuna → Beedrill · Mankey → Primeape → Annihilape · Shellder → Cloyster · Girafarig → Farigiraf ·
Pineco → Forretress · Heracross · Makuhita → Hariyama · Spiritomb · Skorupi → Drapion ·
Sewaddle → Swadloon → Leavanny · Yamask (incl. Galarian) → Cofagrigus / Runerigus · Larvesta → Volcarona ·
Litleo → Pyroar · Dreepy → Drakloak → Dragapult

The four costume lines were chosen by request; the other 14 were picked with
`generate.py pick --count 14 --seed christmas-2026` from the 377 remaining eligible lines.

![Original vs. Christmas](docs/christmas_preview.png)

![Twinkling lights](docs/christmas_lights.gif)

### How to get one

Give a supported Pokémon a **Snowball** as its cosmetic item. With commands: `/pokegive snorlax christmas`,
`/pokegive turtwig christmas shiny`. Pack makers can extend the item tag `#cobbleeffort:christmas_cosmetics`.

## Collection #5: Easter

18 evolutionary lines (**40 Pokémon**). Two of them have their own costume:

| Line | Look |
|------|------|
| **Togepi → Togetic → Togekiss** | **Easter egg**: the white shell and body become a hand-painted egg with pastel bands of solid colour, zigzags, polka dots and white pin-stripes. Togepi's red and blue triangles are repainted raspberry and periwinkle as part of the decoration. Shiny: a **golden Fabergé egg** set with ruby, sapphire, emerald and pearl |
| **Buneary → Lopunny** | **Easter Bunny**: soft white bunny fur with a lavender shadow, pastel-pink fluffy ears, spring daisies and a painted-egg ribbon. Shiny: a **chocolate bunny** in milk and white chocolate with a dark drizzle and gold-foil trim |

The other 16 lines get the **Pastel** look: every colour becomes its soft pastel version, plus a hand-painted
zigzag ribbon like the decoration round an Easter egg and little spring daisies. Shiny: **chocolate** with rainbow
candy sprinkles.

Jigglypuff (incl. Igglybuff, Wigglytuff) · Diglett → Dugtrio · Aerodactyl · Chinchou → Lanturn ·
Mareep → Flaaffy → Ampharos · Smeargle · Slakoth → Vigoroth → Slaking · Latot (Baby Legends) → Latias / Latios · Drifloon → Drifblim ·
Roggenrola → Boldore → Gigalith · Litten → Torracat → Incineroar · Cutiefly → Ribombee · Snom → Frosmoth ·
Eternatus · Wattrel → Kilowattrel · Finizen → Palafin

Togepi and Lopunny were chosen by request. The other 16 were picked with `generate.py pick --count 16 --seed easter-2027`
from the 361 remaining eligible lines.

![Original vs. Easter](docs/easter_preview.png)

![Easter eggs and bunnies, normal and shiny](docs/easter_specials.png)

### How to get one

Give a supported Pokémon an **Egg** as its cosmetic item. With commands: `/pokegive togepi easter`,
`/pokegive lopunny easter shiny`. Pack makers can extend the item tag `#cobbleeffort:easter_cosmetics`.

## Collection #6: Five Nights at Freddy's (Animatronics)

18 evolutionary lines (**40 Pokémon**) rebuilt as pizzeria animatronics, with **eyes that glow in the dark**
(an extra emissive layer). Three of them are the classic cast:

| Line | Look | Shiny |
|------|------|-------|
| **Teddiursa → Ursaring → Ursaluna** | **Classic Freddy**: brown felt bear, pale muzzle, black top hat, bow tie, animatronic grin, glowing blue eyes | **Golden Freddy** |
| **Torchic → Combusken → Blaziken** | **Classic Chica**: yellow felt chicken, orange beak and feet, the "LET'S EAT!!!" bib, teeth, glowing violet eyes | **Toy Chica**: brighter, with rosy cheeks |
| **Sandile → Krokorok → Krookodile** | **Classic Foxy**: rust-red fox suit torn open to the metal endoskeleton, eye patch with strap, sharp teeth, one glowing amber eye | **Mangle**: white and pink |

The other 15 lines each wear the look of one game (dealt round-robin):

| Game | Look | Lines |
|------|------|-------|
| FNAF 1 | **Classic**: worn felt, stitched seams, rivets, square teeth, white pinprick eyes | Seel, Pidove, Fidough |
| FNAF 2 | **Withered**: faded, filthy, torn to the endoskeleton and wires, one eye dark | Horsea, Audino |
| FNAF 2 | **Toy**: glossy plastic, brighter colours, rosy cheeks, shiny eyes | Sunkern, Maractus |
| FNAF 3 | **Springtrap**: rotten olive-yellow suit, stains, wires | Murkrow, Zorua |
| FNAF 4 | **Nightmare**: near-black, jagged tears lined with teeth, red pinprick eyes | Unown, Gothita |
| FNAF 5 | **Funtime**: white glossy plating, pink/purple panels, faceplate seams, rosy cheeks | Finneon, Vanillite |
| FNAF 6 | **Scrap**: rusted and patched with mismatched panels, burns and wires | Patrat, Helioptile |

(each with its whole evolutionary line). Shinies of the generic looks are **Golden** animatronics.

Teddiursa, Torchic and Sandile were chosen by request. The other 15 were picked with `generate.py pick --count 15 --seed fnaf-1987`.

![Freddy, Chica and Foxy](docs/fnaf_characters.png)

![Original vs. animatronic](docs/fnaf_preview.png)

### How to get one

Give a supported Pokémon a **Clock** (the night shift, 12 to 6 AM) as its cosmetic item. With commands:
`/pokegive teddiursa animatronic`, `/pokegive sandile animatronic shiny`. Pack makers can extend the item tag
`#cobbleeffort:animatronic_cosmetics`.

## Collection #7: Ice Sculptures

18 evolutionary lines (**42 Pokémon**) carved out of a block of ice:

* recoloured in clear **glacier-ice blues**, mapped from each Pokémon's own light and shade, so every marking
  is still there, chiselled into the ice
* **faceted chisel planes** that each catch the light differently, **light streaks** refracting through,
  hairline **cracks** and trapped **air bubbles**
* a **frosted rim** along every edge, and **eyes carved** as deeper-blue hollows
* a layer of **glints that twinkle and glow in the dark** (4-frame emissive layer)
* glowing parts (Crocalor's and Skeledirge's fire, for example) turn into an **icy cyan glow**
* shiny: **Aurora Ice**, the same sculpture shimmering teal-to-violet like the northern lights

Zubat → Golbat → Crobat · Oddish → Gloom → Vileplume / Bellossom · Drowzee → Hypno · Lickitung → Lickilicky ·
Shuckle · Whismur → Loudred → Exploud · Cranidos → Rampardos · Hippopotas → Hippowdon · Snover → Abomasnow ·
Axew → Fraxure → Haxorus · Skiddo → Gogoat · Dedenne · Poipole → Naganadel · Sobble → Drizzile → Inteleon ·
Wooloo → Dubwool · Sprigatito → Floragato → Meowscarada · Fuecoco → Crocalor → Skeledirge · Toedscool → Toedscruel

Picked with `generate.py pick --count 18 --seed ice-sculpture-2026` from the 327 remaining eligible lines.

![Original vs. ice sculpture](docs/ice_sculpture_preview.png)

![Normal and shiny Aurora Ice](docs/ice_sculpture_closeup.png)

![Twinkling glints](docs/ice_sculpture_glints.gif)

### How to get one

Give a supported Pokémon **Ice, Packed Ice or Blue Ice** as its cosmetic item. With commands:
`/pokegive axew ice_sculpture`, `/pokegive sprigatito ice_sculpture shiny`. Pack makers can extend the item tag
`#cobbleeffort:ice_sculpture_cosmetics`.

## Collection #8: Stone Statues

18 evolutionary lines (**41 Pokémon**) turned into solid stone statues:

* **granite-grey stone**, mapped from each Pokémon's own light and shade, so its markings remain as carved relief
* mottled **stone grain** with speckles and fine **chisel strokes**
* **weathering**: sunlit top edges, shadowed undersides, small chips, dark **cracks** and the odd patch of
  **moss and lichen**
* **blank, carved eyes**, like a real statue
* **no glow**: flames, lights and other glowing parts are turned off or turned to stone (Quilava's and
  Typhlosion's flames become carved stone flames)
* shiny: polished white **marble** with flowing grey veins and **gold-leaf eyes**

Pidgey → Pidgeotto → Pidgeot · Goldeen → Seaking · Tauros (incl. Paldean breeds) · Cyndaquil → Quilava → Typhlosion
(incl. Hisuian) · Qwilfish → Overqwil · Phanpy → Donphan · Aron → Lairon → Aggron · Trapinch → Vibrava → Flygon ·
Cherubi → Cherrim · Deerling → Sawsbuck (all seasons) · Fennekin → Braixen → Delphox · Rowlet → Dartrix → Decidueye ·
Rookidee → Corvisquire → Corviknight · Rolycoly → Carkol → Coalossal · Stonjourner · Regidrago ·
Tadbulb → Bellibolt · Capsakid → Scovillain

Picked with `generate.py pick --count 18 --seed stone-statue-2026` from the 309 remaining eligible lines.

![Original vs. stone statue](docs/stone_statue_preview.png)

![Stone and shiny marble](docs/stone_statue_closeup.png)

### How to get one

Give a supported Pokémon **Stone, Smooth Stone or Chiseled Stone Bricks** as its cosmetic item. With commands:
`/pokegive aron stone_statue`, `/pokegive fennekin stone_statue shiny`. Pack makers can extend the item tag
`#cobbleeffort:stone_statue_cosmetics`.

## Collection #9: Naruto / Naruto Shippuden / Boruto (Shinobi)

18 evolutionary lines (**35 Pokémon, plus Xurkitree**) as shinobi. Two of them are characters:

| Line | Look | Shiny |
|------|------|-------|
| **Vulpix → Ninetales** (incl. Alolan) | **Kurama**, the Nine-Tails: orange fox fur, black eye markings and ear tips, red slit eyes, and an orange chakra glow flickering on every edge | **Kurama Link Mode**: gold with black seal lines |
| **Xurkitree** ⚠️ *needs AllTheMons x Mega Showdown (or Cobblemon Ultra-Beasts) for its model* | **Sasuke Uchiha**: spiky blue-black star "hair", glowing Sharingan eyes, the Uchiha crest on the back, navy sleeves and trousers with white shin wraps, a purple rope belt, and **Chidori** lightning crackling on both claws (glowing, animated) | Rinnegan purple, with purple-black lightning |

The other 16 lines each get one look:

| Look | What it is | Lines |
|------|------------|-------|
| **Akatsuki** | black cloak with red, white-edged clouds; glowing Sharingan eyes | Venonat, Swinub, Cetoddle |
| **Leaf Shinobi** | navy-toned uniform, olive flak vest with scroll pockets, Leaf forehead protector | Onix, Mantine, Iron Leaves |
| **ANBU** | grey armour, white porcelain mask with red markings | Voltorb, Solrock |
| **Sage Mode** | orange sage pigment, glowing toad eyes, red cloak hem with black flames | Cubone, Popplio |
| **Uzumaki** | Naruto's orange and black, whisker marks, red swirl, forehead protector | Hoothoot, Toxel |
| **Byakugan** | pale lavender robes, pupil-less glowing eyes, bulging veins | Spinarak, Cufant |
| **Karma** (Boruto) | a bold black Karma seal and one glowing blue Jōgan eye | Dunsparce, Rellor |

(each with its whole evolutionary line). Vulpix was chosen by request. The other 16 were picked with
`generate.py pick --count 16 --seed naruto-shippuden`.

**About Xurkitree:** Cobblemon 1.8.4 has no Xurkitree model. **Cobblemon: AllTheMons x Mega Showdown** ships one,
and so does **Cobblemon Ultra-Beasts** (by BileulDevs). ATM's is the same model with a few small glow bulbs added.
CobbleEffort doesn't include either model or any of their art: the Sasuke texture is painted from scratch onto the
union of both UV layouts, so it fits whichever one is installed. Without either mod it does nothing.

![Kurama and Sasuke](docs/naruto_kurama_sasuke.png)

![Original vs. shinobi](docs/naruto_preview.png)

### How to get one

Give a supported Pokémon **Flint** (a kunai) as its cosmetic item. With commands: `/pokegive vulpix shinobi`,
`/pokegive xurkitree shinobi shiny`. Pack makers can extend the item tag `#cobbleeffort:shinobi_cosmetics`.

## Collection #10: Trans Pride

18 evolutionary lines (**34 Pokémon**) wearing the transgender pride flag:

* the flag's five stripes (light blue, pink, white, pink, light blue) run across the **whole body from head to toe**.
  The generator works out how high on the model every texture pixel sits, so a stripe lines up across head, arms,
  body and legs instead of following the texture layout
* each stripe keeps the Pokémon's own light and shade, so markings, fur and plating still read, and outlines stay dark
* the eyes keep their own colours
* glowing parts (Charcadet's line, Lunatone's eyes…) glow in the flag's colours
* megas (Mega Tyranitar, Mega Banette, Mega Meganium) wear it too
* shiny: pastel glitter over the stripes, plus a layer of sparkles that twinkle and glow in the dark

Growlithe → Arcanine (incl. Hisuian) · Chikorita → Bayleef → Meganium · Larvitar → Pupitar → Tyranitar ·
Zigzagoon → Linoone → Obstagoon (incl. Galarian) · Lunatone · Shuppet → Banette · Bronzor → Bronzong · Azelf ·
Panpour → Simipour · Tympole → Palpitoad → Seismitoad · Emolga · Cobalion · Thundurus · Stufful → Bewear ·
Togedemaru · Dhelmise · Lechonk → Oinkologne · Charcadet → Armarouge / Ceruledge

Picked with `generate.py pick --count 18 --seed trans-pride-2026` from the 307 remaining eligible lines.

![Original vs. trans pride](docs/trans_pride_preview.png)

![Shinies: glitter and sparkles](docs/trans_pride_shiny.png)

### How to get one

Give a supported Pokémon a **Light Blue, Pink or White Banner** (the flag's colours) as its cosmetic item. With
commands: `/pokegive togedemaru trans_pride`, `/pokegive emolga trans_pride shiny`. Pack makers can extend the item
tag `#cobbleeffort:trans_pride_cosmetics`.

## Collection #11: Tarot (Major Arcana)

18 evolutionary lines (**41 Pokémon**), each one card of the Major Arcana:

* each line is its card, in that card's colours with a faint pattern behind (harlequin diamonds, pomegranates,
  little hearts, a starry canopy, falling snow, chains, bricks, falling drops, sunflowers…)
* a **tarot card on the chest**: a gold frame round parchment with the card's symbol, drawn from the traditional
  imagery: the Fool's white rose, the High Priestess's crescent between the pillars, the Emperor's ankh, the Lovers'
  heart, the Chariot's winged disc, Strength's infinity sign, the Hermit's lantern, the Wheel, Justice's scales,
  Death's white rose banner, Temperance's triangle in a square, the Devil's inverted pentagram, the Tower struck by
  lightning, the Star, the Moon, the Sun, Judgement's cross banner and the World's laurel wreath
* the card's **Roman numeral** on the forehead, **glowing eyes**, and a **gold-foil sheen** that sweeps over the
  gilding (stars twinkle)
* forms from Mega Showdown and Extra Megas (Mega Sharpedo, Mega Altaria, Mega Infernape, Gigantamax Flapple and
  Appletun) are cards too
* shiny: the card **reversed**: colours turned round, silver foil, the symbol and numeral upside down

Mr. Mime → Mr. Rime (incl. Mime Jr., Galarian): 0 The Fool · Carbink: II The High Priestess ·
Jangmo-o → Hakamo-o → Kommo-o: IV The Emperor · Applin → Flapple / Appletun / Dipplin → Hydrapple: VI The Lovers ·
Walking Wake: VII The Chariot · Cubchoo → Beartic: VIII Strength · Pincurchin: IX The Hermit ·
Delibird: X Wheel of Fortune · Zangoose: XI Justice · Carvanha → Sharpedo: XIII Death · Swablu → Altaria: XIV
Temperance · Salandit → Salazzle: XV The Devil · Chimchar → Monferno → Infernape: XVI The Tower ·
Azurill → Marill → Azumarill: XVII The Star · Kabuto → Kabutops: XVIII The Moon · Lotad → Lombre → Ludicolo:
XIX The Sun · Spearow → Fearow: XX Judgement · Cosmog → Cosmoem → Solgaleo / Lunala: XXI The World

Picked with `generate.py pick --count 18 --seed tarot-major-arcana` from the 289 remaining eligible lines; each line
was given the card that suits it (Mr. Mime the Fool, Kabuto the Moon's crayfish, Chimchar's fire the Tower…).

![Original vs. tarot](docs/tarot_preview.png)

### How to get one

Give a supported Pokémon **Paper** as its cosmetic item. With commands: `/pokegive azumarill tarot`,
`/pokegive zangoose tarot shiny`. Pack makers can extend the item tag `#cobbleeffort:tarot_cosmetics`.

## Collection #12: Game Boy Sprites (2D)

18 evolutionary lines (**33 Pokémon**) turned into flat **Game Boy sprites**, made of layers of 2D artwork:

* the Pokémon is drawn from its own model in its idle pose, **one pixel per model unit**, in the Game Boy's four
  greens, with dark outlines (round the sprite and wherever one part overlaps another), light from the top left and
  a little dithering
* the sprite is split by depth into a few **flat layers** stacked a little apart: head-on it is a sprite, from an
  angle the layers pop out like a paper cut-out, and from behind you see its **back sprite**
* it moves like one: an 8-bit **bob** when standing, a **hop** on every step, a jump for its cry
* every form gets its own sprite: female forms, regional forms, Gigantamax Kingler, the Hisuian/Paldean forms…
* shiny: a **Game Boy Color** sprite, in a four-colour palette taken from the shiny's own colours

Doduo → Dodrio · Krabby → Kingler · Tyrogue → Hitmonlee / Hitmonchan / Hitmontop · Aipom → Ambipom ·
Snubbull → Granbull · Minun · Tropius · Chingling → Chimecho · Relicanth · Pansear → Simisear ·
Bunnelby → Diggersby · Honedge → Doublade → Aegislash · Volcanion · Yungoos → Gumshoos · Minior ·
Shroodle → Grafaiai · Flittle → Espathra · Ogerpon

Picked with `generate.py pick --count 18 --seed gameboy-2d-sprites` from the 271 remaining eligible lines. The
sprites are rendered by the generator from Cobblemon's own models (`tools/sprites.py`, collection `"mode": "sprite"`):
no art from the games is used.

![Original vs. Game Boy sprite](docs/gameboy_preview.png)

### How to get one

Give a supported Pokémon **Lime Dye** (the Game Boy's green) as its cosmetic item. With commands:
`/pokegive krabby gb_sprite`, `/pokegive aipom gb_sprite shiny`. Pack makers can extend the item tag
`#cobbleeffort:gb_sprite_cosmetics`.

## Collection #13: Cosmic Starlight

18 evolutionary lines (**34 Pokémon**), each one a celestial body (two lines per look):

* **nebula** (Bulbasaur, Frillish): deep violets and magentas in drifting gas clouds with teal wisps
* **galaxy** (Ekans, Spoink): midnight blue with pale spiral arms and pink dust swirling round a bright core on the chest
* **sun** (Victini, Archen): a burning, granulated surface with sunspots and a glowing corona
* **moon** (Karrablast, Fomantis): grey regolith, dark maria, cratered rims; shiny: a **blood moon**
* **comet** (Electrike, Buizel): icy blue with glowing tail streaks running back across the body
* **black hole** (Stunky, Genesect): near-black with a blazing accretion ring round the chest and a purple rim
* **ringed planet** (Spritzee, Bruxish): pastel gas-giant bands from head to toe and a bright ring round the middle
* **aurora** (Feebas, Pansage): a night-blue body with green and pink aurora curtains that ripple
* **eclipse** (Pawniard, Falinks): black, with a white-gold corona round its outline
* stars scattered over every dark part **twinkle and glow in the dark**, as do coronas, rings, tails and auroras; eyes glow
* other forms (Mega and Gigantamax Venusaur, Mega Manectric, Mega Falinks, Genesect's drives) are cosmic too
* shiny: the colours turned round the colour wheel (a blue sun, a green nebula…)

Bulbasaur → Ivysaur → Venusaur · Ekans → Arbok · Electrike → Manectric · Spoink → Grumpig · Feebas → Milotic ·
Buizel → Floatzel · Stunky → Skuntank · Victini · Pansage → Simisage · Archen → Archeops ·
Karrablast → Escavalier · Frillish → Jellicent · Pawniard → Bisharp → Kingambit · Genesect · Spritzee → Aromatisse ·
Fomantis → Lurantis · Bruxish · Falinks

Picked with `generate.py pick --count 18 --seed cosmic-starlight` from the 253 remaining eligible lines.

![Original vs. cosmic](docs/cosmic_preview.png)

### How to get one

Give a supported Pokémon **Glowstone Dust** as its cosmetic item. With commands: `/pokegive victini cosmic`,
`/pokegive escavalier cosmic shiny`. Pack makers can extend the item tag `#cobbleeffort:cosmic_cosmetics`.

## Collection #14: 80s Neon Cyberpunk

18 evolutionary lines (**34 Pokémon**) in 80s neon (three lines per look):

* **synthwave** (Duskull, Combee, Purrloin): dark violet with a hot-pink grid and cyan neon outlines
* **outrun** (Kangaskhan, Gible, Heatran): a retro sunset from head to toe (yellow, orange, magenta, purple) cut by
  sunset stripes, pink neon
* **Tron** (Pikachu, Chewtle, Yamper): black with cyan circuit traces and nodes, cyan neon
* **vaporwave** (Goomy, Eiscue, Tandemaus): pastel pink, teal and lavender, a black-and-white checker floor at the feet
* **acid** (Seviper, Corphish, Munkidori): near-black with glitched scanlines in toxic green and purple
* **chrome** (Pinsir, Beldum, Bouffalant): 80s chrome, a sky-blue-to-pink horizon reflection down the body
* **neon outlines** round its main parts and **glowing visor eyes**: the neon pulses, a tube flickers now and then,
  and it all glows in the dark
* megas and Gigantamax forms (Mega Pinsir, Mega Metagross, Mega Garchomp, Mega Raichu X and Y, Gigantamax Pikachu, cosplay Pikachu…) are neon too
* shiny: the neon turned round the colour wheel (pink becomes green, cyan becomes orange…)

Pichu → Pikachu → Raichu · Kangaskhan · Pinsir · Seviper · Corphish → Crawdaunt · Duskull → Dusclops → Dusknoir ·
Beldum → Metang → Metagross · Combee → Vespiquen · Gible → Gabite → Garchomp · Heatran · Purrloin → Liepard ·
Bouffalant · Goomy → Sliggoo → Goodra · Chewtle → Drednaw · Yamper → Boltund · Eiscue · Tandemaus → Maushold ·
Munkidori

Picked with `generate.py pick --count 18 --seed neon-cyberpunk-1985` from the 235 remaining eligible lines.

![Original vs. neon](docs/neon_preview.png)

### How to get one

Give a supported Pokémon a **Glow Ink Sac** as its cosmetic item. With commands: `/pokegive pikachu neon`,
`/pokegive metagross neon shiny`. Pack makers can extend the item tag `#cobbleeffort:neon_cosmetics`.

## Collection #15: Bioluminescent Deep Sea

18 evolutionary lines (**44 Pokémon**) as glowing creatures of the deep, dark abyssal bodies with living light (three
lines per look):

* **anglerfish** (Slowpoke, Rufflet, Quaxly): near-black and warty, a glowing lure over the forehead
* **jellyfish** (Skitty, Calyrex, Smoliv): pale violet with glowing radial canals and a glowing rim
* **lanternfish** (Spheal, Bergmite, Frigibax): dark silver-blue with rows of cyan photophores along the belly
* **comb jelly** (Paras, Gligar, Clauncher): glassy blue with comb rows of rainbow light that **ripple**
* **firefly squid** (Nidoran♀, Elekid, Zarude): deep blue speckled with tiny blue lights that **twinkle**
* **dragonfish** (Magby, Klink, Grookey): velvet black with red lights under the eyes and down the body
* the lights **glow in the dark** and pulse; glowing eyes
* other forms (Mega Slowbro, Mega Baxcalibur, Gigantamax Rillaboom, Ice and Shadow Rider Calyrex) glow too
* shiny: the lights' colours turned round the colour wheel

Nidoran♀ → Nidorina → Nidoqueen · Paras → Parasect · Slowpoke → Slowbro / Slowking (incl. Galarian) ·
Elekid → Electabuzz → Electivire · Magby → Magmar → Magmortar · Gligar → Gliscor · Skitty → Delcatty ·
Spheal → Sealeo → Walrein · Klink → Klang → Klinklang · Rufflet → Braviary (incl. Hisuian) · Clauncher → Clawitzer ·
Bergmite → Avalugg (incl. Hisuian) · Grookey → Thwackey → Rillaboom · Zarude · Calyrex · Quaxly → Quaxwell → Quaquaval ·
Smoliv → Dolliv → Arboliva · Frigibax → Arctibax → Baxcalibur

Picked with `generate.py pick --count 18 --seed bioluminescent-abyss` from the 217 remaining eligible lines.

![Original vs. deep sea](docs/deep_sea_preview.png)

### How to get one

Give a supported Pokémon a **Sea Pickle** as its cosmetic item. With commands: `/pokegive slowpoke deep_sea`,
`/pokegive spheal deep_sea shiny`. Pack makers can extend the item tag `#cobbleeffort:deep_sea_cosmetics`.

## Collection #16: Stained Glass

18 evolutionary lines (**37 Pokémon**) as leaded stained-glass windows, lit from behind:

* the body is cut into irregular **panes of glass** with dark **lead came** between them and round every part; each
  pane takes its colour from the original's colour there, with a bevel highlight and a streaky glass texture
* each line's glass (three lines each): **cathedral** jewels (Totodile, Uxie, Hatenna), **Tiffany** ambers and greens
  (Seedot, Cacnea, Kricketot), **rose window** blues and reds (Poliwag, Mudkip, Luvdisc), **art nouveau** pastels
  (Cottonee, Solosis, Elgyem), **grisaille** grey with yellow stain (Grimer, Klefki, Arctozolt), **kaleidoscope**
  (Basculin, Hawlucha, Cyclizar)
* the glass glows softly as if light shines through it, so it **shines in the dark**; clear glowing eyes
* other forms (Mega Feraligatr, Mega Swampert, Mega Hawlucha, Gigantamax Hatterene) are glass too
* shiny: **gold came** instead of lead, and the glass turned round the colour wheel

Poliwag → Poliwhirl → Poliwrath / Politoed · Grimer → Muk (incl. Alolan) · Totodile → Croconaw → Feraligatr ·
Mudkip → Marshtomp → Swampert · Seedot → Nuzleaf → Shiftry · Cacnea → Cacturne · Luvdisc ·
Kricketot → Kricketune · Uxie · Cottonee → Whimsicott · Basculin → Basculegion · Solosis → Duosion → Reuniclus ·
Elgyem → Beheeyem · Hawlucha · Klefki · Hatenna → Hattrem → Hatterene · Arctozolt · Cyclizar

Picked with `generate.py pick --count 18 --seed stained-glass-window` from the 199 remaining eligible lines.

![Original vs. stained glass](docs/stained_glass_preview.png)

### How to get one

Give a supported Pokémon a **Glass Pane** as its cosmetic item. With commands: `/pokegive uxie stained_glass`,
`/pokegive mudkip stained_glass shiny`. Pack makers can extend the item tag `#cobbleeffort:stained_glass_cosmetics`.

## Collection #17: Steampunk

18 evolutionary lines (**34 Pokémon**) as riveted, gear-driven contraptions:

* the body in its metal, cut into **riveted plates**, a **gear** on the chest, **brass goggles** round the eyes with
  glowing amber lenses, and **furnace vents** low on the body that glow and flicker in the dark
* each line's metal (three lines each): **brass** (Clefairy, Jynx, Terapagos), **copper** gone green with verdigris
  (Tangela, Barboach, Tynamo), gunmetal **iron** with brass rivets (Crabrawler, Marshadow, Clobbopus),
  **clockwork** with exposed gears that **turn** (Mesprit, Durant, Hoopa), **airship** leather with brass straps
  (Bidoof, Pikipek, Rockruff), black-iron **boiler** with pipes and many vents (Tepig, Drilbur, Ting-Lu)
* other forms (Mega Clefable, Mega Emboar, Mega Excadrill, Mega Eelektross, Mega Crabominable, Hoopa Unbound,
  Terastal and Stellar Terapagos) are steampunk too
* shiny: silver and blued steel instead of brass and copper

Cleffa → Clefairy → Clefable · Tangela → Tangrowth · Smoochum → Jynx · Barboach → Whiscash · Bidoof → Bibarel ·
Mesprit · Tepig → Pignite → Emboar · Drilbur → Excadrill · Tynamo → Eelektrik → Eelektross · Durant · Hoopa ·
Pikipek → Trumbeak → Toucannon · Crabrawler → Crabominable · Rockruff → Lycanroc · Marshadow ·
Clobbopus → Grapploct · Ting-Lu · Terapagos

Picked with `generate.py pick --count 18 --seed steampunk-clockwork` from the 181 remaining eligible lines.

![Original vs. steampunk](docs/steampunk_preview.png)

### How to get one

Give a supported Pokémon a **Copper Ingot** as its cosmetic item. With commands: `/pokegive durant steampunk`,
`/pokegive tepig steampunk shiny`. Pack makers can extend the item tag `#cobbleeffort:steampunk_cosmetics`.

## New Pokémon (CobbleEffort's own)

Original Pokémon from the user's designs (idea and look), with names, Pokédex entries, stats and moves made up for
them. Each one has a hand-built box model in Cobblemon's style, a shiny, animations (idle, walking, battle stance,
sleep, cry, moves, fainting), wild spawns, drops and a CobbleEffort page in the Pokédex. They use National Pokédex
numbers from #3001, which nothing else in the supported mod stack uses. In commands, use the namespaced id:
`/pokegive cobbleeffort:cavitot`.

**The dentistry line** (Cavitot, Amalgum, Orthodread): shinies have minty enamel (fresh toothpaste) and gold metal:
gold fillings, caps and braces.

**The coal butterfly line** (Coalarva, Cinderoon, Gatterfly) is CobbleEffort's **starter**: Coalarva has its own
"CobbleEffort" page on Cobblemon's starter screen (with Mumpillar, the water starter), after the regions. (Cobblemon shows only data-pack starter pages
once any exist, so CobbleEffort ships Cobblemon's own region pages too, exactly as in its default config: every usual
starter stays available. If your server turns on `useConfigStarters`, the CobbleEffort page is simply added to your
config's list.) Cinderoon's cocoon is a see-through ash layer with the Coalarva visible inside; their abdomens, the
cocoon's embers and bands, and Gatterfly's wings, cracks and gun barrels glow in the dark. Shinies burn with blue fire.

Gatterfly learns its own move when it evolves, **Machine Gun Stinger**: Bug, physical, 25 power, 95% accuracy, 15 PP,
hits 2-5 times (always 5 with its hidden ability Skill Link), each hit with a 20% chance to burn. It is a bullet move
(Bulletproof blocks it). Its Gatling drums spin when it attacks.

**The mantis line** (Prayling, Mawntis, Mantasma) is blind: none of them has eyes. Their own ability, **Blindsight**,
makes every move they use hit, whatever its accuracy and whatever evasion boosts the target has, and even targets
that are flying, underground or underwater (like No Guard, but only for its own moves). Prayling and Mawntis are
Grass/Bug; Mawntis evolves into the Grass/Ghost Mantasma at level 40 **at night**, and it learns Poltergeist as it
does. Mantasma's maw, ghost blades, leg rings and abdomen stripes glow in the dark. Shinies are orchid mantises: petal
pink and white, glowing violet.

**The mummy line** (Mumpillar, Sarcoon, Pharantis) is CobbleEffort's **water starter** (Water/Bug), on the
CobbleEffort starter page next to Coalarva: a bandaged mummy caterpillar, a cocoon shaped like a pharaoh's
sarcophagus, and a nimble mantis pharaoh. Their own ability, **Pharaoh's Curse**: once per battle, a hit that would
knock the Pokémon out doesn't. It rises again at half its HP (healed up to half if it was lower) and its Attack and Sp.
Atk rise by two stages. Their eyes glow. Shinies are turquoise and rose gold.

<!-- newmons:start -->
| # | Pokémon | Types | Abilities | HP / Atk / Def / SpA / SpD / Spe | Height / Weight | How to get it | Pokédex |
|---|---|---|---|---|---|---|---|
| 3001 | **Cavitot** | Dark | Strong Jaw / Stench / Stakeout (hidden) | 50 / 65 / 60 / 30 / 45 / 50 | 2'4" (0.7 m) / 18.5 kg | Wild: common near sugar cane (sugar rots teeth) and in Dripstone Caves, uncommon underground and in villages at night. Evolves into Amalgum at level 24. | It started out as a baby tooth that was never brushed. The cavity in its crown aches all the time, which is why it always looks so grumpy. It can't resist sweets, even though they make the ache worse. |
| 3002 | **Amalgum** | Dark / Steel | Strong Jaw / Sturdy / Stakeout (hidden) | 65 / 85 / 95 / 40 / 60 / 55 | 3'7" (1.1 m) / 72.4 kg | Evolve Cavitot at level 24. Wild: uncommon in Dripstone Caves, rare in the Deep Dark. | Three Cavitot that had their cavities filled and fused into one. The metal in their fillings makes it tough to crack, but all three of its faces still frown. It gnaws on iron ore to keep its caps shiny. |
| 3003 | **Orthodread** | Dark / Steel | Strong Jaw / Iron Barbs / Stakeout (hidden) | 85 / 120 / 120 / 50 / 80 / 70 | 5'11" (1.8 m) / 205 kg | Evolve Amalgum at level 42. Wild: very rare in the Deep Dark and Dripstone Caves. | Eight teeth held together by braces it can never take off. It scuttles through dark caves on its steel legs and its bite can crunch through iron. The braces put it in a foul mood, and it takes that out on anyone it meets. |
| 3004 | **Coalarva** | Fire / Bug | Blaze / Skill Link (hidden) | 45 / 55 / 50 / 49 / 50 / 60 | 1'4" (0.4 m) / 12 kg | The CobbleEffort starter: pick it at the starter screen (its own CobbleEffort page, after Cobblemon's regions). Wild: very rare underground next to coal ore. Evolves into Cinderoon at level 16. | It lives in caves deep underground where coal seams run thick, and it eats nothing but coal. A special organ in its abdomen turns the minerals it swallows into heat, which is why its tail end always glows. |
| 3005 | **Cinderoon** | Fire / Bug | Blaze / Skill Link (hidden) | 60 / 45 / 95 / 60 / 85 / 60 | 3'3" (1 m) / 38.5 kg | Evolve Coalarva at level 16. | Once it has eaten enough coal, it wraps its soft body in a cocoon of cinders. The ash is thin enough to see the Coalarva curled up inside, and it can burn some of it away to hurl a blast of fire at anything that disturbs it. |
| 3006 | **Gatterfly** | Fire / Bug | Blaze / Skill Link (hidden) | 78 / 115 / 80 / 104 / 75 / 82 | 5'7" (1.7 m) / 125 kg | Evolve Cinderoon at level 36. Learns its own move, Machine Gun Stinger, when it evolves. | Its arms have become guns that spray stingers so fast and so hot they glow, and its wings are made of fire. Besides fighting with them, it melts stone with its flames to build its nest. |
| 3007 | **Prayling** | Grass / Bug | Blindsight (its own: every move it uses hits) / Sniper (hidden) | 45 / 60 / 40 / 35 / 40 / 55 | 1'4" (0.4 m) / 2.2 kg | Wild: common in jungles, uncommon in flower forests, meadows and forests. Evolves into Mawntis at level 22. | It is born without eyes, yet it never misses. It feels the faintest stir of air through its leafy feelers and knows exactly where its prey is, then holds its little forelegs together and waits. |
| 3008 | **Mawntis** | Grass / Bug | Blindsight (its own: every move it uses hits) / Sniper (hidden) | 65 / 95 / 65 / 45 / 60 / 80 | 3'7" (1.1 m) / 38 kg | Evolve Prayling at level 22. Wild: rare in jungles. | Its head has split into a maw full of fangs, and a second set of legs lets it run down prey in the undergrowth. It still has no eyes, but its scythes find their mark every time. |
| 3009 | **Mantasma** | Grass / Ghost | Blindsight (its own: every move it uses hits) / Sniper (hidden) | 90 / 130 / 90 / 70 / 85 / 75 | 11'6" (3.5 m) / 210 kg | Evolve Mawntis at level 40 or higher at night. Wild: very rare in dark forests and jungles at night. | A Mawntis that hunted on a moonless night and came back as something else. It towers over the trees, its grin glows in the dark, and its ghostly scythes cut through anything without ever missing. Even so, it still clasps its forelegs together the way it did as a Prayling. |
| 3010 | **Mumpillar** | Water / Bug | Pharaoh's Curse (its own: once per battle, survives a knockout at half health with +2 Attack and Sp. Atk) / Torrent (hidden) | 50 / 52 / 48 / 52 / 57 / 50 | 1'4" (0.4 m) / 9.5 kg | A CobbleEffort starter: pick it at the starter screen (the CobbleEffort page, with Coalarva). Wild: very rare in deserts next to water (an oasis). Evolves into Sarcoon at level 16. | It wraps itself in strips of silk soaked in river water and never takes them off. Old tales say anyone who unwraps one is cursed, and that it cannot be finished off: struck down, it rises again angrier than before. |
| 3011 | **Sarcoon** | Water / Bug | Pharaoh's Curse (its own: once per battle, survives a knockout at half health with +2 Attack and Sp. Atk) / Torrent (hidden) | 65 / 55 / 100 / 55 / 90 / 40 | 3'3" (1 m) / 41 kg | Evolve Mumpillar at level 16. | Its silk hardens into a coffin painted like a pharaoh's. It lies still for weeks, but anything foolish enough to pry at the lid wakes the curse, and the case's eyes light up. |
| 3012 | **Pharantis** | Water / Bug | Pharaoh's Curse (its own: once per battle, survives a knockout at half health with +2 Attack and Sp. Atk) / Torrent (hidden) | 75 / 110 / 70 / 100 / 74 / 105 | 5'3" (1.6 m) / 62 kg | Evolve Sarcoon at level 36. Learns Liquidation when it evolves. | It rules the river valleys with a crook of gold at the end of each scythe, and moves so fast its foes never see it strike. Those who think they have defeated it soon learn about the pharaoh's curse. |
<!-- newmons:end -->

![CobbleEffort's own Pokémon: the dentistry, coal butterfly, mantis and mummy lines, with shinies](docs/newmons_preview.png)

## Paradox Mega Evolutions (with Mega Showdown)

Every Paradox Pokémon (the 22 the Pokémon Fandom wiki lists: 11 Ancient including Koraidon, 11 Future including
Miraidon) gets a Mega Evolution through **Mega Showdown**, with a mega stone you can craft in survival. Each model is
hand-built from boxes in Cobblemon's style (bones and boxes placed by hand, clean painted textures with soft shading,
a glow layer where it glows) and has animations for idle, walking (or floating), battle stance, sleep, cry,
physical/special/status moves and fainting. Each mega adds 100 base stats and keeps its types; Ancient megas' stats
stay odd and Future megas' even, like the Paradox Pokémon's own. Shinies have their own colours.

<!-- megas:start -->
| Mega | Era | Types | Ability | HP / Atk / Def / SpA / SpD / Spe | Stone | Look |
|---|---|---|---|---|---|---|
| Mega Great Tusk | Ancient | Ground / Fighting | Tough Claws | 115 / 171 / 171 / 53 / 53 / 107 | Great Tuskite | heavy navy armour with glowing crimson seams over shaggy pale-blue fur, crimson crystals from head to tail, red fur cuffs, ivory claws and great double-curled tusks |
| Mega Scream Tail | Ancient | Fairy / Psychic | Punk Rock | 115 / 65 / 129 / 95 / 135 / 131 | Scream Tailite | punk rock: a tall swooshing crest streaked with magenta, star cheek marks, big yellow eyes and a fang, a fluffy collar and a long tail ending in a big curl |
| Mega Brute Bonnet | Ancient | Grass / Dark | Grassy Surge | 121 / 167 / 129 / 79 / 129 / 45 | Brute Bonnetite | a towering prototaxite: a pale ringed trunk with glowing shelf fungi, stubby root legs and arms gripping mushroom-cap shields, two glaring eyes and a fanged mouth, under a huge brown cap with red and grey spiked panels and long hanging moss |
| Mega Flutter Mane | Ancient | Ghost / Fairy | Levitate | 75 / 55 / 75 / 175 / 155 / 135 | Flutter Manite | two tiers of feathered mane-wings with glowing pink tips, a crown of red spikes, glaring red-and-yellow eyes, a glowing bead necklace and a long tattered skirt |
| Mega Slither Wing | Ancient | Bug / Fighting | Moxie | 85 / 175 / 109 / 85 / 115 / 101 | Slither Wingite | six blazing flame wings with glowing yellow tips and glowing green diamonds, a big white fluffy collar, a red horned head with one yellow eye, a teal tail and little dark legs |
| Mega Sandy Shocks | Ancient | Electric / Ground | Magnet Pull | 85 / 81 / 127 / 161 / 105 / 111 | Sandy Shockite | three grey Magneton spheres with yellow eyes and screws, great magnet arches with red and blue tips crackling with glowing yellow arcs, black iron-sand spikes everywhere and a spiked iron-sand crown |
| Mega Roaring Moon | Ancient | Dragon / Dark | Intimidate | 105 / 179 / 91 / 55 / 121 / 139 | Roaring Moonite | a lean blue dragon with a swept white crest and yellow chest mark, its crimson wings swept round into a blood-moon crescent edged with light-blue spikes and a glowing rim, black wingtips and red claws |
| Mega Koraidon | Ancient | Fighting / Dragon | Tough Claws | 100 / 175 / 135 / 85 / 120 / 155 | Koraidonite | a red bipedal dragon whose feather crest flares into a blazing crown with glowing orange tips, a black chest plate glowing like molten orichalcum, white feather fans at its sides, long white antennae and a feathered tail |
| Mega Walking Wake | Ancient | Water / Dragon | Drizzle | 99 / 83 / 111 / 165 / 103 / 129 | Walking Wakite | a teal four-legged dragon with a purple mane surging up like a breaking wave, glowing red and orange flame streaks, a tall teal crest fin, white muzzle, whiskers and claws, and a long white tail streaming in two ribbons |
| Mega Gouging Fire | Ancient | Fire / Dragon | Drought | 105 / 155 / 141 / 65 / 113 / 111 | Gouging Firite | a stocky brown beast with glowing magma cracks in its fur, black anklets, a red face mask with white fangs, a billowing grey smoke mane and a huge golden crest of curved spikes with glowing fiery tips |
| Mega Raging Bolt | Ancient | Electric / Dragon | Electric Surge | 125 / 73 / 111 / 177 / 109 / 95 | Raging Boltite | a long-necked yellow dragon striped black with a white neck and belly, red-and-blue feet, a towering purple thunderhead crackling with glowing lightning on its head, and a big glowing crystal ball on its teal tail |
| Mega Iron Treads | Future | Ground / Steel | Steelworker | 90 / 142 / 150 / 72 / 90 / 126 | Iron Treadite | a grey robot Donphan under two black tread wheels with glowing red panels, long black tusk-blades and a glowing red visor |
| Mega Iron Bundle | Future | Ice / Water | Snow Warning | 56 / 80 / 114 / 164 / 90 / 166 | Iron Bundlite | a robot Delibird with a tall spiky white crest, glowing blue goggle eyes, a red body with a white zigzag collar, red flippers and a great glowing blue ice-cannon ring on its back |
| Mega Iron Hands | Future | Fighting / Electric | Iron Fist | 154 / 180 / 138 / 50 / 98 / 50 | Iron Handite | a round grey robot with a navy belly and legs, a small helmeted head with a glowing visor, shoulder pylons and colossal piston hands with glowing yellow fingers |
| Mega Iron Jugulis | Future | Dark / Flying | Levitate | 94 / 80 / 106 / 162 / 100 / 128 | Iron Jugulite | a black robot Hydreigon with a glowing blue visor, glowing pink spike rings round its arm-heads, long black blade wings and a pink-and-blue segmented tail |
| Mega Iron Moth | Future | Fire / Poison | Corrosion | 80 / 70 / 80 / 180 / 130 / 130 | Iron Mothite | a robot Volcarona in a halo of eight glowing orange wing panels with dark triangle marks, a white mask face with black markings, a crest of red horns and a pale body with a black shell |
| Mega Iron Thorns | Future | Rock / Electric | Sand Stream | 100 / 174 / 140 / 70 / 104 / 82 | Iron Thornite | a lime-green robot Tyranitar with glowing teal windows, a black belly, a tall spiked crest and a fortress of spikes down its back and tail |
| Mega Iron Valiant | Future | Fairy / Fighting | Justified | 74 / 160 / 100 / 150 / 70 / 136 | Iron Valiantite | a white and green robot knight with a tall glowing green crest-blade, a red eye, long white arm-blades edged in glowing pink and a flowing cape of green blades |
| Mega Miraidon | Future | Electric / Dragon | Transistor | 100 / 85 / 120 / 175 / 135 / 155 | Miraidonite | a dark purple robot dragon traced with glowing yellow and cyan lines, wings of light flaring from its back, crackling lightning antennae and a long tail with a lightning tip |
| Mega Iron Leaves | Future | Grass / Psychic | Sharpness | 90 / 170 / 108 / 70 / 128 / 124 | Iron Leafite | a green robot Virizion with pink accents, a crest of glowing sword-horns, long leaf-blades at its shoulders, grey joints and four long legs with pink-edged hooves |
| Mega Iron Boulder | Future | Rock / Psychic | Solid Rock | 90 / 160 / 100 / 68 / 128 / 144 | Iron Boulderite | a sturdy robot Terrakion: a round dark torso ringed with glowing orange armour, a helmeted head with cat-ear points, a long white-hot blade-horn and grey legs with glowing orange rings |
| Mega Iron Crown | Future | Steel / Psychic | Psychic Surge | 90 / 72 / 120 / 162 / 128 / 118 | Iron Crownite | a teal robot Cobalion with grey joints and white tufts, its crest-blades spread into a crown of floating glowing golden swords round its head |
<!-- megas:end -->

**Getting a stone:** craft it: a Mega Showdown Mega Stone in the middle, a Diamond below, and themed items around
it (the recipes are in the zip's README). The stones are also in the CobbleEffort creative tab. Then do it the Mega
Showdown way: the Pokémon holds the stone, you wear a Mega Bracelet, and you press Mega Evolve in battle.

![The Paradox megas, normal and shiny](docs/paradox_megas_preview.png)

How it works without code: Mega Showdown reads megas from data (`data/<ns>/mega_showdown/mega/*.json`), Showdown
items from `data/<ns>/mega_showdown/showdown/held_items/*.js`, and treats any item stack carrying its components
`mega_showdown:registry_type_component: "mega"` and `mega_showdown:registry_location_component: <mega id>` as that
mega's stone. So each stone is an amethyst shard with those components (plus a name, lore and `custom_model_data`
for its own icon), made by a crafting recipe. The "Mega" forms are added with `species_additions`. Built by
`tools/megas/build.py` from the models in `tools/megas/models/`.

## Compatibility

CobbleEffort is built to be used alongside this mod stack, and every update is generated against it:

| Mod | What CobbleEffort does with it |
|-----|--------------------------------|
| **Mega Showdown** | Every mega, Gigantamax, Eternamax and mode form (e.g. Mega Charizard X/Y, Gmax Snorlax, Xerneas' active mode) of a Pokémon in a collection gets its own cosmetic texture, adapted from Mega Showdown's (CC BY-NC-SA 4.0). Where Mega Showdown replaces a Cobblemon model or texture (Audino, Latias, Xerneas…), the cosmetic follows its version |
| **Mega Showdown: Extra Megas** | Its megas (Torterra, Luxray, Gogoat, Annihilape…) get cosmetic textures too |
| **Mega Showdown Ores** | Nothing to change (no Pokémon visuals) |
| **AllTheMons x Mega Showdown** | It replaces some Cobblemon models (Absol, Typhlosion, Rolycoly line, Bounsweet line, Frosmoth, Runerigus, Incineroar…). A cosmetic texture is painted for Cobblemon's model, so CobbleEffort ships Cobblemon's model, poser and animations for those Pokémon under its own name and the cosmetic uses them. ATM's own forms show unchanged under the cosmetic (its licence doesn't allow recoloured copies). Also provides Xurkitree's model for the Sasuke cosmetic |
| **Cobblemon Baby Legends** | Its babies join their legendary's evolutionary line: Xerfawn (→ Xerneas) is in Backrooms, Latot (→ Latias / Latios) in Easter. Its art is All Rights Reserved, so their cosmetic textures are painted from scratch on the model's UV layout, in the evolved form's colours |
| **Cobblemon Lost Lore** | Its forms on collection Pokémon (snowman Snorlax/Munchlax, crystal Onix/Steelix, clone Charmander/Squirtle lines, coloured Kecleon) show unchanged under the cosmetic, since its licence doesn't allow modified copies |
| **Legendary Monuments** | Nothing to change: it adds structures, items and NPCs but no Pokémon models or forms (checked against 8.2) |
| **Fully Hisuian Starters** (resource pack) | Its Hisui-bias Cyndaquil/Quilava, Oshawott/Dewott and Rowlet/Dartrix (`region-bias-hisui`) show unchanged under the cosmetic (no licence is given, so its art isn't adapted). Cyndaquil, Quilava, Rowlet and Dartrix are in collections |
| **Poke Costumes** (data pack) | Its costume forms (Rowlet, Magneton, Krookodile, Gengar…) show unchanged under the cosmetic. Its cosmetic items don't clash with ours. It replaces Cobblemon's Black Glasses item list, which the generator follows |
| **Planeta Cobblemon free pack** (resource pack) | Used through a bridge (below). Its models of Trubbish, Audino and Dedenne replace Cobblemon's, so their cosmetics (Christmas, FNAF, Ice Sculpture) ship Cobblemon's / Mega Showdown's model, poser and animations under CobbleEffort's name and keep their look. Its Iron Boulder is the Iron Boulder Mega Iron Boulder evolves from |

How it works: a resolver may only name models that exist whatever is installed, either Cobblemon's own or copies
shipped in CobbleEffort. Cobblemon loads every named model at startup, and a missing one stops the game on the
loading screen (v0.10.0 and v0.10.1 had this bug). Where a mod whose art can't be adapted would put a different model
under a cosmetic texture, that species' cosmetic variations pin their model (shipping a copy when needed). Elsewhere
the cosmetic only swaps textures. Forms added by those mods get a "passthrough" entry (texture and layers only) that
restores what the game shows without the cosmetic. On the few pinned species the cosmetic shows on its own model
instead.

Base-form layers also merge into every form by name, so each Paradox mega switches off the glow, sleep and
alpha-eye layers Cobblemon or ATM give its base form (painted for the base mesh; up to 0.23.0 they showed on 12 megas).

![Mega Showdown forms and Baby Legends babies, original vs. cosmetic](docs/compat_forms_preview.png)

### Planeta Cobblemon free pack: the bridge

The pack (16 Pokémon: Electrike, Heatran, Audino, Trubbish, Terrakion, Virizion, Dedenne, Celesteela, Iron Treads,
Iron Hands, Iron Jugulis, Wo-Chien, Ting-Lu, Roaring Moon, Iron Boulder, Iron Crown) uses Cobblemon's old folder
layout (`bedrock/models`, `bedrock/posers`, `bedrock/animations`, `bedrock/species`). Cobblemon 1.8 still reads it,
but loads it **before** `bedrock/pokemon/...`, into the same names (model file name, poser id, animation group), and
the later load wins. So for the 14 of them that Cobblemon, Mega Showdown or ATM x MSD also ship, the pack's mesh,
poser and animations are thrown away whatever the pack order, while its textures (same paths) still win: Planeta's
texture on another mod's mesh, scrambled. Base glow and alpha-eye layers made for the other mesh stay on as well.
Celesteela and Iron Boulder were fine (nothing else ships them).

`tools/bridge.py` rebuilds the pack from your own copy in the current layout so it wins as a whole: every model,
poser and animation at the path each competing file uses, its resolver first (a lower order than any other for that
species), and the other resolvers for those species cut down to the forms with their own mesh (Mega Audino stays).
Planeta's art is never committed or shipped in CobbleEffort: the bridge is built locally into `build/bridge/`
(`generate.py build` does it when the pack is in `tools/compat/jars/`), for your own use. Install it **instead of**
the original pack, above the other resource packs.

```
python3 tools/bridge.py --cobblemon cobblemon/common/src/main/resources   # -> build/bridge/<pack>-CobbleEffort-bridge.zip
```

## Requirements & versions

| | |
|---|---|
| Loader | Fabric **or** NeoForge. It's a single jar for both: all data and assets, plus one small class per loader for the creative tab |
| Cobblemon | 1.7.0+ (built against **1.8.4**) |
| Minecraft | **1.21.1** (whatever version Cobblemon supports) |

> **About "Minecraft 1.26.1":** Minecraft moved to year-based version numbers in 2026 (26.1, 26.2, 26.3 …),
> and Cobblemon (latest 1.8.4) still only supports **1.21.1**. There is no Cobblemon build for the 26.x line yet,
> so this release targets 1.21.1. The mod is pure data, and its metadata only asks for "Minecraft ≥ 1.21.1 +
> Cobblemon ≥ 1.7.0". When Cobblemon ships for 26.x, the same content should load. At most it may need its
> metadata and `pack.mcmeta` bumped.

## Building

```
./gradlew build        # -> build/libs/cobbleeffort-<version>+1.21.1.zip  (the .jar + README.txt; also runs validateData)
```

The zip's `README.txt` is a player guide listing every collection, its cosmetic item, its command and its Pokémon.
It is generated (`dist/README.txt`, by `tools/make_readme.py`) from the collection configs' `readme` blocks.

`validateData` checks that every JSON file parses, that every texture a resolver points to exists, and that every
pinned `cobbleeffort:` model, poser and animation group exists.

### Regenerating / adding collections

Each collection is a config in `tools/collections/<name>.json` (aspect, cosmetic item, `lines`, optional
`line_styles` to give one line its own look) plus a texture style in `tools/styles/<style>.py`. A style can set
`FRAMES`/`FPS` to make every texture an animation (Halloween does), and `EXTRA_LAYERS` + `extra_layer()` to add
its own layers on top of the body, such as Christmas's glowing, twinkling fairy lights. A style that sets
`WANTS_HINTS` is told where the model's head front/top and torso front faces are in the texture (read from the
`.geo.json`). FNAF uses this to put Freddy's hat on top of his head and Chica's bib on her chest. A style that sets
`WANTS_HEIGHTS` gets the height on the model of every texture pixel, which Trans Pride uses to run the flag's stripes
across the whole body. Everything under `assets/cobbleeffort` and `data/cobbleeffort` is generated:

The generator reads the mod stack from `tools/compat/mods.json`. Put each mod's jar (or a directory of its
resources) in `tools/compat/jars/`, which is gitignored: other mods' files are never committed. Pass `--no-compat`
to build against Cobblemon alone. Resource packs in Cobblemon's old layout are marked `"bridge": true` and seen as
their bridge (see [the bridge](#planeta-cobblemon-free-pack-the-bridge)). The Paradox megas are built by
`python3 tools/megas/build.py --cobblemon cobblemon/common/src/main/resources`.

```
pip install pillow
git clone --depth 1 --branch 1.8.4 https://gitlab.com/cable-mc/cobblemon.git
python3 tools/generate.py --cobblemon cobblemon/common/src/main/resources build              # every collection
python3 tools/generate.py --cobblemon cobblemon/common/src/main/resources build thanksgiving # just one
python3 tools/generate.py --cobblemon cobblemon/common/src/main/resources pick --count 18 --seed <text>
```

`pick` randomly chooses new evolutionary lines that are fully modelled and not used by any collection yet. Put
its first column into a new config's `lines`. Each species has a fixed seed per collection, so reruns give
byte-identical output, and each collection's generated folders are wiped and rebuilt on every run.
`tools/preview/` renders original vs. retextured models in headless Chromium (three.js) for a quick look.

### Addon lines (Pokémon modelled by another mod)

A collection can list `addon_lines` for Pokémon Cobblemon doesn't model but another mod does (Xurkitree, from
Cobblemon Ultra-Beasts). The model's UV layout, with no art, is extracted with
`python3 -I tools/addons/extract_layout.py <their .geo.json> tools/addons/<name>_layout.json`. A builder in
`tools/addons/` then paints an original texture onto it. The resolver only swaps textures and layers, so the
cosmetic is active only when that mod is installed. To preview it, pass the other mod's model folder with
`EXTRA_MODEL_ROOTS=...`.

### Collection rules

These hold for every collection, now and in future:

1. **Whole evolutionary lines only.** Configs list lines, never single stages. The generator works out each family
   (pre-evolutions, evolutions, branches, forms' evolution links) from Cobblemon's `data/cobblemon/species`, and
   **stops with an error** if any member of a line has no Cobblemon model to retexture. Evolutions Cobblemon's data
   doesn't link can be joined with `extra_links`.
2. **Every vanilla variation is mirrored.** For each species, every variation in Cobblemon's resolver
   (shiny, gender, regional forms, model swaps, animated textures, extra layers) is copied with the cosmetic aspect
   added and its textures retextured. So the form keeps working through evolution, gender, regional and shiny changes.
3. **No overlap.** A species belongs to at most one collection, and each collection has its own cosmetic item.
   The generator refuses to build otherwise.
4. **Releases are zips.** `./gradlew build` puts the jar inside `build/libs/<name>.zip`.
5. **Built for the mod stack.** Families include other mods' pre-evolutions and evolutions. Other mods' forms are
   retextured where their licence allows, and passed through otherwise. Models are pinned (and vendored when a mod
   overwrites one). See [Compatibility](#compatibility).

## How it works (for future collections)

Per collection (`<aspect>` = `backrooms`, `thanksgiving`, …):

| File | Purpose |
|------|---------|
| `data/cobbleeffort/cosmetic_items/<aspect>.json` | the collection's item in the cosmetic slot → aspect `<aspect>` |
| `data/cobbleeffort/species_features/<feature>.json` | flag feature (for `/pokegive … <aspect>`) |
| `data/cobbleeffort/species_feature_assignments/<feature>.json` | which species get the flag |
| `data/cobbleeffort/tags/item/<aspect>_cosmetics.json` | items accepted for the cosmetic |
| `assets/cobbleeffort/bedrock/pokemon/resolvers/<aspect>/<species>/9000_*.json` | `order: 9000` copies of every vanilla variation with the aspect added |
| `assets/cobbleeffort/textures/pokemon/<aspect>/<species>/` | the retextured textures |

**The creative tab** is the mod's only code (`src/main/java`). Minecraft has no data-driven creative tabs, so
`CreativeTab.java` builds one by reflection: Fabric runs on intermediary names and NeoForge on Mojang's, and every
name is given in both (checked against the 1.21.1 mappings), so the same class works in one jar on both loaders.
`fabric/CobbleEffortFabric` (the `main` entrypoint in `fabric.mod.json`) and `neoforge/CobbleEffortNeoForge`
(`@Mod`, `javafml`) start it. They compile against the JDK plus stand-ins for four loader types (`src/stubs/java`,
never packaged). Its items come from `cobbleeffort_creative_tab.json`, written by `tools/make_creative_tab.py`
(run by `generate.py build` and `tools/megas/build.py`). Any failure only logs a `[CobbleEffort]` line and leaves the tab out.

Cobblemon merges every resolver file for a species, sorted by `order`, and the **last** matching variation wins.
So the high order, combined with mirroring the vanilla variations in order, puts the right texture on top in every
combination (base, shiny, female, regional…) without touching Cobblemon's files.

## Credits & licence

See [CREDITS.md](CREDITS.md). In short: the code and data are MPL-2.0. The textures are **modified Cobblemon
assets** (CC BY-NC 3.0 where Cobblemon marks them so), so this mod is **non-commercial**. Pokémon belongs to
Nintendo / Game Freak / The Pokémon Company. *The Backrooms* Still Life concept belongs to Kane Parsons (Kane Pixels).
This project is not affiliated with any of them.
