{
"onModifyTypePriority": -1,
onModifyType(move, pokemon) {
      if (move.flags["sound"] && !pokemon.volatiles["dynamax"]) {
        move.type = "Grass";
      }
    },
"flags": {},
"name": "Blossom Voice",
"rating": 1.5,
"num": -31102
}
