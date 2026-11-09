({
  name: "Roaring Moonite",
  spritenum: 0,
  megaStone: { "Roaring Moon": "Roaring Moon-Mega" },
  itemUser: ["Roaring Moon"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9106,
  gen: 9,
  isNonstandard: "Past",
})
