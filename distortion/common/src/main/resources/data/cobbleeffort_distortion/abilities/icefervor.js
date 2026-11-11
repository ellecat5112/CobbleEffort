{
"onModifyAtkPriority": 5,
onModifyAtk(atk, attacker, defender, move) {
      if (move.type === "Ice" && attacker.hp <= attacker.maxhp / 3) {
        this.debug("Blaze boost");
        return this.chainModify(1.5);
      }
    },
"onModifySpAPriority": 5,
onModifySpA(atk, attacker, defender, move) {
      if (move.type === "Ice" && attacker.hp <= attacker.maxhp / 3) {
        this.debug("Blaze boost");
        return this.chainModify(1.5);
      }
    },
"flags": {},
"name": "Ice Fervor",
"rating": 2,
"num": -31116
}
