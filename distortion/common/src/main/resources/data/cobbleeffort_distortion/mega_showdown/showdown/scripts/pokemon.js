({
  setSpecies(rawSpecies, source, isTransform) {
    const Pokemon = require("./sim/pokemon").Pokemon;
    const species = Pokemon.prototype.setSpecies.call(this, rawSpecies, source, isTransform);
    if (species && this.distorted && !isTransform) this.battle.actions.applyDistortTypes(this);
    return species;
  },
})
