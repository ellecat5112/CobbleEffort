{
onModifyPriority(priority, pokemon, target, move) {
      if (move?.type === "Electric" && pokemon.hp === pokemon.maxhp)
        return priority + 1;
    },
"flags": {},
"name": "Electric Gale Wings",
"rating": 1.5,
"num": -31141
}
