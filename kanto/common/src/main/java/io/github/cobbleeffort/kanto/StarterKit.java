package io.github.cobbleeffort.kanto;

import dev.architectury.event.events.common.CommandRegistrationEvent;
import dev.architectury.event.events.common.PlayerEvent;
import dev.architectury.registry.registries.RegistrySupplier;
import net.minecraft.ChatFormatting;
import net.minecraft.commands.Commands;
import net.minecraft.commands.arguments.EntityArgument;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.stats.Stats;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.BonemealableBlock;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.level.block.state.properties.Property;
import net.minecraft.world.level.levelgen.feature.ConfiguredFeature;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;

import java.util.List;

/**
 * The starter kit (the user's request). The Starter Bundle is given once to each player the first time they join a
 * world they haven't played in yet (a new world; config/cobbleeffort_kanto.json "give_starter_kit" turns it off;
 * {@code /kanto starterkit [players]} gives one by hand). Opened, it gives 64 oak logs, 32 cobblestone, 32 Poké Balls,
 * 16 Exp. Candy S, 64 cooked porkchops and the Starter Base Token. Used on the ground, the token builds the starter base
 * (data/cobbleeffort_kanto/structure/starter_base.nbt, from tools/make_starter.py) right in front of the player, its
 * door facing them: the space is cleared, a dirt foundation fills any gaps under it, the template is placed, then
 * Cobblemon's own apricorn trees grow on the farm's tree spots (ripe), and the berry bushes are grown until they fruit.
 */
public final class StarterKit {
    static final String TAG = "cobbleeffort_kanto_starter_kit";
    /** Ten minutes: someone who has played longer than this in the world already had their start. */
    static final int NEW_PLAYER_TICKS = 20 * 60 * 10;
    static final ResourceLocation TEMPLATE = Kanto.id("starter_base");
    /** The template-space point that lands on the block the token is used on: just in front of the porch. */
    static final BlockPos ANCHOR = new BlockPos(8, 10, -1);
    static final int GROUND = 10;
    static final int[][] TREES = {{20, 17}, {24, 17}, {28, 17}, {32, 17}, {22, 22}, {26, 22}, {30, 22}};
    static final String[] TREE_COLOURS = {"red", "yellow", "green", "blue", "pink", "black", "white"};

    public static final RegistrySupplier<Item> BUNDLE = Kanto.ITEMS.register("starter_bundle", () ->
            new BundleItem(new Item.Properties().stacksTo(1).rarity(Rarity.UNCOMMON).arch$tab(Kanto.TAB)));
    public static final RegistrySupplier<Item> TOKEN = Kanto.ITEMS.register("starter_base_token", () ->
            new TokenItem(new Item.Properties().stacksTo(1).rarity(Rarity.RARE).arch$tab(Kanto.TAB)));

    private StarterKit() {
    }

    /** Loads the class, so the items are queued before Kanto.ITEMS registers. */
    static void register() {
    }

    static void init() {
        PlayerEvent.PLAYER_JOIN.register(StarterKit::onJoin);
        CommandRegistrationEvent.EVENT.register((dispatcher, registry, selection) -> dispatcher.register(
                Commands.literal("kanto").then(Commands.literal("starterbase").requires(src -> src.hasPermission(2))
                        .then(Commands.argument("pos", net.minecraft.commands.arguments.coordinates.BlockPosArgument.blockPos())
                                .executes(ctx -> buildCommand(ctx.getSource(),
                                        net.minecraft.commands.arguments.coordinates.BlockPosArgument.getLoadedBlockPos(ctx, "pos"), "south"))
                                .then(Commands.argument("facing", com.mojang.brigadier.arguments.StringArgumentType.word())
                                        .suggests((c, b) -> b.suggest("north").suggest("south").suggest("east").suggest("west").buildFuture())
                                        .executes(ctx -> buildCommand(ctx.getSource(),
                                                net.minecraft.commands.arguments.coordinates.BlockPosArgument.getLoadedBlockPos(ctx, "pos"),
                                                com.mojang.brigadier.arguments.StringArgumentType.getString(ctx, "facing"))))))));
        CommandRegistrationEvent.EVENT.register((dispatcher, registry, selection) -> dispatcher.register(
                Commands.literal("kanto").then(Commands.literal("starterkit").requires(src -> src.hasPermission(2))
                        .executes(ctx -> {
                            ServerPlayer p = ctx.getSource().getPlayerOrException();
                            give(p, new ItemStack(BUNDLE.get()));
                            ctx.getSource().sendSuccess(() -> Component.translatable(Kanto.MOD_ID + ".starter.given", p.getDisplayName()), true);
                            return 1;
                        })
                        .then(Commands.argument("players", EntityArgument.players()).executes(ctx -> {
                            int n = 0;
                            for (ServerPlayer p : EntityArgument.getPlayers(ctx, "players")) {
                                give(p, new ItemStack(BUNDLE.get()));
                                ctx.getSource().sendSuccess(() -> Component.translatable(Kanto.MOD_ID + ".starter.given", p.getDisplayName()), true);
                                n++;
                            }
                            return n;
                        })))));
    }

