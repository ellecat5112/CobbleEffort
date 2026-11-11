{
"onModifyAtkPriority": 5,
onModifyAtk(atk, attacker, defender, move) {
      if (move.type === "Dark" && attacker.hp <= attacker.maxhp / 3) {
        this.debug("Blaze boost");
        return this.chainModify(1.5);
      }
    },
"onModifySpAPriority": 5,
onModifySpA(atk, attacker, defender, move) {
      if (move.type === "Dark" && attacker.hp <= attacker.maxhp / 3) {
        this.debug("Blaze boost");
        return this.chainModify(1.5);
      }
    },
"flags": {},
"name": "Dark Fervor",
"rating": 2,
"num": -31125
}
