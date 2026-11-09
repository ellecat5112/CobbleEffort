package io.github.cobbleeffort;

import java.io.InputStream;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.function.Consumer;
import java.util.function.Supplier;

/**
 * The "CobbleEffort" creative inventory tab: every item the mod uses (the cosmetic items of each collection), read from {@code cobbleeffort_creative_tab.json} (written by tools/make_creative_tab.py).
 *
 * <p>CobbleEffort is one jar for Fabric and NeoForge, so this class is compiled against nothing but the JDK and
 * reaches Minecraft by reflection: Fabric runs on intermediary names, NeoForge on Mojang's, and every name below is
 * given in both (checked against the 1.21.1 mappings). Everything is wrapped so that a failure only logs a line and
 * leaves the tab out: it can never stop the game from loading.
 */
public final class CreativeTab {
    public static final String MOD_ID = "cobbleeffort";
    private static final String LIST = "/cobbleeffort_creative_tab.json";
    private static boolean warned;

    private final boolean fabric;
    private final ClassLoader loader = CreativeTab.class.getClassLoader();

    public CreativeTab(boolean fabric) {
        this.fabric = fabric;
    }

    public static void log(String message, Throwable error) {
        System.out.println("[CobbleEffort] " + message + (error == null ? "" : ": " + error));
    }

    // --- names ---------------------------------------------------------------------------------------------------

    private String n(String mojang, String intermediary) {
        return fabric ? intermediary : mojang;
    }

    private Class<?> mc(String mojang, String intermediary) throws ClassNotFoundException {
        return Class.forName(n("net.minecraft." + mojang, "net.minecraft." + intermediary), false, loader);
    }

    private Class<?> creativeModeTab() throws ClassNotFoundException { return mc("world.item.CreativeModeTab", "class_1761"); }
    private Class<?> builderClass() throws ClassNotFoundException { return mc("world.item.CreativeModeTab$Builder", "class_1761$class_7913"); }
    private Class<?> generatorClass() throws ClassNotFoundException { return mc("world.item.CreativeModeTab$DisplayItemsGenerator", "class_1761$class_7914"); }
    private Class<?> outputClass() throws ClassNotFoundException { return mc("world.item.CreativeModeTab$Output", "class_1761$class_7704"); }
    private Class<?> parametersClass() throws ClassNotFoundException { return mc("world.item.CreativeModeTab$ItemDisplayParameters", "class_1761$class_8128"); }
    private Class<?> providerClass() throws ClassNotFoundException { return mc("core.HolderLookup$Provider", "class_7225$class_7874"); }
    private Class<?> itemStack() throws ClassNotFoundException { return mc("world.item.ItemStack", "class_1799"); }
    private Class<?> component() throws ClassNotFoundException { return mc("network.chat.Component", "class_2561"); }
    private Class<?> resourceLocation() throws ClassNotFoundException { return mc("resources.ResourceLocation", "class_2960"); }
    private Class<?> registry() throws ClassNotFoundException { return mc("core.Registry", "class_2378"); }
    private Class<?> dynamicOps() throws ClassNotFoundException { return Class.forName("com.mojang.serialization.DynamicOps", false, loader); }

    /** The one public method of {@code owner} with these parameter types and a return type assignable to {@code returns}. */
    private static Method byType(Class<?> owner, Class<?> returns, Class<?>... params) throws NoSuchMethodException {
        for (Method m : owner.getMethods()) {
            if (java.util.Arrays.equals(m.getParameterTypes(), params) && returns.isAssignableFrom(m.getReturnType())) {
                return m;
            }
        }
        throw new NoSuchMethodException(owner.getName() + " method " + java.util.Arrays.toString(params) + " -> " + returns.getName());
    }

    // --- the tab -------------------------------------------------------------------------------------------------

    public Object id() throws ReflectiveOperationException {
        Class<?> rl = resourceLocation();
        return rl.getMethod(n("fromNamespaceAndPath", "method_60655"), String.class, String.class).invoke(null, MOD_ID, MOD_ID);
    }

    /** Builds the tab from a fresh CreativeModeTab.Builder. */
    public Object build(Object builder) throws ReflectiveOperationException {
        Class<?> b = builderClass();
        Object title = component().getMethod(n("translatable", "method_43471"), String.class).invoke(null, "itemGroup." + MOD_ID);
        byType(b, b, component()).invoke(builder, title);
        Supplier<Object> icon = this::icon;
        byType(b, b, Supplier.class).invoke(builder, icon);
        Class<?> gen = generatorClass();
        Object generator = Proxy.newProxyInstance(loader, new Class<?>[] {gen}, (proxy, method, args) -> {
            if (method.getDeclaringClass() == Object.class) {
                switch (method.getName()) {
                    case "equals": return proxy == args[0];
                    case "hashCode": return System.identityHashCode(proxy);
                    default: return "CobbleEffort creative tab";
                }
            }
            if (args != null && args.length == 2) {
                fill(args[0], args[1]);
            }
            return null;
        });
        byType(b, b, gen).invoke(builder, generator);
        return byType(b, creativeModeTab()).invoke(builder);
    }

