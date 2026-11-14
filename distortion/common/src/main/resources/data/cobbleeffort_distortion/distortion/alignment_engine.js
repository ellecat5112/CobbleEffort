(function () {
  /* The Shadow and Crystal types in Cobblemon's battle engine (Showdown), run by AlignmentEngine before battles.
     Shadow (Pokemon XD): Shadow moves hit every non-Shadow Pokemon for 2x, Shadow Pokemon for 0.5x, whatever their
     other type; only Crystal hits Shadow Pokemon super effectively.
     Crystal (glassy, like the Crystal Onix): weak to Fighting, Ground, Steel and Rock; resists Water, Ice, Electric,
     Normal and Crystal; refracts special attacks (3/4 damage); its attacks are 2x on Dark, Ghost, Dragon and Shadow,
     0.5x on Steel, Rock, Fire and Crystal.
     A Pokemon whose UUID is in globalThis.__ceAlign gets [its first type, Shadow|Crystal] whenever its species is set. */
  globalThis.__ceAlign = globalThis.__ceAlign || {};
  const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
  const CRYSTAL_TAKEN = {Fighting: 1, Ground: 1, Steel: 1, Rock: 1, Water: 2, Ice: 2, Electric: 2, Normal: 2, Crystal: 2};
  const CRYSTAL_HITS = {Dark: 1, Ghost: 1, Dragon: 1, Shadow: 1, Steel: 2, Rock: 2, Fire: 2};
  const SHADOW_TAKEN = {Crystal: 1};
  const patch = function (dex) {
    const cache = dex.dataCache;
    if (!cache || !cache.TypeChart) return false;
    if (cache.TypeChart.shadow && cache.TypeChart.crystal) return false;
    const chart = {};
    for (const id in cache.TypeChart) {
      const e = cache.TypeChart[id];
      const taken = Object.assign({}, e.damageTaken, {Shadow: 0, Crystal: CRYSTAL_HITS[cap(id)] || 0});
      chart[id] = Object.assign({}, e, {damageTaken: taken});
    }
    const all = {};
    for (const id in chart) all[cap(id)] = 0;
    chart.shadow = {damageTaken: Object.assign({}, all, {Shadow: 0, Crystal: 0}, SHADOW_TAKEN), isNonstandard: 'Custom'};
    chart.crystal = {damageTaken: Object.assign({}, all, {Shadow: 0, Crystal: 0}, CRYSTAL_TAKEN), isNonstandard: 'Custom'};
    cache.TypeChart = chart;
    dex.types.typeCache.clear();
    dex.types.allCache = null;
    dex.types.namesCache = null;
    return true;
  };
  const {Dex} = require('./sim/dex');
  Dex.includeData();
  patch(Dex);
  for (const id in Dex.dexes) {
    const d = Dex.dexes[id];
    if (id === 'cobblemon' || d.dataCache) {
      try { d.includeData(); } catch (e) {}
      patch(d);
    }
  }

  const P = require('./sim/pokemon').Pokemon;
  if (!P.prototype.runEffectiveness.__ceAlign) {
    const runEffectiveness = P.prototype.runEffectiveness;
    const wrapped = function (move) {
      if (move && move.type === 'Shadow') return this.hasType('Shadow') ? -1 : 1;
      return runEffectiveness.call(this, move);
    };
    wrapped.__ceAlign = true;
    P.prototype.runEffectiveness = wrapped;
  }
  /* other add-ons (CobbleEffort: Fusion) wrap setSpecies too and set their own types: ours must run last, so it
     wraps again whenever it isn't the outermost */
  if (!P.prototype.setSpecies.__ceAlign) {
    const setSpecies = P.prototype.setSpecies;
    const wrapped = function (rawSpecies, source, isTransform) {
      const species = setSpecies.call(this, rawSpecies, source, isTransform);
      const a = globalThis.__ceAlign[this.uuid];
      if (!species || !a || isTransform || this.terastallized) return species;
      const first = this.types.find(t => t !== 'Shadow' && t !== 'Crystal') || 'Normal';
      const types = [first, a];
      this.setType(types, true);
      this.apparentType = types.join('/');
      return species;
    };
    wrapped.__ceAlign = true;
    P.prototype.setSpecies = wrapped;
  }

  const BA = require('./sim/battle-actions').BattleActions;
  if (!BA.prototype.modifyDamage.__ceAlign) {
    const modifyDamage = BA.prototype.modifyDamage;
    const wrapped = function (baseDamage, pokemon, target, move, suppressMessages) {
      let d = modifyDamage.call(this, baseDamage, pokemon, target, move, suppressMessages);
      if (typeof d === 'number' && d > 1 && move.category === 'Special' && target.hasType('Crystal')) {
        d = Math.max(1, Math.floor(d * 0.75));            /* the crystal body refracts special attacks */
      }
      return d;
    };
    wrapped.__ceAlign = true;
    BA.prototype.modifyDamage = wrapped;
  }
  globalThis.__ceAlignInstalled = true;
  return 'ok';
})();
