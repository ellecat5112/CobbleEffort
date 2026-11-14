package io.github.cobbleeffort.kanto;

import dev.architectury.registry.registries.RegistrySupplier;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.QuartPos;
import net.minecraft.core.SectionPos;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.chunk.ChunkAccess;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.feature.ConfiguredFeature;
import net.minecraft.world.level.levelgen.structure.BoundingBox;

import java.util.ArrayList;
import java.util.List;

/**
 * Creative testing tools (operators in creative mode only): the Biome Wand and the Structure Wand. Sneak + use cycles
 * the target; use in the air locates the nearest one (vanilla's /locate, with its click-to-teleport coordinates); use
 * on a block forces it right there: the biome is painted over a 65-block square round the block and decorated with
 * its features (giant cigarettes, bottles, ponds), or the structure is placed at the block (vanilla's /place).
 */
public final class TestTools {
    /** The biomes the Biome Wand knows: the overworld biomes this add-on adds. */
    static final List<ResourceLocation> BIOMES = List.of(Kanto.id("ashtray"), Kanto.id("liquor_meadows"));
    /** The structures the Structure Wand knows: every structure of these namespaces (CobbleEffort's and Kanto's). */
    static final List<String> STRUCTURE_NAMESPACES = List.of("cobbleeffort", Kanto.MOD_ID);
    static final int BIOME_RADIUS = 32;

    public static final RegistrySupplier<Item> BIOME_WAND = Kanto.ITEMS.register("biome_wand", () -> new Wand(false));
    public static final RegistrySupplier<Item> STRUCTURE_WAND = Kanto.ITEMS.register("structure_wand", () -> new Wand(true));

    private TestTools() {}

    /** Loads the class, so the items are queued before Kanto.ITEMS registers. */
    static void register() {}

    static List<ResourceLocation> structures(ServerLevel level) {
        List<ResourceLocation> out = new ArrayList<>();
        for (ResourceLocation id : level.registryAccess().registryOrThrow(Registries.STRUCTURE).keySet()) {
            if (STRUCTURE_NAMESPACES.contains(id.getNamespace())) out.add(id);
        }
        out.sort(ResourceLocation::compareTo);
        return out;
    }

    public static final class Wand extends Item {
        private final boolean structures;

        Wand(boolean structures) {
            super(new Item.Properties().stacksTo(1).rarity(Rarity.EPIC).arch$tab(Kanto.TAB));
            this.structures = structures;
        }

        private List<ResourceLocation> targets(ServerLevel level) {
            return structures ? structures(level) : BIOMES;
        }

        private static int index(ItemStack stack) {
            CustomData data = stack.get(DataComponents.CUSTOM_DATA);
            return data == null ? 0 : data.copyTag().getInt("target");
        }

        private ResourceLocation current(ItemStack stack, List<ResourceLocation> targets) {
            return targets.get(Math.floorMod(index(stack), targets.size()));
        }

        private static boolean allowed(ServerPlayer player) {
            if (player.canUseGameMasterBlocks()) return true;
            player.displayClientMessage(Component.translatable(Kanto.MOD_ID + ".wand.not_allowed").withStyle(ChatFormatting.RED), true);
            return false;
        }

        private void cycle(ServerPlayer player, ItemStack stack, List<ResourceLocation> targets) {
            int next = Math.floorMod(index(stack) + 1, targets.size());
            CustomData.update(DataComponents.CUSTOM_DATA, stack, tag -> tag.putInt("target", next));
            player.displayClientMessage(Component.translatable(Kanto.MOD_ID + ".wand.target",
                    Component.literal(targets.get(next).toString()).withStyle(ChatFormatting.GOLD)), true);
        }

        private static void run(ServerPlayer player, String command) {
            player.server.getCommands().performPrefixedCommand(player.createCommandSourceStack().withPermission(2), command);
        }

        @Override
        public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
            ItemStack stack = player.getItemInHand(hand);
            if (!(player instanceof ServerPlayer sp) || !(level instanceof ServerLevel server)) return InteractionResultHolder.success(stack);
            if (!allowed(sp)) return InteractionResultHolder.fail(stack);
            List<ResourceLocation> targets = targets(server);
            if (targets.isEmpty()) {
                sp.displayClientMessage(Component.translatable(Kanto.MOD_ID + ".wand.none"), true);
                return InteractionResultHolder.fail(stack);
            }
            if (player.isShiftKeyDown()) cycle(sp, stack, targets);
            else run(sp, "locate " + (structures ? "structure " : "biome ") + current(stack, targets));
            return InteractionResultHolder.success(stack);
        }

        @Override
        public InteractionResult useOn(UseOnContext context) {
            if (!(context.getPlayer() instanceof ServerPlayer sp) || !(context.getLevel() instanceof ServerLevel level)) {
                return InteractionResult.SUCCESS;
            }
            if (!allowed(sp)) return InteractionResult.FAIL;
            ItemStack stack = context.getItemInHand();
            List<ResourceLocation> targets = targets(level);
            if (targets.isEmpty()) return InteractionResult.FAIL;
            if (sp.isShiftKeyDown()) {
                cycle(sp, stack, targets);
                return InteractionResult.SUCCESS;
            }
            ResourceLocation id = current(stack, targets);
            BlockPos at = context.getClickedPos().above();
            if (structures) {
                run(sp, "place structure " + id + " " + at.getX() + " " + at.getY() + " " + at.getZ());
            } else {
                forceBiome(level, context.getClickedPos(), id, sp::sendSystemMessage);
            }
            return InteractionResult.SUCCESS;
        }

