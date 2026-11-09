({
  name: "Gouging Firite",
  spritenum: 0,
  megaStone: { "Gouging Fire": "Gouging Fire-Mega" },
  itemUser: ["Gouging Fire"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9109,
  gen: 9,
  isNonstandard: "Past",
})
