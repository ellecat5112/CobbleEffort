{
onPreStart(pokemon) {
      if (pokemon.species.id === "xerneas") {
        pokemon.formeChange("xerneasactive", false);
      }
    },
onStart(pokemon) {
      if (this.suppressingAbility(pokemon)) return;
      this.add("-ability", pokemon, "Fairy Aura");
    },
"onAnyBasePowerPriority": 20,
onAnyBasePower(basePower, source, target, move) {
      if (
        target === source ||
        move.category === "Status" ||
        move.type !== "Steel"
      )
        return;
      if (!move.auraBooster?.hasAbility("Fairy Aura"))
        move.auraBooster = this.effectState.target;
      if (move.auraBooster !== this.effectState.target) return;
      return this.chainModify([move.hasAuraBreak ? 3072 : 5448, 4096]);
    },
"flags": {},
"name": "Steel Aura",
"rating": 3,
"num": -31159
}