    /** Fabric: FabricItemGroup.builder(), registered straight into the creative tab registry during mod init. */
    public void registerFabric() throws ReflectiveOperationException {
        Object resolver = Class.forName("net.fabricmc.loader.api.FabricLoader", false, loader).getMethod("getInstance").invoke(null);
        resolver = resolver.getClass().getMethod("getMappingResolver").invoke(resolver);
        Object namespace = Class.forName("net.fabricmc.loader.api.MappingResolver", false, loader)
                .getMethod("getCurrentRuntimeNamespace").invoke(resolver);
        if (!"intermediary".equals(namespace)) {
            log("creative tab skipped: runs on intermediary names, not " + namespace, null);
            return;
        }
        Object builder = Class.forName("net.fabricmc.fabric.api.itemgroup.v1.FabricItemGroup", true, loader).getMethod("builder").invoke(null);
        Object tab = build(builder);
        Object tabs = mc("core.registries.BuiltInRegistries", "class_7923").getField("field_44687").get(null);
        Class<?> reg = registry();
        reg.getMethod("method_10230", reg, resourceLocation(), Object.class).invoke(null, tabs, id(), tab);
    }

    /** NeoForge: called for every RegisterEvent; adds the tab when the creative tab registry is filled. */
    public void onRegisterEvent(Object event) throws ReflectiveOperationException {
        Class<?> keyClass = mc("resources.ResourceKey", "class_5321");
        Object key = mc("core.registries.Registries", "class_7924").getField("CREATIVE_MODE_TAB").get(null);
        Method register = event.getClass().getMethod("register", keyClass, Consumer.class);
        Class<?> helperClass = Class.forName("net.neoforged.neoforge.registries.RegisterEvent$RegisterHelper", false, loader);
        Method helperRegister = helperClass.getMethod("register", resourceLocation(), Object.class);
        Consumer<Object> consumer = helper -> {
            try {
                helperRegister.invoke(helper, id(), build(newNeoForgeBuilder()));
            } catch (Throwable t) {
                log("creative tab not registered", t);
            }
        };
        register.invoke(event, key, consumer);
    }

    private Object newNeoForgeBuilder() throws ReflectiveOperationException {
        Class<?> tab = creativeModeTab();
        try {
            return tab.getMethod("builder").invoke(null);                  // NeoForge's own (it places modded tabs)
        } catch (NoSuchMethodException e) {
            Class<?> row = mc("world.item.CreativeModeTab$Row", "class_1761$class_7915");
            return tab.getMethod("builder", row, int.class).invoke(null, row.getField("TOP").get(null), 0);
        }
    }

    // --- contents ------------------------------------------------------------------------------------------------

    private Object jsonOps() throws ReflectiveOperationException {
        return Class.forName("com.mojang.serialization.JsonOps", false, loader).getField("INSTANCE").get(null);
    }

    private Object readList() throws Exception {
        try (InputStream in = CreativeTab.class.getResourceAsStream(LIST)) {
            if (in == null) throw new IllegalStateException(LIST + " is missing from the jar");
            String text = new String(in.readAllBytes(), StandardCharsets.UTF_8);
            return Class.forName("com.google.gson.JsonParser", false, loader).getMethod("parseString", String.class).invoke(null, text);
        }
    }

    /** ItemStack.CODEC.parse(ops, json).result() */
    private Optional<?> decode(Object ops, Object json) throws ReflectiveOperationException {
        Object codec = itemStack().getField(n("CODEC", "field_24671")).get(null);
        Method parse = Class.forName("com.mojang.serialization.Decoder", false, loader).getMethod("parse", dynamicOps(), Object.class);
        Object result = parse.invoke(codec, ops, json);
        return (Optional<?>) Class.forName("com.mojang.serialization.DataResult", false, loader).getMethod("result").invoke(result);
    }

    private static List<Object> elements(Object array) {
        List<Object> out = new ArrayList<>();
        for (Object element : (Iterable<?>) array) out.add(element);      // a Gson JsonArray
        return out;
    }

    /** A short name for the log: the item id. */
    private static String label(Object json) {
        String text = String.valueOf(json);
        int id = text.indexOf("\"id\":\"");
        return id >= 0 ? text.substring(id + 6, text.indexOf('"', id + 6)) : text;
    }

    private Object icon() {
        try {
            Object root = readList();
            Object iconJson = root.getClass().getMethod("get", String.class).invoke(root, "icon");
            Optional<?> stack = decode(jsonOps(), iconJson);
            if (stack.isPresent()) return stack.get();
        } catch (Throwable t) {
            log("creative tab icon", t);
        }
        try {
            return itemStack().getField(n("EMPTY", "field_8037")).get(null);
        } catch (ReflectiveOperationException e) {
            throw new IllegalStateException(e);
        }
    }

    /** DisplayItemsGenerator.accept(parameters, output): every listed stack this game can make. */
    private void fill(Object parameters, Object output) {
        try {
            Object ops = jsonOps();
            try {   // registry-aware ops, as recipes use; plain JSON ops otherwise
                Object holders = byType(parametersClass(), providerClass()).invoke(parameters);
                ops = providerClass().getMethod(n("createSerializationContext", "method_57093"), dynamicOps()).invoke(holders, ops);
            } catch (Throwable t) {
                if (!warned) log("creative tab: plain JSON for its items", t);
            }
            Method accept = byType(outputClass(), void.class, itemStack());
            Object root = readList();
            Object items = root.getClass().getMethod("get", String.class).invoke(root, "items");
            List<String> skipped = new ArrayList<>();
            for (Object json : elements(items)) {
                try {
                    Optional<?> stack = decode(ops, json);
                    if (stack.isPresent()) {
                        accept.invoke(output, stack.get());
                    } else {
                        skipped.add(label(json));               // e.g. an item from a mod that isn't installed
                    }
                } catch (Throwable t) {
                    skipped.add(label(json) + " (" + t + ")");
                }
            }
            if (!skipped.isEmpty() && !warned) {
                log("creative tab left out " + skipped.size() + " item(s) this game can't make: " + skipped, null);
            }
        } catch (Throwable t) {
            if (!warned) log("creative tab contents", t);
        }
        warned = true;
    }
}
