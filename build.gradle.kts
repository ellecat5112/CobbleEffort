// CobbleEffort is a content-only Cobblemon addon: it contains no Java/Kotlin code,
// just data (cosmetic items, species features) and assets (resolvers, textures).
// One jar works on both Fabric and NeoForge, so we only need to package resources.
plugins {
    base
}

val modId = property("mod_id") as String
val modName = property("mod_name") as String
val modVersion = property("mod_version") as String
val minecraftVersion = property("minecraft_version") as String

version = modVersion
group = "io.github.cobbleeffort"

val expandProps = mapOf(
    "mod_id" to modId,
    "mod_name" to modName,
    "version" to modVersion,
    "minecraft_range_fabric" to property("minecraft_range_fabric"),
    "minecraft_range_neoforge" to property("minecraft_range_neoforge"),
    "cobblemon_range_fabric" to property("cobblemon_range_fabric"),
    "cobblemon_range_neoforge" to property("cobblemon_range_neoforge"),
)

val processResources by tasks.registering(Copy::class) {
    from("src/main/resources")
    into(layout.buildDirectory.dir("resources"))
    inputs.properties(expandProps)
    filesMatching(listOf("fabric.mod.json", "META-INF/neoforge.mods.toml", "pack.mcmeta")) {
        expand(expandProps)
    }
}

val jar by tasks.registering(Jar::class) {
    group = "build"
    description = "Packages the mod jar (Fabric + NeoForge)."
    archiveBaseName.set(modId)
    archiveVersion.set("$modVersion+$minecraftVersion")
    // Intermediate output: the jar is shipped inside a zip (see distZip below).
    destinationDirectory.set(layout.buildDirectory.dir("tmp/jar"))
    from(processResources)
    from("LICENSE") { rename { "LICENSE_$modId" } }
    // attribution and licences of the adapted art (Cobblemon CC BY-NC 3.0, Mega Showdown CC BY-NC-SA 4.0) travel with it
    from("CREDITS.md") { rename { "CREDITS_$modId.md" } }
    manifest {
        attributes(
            "Specification-Title" to modName,
            "Implementation-Title" to modName,
            "Implementation-Version" to modVersion,
        )
    }
}

// Every jar we produce is delivered compressed: build/libs/<name>.zip containing <name>.jar.
val distZip by tasks.registering(Zip::class) {
    group = "build"
    description = "Wraps the mod jar in a zip."
    archiveFileName.set(jar.flatMap { it.archiveFileName }.map { it.removeSuffix(".jar") + ".zip" })
    destinationDirectory.set(layout.buildDirectory.dir("libs"))
    from(jar)
}

val validateData by tasks.registering {
    group = "verification"
    description = "Checks that every JSON file parses and every texture a resolver references exists."
    val resDir = file("src/main/resources")
    inputs.dir(resDir)
    doLast {
        val slurper = groovy.json.JsonSlurper()
        var count = 0
        resDir.walkTopDown().filter { it.isFile && it.extension in setOf("json", "mcmeta") }.forEach {
            try { slurper.parse(it) } catch (e: Exception) { throw GradleException("Invalid JSON: ${it.relativeTo(resDir)}: ${e.message}") }
            count++
        }
        val resolvers = resDir.resolve("assets/$modId/bedrock/pokemon/resolvers")
        var textures = 0
        // a texture is either "ns:path" or an animation {"frames": ["ns:path", ...], ...}
        fun texturesOf(t: Any?): List<String> = when (t) {
            is String -> listOf(t)
            is Map<*, *> -> (t["frames"] as? List<*>)?.map { it.toString() } ?: emptyList()
            else -> emptyList()
        }
        // vendored models / posers / animation groups (see Vendor in tools/generate.py), found by file name
        val bedrock = resDir.resolve("assets/$modId/bedrock/pokemon")
        fun namesIn(kind: String, suffix: String) = bedrock.resolve(kind).takeIf { it.isDirectory }?.walkTopDown()
            ?.filter { it.isFile && it.name.endsWith(suffix) }?.map { it.name.removeSuffix(suffix) }?.toSet() ?: emptySet()
        val models = namesIn("models", ".json")
        val posers = namesIn("posers", ".json")
        val groups = namesIn("animations", ".animation.json")
        bedrock.resolve("posers").takeIf { it.isDirectory }?.walkTopDown()?.filter { it.isFile && it.extension == "json" }?.forEach { f ->
            Regex("""bedrock\w*\(\s*'(ce_\w+)'""").findAll(f.readText()).forEach {
                if (it.groupValues[1] !in groups) throw GradleException("${f.name} uses missing animation group ${it.groupValues[1]}")
            }
        }
        var pinned = 0
        resolvers.walkTopDown().filter { it.isFile && it.extension == "json" }.forEach { f ->
            @Suppress("UNCHECKED_CAST")
            val json = slurper.parse(f) as Map<String, Any?>
            (json["variations"] as List<Map<String, Any?>>).forEach { v ->
                (v["model"] as? String)?.split(":", limit = 2)?.let { (ns, name) ->
                    // Cobblemon loads every named model at startup and the game hangs on the loading screen if one
                    // is missing, so only Cobblemon's own models or ones shipped here may be named
                    if (ns != modId && ns != "cobblemon") throw GradleException("${f.name} names another mod's model ${v["model"]}")
                    if (ns == modId && name !in models) throw GradleException("${f.name} references missing model ${v["model"]}")
                    pinned++
                }
                (v["poser"] as? String)?.split(":", limit = 2)?.let { (ns, name) ->
                    if (ns == modId && name !in posers) throw GradleException("${f.name} references missing poser ${v["poser"]}")
                }
                val layers = (v["layers"] as? List<*>)?.mapNotNull { (it as? Map<*, *>)?.get("texture") } ?: emptyList()
                (listOf(v["texture"]) + layers).flatMap(::texturesOf).forEach { tex ->
                    val (ns, path) = tex.split(":", limit = 2)
                    if (ns == modId && !resDir.resolve("assets/$ns/$path").isFile) {
                        throw GradleException("${f.name} references missing texture $tex")
                    }
                    textures++
                }
            }
        }
        println("validateData: $count JSON files OK, all $textures resolver texture references present, $pinned model pins OK" +
                " (${models.size} vendored models, ${posers.size} posers, ${groups.size} animation groups).")
    }
}

tasks.named("check") { dependsOn(validateData) }
tasks.named("assemble") { dependsOn(distZip) }
