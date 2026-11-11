{
"onModifyAtkPriority": 5,
onModifyAtk(atk, attacker, defender, move) {
      if (move.type === "Fairy") {
        this.debug("Dragon's Maw boost");
        return this.chainModify(1.5);
      }
    },
"onModifySpAPriority": 5,
onModifySpA(atk, attacker, defender, move) {
      if (move.type === "Fairy") {
        this.debug("Dragon's Maw boost");
        return this.chainModify(1.5);
      }
    },
"flags": {},
"name": "Fairy's Maw",
"rating": 3.5,
"num": -31156
}
