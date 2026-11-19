(function () {
  /* CobbleEffort: Digital's rules in Cobblemon's battle engine (Showdown), run by DigitalEngine.
     The attribute triangle: Vaccine beats Virus, Virus beats Data, Data beats Vaccine. A Digimon hitting the attribute
     it beats does 1.25x damage, hitting the one that beats it 0.8x (Free and Variable are neutral); Bug Code
     (volatile 'bugcode') on either side inverts that.
     Field buffs: a Digimon whose field suits the battleground (DigitalEngine works it out as the battle starts) does
     1.15x damage.
     globalThis.__ceDigi: UUID -> attribute; globalThis.__ceDigiField: UUID -> the field that is boosted. */
  globalThis.__ceDigi = globalThis.__ceDigi || {};
  globalThis.__ceDigiField = globalThis.__ceDigiField || {};
  const BEATS = {Vaccine: 'Virus', Virus: 'Data', Data: 'Vaccine'};
  const BA = require('./sim/battle-actions').BattleActions;
  if (!BA.prototype.modifyDamage.__ceDigi) {
    const modifyDamage = BA.prototype.modifyDamage;
    const wrapped = function (baseDamage, pokemon, target, move, suppressMessages) {
      let d = modifyDamage.call(this, baseDamage, pokemon, target, move, suppressMessages);
      if (typeof d !== 'number' || d <= 1) return d;
      const field = globalThis.__ceDigiField[pokemon.uuid];
      if (field) {
        d = Math.floor(d * 1.15);
        if (!suppressMessages && !pokemon.m.ceFieldShown) {
          pokemon.m.ceFieldShown = true;
          this.battle.add('-activate', pokemon, 'fieldboost');
        }
      }
      const a = globalThis.__ceDigi[pokemon.uuid];
      const b = globalThis.__ceDigi[target.uuid];
      if (!a || !b) return d;
      let up = BEATS[a] === b, down = BEATS[b] === a;
      if (pokemon.volatiles['bugcode'] || target.volatiles['bugcode']) {
        const t = up;
        up = down;
        down = t;
      }
      let tag = null;
      if (up) {
        d = Math.floor(d * 1.25);
        tag = 'attributeadvantage';
      } else if (down) {
        d = Math.max(1, Math.floor(d * 0.8));
        tag = 'attributedisadvantage';
      }
      if (tag && !suppressMessages && move && !move.ceDigiShown) {
        move.ceDigiShown = true;
        this.battle.add('-activate', pokemon, tag);
      }
      return d;
    };
    wrapped.__ceDigi = true;
    BA.prototype.modifyDamage = wrapped;
  }
  return 'attribute triangle, field buffs';
})();
