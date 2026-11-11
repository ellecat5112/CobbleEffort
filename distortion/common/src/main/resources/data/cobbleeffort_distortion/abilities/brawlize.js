{
"onModifyTypePriority": 1,
onModifyType(move, pokemon) {
      const noModifyType = [
        "hiddenpower",
        "judgment",
        "multiattack",
        "naturalgift",
        "revelationdance",
        "struggle",
        "technoblast",
        "terrainpulse",
        "weatherball",
      ];
      if (
        !(move.isZ && move.category !== "Status") &&
        !noModifyType.includes(move.id) && 
        !(move.name === "Tera Blast" && pokemon.terastallized)
      ) {
        move.type = "Fighting";
        move.typeChangerBoosted = this.effect;
      }
    },
"onBasePowerPriority": 23,
onBasePower(basePower, pokemon, target, move) {
      if (move.typeChangerBoosted === this.effect)
        return this.chainModify([4915, 4096]);
    },
"flags": {},
"name": "Brawlize",
"rating": 0,
"num": -31130
}
