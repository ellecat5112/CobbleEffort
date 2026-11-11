{
"onBasePowerPriority": 21,
onBasePower(basePower, attacker, defender, move) {
      if (this.field.isWeather("sandstorm")) {
        if (
          move.type === "Fighting" ||
          move.type === "Ground" ||
          move.type === "Ground"
        ) {
          this.debug("Sand Force boost");
          return this.chainModify([5325, 4096]);
        }
      }
    },
onImmunity(type, pokemon) {
      if (type === "sandstorm") return false;
    },
"flags": {},
"name": "Fighting Sand Force",
"rating": 2,
"num": -31153
}
