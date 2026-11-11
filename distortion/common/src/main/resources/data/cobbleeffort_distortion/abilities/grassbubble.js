{
"onSourceModifyAtkPriority": 5,
onSourceModifyAtk(atk, attacker, defender, move) {
      if (move.type === "Fire") {
        return this.chainModify(0.5);
      }
    },
"onSourceModifySpAPriority": 5,
onSourceModifySpA(atk, attacker, defender, move) {
      if (move.type === "Fire") {
        return this.chainModify(0.5);
      }
    },
onModifyAtk(atk, attacker, defender, move) {
      if (move.type === "Grass") {
        return this.chainModify(2);
      }
    },
onModifySpA(atk, attacker, defender, move) {
      if (move.type === "Grass") {
        return this.chainModify(2);
      }
    },
onUpdate(pokemon) {
      if (pokemon.status === "brn") {
        this.add("-activate", pokemon, "ability: Grass Bubble");
        pokemon.cureStatus();
      }
    },
onSetStatus(status, target, source, effect) {
      if (status.id !== "brn") return;
      if (effect?.status) {
        this.add("-immune", target, "[from] ability: Grass Bubble");
      }
      return false;
    },
"flags": {"breakable":1},
"name": "Grass Bubble",
"rating": 4.5,
"num": -31107
}
