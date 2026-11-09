{
"onModifyTypePriority": -1,
onModifyType(move, pokemon) {
      const noModifyType = [
        "judgment",
        "multiattack",
        "naturalgift",
        "revelationdance",
        "technoblast",
        "terrainpulse",
        "weatherball",
      ];
      if (
        move.type === "Normal" &&
        !noModifyType.includes(move.id) &&
        !(move.isZ && move.category !== "Status") &&
        !(move.name === "Tera Blast" && pokemon.terastallized)
      ) {
        move.type = "Ground";
        move.typeChangerBoosted = this.effect;
      }
    },
"onBasePowerPriority": 23,
onBasePower(basePower, pokemon, target, move) {
      if (move.typeChangerBoosted === this.effect)
        return this.chainModify([4915, 4096]);
    },
"flags": {},
"name": "Tectonize",
"rating": 4,
"num": -31114
}
