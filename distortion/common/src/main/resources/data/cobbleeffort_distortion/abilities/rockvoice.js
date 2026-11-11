{
"onModifyTypePriority": -1,
onModifyType(move, pokemon) {
      if (move.flags["sound"] && !pokemon.volatiles["dynamax"]) {
        move.type = "Rock";
      }
    },
"flags": {},
"name": "Rock Voice",
"rating": 1.5,
"num": -31117
}
