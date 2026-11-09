{
"onAllyBasePowerPriority": 22,
onAllyBasePower(basePower, attacker, defender, move) {
      if (move.type === "Ground") {
        this.debug("Steely Spirit boost");
        return this.chainModify(1.5);
      }
    },
"flags": {},
"name": "Earthen Spirit",
"rating": 3.5,
"num": -31121
}
