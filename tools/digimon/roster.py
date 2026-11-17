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
    # --- 0.98.0: the rest of A, at the detail standard ------------------------------------------------------------
    {"name": "Algomon (Baby I)", "types": ["poison"], "role": "special", "stage": "Baby I",
     "abilities": ["liquidooze", "h:levitate"],
     "entry": "A glossy droplet of living code that floats wherever the network takes it. Its one great eye records "
              "everything it sees, and it was born from a program that rewrote itself."},
    {"name": "Algomon (Baby II)", "types": ["poison"], "role": "special", "stage": "Baby II",
     "abilities": ["liquidooze", "h:roughskin"],
     "entry": "A spiky ball that scuttles about on four thin legs. It copies the moves of anything it watches, though "
              "it gets most of them a little wrong."},
    {"name": "Algomon (Child)", "types": ["poison", "psychic"], "role": "special", "stage": "Child",
     "abilities": ["levitate", "h:synchronize"],
     "entry": "It floats on a bundle of tentacles and flings bursts of corrupted data from its eye. It learns from "
              "every battle and never makes the same mistake twice."},
    {"name": "Algomon (Adult)", "types": ["poison", "steel"], "role": "mixed", "stage": "Adult",
     "abilities": ["download", "h:levitate"],
     "entry": "A great violet sphere that drags itself along on a skirt of tentacles. Its mechanical gauntlets were "
              "built from the programs it swallowed, and its zipped mouth leaks poisonous steam."},
    {"name": "Algomon (Perfect)", "types": ["poison", "dark"], "role": "special", "stage": "Perfect",
     "abilities": ["download", "h:infiltrator"],
     "entry": "A lean hunter whose bodysuit is covered in watching eyes. It whips its tentacles through the network "
              "and rewrites any Digimon it catches into a copy of itself."},
    {"name": "Algomon (Ultimate)", "types": ["poison", "dark"], "role": "physical", "stage": "Ultimate",
     "abilities": ["download", "h:moxie"],
     "entry": "The final form of the self-rewriting algorithm, armoured and wild-maned. It is said that no system it "
              "has entered has ever been restored."},
    {"name": "Allomon", "types": ["dragon", "fire"], "role": "physical", "stage": "Adult",
     "abilities": ["strongjaw", "h:intimidate"],
     "entry": "A dinosaur Digimon born from the Digi-Egg of Courage. It bites with a jaw full of fangs and breathes a "
              "blast of fire hot enough to melt rock."},
    {"name": "Allomon (X-Antibody)", "types": ["dragon", "fire"], "role": "physical", "stage": "Adult",
     "abilities": ["strongjaw", "h:toughclaws"],
     "entry": "An Allomon awakened by the X-Antibody, wrapped in a fur mantle and a feathered war bonnet. Its fire "
              "breath turns blue-white and its charge can flatten a forest."},
    {"name": "Alphamon", "types": ["steel", "dark"], "role": "mixed", "stage": "Ultimate", "legendary": True,
     "abilities": ["pressure", "h:justified"],
     "entry": "The phantom Royal Knight, said to have stood against the others when they lost their way. It wields "
              "the Holy Sword Grade Alpha, drawn from a magic circle, and its cape is the shadow of a whole army."},
    {"name": "Alphamon: Ouryuken", "types": ["steel", "dragon"], "role": "physical", "stage": "Ultimate",
     "legendary": True, "abilities": ["pressure", "h:toughclaws"],
     "entry": "Alphamon joined with the spirit of the dragon Ouryumon. Its wings blaze with every colour of flame, "
              "and the Ouryuken it carries can split the sky from horizon to horizon."},
    {"name": "Alraumon", "types": ["grass", "poison"], "role": "special", "stage": "Child",
     "abilities": ["effectspore", "h:chlorophyll"],
     "entry": "A mandrake Digimon that dozes half buried in the soil. The scent of its lily lulls attackers to sleep, "
              "and its root claws drink the strength from anything they grip."},
    {"name": "Amaterasumon", "types": ["fire", "fairy"], "role": "special", "stage": "Ultimate",
     "abilities": ["drought", "h:magicbounce"],
     "entry": "The goddess of the sun, who carries two great suns on her back. When she hides herself the whole "
              "Digital World falls dark, and when she shines no shadow can stand."},
    {"name": "Ambromon", "types": ["grass", "fairy"], "role": "special", "stage": "Perfect",
     "abilities": ["naturalcure", "h:serenegrace"],
     "entry": "A laughing radish spirit that wanders with its sun staff, blessing the harvest wherever it dances. "
              "Its laughter is said to heal any sickness."},
    {"name": "Amon", "types": ["fire", "ghost"], "role": "special",
     "abilities": ["flashfire", "h:cursedbody"],
     "entry": "A spirit of crimson flame with a demon's face. It burns in the dark places of the network and feeds "
              "on the anger of those who come near."},
    {"name": "Amphimon", "types": ["water", "electric"], "role": "mixed", "stage": "Ultimate",
     "abilities": ["plus", "h:minus"],
     "entry": "A cyborg that charges the jellyfish orbs on its tendrils with opposite currents. Bringing them "
              "together releases a blast that leaves no machine still running."},
    {"name": "Ancient Beatmon", "types": ["bug", "electric"], "role": "physical", "stage": "Ultimate",
     "legendary": True, "abilities": ["lightningrod", "h:pressure"],
     "entry": "The ancient warrior of thunder, one of the Ten Legendary Warriors who sealed away the Lucemon of old. "
              "Its scythe horns call down lightning, and its spirit lives on in Beetlemon."},
    {"name": "Ancient Garurumon", "types": ["ice", "steel"], "role": "physical", "stage": "Ultimate",
     "legendary": True, "abilities": ["justified", "h:pressure"],
     "entry": "The ancient warrior of light, a wolf knight of the Ten Legendary Warriors. Its blade shines brighter "
              "than the moon, and its spirit lives on in Wolfmon."},
    {"name": "Ancient Greymon", "types": ["fire", "dragon"], "role": "physical", "stage": "Ultimate",
     "legendary": True, "abilities": ["blaze", "h:pressure"],
     "entry": "The ancient warrior of flame and leader of the Ten Legendary Warriors. Its wings of fire scorch the "
              "earth, and its spirit lives on in Agnimon."},
    {"name": "Ancient Irismon", "types": ["flying", "fairy"], "role": "speed", "stage": "Ultimate",
     "legendary": True, "abilities": ["galewings", "h:pressure"],
     "entry": "The ancient warrior of wind, one of the Ten Legendary Warriors. Its rainbow wings raise storms, and "
              "its rapier strikes faster than the eye can follow. Its spirit lives on in Fairymon."},
    {"name": "Ancient Megatheriumon", "types": ["ice", "normal"], "role": "tank", "stage": "Ultimate",
     "legendary": True, "abilities": ["thickfat", "h:pressure"],
     "entry": "The ancient warrior of ice, a beast so vast that glaciers were said to be its sleeping body. Its "
              "spirit lives on in Chakmon."},
    {"name": "Ancient Mermaimon", "types": ["water", "fairy"], "role": "special", "stage": "Ultimate",
     "legendary": True, "abilities": ["swiftswim", "h:pressure"],
     "entry": "The ancient warrior of water, who ruled the seas with her trident. Her song calms storms and raises "
              "tidal waves. Her spirit lives on in Ranamon."},
    {"name": "Ancient Sphinxmon", "types": ["dark", "steel"], "role": "mixed", "stage": "Ultimate",
     "legendary": True, "abilities": ["pressure", "h:intimidate"],
     "entry": "The ancient warrior of darkness, a sphinx who guarded the boundary between light and shadow. Its "
              "spirit lives on in Löwemon."},
    {"name": "Ancient Troiamon", "types": ["grass", "steel"], "role": "tank", "stage": "Ultimate",
     "legendary": True, "abilities": ["megalauncher", "h:pressure"],
     "entry": "The ancient warrior of wood, a war-horse built of living timber and armed with cannons. Its spirit "
              "lives on in Arbormon."},
    {"name": "Ancient Volcamon", "types": ["ground", "fire"], "role": "physical", "stage": "Ultimate",
     "legendary": True, "abilities": ["solidrock", "h:pressure"],
     "entry": "The ancient warrior of earth, a walking volcano with fists like boulders. When it pounds the ground "
              "the mountains erupt. Its spirit lives on in Grottomon."},
    {"name": "Ancient Wisemon", "types": ["steel", "psychic"], "role": "special", "stage": "Ultimate",
     "legendary": True, "abilities": ["magicguard", "h:pressure"],
     "entry": "The ancient warrior of steel, a sage who weighed the hearts of others on its balance of sun and moon. "
              "Its spirit lives on in Mercurymon."},
    {"name": "Andiramon", "types": ["normal", "psychic"], "role": "speed", "stage": "Perfect",
     "abilities": ["innerfocus", "h:speedboost"],
     "entry": "A holy beast with enormous ears that hear every whisper across the land. It moves so fast that its "
              "long sleeves seem to strike from everywhere at once."},
    {"name": "Andiramon (Deva)", "types": ["normal", "psychic"], "role": "speed", "stage": "Perfect",
     "abilities": ["innerfocus", "h:justified"],
     "entry": "Andiramon serving as one of the Twelve Devas, the guardians of the holy beasts. It wears a lilac "
              "scarf as the mark of its rank."},
    {"name": "Andromon", "types": ["steel", "electric"], "role": "mixed", "stage": "Perfect",
     "abilities": ["download", "h:filter"],
     "entry": "An android built to be the perfect machine, its chrome frame wrapped round artificial muscle. It "
              "fires spinning missiles from its chest and its drum arm can cut a wall in two."},
    {"name": "Angemon", "types": ["fairy", "fighting"], "role": "physical", "stage": "Adult",
     "abilities": ["justified", "h:ironfist"],
     "entry": "An angel warrior with six shining wings. It never removes its helm, and its Heaven's Knuckle can "
              "drive any evil back into the dark."},
    {"name": "Angewomon", "types": ["fairy", "flying"], "role": "special", "stage": "Perfect",
     "abilities": ["serenegrace", "h:justified"],
     "entry": "An archangel who shines with holy light. She is gentle with the kind but has no mercy for evil, and "
              "her Holy Arrow never misses its mark."},
    {"name": "Angewomon (X-Antibody)", "types": ["fairy", "flying"], "role": "special", "stage": "Perfect",
     "abilities": ["serenegrace", "h:magicguard"],
     "entry": "Angewomon awakened by the X-Antibody, crowned with a ring of gold light and twelve rainbow wings. "
              "Her light alone is enough to drive back the dark."},
    {"name": "Angoramon", "types": ["normal", "fairy"], "role": "tank", "stage": "Child",
     "abilities": ["fluffy", "h:cutecharm"],
     "entry": "A plump angora rabbit that dozes almost all day. Its fur is so soft that attacks sink into it, and "
              "it can sleep through a whole battle."},
    {"name": "AnheiNüwashou", "types": ["dark", "dragon"], "role": "special", "stage": "Ultimate",
     "legendary": True, "abilities": ["pressure", "h:shadowtag"],
     "entry": "A dark goddess seen so far only as a shadow on the edge of the Digital World. It is said to be the "
              "darkness of the goddess who mended the sky."},
    {"name": "Ankylomon", "types": ["rock", "steel"], "role": "tank", "stage": "Adult",
     "abilities": ["sturdy", "h:roughskin"],
     "entry": "An armoured dinosaur whose spiked shell is harder than diamond. It curls up and rolls at its foes, "
              "or smashes them with its mace of a tail."},
    {"name": "Anomalocarimon", "types": ["water", "bug"], "role": "physical", "stage": "Perfect",
     "abilities": ["swiftswim", "h:shellarmor"],
     "entry": "An ancient crustacean revived from data of the first seas. It scoops prey in with its curled claws "
              "and cuts with the blade-fins down its sides."},
    {"name": "Anomalocarimon (X-Antibody)", "types": ["water", "bug"], "role": "physical", "stage": "Perfect",
     "abilities": ["swiftswim", "h:sharpness"],
     "entry": "Anomalocarimon awakened by the X-Antibody, its shell a rainbow and its head crowned with two great "
              "scythe blades."},
    {"name": "Anubimon", "types": ["ghost", "psychic"], "role": "special", "stage": "Ultimate",
     "abilities": ["pressure", "h:cursedbody"],
     "entry": "The god who guards the gate between the Digital World and the Dark Area. It weighs the data of every "
              "deleted Digimon and decides whether it will be reborn."},
    {"name": "Apocalymon", "types": ["dark", "steel"], "role": "special", "stage": "Ultimate", "legendary": True,
     "abilities": ["pressure", "h:shadowtag"],
     "entry": "Born from the grudges of every Digimon that was deleted without ever evolving. It can use the "
              "techniques of any Digimon it has absorbed, and wants only to erase the whole world."},
    {"name": "Apollomon", "types": ["fire", "fighting"], "role": "physical", "stage": "Ultimate", "legendary": True,
     "abilities": ["drought", "h:pressure"],
     "entry": "One of the Olympus Twelve, the god of the sun. Its mane and tail burn with solar flame and its "
              "fists strike with the heat of a sunrise."},
    {"name": "Apollomon: Whispered", "types": ["fire", "dark"], "role": "physical", "stage": "Ultimate",
     "legendary": True, "abilities": ["flashfire", "h:pressure"],
     "entry": "Apollomon after the whispers of darkness turned its flames cold and blue. It still burns, but its "
              "fire freezes the heart."},
    {"name": "Apollomon Darkness Mode", "types": ["dark", "fighting"], "role": "physical", "stage": "Ultimate",
     "legendary": True, "abilities": ["moxie", "h:pressure"],
     "entry": "Apollomon swallowed completely by darkness. Its flames have gone out, and it swings a great black "
              "axe at anything that shines."},
    {"name": "Aquilamon", "types": ["flying", "normal"], "role": "speed", "stage": "Adult",
     "abilities": ["keeneye", "h:bigpecks"],
     "entry": "A giant eagle that rules the sky over the plains. It rams its foes with its horns at full speed and "
              "fires rings of energy from its beak."},
    {"name": "Arbormon", "types": ["grass", "steel"], "role": "tank", "stage": "Adult",
     "abilities": ["overgrow", "h:sturdy"],
     "entry": "The warrior of wood, a puppet of carved timber. It fights with stretching arms and legs, and its "
              "wooden body shrugs off blows that would break stone."},
    {"name": "Archelomon", "types": ["water", "rock"], "role": "tank", "stage": "Adult",
     "abilities": ["shellarmor", "h:swiftswim"],
     "entry": "An ancient sea turtle born from the Digi-Egg of Sincerity. It glides through the water on its "
              "bladed flippers and ploughs through enemies with its spiked shell."},
    {"name": "Archnemon", "types": ["bug", "dark"], "role": "special", "stage": "Perfect",
     "abilities": ["swarm", "h:prankster"],
     "entry": "A demon beast who spins webs across the Digital World to catch the unwary. She laughs as she toys "
              "with her prey before striking with her spider legs."},
    {"name": "Arcturusmon", "types": ["dragon", "dark"], "role": "physical", "stage": "Ultimate",
     "abilities": ["toughclaws", "h:pressure"],
     "entry": "A dragon-man named for a bright star. It drives its spinning drill lances through anything in its "
              "way, and its wings blot out the night sky."},
    {"name": "Ariemon", "types": ["water", "psychic"], "role": "special", "stage": "Ultimate",
     "abilities": ["waterveil", "h:magicbounce"],
     "entry": "A sea sorceress who calls the tides with her shell staff. Her robes trail water wherever she goes, "
              "and her spells can raise the ocean floor."},
    {"name": "Arkadimon Baby", "types": ["bug", "dark"], "role": "speed", "stage": "Baby II",
     "abilities": ["swarm", "h:prankster"],
     "entry": "A small grey creature that skitters on four steel legs. It eats data to grow, and nobody knows what "
              "made it."},
    {"name": "Arkadimon Child", "types": ["dark"], "role": "physical", "stage": "Child",
     "abilities": ["moxie", "h:pressure"],
     "entry": "A pink imp that slashes with the blades on its arms. Every Digimon it defeats makes it stronger, for "
              "it absorbs their data."},
    {"name": "Arkadimon Adult", "types": ["dark", "fighting"], "role": "physical", "stage": "Adult",
     "abilities": ["moxie", "h:pressure"],
     "entry": "A gaunt beast that stalks on its huge hands. It grows in leaps by devouring the data of other "
              "Digimon, and nothing seems to satisfy its hunger."},
    {"name": "Arkadimon Perfect", "types": ["dark", "poison"], "role": "physical", "stage": "Perfect",
     "abilities": ["moxie", "h:pressure"],
     "entry": "Its shoulders sprout masses of crimson tentacles that seize its prey. It has eaten so much data that "
              "it can mimic the techniques of those it devoured."},
    {"name": "Arkadimon Ultimate", "types": ["dark", "dragon"], "role": "physical", "stage": "Ultimate",
     "abilities": ["moxie", "h:pressure"],
     "entry": "The bewitching beast grown into a winged demon. It has devoured whole armies of Digimon and is said "
              "to be close to becoming something no one can stop."},
    {"name": "Arkadimon Super Ultimate", "types": ["dark", "steel"], "role": "tank", "stage": "Super Ultimate",
     "abilities": ["pressure", "h:moxie"],
     "entry": "The final form of Arkadimon, a fortress-like head of steel the size of a hill. Its single eye sees "
              "every Digimon as food."},
    {"name": "Arkhai Angemon", "types": ["fairy", "fire"], "role": "mixed", "stage": "Perfect",
     "abilities": ["flashfire", "h:justified"],
     "entry": "An angel of the rank of Principality, who leads the lesser angels into battle. The flame of its torch "
              "never goes out, and evil cannot bear to look at it."},
    {"name": "Arma Lizamon", "types": ["poison", "rock"], "role": "physical", "stage": "Adult",
     "abilities": ["roughskin", "h:poisontouch"],
     "entry": "A lizard covered in overlapping spiked plates. It curls its tail over its back to strike with the "
              "green spear-tip, and its claws crackle with stored energy."},
    {"name": "Armadimon", "types": ["ground", "steel"], "role": "tank", "stage": "Child",
     "abilities": ["shellarmor", "h:sandveil"],
     "entry": "A cheerful armadillo that rolls into a ball when it is scared, or when it wants to bowl someone over. "
              "Its claws can dig through solid rock."},
    {"name": "Armagemon", "types": ["dark", "bug"], "role": "physical", "stage": "Ultimate", "legendary": True,
     "abilities": ["pressure", "h:moxie"],
     "entry": "The Armageddon of the Digital World, born when countless Digimon fused into one. It crawls over the "
              "land on its spindly legs, erasing everything in its path."},
    {"name": "Armamon", "types": ["steel", "fighting"], "role": "physical", "stage": "Ultimate",
     "abilities": ["sharpness", "h:steelworker"],
     "entry": "A living arsenal whose body is made of weapons. Every blade on it can be drawn and thrown, and it "
              "never runs out of swords."},
    {"name": "Armamon: Burst Mode", "types": ["steel", "fire"], "role": "physical", "stage": "Ultimate",
     "abilities": ["sharpness", "h:steelworker"],
     "entry": "Armamon at the peak of its power, its armour turned to burning bronze. A ring of swords floats round "
              "it, each ready to strike on its own."},
    {"name": "Arresterdramon", "types": ["dragon", "dark"], "role": "speed", "stage": "Adult",
     "abilities": ["pickpocket", "h:speedboost"],
     "entry": "A sly dragon-man who hunts treasure across the Digital World. Its anchor-hook tail snatches things "
              "from enemies before they notice."},
    {"name": "Arresterdramon: Superior Mode", "types": ["dragon", "flying"], "role": "speed", "stage": "Perfect",
     "abilities": ["pickpocket", "h:speedboost"],
     "entry": "Arresterdramon at full power. Its great yellow wings carry it faster than sound, and its tail ends "
              "in a golden trident."},
    {"name": "Arresterdramon: Superior Mode (Brave Snatcher)", "types": ["dragon", "steel"], "role": "physical",
     "stage": "Perfect", "abilities": ["toughclaws", "h:pickpocket"],
     "entry": "Superior Mode armed with the Brave Snatcher, a huge gauntlet that can grab and crush even the "
              "strongest Digimon. Its gold ring spins faster the harder it grips."},
    {"name": "Artiomon", "types": ["normal", "fighting"], "role": "physical", "stage": "Ultimate",
     "abilities": ["guts", "h:scrappy"],
     "entry": "A bear-beast huntress who guards the forests. Her spear never misses, and she roars loud enough to "
              "shake the trees bare."},
    {"name": "Assaultmon", "types": ["steel", "fighting"], "role": "physical", "stage": "Perfect",
     "abilities": ["megalauncher", "h:skilllink"],
     "entry": "A cyborg soldier sealed in a heavy mech-suit. It never stops firing its gatling arm, and its gas "
              "mask lets it fight through any smoke or poison."},
    {"name": "Astamon", "types": ["dark", "fire"], "role": "mixed", "stage": "Perfect",
     "abilities": ["intimidate", "h:skilllink"],
     "entry": "A demon lord who dresses like a gangster and settles every argument with its submachine gun. It is "
              "said to keep its word, and to expect the same of everyone else."},
    {"name": "Asuramon", "types": ["fighting", "fire"], "role": "physical", "stage": "Perfect",
     "abilities": ["ironfist", "h:justified"],
     "entry": "A wrathful guardian deity with a mane of flame. Its burning fists strike faster than a hundred "
              "blows a second, and it never retreats."},
    {"name": "Atamadekachimon", "types": ["dragon", "normal"], "role": "physical", "stage": "Adult",
     "abilities": ["strongjaw", "h:unaware"],
     "entry": "A dinosaur whose head is far bigger than the rest of it. It can barely walk without toppling over, "
              "but anything that ends up in its jaws is never seen again."},
    {"name": "Atlur Ballistamon", "types": ["bug", "steel"], "role": "physical", "stage": "Perfect",
     "abilities": ["ironfist", "h:motordrive"],
     "entry": "A beetle-robot heavyweight that charges its fists with lightning. One punch from its giant right "
              "hand can knock a mountain flat."},
    {"name": "Atlur Kabuterimon (Blue)", "types": ["bug", "electric"], "role": "physical", "stage": "Perfect",
     "abilities": ["swarm", "h:lightningrod"],
     "entry": "A hulking insect Digimon that fires lightning from its horns. Its six clawed limbs can tear through "
              "steel plate."},
    {"name": "Atlur Kabuterimon (Red)", "types": ["bug", "fire"], "role": "physical", "stage": "Perfect",
     "abilities": ["swarm", "h:flamebody"],
     "entry": "A crimson Atlur Kabuterimon whose hide burns hot to the touch. It hurls fireballs from its maw and "
              "never backs down from a fight."},
    {"name": "Atratusmon", "types": ["dark", "flying"], "role": "special", "stage": "Ultimate",
     "abilities": ["pressure", "h:magicbounce"],
     "entry": "A dark swan-knight whose wings blaze with magenta light. Its crystal shields reflect any attack back "
              "at the one who made it."},
    {"name": "Avenge Kidmon", "types": ["dark", "dragon"], "role": "special", "stage": "Ultimate",
     "abilities": ["sniper", "h:pressure"],
     "entry": "A dragon-man gunslinger who lives only for revenge. It hunts across the network with its gun-blade "
              "and never forgets a single wrong."},
    {"name": "Azhdarmon", "types": ["flying", "steel"], "role": "speed", "stage": "Perfect",
     "abilities": ["sharpness", "h:galewings"],
     "entry": "A pterosaur whose crest is a great axe-blade. It dives from the clouds at incredible speed, slicing "
              "anything below with its crest and wing blades."},
    # --- 0.99.0: the B section ------------------------------------------------------------------------------------
    {"name": "Baalmon", "types": ["dark", "fighting"], "role": "physical", "stage": "Perfect",
     "abilities": ["sharpness", "h:pressure"],
     "entry": "A wandering demon swordsman who hunts other demons. The talismans on its cape seal away the spirits "
              "of those it defeats."},
    {"name": "Baalmon (X-Antibody)", "types": ["dark", "psychic"], "role": "mixed", "stage": "Perfect",
     "abilities": ["magicguard", "h:pressure"],
     "entry": "Baalmon awakened by the X-Antibody. It reads curses from its spellbook and strikes with a gauntlet "
              "that has crushed a thousand demons."},
    {"name": "Babamon", "types": ["ghost", "psychic"], "role": "special", "stage": "Ultimate",
     "abilities": ["forewarn", "h:magicguard"],
     "entry": "An ancient Digimon who looks like a little old woman. She has outlived most of the Digital World and "
              "still sweeps evil away with her broom."},
    {"name": "Baboongamon", "types": ["rock", "fighting"], "role": "physical", "stage": "Adult",
     "abilities": ["rockhead", "h:guts"],
     "entry": "A baboon armoured in boulders. It swings the stone mace on its tail to crack open anything that "
              "challenges its troop."},
    {"name": "Babydmon", "types": ["dragon"], "role": "speed", "stage": "Baby II",
     "abilities": ["levitate", "h:hydration"],
     "entry": "A baby dragon that swims through the air with its curled tail. It blows tiny bubbles of fire when it "
              "is excited."},
    {"name": "Bacchusmon", "types": ["fairy", "poison"], "role": "special", "stage": "Ultimate", "legendary": True,
     "abilities": ["pressure", "h:gluttony"],
     "entry": "One of the Olympus Twelve, the god of wine and revelry. Its grin is wide enough to swallow a feast "
              "whole, and its parties can last for years."},
    {"name": "Bacomon", "types": ["normal", "ghost"], "role": "tank", "stage": "Child",
     "abilities": ["stamina", "h:pickup"],
     "entry": "A Digimon that lives inside a cardboard box. Nobody has ever seen what is inside, and it gets very "
              "upset if you try to look."},
    {"name": "Bagramon", "types": ["dark", "fighting"], "role": "physical", "stage": "Ultimate", "legendary": True,
     "abilities": ["pressure", "h:ironfist"],
     "entry": "The emperor of the Bagra Army. Its grafted arm can tear the code out of anything it grips, and it "
              "dreams of rewriting the whole Digital World."},
    {"name": "Bagramon (Archangel Form)", "types": ["fairy", "psychic"], "role": "special", "stage": "Ultimate",
     "legendary": True, "abilities": ["pressure", "h:serenegrace"],
     "entry": "Bagramon as it was before its fall, one of the archangels who served the Digital World. Its voice "
              "was said to calm any storm."},
    {"name": "Baihumon", "types": ["steel", "normal"], "role": "physical", "stage": "Ultimate", "legendary": True,
     "abilities": ["pressure", "h:toughclaws"],
     "entry": "The White Tiger, one of the Four Holy Beasts, who guards the west. Its golden orbs hold the power of "
              "metal, and its roar shakes the mountains."},
    {"name": "Bakemon", "types": ["ghost"], "role": "special", "stage": "Adult",
     "abilities": ["cursedbody", "h:levitate"],
     "entry": "A ghost hiding under a sheet. It loves to scare travellers, and nobody knows what its body looks "
              "like underneath."},
    {"name": "Bakumon", "types": ["psychic", "normal"], "role": "special", "stage": "Child",
     "abilities": ["insomnia", "h:magicguard"],
     "entry": "A holy beast that eats bad dreams. It wanders into sleeping minds at night and leaves only good "
              "dreams behind."},
    {"name": "Balli Bastemon", "types": ["normal", "fighting"], "role": "tank",
     "abilities": ["thickfat", "h:guts"],
     "entry": "A stout war-beast in tribal regalia. It stamps its clawed feet to a drumbeat only it can hear, and "
              "charges when the rhythm stops."},
    {"name": "Ballistamon", "types": ["steel", "bug"], "role": "physical", "stage": "Adult",
     "abilities": ["ironfist", "h:motordrive"],
     "entry": "A gentle beetle-robot that loves music. It only fights to protect its friends, but its giant fists can "
              "punch through a mountain."},
    {"name": "Ballistamon MC", "types": ["steel", "rock"], "role": "tank", "stage": "Ultimate",
     "abilities": ["shellarmor", "h:sturdy"],
     "entry": "Ballistamon grown into a walking fortress. Smaller Digimon shelter in the rooms inside it, and its "
              "towers fire on anything that threatens them."},
    {"name": "Ballistamon SR", "types": ["steel", "bug"], "role": "physical", "stage": "Perfect",
     "abilities": ["ironfist", "h:megalauncher"],
     "entry": "Ballistamon rebuilt for war, with a drill for a fist and twin cannons on its back. It still hums a "
              "tune as it fights."},
    {"name": "Baluchimon", "types": ["normal", "fairy"], "role": "tank", "stage": "Adult",
     "abilities": ["thickfat", "h:serenegrace"],
     "entry": "A holy beast of the high plains. The mist that flows from its back hides the traveller it protects, "
              "and its horn can call down rain."},
    {"name": "Bancho Golemon", "types": ["rock", "fighting"], "role": "tank", "stage": "Ultimate",
     "abilities": ["solidrock", "h:ironfist"],
     "entry": "The delinquent boss of the golems. It wears its torn coat with pride, and its drill-fist settles every "
              "argument for good."},
    {"name": "Bancho Leomon", "types": ["fighting", "fire"], "role": "physical", "stage": "Ultimate",
     "abilities": ["ironfist", "h:justified"],
     "entry": "The boss of all delinquent Digimon, who fights only for the weak. Its fists are said to be the "
              "strongest in the Digital World, and it never draws its sword in anger."},
    {"name": "Bancho Leomon: Burst Mode", "types": ["fighting", "fire"], "role": "physical", "stage": "Ultimate",
     "abilities": ["ironfist", "h:blaze"],
     "entry": "Bancho Leomon burning with its full spirit. Its whole body blazes gold, and a single punch can split "
              "the clouds."},
    {"name": "Bancho Lilimon", "types": ["grass", "fairy"], "role": "speed", "stage": "Ultimate",
     "abilities": ["technician", "h:justified"],
     "entry": "The delinquent boss of the fairies. Her thorned whip and spiked bud flail keep every troublemaker in "
              "the forest in line."},
    {"name": "Bancho Mamemon", "types": ["steel", "fighting"], "role": "physical", "stage": "Ultimate",
     "abilities": ["ironfist", "h:guts"],
     "entry": "The tiny boss of the Mamemon, with more pride than anyone ten times its size. Its bat and brass club "
              "have never lost a fight."},
    {"name": "Bancho Stingmon", "types": ["bug", "fighting"], "role": "speed", "stage": "Ultimate",
     "abilities": ["swarm", "h:sniper"],
     "entry": "The delinquent boss of the insects. It strikes faster than sight with its stinger lance, then walks "
              "off before its foe has fallen."},
    {"name": "Bao Huckmon", "types": ["dragon", "steel"], "role": "speed", "stage": "Adult",
     "abilities": ["speedboost", "h:toughclaws"],
     "entry": "A young dragon-knight that dashes across the battlefield on its thrusters. It dreams of joining the "
              "Royal Knights one day."},
    {"name": "Barbamon", "types": ["dark", "psychic"], "role": "special", "stage": "Ultimate", "legendary": True,
     "abilities": ["pressure", "h:pickpocket"],
     "entry": "One of the Seven Great Demon Lords, the Demon Lord of Greed. It hoards every treasure and every soul "
              "it can find, and trades in nothing but curses."},
    {"name": "Barbamon (X-Antibody)", "types": ["dark", "psychic"], "role": "special", "stage": "Ultimate",
     "legendary": True, "abilities": ["pressure", "h:magicguard"],
     "entry": "The Demon Lord of Greed awakened by the X-Antibody. A seal of crimson light burns above it, and its "
              "greed now reaches into the code of the world itself."},
    {"name": "Baromon", "types": ["fire", "dark"], "role": "special", "stage": "Adult",
     "abilities": ["flashfire", "h:intimidate"],
     "entry": "A demon-masked shaman born from the Digi-Egg of Kindness. Its dances call down fire and its mask is "
              "said to see the future."},
    {"name": "Bastemon", "types": ["normal", "psychic"], "role": "speed", "stage": "Perfect",
     "abilities": ["cutecharm", "h:limber"],
     "entry": "A cat-goddess who lives like a queen. Its gaze charms anyone who meets it, and its claws strike before "
              "they know they are in danger."},
    {"name": "Batterimon", "types": ["electric"], "role": "special", "stage": "Child",
     "abilities": ["static", "h:voltabsorb"],
     "entry": "A living battery that dozes until it is fully charged. It shares its spare power with any machine "
              "Digimon that runs low."},
    {"name": "Battle Armament Trailmon", "types": ["steel", "normal"], "role": "tank", "stage": "Adult",
     "abilities": ["megalauncher", "h:heavymetal"],
     "entry": "An armoured war-train that rolls along its own rails. Its turrets can fire in every direction at "
              "once, and nothing stops it once it builds up speed."},
    {"name": "Bearcatmon", "types": ["fighting", "dark"], "role": "speed", "stage": "Perfect",
     "abilities": ["ironfist", "h:speedboost"],
     "entry": "A bearcat that skates into battle on jet boots. Its spiked fist hits like a train, and it never "
              "misses a chance to show off."},
    {"name": "Bearmon", "types": ["normal", "fighting"], "role": "physical", "stage": "Child",
     "abilities": ["guts", "h:ironfist"],
     "entry": "A scrappy bear cub that wears its cap backwards. It practises its punches all day long and dreams of "
              "becoming the strongest Digimon around."},
    {"name": "Beel Starmon", "types": ["dark", "steel"], "role": "special", "stage": "Ultimate",
     "abilities": ["sniper", "h:pressure"],
     "entry": "A Demon Lord gunslinger who fights alongside her floating Star-bits. Her pistols never miss, and she "
              "never forgives a broken promise."},
    {"name": "Beel Starmon (X-Antibody)", "types": ["dark", "flying"], "role": "special", "stage": "Ultimate",
     "abilities": ["sniper", "h:pressure"],
     "entry": "Beel Starmon awakened by the X-Antibody, on wings of violet feathers. Her rifle can hit a target on "
              "the far side of the Digital World."},
    {"name": "Beelzebumon", "types": ["dark", "steel"], "role": "physical", "stage": "Ultimate", "legendary": True,
     "abilities": ["pressure", "h:moxie"],
     "entry": "One of the Seven Great Demon Lords, the Demon Lord of Gluttony. A lone demon biker who answers to no "
              "one, and fires its twin shotguns faster than the eye can follow."},
    {"name": "Beelzebumon (X-Antibody)", "types": ["dark", "flying"], "role": "physical", "stage": "Ultimate",
     "legendary": True, "abilities": ["pressure", "h:moxie"],
     "entry": "The Demon Lord of Gluttony awakened by the X-Antibody, on great blue wings. Its arm cannon can "
              "devour the light of a star."},
    {"name": "Beelzebumon: Blast Mode", "types": ["dark", "flying"], "role": "special", "stage": "Ultimate",
     "legendary": True, "abilities": ["pressure", "h:megalauncher"],
     "entry": "Beelzebumon at full power, on ten black wings. Its positron cannon erases anything in its path, and "
              "its demon claw can tear through any armour."},
    {"name": "Belial Vamdemon", "types": ["dark", "ghost"], "role": "physical", "stage": "Ultimate",
     "legendary": True, "abilities": ["pressure", "h:strongjaw"],
     "entry": "The final form of Vamdemon's ambition. Its second face in its chest speaks curses while its main head "
              "devours, and its wings blot out the sun."},
    {"name": "Belphemon (X-Antibody)", "types": ["dark", "steel"], "role": "physical", "stage": "Ultimate",
     "legendary": True, "abilities": ["pressure", "h:toughclaws"],
     "entry": "The Demon Lord of Sloth awakened by the X-Antibody, armoured in gold and crystal. Its wrath when it "
              "wakes could level a continent."},
    {"name": "Belphemon: Rage Mode", "types": ["dark", "fighting"], "role": "physical", "stage": "Ultimate",
     "legendary": True, "abilities": ["pressure", "h:moxie"],
     "entry": "The Demon Lord of Sloth awake at last. It wakes only once in a thousand years, and in its rage it "
              "destroys everything around it with claws of green fire."},
    {"name": "Belphemon: Sleep Mode", "types": ["dark", "normal"], "role": "tank", "stage": "Ultimate",
     "legendary": True, "abilities": ["comatose", "h:pressure"],
     "entry": "One of the Seven Great Demon Lords, fast asleep. It dozes for a thousand years at a time, and even "
              "asleep it attacks whatever comes too close."},
    {"name": "BEMmon", "types": ["dark", "psychic"], "role": "speed", "stage": "Child",
     "abilities": ["infiltrator", "h:download"],
     "entry": "A little alien raider from beyond the network. It sneaks into systems to steal their data, and its "
              "one green eye can see through walls."},
    {"name": "Beowolfmon", "types": ["steel", "fairy"], "role": "physical", "stage": "Perfect",
     "abilities": ["justified", "h:sharpness"],
     "entry": "The beast warrior of light, a wolf knight wielding a double-ended blade of gold. Its cannon arm "
              "fires bolts of pure light."},
    {"name": "Berserk Titamon", "types": ["dark", "rock"], "role": "physical", "stage": "Ultimate",
     "legendary": True, "abilities": ["pressure", "h:angerpoint"],
     "entry": "A god of the Titans driven mad. Its armour is rotting away, red rage burns through every crack, and "
              "its greatsword cuts mountains in half."},
    {"name": "Beso Bombmon", "types": ["normal"], "role": "mixed", "stage": "Child",
     "abilities": ["aftermath", "h:pickup"],
     "entry": "A Digimon known only by its shadow. Nobody has seen it clearly yet, and every sighting tells a "
              "different story."},
    {"name": "Betamon", "types": ["water", "electric"], "role": "special", "stage": "Child",
     "abilities": ["swiftswim", "h:static"],
     "entry": "An amphibian Digimon that lives in rivers and lakes. Its fin crest stores electricity, and it zaps "
              "anything that bothers it."},
    {"name": "Betamon (X-Antibody)", "types": ["water", "electric"], "role": "special", "stage": "Child",
     "abilities": ["swiftswim", "h:voltabsorb"],
     "entry": "Betamon awakened by the X-Antibody. Its fin glows red-hot with charge and the spikes along its sides "
              "spark when it is angry."},
    {"name": "Betel Gammamon", "types": ["dragon", "fire"], "role": "physical", "stage": "Adult",
     "abilities": ["blaze", "h:moxie"],
     "entry": "A red dragon-man of explosive power. Its scarf streams behind it like wings as it dashes in, fists "
              "wrapped in dark fire."},
    {"name": "Betsumon", "types": ["normal", "ghost"], "role": "physical", "stage": "Perfect",
     "abilities": ["prankster", "h:ironfist"],
     "entry": "A puppet that wears a cat suit and never takes it off. Its smug look never changes, even when its "
              "huge paw-gloves are pounding a foe flat."},
    {"name": "Bibimon", "types": ["electric"], "role": "speed", "stage": "Baby II",
     "abilities": ["static", "h:motordrive"],
     "entry": "A little ball of spikes that crackles with static. It rolls around so fast that it glows."},
    {"name": "Big Mamemon", "types": ["steel", "fighting"], "role": "tank", "stage": "Perfect",
     "abilities": ["ironfist", "h:heavymetal"],
     "entry": "A Mamemon that just kept growing. It is slow but impossibly heavy, and its boxing-glove fists can "
              "flatten a fortress."},
    {"name": "Big Ukkomon", "types": ["fairy", "ghost"], "role": "special", "stage": "Ultimate",
     "abilities": ["levitate", "h:cursedbody"],
     "entry": "An ancient fairy spirit that drifts through the clouds. Its laugh echoes for miles, and the orb in "
              "its belly holds a thousand years of dreams."},
    {"name": "Bio Coatlmon", "types": ["dragon", "flying"], "role": "special", "stage": "Adult",
     "abilities": ["flashfire", "h:serenegrace"],
     "entry": "A feathered serpent born of a Bio Hybrid. It soars on white wings and lights the sky with the torch "
              "at the end of its tail."},
    {"name": "Bio Darkdramon", "types": ["dragon", "electric"], "role": "physical", "stage": "Ultimate",
     "abilities": ["lightningrod", "h:pressure"],
     "entry": "A Bio Hybrid dragon-knight charged with lightning. Its lance carries the full strength of the storm, "
              "and its axe-tail cuts down anything behind it."},
    {"name": "Bio Lotusmon", "types": ["grass", "psychic"], "role": "special", "stage": "Ultimate",
     "abilities": ["naturalcure", "h:magicbounce"],
     "entry": "A Bio Hybrid lotus fairy whose dance calms every storm. Her staff can make a whole forest bloom, or "
              "wither it in a breath."},
    {"name": "Bio Spinomon", "types": ["dragon", "steel"], "role": "physical", "stage": "Ultimate",
     "abilities": ["roughskin", "h:pressure"],
     "entry": "A Bio Hybrid spinosaur. The steel blades of its sail spin up into a storm of edges that can cut "
              "through mountains."},
    {"name": "Bio Stegomon", "types": ["rock", "water"], "role": "tank", "stage": "Adult",
     "abilities": ["shellarmor", "h:swiftswim"],
     "entry": "A Bio Hybrid stegosaur. Its back plates channel the power of the sea, and it charges like a tidal "
              "wave."},
    {"name": "Bio Thunderbirmon", "types": ["electric", "flying"], "role": "speed", "stage": "Adult",
     "abilities": ["lightningrod", "h:galewings"],
     "entry": "A Bio Hybrid thunderbird. Each beat of its wings throws bolts of lightning from the feather tips."},
    {"name": "Birdramon", "types": ["fire", "flying"], "role": "special", "stage": "Adult",
     "abilities": ["flamebody", "h:galewings"],
     "entry": "A giant bird of fire. It soars on wings of living flame and rains fireballs on anything below."},
    {"name": "Bishop Chessmon (Black)", "types": ["dark", "psychic"], "role": "special", "stage": "Perfect",
     "abilities": ["magicguard", "h:pressure"],
     "entry": "The bishop of the black chess army. It moves only on the diagonal, and its staff casts curses on "
              "anything in its line."},
    {"name": "Bishop Chessmon (White)", "types": ["fairy", "psychic"], "role": "special", "stage": "Perfect",
     "abilities": ["magicguard", "h:justified"],
     "entry": "The bishop of the white chess army. It guards the white king with blessings, and its long neck "
              "lets it watch the whole battlefield."},
    {"name": "Bitmon", "types": ["normal", "electric"], "role": "speed", "stage": "Adult",
     "abilities": ["static", "h:cutecharm"],
     "entry": "A pink armoured mouse-cat born from a Digi-Egg. Its long ribbon ears sense electric signals, and it "
              "darts away faster than you can blink."},
    {"name": "Black Galgomon", "types": ["dark", "normal"], "role": "physical", "stage": "Adult",
     "abilities": ["skilllink", "h:moxie"],
     "entry": "A dark twin of Galgomon. It sprays its gatling arms wildly and laughs while it does it."},
    {"name": "Black Gaogamon", "types": ["dark", "fighting"], "role": "physical", "stage": "Adult",
     "abilities": ["ironfist", "h:intimidate"],
     "entry": "A dark twin of Gaogamon. It boxes with its red-gloved forelegs and stings with its steel tail."},
    {"name": "Black Growmon", "types": ["dark", "dragon"], "role": "physical", "stage": "Adult",
     "abilities": ["blaze", "h:moxie"],
     "entry": "A dark twin of Growmon, born from a corrupted Guilmon. Its elbow blades slash with terrible speed, "
              "and its fire burns black."},
    {"name": "Black Guilmon", "types": ["dark", "dragon"], "role": "physical", "stage": "Child",
     "abilities": ["blaze", "h:moxie"],
     "entry": "A Guilmon whose data turned dark. It carries the same Hazard mark, but its temper is far wilder."},
    {"name": "Black King Numemon", "types": ["poison", "steel"], "role": "tank", "stage": "Perfect",
     "abilities": ["stickyhold", "h:heavymetal"],
     "entry": "A Numemon who became king and never lets anyone forget it. Its silver crown is the heaviest thing in "
              "the slug kingdom."},
    {"name": "Black Mach Gaogamon", "types": ["dark", "fighting"], "role": "speed", "stage": "Perfect",
     "abilities": ["ironfist", "h:speedboost"],
     "entry": "A dark twin of Mach Gaogamon. It blasts in on its jetpack and strikes with its steel gauntlet before "
              "the foe can react."},
    {"name": "Black Megalo Growmon", "types": ["dark", "steel"], "role": "mixed", "stage": "Perfect",
     "abilities": ["megalauncher", "h:moxie"],
     "entry": "A dark cyborg twin of Megalo Growmon. Its twin chest cannons fire black fire, and its mechanical "
              "wings let it leap across whole valleys."},
    {"name": "Black Rapidmon", "types": ["dark", "steel"], "role": "speed", "stage": "Perfect",
     "abilities": ["speedboost", "h:megalauncher"],
     "entry": "A dark twin of Rapidmon. Its rocket ears carry it at blinding speed while its arm cannons fire "
              "homing shots."},
    {"name": "Black Saint Galgomon", "types": ["dark", "steel"], "role": "mixed", "stage": "Ultimate",
     "abilities": ["megalauncher", "h:skilllink"],
     "entry": "A dark twin of Saint Galgomon, a walking arsenal. The warheads on its back can level a city block."},
    {"name": "Black Seraphimon", "types": ["dark", "fairy"], "role": "special", "stage": "Ultimate",
     "legendary": True, "abilities": ["pressure", "h:cursedbody"],
     "entry": "A seraph who fell to darkness, spreading ten bat-wings. The violet orbs in its hands swallow the "
              "light of anything they touch."},
    {"name": "Black Shoutmon X7", "types": ["dark", "dragon"], "role": "physical", "stage": "Ultimate",
     "legendary": True, "abilities": ["pressure", "h:moxie"],
     "entry": "The dark fusion of seven Digimon, a towering knight with a dragon's head on its shoulder. Its sword "
              "carries the strength of all seven."},
    {"name": "Black Tailmon", "types": ["dark", "normal"], "role": "speed", "stage": "Adult",
     "abilities": ["prankster", "h:limber"],
     "entry": "A dark twin of Tailmon. Its claws are just as sharp, but it uses them to cause trouble instead of "
              "stopping it."},
    {"name": "Black Tailmon Uver.", "types": ["dark", "normal"], "role": "speed", "stage": "Adult",
     "abilities": ["prankster", "h:pickup"],
     "entry": "Black Tailmon dressed for a day out with its backpack. It looks sleepy, but nothing escapes its "
              "notice."},
    {"name": "Black War Greymon", "types": ["dark", "dragon"], "role": "physical", "stage": "Ultimate",
     "abilities": ["toughclaws", "h:pressure"],
     "entry": "A dark twin of War Greymon born from a Control Spire. It searches for a reason to exist, and its "
              "Dramon Destroyers cut through any armour."},
    {"name": "Black War Greymon (X-Antibody)", "types": ["dark", "dragon"], "role": "physical",
     "stage": "Ultimate", "abilities": ["toughclaws", "h:pressure"],
     "entry": "Black War Greymon awakened by the X-Antibody. Its Brave Shield splits open into blade-wings, and "
              "red light burns along every seam of its armour."},
    {"name": "Black War Greymon: \"G\" Erosion Mode", "types": ["dark", "poison"], "role": "physical",
     "stage": "Ultimate", "legendary": True, "abilities": ["pressure", "h:moxie"],
     "entry": "Black War Greymon eroded by a monstrous power. Violet spines burst from its back, and it no longer "
              "remembers anything but destruction."},
    {"name": "Blade Kuwagamon", "types": ["bug", "steel"], "role": "speed", "stage": "Adult",
     "abilities": ["sharpness", "h:speedboost"],
     "entry": "A stag beetle that became a living blade. It slices through the air with a crack of lightning, "
              "cutting anything in its flight path."},
]
