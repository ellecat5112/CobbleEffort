{
"onModifyAtkPriority": 5,
onModifyAtk(atk, attacker, defender, move) {
      if (move.type === "Ground") {
        this.debug("Transistor boost");
        return this.chainModify([5325, 4096]);
      }
    },
"onModifySpAPriority": 5,
onModifySpA(atk, attacker, defender, move) {
      if (move.type === "Ground") {
        this.debug("Transistor boost");
        return this.chainModify([5325, 4096]);
      }
    },
"flags": {},
"name": "Ground Transistor",
"rating": 3.5,
"num": -31156
}
