{
onModifySpe(spe, pokemon) {
  if (this.field.isWeather(['hail', 'snow'])) return this.chainModify(2);
},
onImmunity(type, pokemon) {
  if (type === 'hail' || type === 'sandstorm' || type === 'frz') return false;
},
flags: {},
name: "Alpine Spirit",
rating: 3,
num: -3054
}
