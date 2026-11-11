{
"onSourceModifyAtkPriority": 6,
onSourceModifyAtk(atk, attacker, defender, move) {
      if (move.type === "Ice" || move.type === "Psychic") {
        this.debug("Thick Fat weaken");
        return this.chainModify(0.5);
      }
    },
"onSourceModifySpAPriority": 5,
onSourceModifySpA(atk, attacker, defender, move) {
      if (move.type === "Ice" || move.type === "Psychic") {
        this.debug("Thick Fat weaken");
        return this.chainModify(0.5);
      }
    },
"flags": {"breakable":1},
"name": "Psychic Thick Fat",
"rating": 3.5,
"num": -31153
}
