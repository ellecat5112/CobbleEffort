{
"onModifyAtkPriority": 5,
onModifyAtk(atk, attacker, defender, move) {
      if (move.type === "Flying" && attacker.hp <= attacker.maxhp / 3) {
        this.debug("Torrent boost");
        return this.chainModify(1.5);
      }
    },
"onModifySpAPriority": 5,
onModifySpA(atk, attacker, defender, move) {
      if (move.type === "Flying" && attacker.hp <= attacker.maxhp / 3) {
        this.debug("Torrent boost");
        return this.chainModify(1.5);
      }
    },
"flags": {},
"name": "Flying Fervor",
"rating": 2,
"num": -31138
}