        @Override
        public void appendHoverText(ItemStack stack, Item.TooltipContext context, List<Component> lines, TooltipFlag flag) {
            String kind = structures ? "structure" : "biome";
            lines.add(Component.translatable(Kanto.MOD_ID + ".wand." + kind + ".tip1").withStyle(ChatFormatting.GRAY));
            lines.add(Component.translatable(Kanto.MOD_ID + ".wand." + kind + ".tip2").withStyle(ChatFormatting.GRAY));
            lines.add(Component.translatable(Kanto.MOD_ID + ".wand.tip3").withStyle(ChatFormatting.GRAY));
            if (!structures) {
                lines.add(Component.translatable(Kanto.MOD_ID + ".wand.target",
                        Component.literal(BIOMES.get(Math.floorMod(index(stack), BIOMES.size())).toString())
                                .withStyle(ChatFormatting.GOLD)));
            }
        }
    }

    // --- forcing a biome here --------------------------------------------------------------------------------------

    /** Paints the biome over a square round `centre` (every height), resends those chunks' biomes, then decorates it
     * with the biome's own features. */
    static void forceBiome(ServerLevel level, BlockPos centre, ResourceLocation id, java.util.function.Consumer<Component> say) {
        Holder<Biome> biome = level.registryAccess().registryOrThrow(Registries.BIOME)
                .getHolder(ResourceKey.create(Registries.BIOME, id)).orElse(null);
        if (biome == null) {
            say.accept(Component.translatable(Kanto.MOD_ID + ".wand.none"));
            return;
        }
        int r = BIOME_RADIUS;
        BoundingBox box = new BoundingBox(centre.getX() - r, level.getMinBuildHeight(), centre.getZ() - r,
                centre.getX() + r, level.getMaxBuildHeight() - 1, centre.getZ() + r);
        List<ChunkAccess> chunks = new ArrayList<>();
        for (int cz = SectionPos.blockToSectionCoord(box.minZ()); cz <= SectionPos.blockToSectionCoord(box.maxZ()); cz++) {
            for (int cx = SectionPos.blockToSectionCoord(box.minX()); cx <= SectionPos.blockToSectionCoord(box.maxX()); cx++) {
                ChunkAccess chunk = level.getChunk(cx, cz);
                chunk.fillBiomesFromNoise((x, y, z, sampler) -> box.isInside(QuartPos.toBlock(x), QuartPos.toBlock(y), QuartPos.toBlock(z))
                        ? biome : chunk.getNoiseBiome(x, y, z), level.getChunkSource().randomState().sampler());
                chunk.setUnsaved(true);
                chunks.add(chunk);
            }
        }
        level.getChunkSource().chunkMap.resendBiomesForChunks(chunks);
        int placed = 0;
        if (id.equals(Kanto.id("ashtray"))) {
            for (ChunkAccess chunk : chunks) {
                placed += feature(level, "ashtray_surface", chunk.getPos().getWorldPosition(), 1);
            }
            placed += scatter(level, centre, "giant_cigarette", 5) + scatter(level, centre, "cigarette_butt", 12)
                    + scatter(level, centre, "tar_lake", 1);
        } else if (id.equals(Kanto.id("liquor_meadows"))) {
            placed += scatter(level, centre, "liquor_pond", 1) + scatter(level, centre, "giant_bottle", 5)
                    + scatter(level, centre, "fallen_bottle", 10);
        }
        say.accept(Component.translatable(Kanto.MOD_ID + ".wand.forced",
                Component.literal(id.toString()).withStyle(ChatFormatting.GOLD), 2 * r + 1, placed));
    }

    /** Places a configured feature at random surface spots within the painted square (kept inside its edge). */
    private static int scatter(ServerLevel level, BlockPos centre, String name, int count) {
        int placed = 0;
        int inner = BIOME_RADIUS - 12;
        for (int i = 0; i < count; i++) {
            int x = centre.getX() + level.getRandom().nextInt(2 * inner + 1) - inner;
            int z = centre.getZ() + level.getRandom().nextInt(2 * inner + 1) - inner;
            int y = level.getHeight(Heightmap.Types.WORLD_SURFACE, x, z);
            placed += feature(level, name, new BlockPos(x, y, z), 1);
        }
        return placed;
    }

    private static int feature(ServerLevel level, String name, BlockPos pos, int times) {
        var holder = level.registryAccess().registryOrThrow(Registries.CONFIGURED_FEATURE)
                .getHolder(ResourceKey.create(Registries.CONFIGURED_FEATURE, Kanto.id(name)));
        if (holder.isEmpty()) return 0;
        ConfiguredFeature<?, ?> feature = holder.get().value();
        int placed = 0;
        for (int i = 0; i < times; i++) {
            try {
                if (feature.place(level, level.getChunkSource().getGenerator(), level.getRandom(), pos)) placed++;
            } catch (Throwable t) {
                Kanto.LOG.error("Biome Wand: placing {} failed", name, t);
            }
        }
        return placed;
    }
}
