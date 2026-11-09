// dump_showdown.js <showdown dir> <out.json>: the Showdown data make_battle.py needs, from Cobblemon's Showdown
// (with Mega Showdown's patches): its moves (no functions, for matching twins) and its abilities (with their code as
// source text, for matching and generating ability twins). The showdown dir is Cobblemon's showdown.zip extracted,
// with Mega Showdown's replacements copied over it.
const path = require('path'), fs = require('fs');
const SD = path.resolve(process.argv[2]);
const M = require(path.join(SD, 'data/moves.js')).Moves;
const A = require(path.join(SD, 'data/mods/cobblemon/abilities.js')).Abilities;
const moves = {};
for (const [id, m] of Object.entries(M)) {
  const fns = Object.keys(m).filter(k => typeof m[k] === 'function');
  moves[id] = {name: m.name, num: m.num, type: m.type, category: m.category, basePower: m.basePower,
               accuracy: m.accuracy, pp: m.pp, priority: m.priority, target: m.target, flags: m.flags || {},
               secondary: m.secondary ? {chance: m.secondary.chance || null, status: m.secondary.status || null,
                                         volatileStatus: m.secondary.volatileStatus || null, boosts: m.secondary.boosts || null,
                                         hasSelf: !!m.secondary.self} : null,
               secondaries: m.secondaries ? m.secondaries.length : 0, fns, isNonstandard: m.isNonstandard || null,
               isZ: !!m.isZ, isMax: !!m.isMax, self: !!m.self, drain: m.drain || null, recoil: m.recoil || null,
               multihit: m.multihit || null, critRatio: m.critRatio || null, boosts: m.boosts || null, status: m.status || null,
               volatileStatus: m.volatileStatus || null};
}
// each member as JS source for an object literal ("key: value", or a method as written), nested objects included
function member(k, v) {
  if (typeof v === 'function') {
    const src = v.toString();
    return src.startsWith(k + '(') ? src : `${JSON.stringify(k)}: ${src}`;
  }
  if (v && typeof v === 'object' && !Array.isArray(v) && Object.values(v).some(x => typeof x === 'function' || (x && typeof x === 'object'))) {
    return `${JSON.stringify(k)}: {\n${Object.entries(v).map(([k2, v2]) => member(k2, v2)).join(',\n')}\n}`;
  }
  return `${JSON.stringify(k)}: ${JSON.stringify(v)}`;
}
const abilities = {};
for (const [id, a] of Object.entries(A)) {
  const members = {};
  for (const [k, v] of Object.entries(a)) members[k] = member(k, v);
  abilities[id] = {name: a.name, num: a.num, isNonstandard: a.isNonstandard || null, members};
}
fs.writeFileSync(process.argv[3], JSON.stringify({moves, abilities}));
console.log(Object.keys(moves).length, 'moves,', Object.keys(abilities).length, 'abilities');