    /** /kanto starterbase <pos> [facing]: builds the base with `pos` as its ground, extending toward `facing`. */
    private static int buildCommand(net.minecraft.commands.CommandSourceStack src, BlockPos pos, String facing) {
        Direction d = Direction.byName(facing.toLowerCase());
        if (d == null || d.getAxis().isVertical()) d = Direction.SOUTH;
        boolean ok = build(src.getLevel(), pos, d);
        src.sendSuccess(() -> Component.translatable(Kanto.MOD_ID + (ok ? ".starter.built" : ".starter.failed")), true);
        return ok ? 1 : 0;
    }

    private static void onJoin(ServerPlayer player) {
        try {
            if (!KantoConfig.giveStarterKit || player.getTags().contains(TAG)) return;
            player.addTag(TAG);
            int played = player.getStats().getValue(Stats.CUSTOM.get(Stats.PLAY_TIME));
            if (played > NEW_PLAYER_TICKS) return;                       // an old world: they've already started
            give(player, new ItemStack(BUNDLE.get()));
            player.sendSystemMessage(Component.translatable(Kanto.MOD_ID + ".starter.welcome").withStyle(ChatFormatting.GOLD));
        } catch (Throwable t) {
            Kanto.LOG.error("Couldn't give the starter kit", t);
        }
    }

    static void give(Player player, ItemStack stack) {
        if (!player.getInventory().add(stack)) player.drop(stack, false);
    }

    private static Item item(String id) {
        return BuiltInRegistries.ITEM.get(ResourceLocation.parse(id));
    }

    // --- the Starter Bundle -----------------------------------------------------------------------------------------
    static final class BundleItem extends Item {
        BundleItem(Properties p) {
            super(p);
        }

        @Override
        public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
            ItemStack held = player.getItemInHand(hand);
            if (level.isClientSide) return InteractionResultHolder.success(held);
            List<ItemStack> contents = List.of(new ItemStack(Blocks.OAK_LOG, 64), new ItemStack(Blocks.COBBLESTONE, 32),
                    new ItemStack(item("cobblemon:poke_ball"), 32), new ItemStack(item("cobblemon:exp_candy_s"), 16),
                    new ItemStack(item("minecraft:cooked_porkchop"), 64), new ItemStack(TOKEN.get()));
            if (!player.getAbilities().instabuild) held.shrink(1);
            for (ItemStack s : contents) give(player, s.copy());
            level.playSound(null, player.blockPosition(), SoundEvents.BUNDLE_DROP_CONTENTS, SoundSource.PLAYERS, 1F, 1F);
            player.displayClientMessage(Component.translatable(Kanto.MOD_ID + ".starter.opened").withStyle(ChatFormatting.GOLD), false);
            return InteractionResultHolder.consume(held);
        }

