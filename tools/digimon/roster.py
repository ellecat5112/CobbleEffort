"""The Digimon added by the generator (tools/newmons/digimon_gen.py), in the user's order: alphabetical, as wikimon.net
lists them. Stats, moves, spawns, sizes and evolutions come from rules + tools/digimon/data/wikimon.json; this file
holds what needs a decision: types, role (stat spread), abilities when the type default doesn't fit, our own Pokédex
entry and a stage when wikimon has none. The model module is models/<id>.py (id = the name, lower-case, letters and
digits only).

Skipped on purpose: "(2006 Anime Version)" entries (the same design as the base Digimon).
"""

ROSTER = [
    # --- batch 1 (0.96.0) ---------------------------------------------------------------------------------------
    {"name": "Abbadomon", "types": ["dark", "psychic"], "role": "special", "legendary": True,
     "abilities": ["pressure", "h:shadowtag"],
     "entry": "A shape of black ribbons wound round an empty core and covered in staring red eyes. It is said to be "
              "made of everything that was ever deleted, and it pulls the light out of any world it drifts into."},
    {"name": "Abbadomon Core", "types": ["dark", "ghost"], "role": "mixed", "legendary": True,
     "abilities": ["pressure", "h:cursedbody"],
     "entry": "The core of Abbadomon, unwound: a cloaked knight of tattered eye-ribbons with a crimson blade for an "
              "arm. Whatever it cuts is not destroyed but erased, as if it had never been."},
    {"name": "Achillesmon", "types": ["fighting", "flying"], "role": "speed",
     "abilities": ["noguard", "h:speedboost"],
     "entry": "A warrior who has never once been struck. It hurls its golden spear faster than sound, and the cyan "
              "wings on its heels carry it out of reach before anyone can strike back."},
    {"name": "Aegiochusmon", "types": ["electric", "fighting"], "role": "physical",
     "abilities": ["lightningrod", "h:guts"],
     "entry": "A god-man with goat's legs who carries a storm on its back. Its fists come down with the force of a "
              "lightning strike, and the ground cracks wherever it plants its hooves."},
    {"name": "Aegiochusmon: Blue", "types": ["electric", "steel"], "role": "tank",
     "abilities": ["lightningrod", "h:ironfist"],
     "entry": "Aegiochusmon in blue cyber-armour, with a gauntlet many times its own size hovering beside it. The "
              "gauntlet can catch a falling meteor and throw it back."},
    {"name": "Aegiochusmon: Dark", "types": ["electric", "dark"], "role": "physical",
     "abilities": ["intimidate", "h:moxie"],
     "entry": "Aegiochusmon fallen to darkness: black-winged and red-eyed, it reaps its foes with a storm-forged "
              "scythe and feeds on their fear."},
    {"name": "Aegiochusmon: Green", "types": ["electric", "grass"], "role": "mixed",
     "abilities": ["grasspelt", "h:lightningrod"],
     "entry": "Aegiochusmon wreathed in living vines. Its whips are tipped with spiked seed-pods that burst into "
              "thickets wherever they land, and a forest grows in its footsteps."},
    {"name": "Aegiochusmon: Holy", "types": ["electric", "fairy"], "role": "special",
     "abilities": ["lightningrod", "h:serenegrace"],
     "entry": "Aegiochusmon in holy armour of golden gears, a halo over its horns and a sun blazing behind it. Its "
              "light drives off the darkness and heals those who fight beside it."},
    {"name": "Aegiomon", "types": ["electric", "fighting"], "role": "physical",
     "abilities": ["static", "h:ironfist"],
     "entry": "A young god-man with a goat's horns and legs. It hums a tune through its syrinx that makes anyone who "
              "hears it forget everything but Aegiomon, then floors them with a crackling punch."},
    {"name": "Aegisdramon", "types": ["water", "steel"], "role": "tank",
     "abilities": ["filter", "h:megalauncher"],
     "entry": "A golden dragon-ship that guards the deep oceans. Its hull bristles with cannons and lances, and its "
              "barrier turns back any attack aimed at the ones it protects."},
    {"name": "Aequcedramon", "types": ["ice", "dragon"], "role": "special", "stage": "Adult",
     "abilities": ["snowcloak", "h:refrigerate"],
     "entry": "A small blue dragon with a white ruff and wide bat wings. It whips up whirlwinds of frost as it flies, "
              "and a hole opens in the sky wherever it goes."},
    {"name": "Aero V-dramon", "types": ["dragon", "flying"], "role": "physical",
     "abilities": ["aerilate", "h:toughclaws"],
     "entry": "A holy dragon that guards the skies, with red wings and white armour over its blue scales. It strikes "
              "with a V-shaped blast of light from its chest."},
    {"name": "Agnimon", "types": ["fire", "fighting"], "role": "physical",
     "abilities": ["blaze", "h:ironfist"],
     "entry": "A warrior of flame in red armour, born from the spirit of fire. It fights with blazing fists and kicks, "
              "and its spinning dance of flame burns away any evil."},
    {"name": "Agumon (X-Antibody)", "types": ["fire", "dragon"], "role": "physical",
     "abilities": ["blaze", "h:toughclaws"],
     "entry": "An Agumon awakened by the X-Antibody, with long chrome claws and a fiercer, more dinosaur-like body. "
              "Its Baby Flame burns far hotter than any other Agumon's."},
    {"name": "Agumon (Black)", "types": ["fire", "dark"], "role": "physical",
     "abilities": ["blaze", "h:moxie"],
     "entry": "A black-scaled Agumon with a fiercer temper. It picks fights with Digimon far bigger than itself and "
              "often wins."},
    {"name": "Agumon (Black) (X-Antibody)", "types": ["fire", "dark"], "role": "physical",
     "abilities": ["blaze", "h:toughclaws"],
     "entry": "A black Agumon awakened by the X-Antibody, scarred with red stripes. It breathes a roaring stream of "
              "fire and slashes with chrome claws."},
    {"name": "Agumon -Yuki no Kizuna-", "types": ["fire", "fighting"], "role": "physical",
     "abilities": ["blaze", "h:justified"],
     "entry": "Agumon's courage given a warrior's form by an unbreakable bond. Two great wings of fire cross behind it "
              "in an X, and its gauntlet claws shine red-hot."},
    {"name": "Agumon: Burst Mode", "types": ["fire", "fairy"], "role": "special",
     "abilities": ["flashfire", "h:levitate"],
     "entry": "An Agumon that has turned to pure spirit, glowing pink and floating with its arms spread wide. It is "
              "said to appear only when a partner's feelings reach their peak."},
    {"name": "Agumon Hakase", "types": ["fire", "psychic"], "role": "special",
     "abilities": ["forewarn", "h:analytic"],
     "entry": "An Agumon in a mortarboard and a lab coat that drags on the ground. It has read every book in the "
              "Digital World and lectures anyone who stands still long enough, pointer in hand."},
    # --- batch 2 (0.97.0): the detail standard (_digidetail.py / _digibody.py) --------------------------------
    {"name": "Aircraft Carrier Whamon", "types": ["water", "steel"], "role": "tank", "stage": "Perfect",
     "abilities": ["shellarmor", "h:megalauncher"],
     "entry": "A whale that carries a whole flight deck on its back. Smaller Digimon live in its island tower, and it "
              "launches them into the sky from its runway before charging into battle mouth first."},
    {"name": "Airdramon", "types": ["dragon", "flying"], "role": "speed",
     "abilities": ["aerilate", "h:intimidate"],
     "entry": "A winged serpent said to be a messenger of the gods. It stirs up whirlwinds with a beat of its ragged "
              "wings and rains spinning needles of wind on anything below."},
    {"name": "Ajatarmon", "types": ["grass", "fighting"], "role": "physical",
     "abilities": ["grasspelt", "h:toughclaws"],
     "entry": "A warrior made of living vines that guards the deep forest. It ties intruders up in thorny ivy, then "
              "brings its sickle-hatchet down in one swing."},
    {"name": "Akatorimon", "types": ["fire", "flying"], "role": "physical",
     "abilities": ["guts", "h:moxie"],
     "entry": "A giant rooster with a temper as hot as its blazing feathers. One glare from its scarred red eye is "
              "enough to make most Digimon back away; the rest meet its charging talons."},
    {"name": "Albatusmon", "types": ["steel", "fairy"], "role": "special",
     "abilities": ["magicguard", "h:pressure"],
     "entry": "An armoured angel that judges the wicked. The circle of runes on its staff blazes like the sun, and "
              "the sphere of light it calls down erases whatever it touches."},
    {"name": "Aldamon", "types": ["fire", "dragon"], "role": "physical", "stage": "Perfect",
     "abilities": ["blaze", "h:sheerforce"],
     "entry": "A warrior who joined the spirits of beast and man into one blazing form. Fire pours from its fists and "
              "the flames at its back, and its golden ray-blades cut through solid rock."},
]
