{
onStart(pokemon) {
      if (this.suppressingAbility(pokemon)) return;
      this.add("-ability", pokemon, "Dark Aura");
    },
"onAnyBasePowerPriority": 20,
onAnyBasePower(basePower, source, target, move) {
      if (
        target === source ||
        move.category === "Status" ||
        move.type !== "Fairy"
      )
        return;
      if (!move.auraBooster?.hasAbility("Dark Aura"))
        move.auraBooster = this.effectState.target;
      if (move.auraBooster !== this.effectState.target) return;
      return this.chainModify([move.hasAuraBreak ? 3072 : 5448, 4096]);
    },
"flags": {},
"name": "Fairy Aura",
"rating": 3,
"num": -31160
}