        @Override
        public void appendHoverText(ItemStack stack, TooltipContext ctx, List<Component> tooltip, TooltipFlag flag) {
            tooltip.add(Component.translatable(getDescriptionId() + ".tooltip").withStyle(ChatFormatting.GRAY));
        }
    }

    // --- the Starter Base Token -------------------------------------------------------------------------------------
    static final class TokenItem extends Item {
        TokenItem(Properties p) {
            super(p);
        }

        @Override
        public InteractionResult useOn(UseOnContext ctx) {
            if (!(ctx.getLevel() instanceof ServerLevel level)) return InteractionResult.SUCCESS;
            Player player = ctx.getPlayer();
            boolean ok;
            try {
                ok = build(level, ctx.getClickedPos(), ctx.getHorizontalDirection());
            } catch (Throwable t) {
                Kanto.LOG.error("Building the starter base failed", t);
                ok = false;
            }
            if (!ok) {
                if (player != null) player.displayClientMessage(Component.translatable(Kanto.MOD_ID + ".starter.failed"), true);
                return InteractionResult.FAIL;
            }
            if (player != null) {
                if (!player.getAbilities().instabuild) ctx.getItemInHand().shrink(1);
                player.displayClientMessage(Component.translatable(Kanto.MOD_ID + ".starter.built").withStyle(ChatFormatting.GOLD), false);
            }
            return InteractionResult.CONSUME;
        }

        @Override
        public void appendHoverText(ItemStack stack, TooltipContext ctx, List<Component> tooltip, TooltipFlag flag) {
            tooltip.add(Component.translatable(getDescriptionId() + ".tooltip").withStyle(ChatFormatting.GRAY));
        }
    }

    /** The rotation that turns the template's depth (+z, away from the door) into the direction the player faces. */
    static Rotation rotationFor(Direction facing) {
        return switch (facing) {
            case NORTH -> Rotation.CLOCKWISE_180;
            case EAST -> Rotation.COUNTERCLOCKWISE_90;
            case WEST -> Rotation.CLOCKWISE_90;
            default -> Rotation.NONE;
        };
    }

    private static boolean soft(BlockState s) {
        return s.isAir() || s.canBeReplaced() || !s.getFluidState().isEmpty()
                || s.is(net.minecraft.tags.BlockTags.LEAVES) || s.is(net.minecraft.tags.BlockTags.LOGS);
    }

    /** Builds the base with the block `at` (the surface) as its ground level, extending away in `facing`. */
    public static boolean build(ServerLevel level, BlockPos at, Direction facing) {
        StructureTemplate template = level.getStructureManager().get(TEMPLATE).orElse(null);
        if (template == null) {
            Kanto.LOG.error("Missing template {}", TEMPLATE);
            return false;
        }
        StructurePlaceSettings settings = new StructurePlaceSettings().setRotation(rotationFor(facing)).setIgnoreEntities(true);
        BlockPos origin = at.subtract(StructureTemplate.calculateRelativePosition(settings, ANCHOR));
        BoundingBox box = template.getBoundingBox(settings, origin);
        if (box.minY() < level.getMinBuildHeight() + 1 || box.maxY() + 10 > level.getMaxBuildHeight()) return false;
        int ground = at.getY();
        // clear the space above the ground (trees, hills) and lay a dirt foundation under the ground layer
        for (int x = box.minX(); x <= box.maxX(); x++) {
            for (int z = box.minZ(); z <= box.maxZ(); z++) {
                for (int y = ground + 1; y <= box.maxY() + 8; y++) {
                    BlockPos p = new BlockPos(x, y, z);
                    if (!level.getBlockState(p).isAir()) level.setBlock(p, Blocks.AIR.defaultBlockState(), Block.UPDATE_CLIENTS);
                }
                for (int y = ground - 4; y > Math.max(level.getMinBuildHeight(), ground - 40); y--) {
                    BlockPos p = new BlockPos(x, y, z);
                    if (!soft(level.getBlockState(p))) break;
                    level.setBlock(p, Blocks.DIRT.defaultBlockState(), Block.UPDATE_CLIENTS);
                }
            }
        }
        RandomSource random = level.getRandom();
        template.placeInWorld(level, origin, origin, settings, random, Block.UPDATE_CLIENTS);
        growFarm(level, settings, origin, box, random);
        level.playSound(null, at, SoundEvents.PLAYER_LEVELUP, SoundSource.BLOCKS, 1F, 1.2F);
        level.sendParticles(ParticleTypes.HAPPY_VILLAGER, at.getX() + 0.5, at.getY() + 2, at.getZ() + 0.5, 40, 3, 2, 3, 0.1);
        return true;
    }

    /** Grows Cobblemon's own apricorn trees on the farm (their apricorns ripe) and the berry bushes until they fruit. */
    private static void growFarm(ServerLevel level, StructurePlaceSettings settings, BlockPos origin, BoundingBox box, RandomSource random) {
        var features = level.registryAccess().registryOrThrow(Registries.CONFIGURED_FEATURE);
        for (int i = 0; i < TREES.length; i++) {
            BlockPos p = origin.offset(StructureTemplate.calculateRelativePosition(settings, new BlockPos(TREES[i][0], GROUND + 1, TREES[i][1])));
            ConfiguredFeature<?, ?> tree = features.get(ResourceLocation.parse("cobblemon:" + TREE_COLOURS[i] + "_apricorn_tree"));
            try {
                if (tree != null) tree.place(level, level.getChunkSource().getGenerator(), random, p);
            } catch (Throwable t) {
                Kanto.LOG.warn("Couldn't grow the {} apricorn tree", TREE_COLOURS[i], t);
            }
        }
        for (int x = box.minX() - 3; x <= box.maxX() + 3; x++) {
            for (int z = box.minZ() - 3; z <= box.maxZ() + 3; z++) {
                for (int y = box.minY() + GROUND; y <= box.minY() + GROUND + 10; y++) {
                    BlockPos p = new BlockPos(x, y, z);
                    BlockState s = level.getBlockState(p);
                    ResourceLocation id = BuiltInRegistries.BLOCK.getKey(s.getBlock());
                    if (!"cobblemon".equals(id.getNamespace())) continue;
                    String path = id.getPath();
                    if (path.endsWith("_apricorn")) {
                        Property<?> age = s.getBlock().getStateDefinition().getProperty("age");
                        if (age instanceof IntegerProperty ip) {
                            int max = ip.getPossibleValues().stream().max(Integer::compare).orElse(0);
                            level.setBlock(p, s.setValue(ip, max), Block.UPDATE_CLIENTS);
                        }
                    } else if (path.endsWith("_berry") && s.getBlock() instanceof BonemealableBlock grow) {
                        for (int k = 0; k < 12 && grow.isValidBonemealTarget(level, p, s); k++) {
                            grow.performBonemeal(level, random, p, s);
                            s = level.getBlockState(p);
                            if (!(s.getBlock() instanceof BonemealableBlock)) break;
                        }
                    }
                }
            }
        }
    }
}
