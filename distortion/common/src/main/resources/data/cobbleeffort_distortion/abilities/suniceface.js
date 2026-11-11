{
onStart(pokemon) {
      if (
        this.field.isWeather(["sunnyday", "desolateland"]) &&
        pokemon.species.id === "eiscuenoice"
      ) {
        this.add("-activate", pokemon, "ability: Sun Ice Face");
        this.effectState.busted = false;
        pokemon.formeChange("Eiscue", this.effect, true);
      }
    },
"onDamagePriority": 1,
onDamage(damage, target, source, effect) {
      if (
        effect?.effectType === "Move" &&
        effect.category === "Physical" &&
        target.species.id === "eiscue"
      ) {
        this.add("-activate", target, "ability: Sun Ice Face");
        this.effectState.busted = true;
        return 0;
      }
    },
onCriticalHit(target, type, move) {
      if (!target) return;
      if (move.category !== "Physical" || target.species.id !== "eiscue")
        return;
      if (
        target.volatiles["substitute"] &&
        !(move.flags["bypasssub"] || move.infiltrates)
      )
        return;
      if (!target.runImmunity(move.type)) return;
      return false;
    },
onEffectiveness(typeMod, target, type, move) {
      if (!target) return;
      if (move.category !== "Physical" || target.species.id !== "eiscue")
        return;
      const hitSub =
        target.volatiles["substitute"] &&
        !move.flags["bypasssub"] &&
        !(move.infiltrates && this.gen >= 6);
      if (hitSub) return;
      if (!target.runImmunity(move.type)) return;
      return 0;
    },
onUpdate(pokemon) {
      if (pokemon.species.id === "eiscue" && this.effectState.busted) {
        pokemon.formeChange("Eiscue-Noice", this.effect, true);
      }
    },
onWeatherChange(pokemon, source, sourceEffect) {
      if (sourceEffect?.suppressWeather) return;
      if (!pokemon.hp) return;
      if (
        this.field.isWeather(["sunnyday", "desolateland"]) &&
        pokemon.species.id === "eiscuenoice"
      ) {
        this.add("-activate", pokemon, "ability: Sun Ice Face");
        this.effectState.busted = false;
        pokemon.formeChange("Eiscue", this.effect, true);
      }
    },
"flags": {"failroleplay":1,"noreceiver":1,"noentrain":1,"notrace":1,"failskillswap":1,"cantsuppress":1,"breakable":1,"notransform":1},
"name": "Sun Ice Face",
"rating": 3,
"num": -31137
}
