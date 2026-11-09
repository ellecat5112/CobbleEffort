{
"onSourceModifyAtkPriority": 6,
onSourceModifyAtk(atk, attacker, defender, move) {
      if (move.type === "Fire" || move.type === "Fire") {
        this.debug("Thick Fat weaken");
        return this.chainModify(0.5);
      }
    },
"onSourceModifySpAPriority": 5,
onSourceModifySpA(atk, attacker, defender, move) {
      if (move.type === "Fire" || move.type === "Fire") {
        this.debug("Thick Fat weaken");
        return this.chainModify(0.5);
      }
    },
"flags": {"breakable":1},
"name": "Insulation",
"rating": 3.5,
"num": -31110
}
