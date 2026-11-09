({
  name: "Great Tuskite",
  spritenum: 0,
  megaStone: { "Great Tusk": "Great Tusk-Mega" },
  itemUser: ["Great Tusk"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9100,
  gen: 9,
  isNonstandard: "Past",
})
