# Spring Boot Upgrader

A Agy skill for migrating Spring Boot applications to version 4.0. Scans the project, auto-detects the migration path, and generates a phased upgrade plan — no questions asked.

## What It Does

This skill reads your Spring Boot project, identifies the current version and all affected dependencies, and produces a step-by-step upgrade plan with concrete code changes:

1. **Project scanning** — Reads pom.xml / build.gradle, application properties, source files, and test files to detect the current state.
2. **Migration path detection** — Determines the upgrade route (e.g. 3.2 → 3.5 → 4.0) and classifies scope automatically from the scan results.
3. **Phased upgrade plan** — Generates incremental phases: bridge to 3.5.x, upgrade to 4.0, migrate Jackson 3, update ecosystem dependencies. Each phase keeps the build green.
4. **Concrete code changes** — Provides exact old → new mappings for starters, imports, annotations, configuration properties, and deprecated APIs.
5. **OpenRewrite integration** — Suggests automated recipes for mechanical changes.

## When Does It Activate?

The skill activates when you ask Agy to upgrade or migrate a Spring Boot application. It scans the project and auto-detects everything — no setup questions required.

| Trigger | Example |
|---------|---------|
| Upgrade Spring Boot | "Upgrade this project to Spring Boot 4" |
| Migrate Spring version | "Migrate this app from Spring Boot 3.2 to 4.0" |
| Modernize Java project | "Modernize this Spring application to the latest version" |
| Check migration scope | "What would it take to upgrade this to Spring Boot 4?" |
| Fix deprecation warnings | "Fix all the Spring Boot deprecation warnings in this project" |

## Topics Covered

| Area | Details |
|------|---------|
| **Version Detection** | Auto-detects Spring Boot version from Maven, Gradle, or Gradle Kotlin DSL |
| **Migration Path** | Mandatory 3.5.x bridge, multi-hop planning for 1.x/2.x/3.x sources |
| **Starter Renames** | All 6 renamed starters + new required starters for Flyway, Liquibase, Batch |
| **Jackson 3** | Group ID migration, annotation renames, property changes, temporary fallback |
| **Test Framework** | `@MockBean` → `@MockitoBean`, `@SpringBootTest` changes, HtmlUnit config |
| **Configuration** | Property renames for MongoDB, Redis, Kafka, Jackson, Session |
| **Ecosystem** | Hibernate 7, Spring Security 7, Spring Batch 6, Elasticsearch 9, Kafka 4 |
| **OpenRewrite** | Maven and Gradle recipes for automated migration |

## Installation

### Option B: One-liner

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- spring-boot-upgrader
```

For user-scope installation (available across all projects):

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- spring-boot-upgrader --scope user
```

### Option C: Manual

```bash
cp -r skills/spring-boot-upgrader ~/.gemini/config/skills/spring-boot-upgrader
```

## Usage Examples

Once installed, the skill activates when you ask Agy to upgrade or migrate Spring Boot projects.

### Full migration to Spring Boot 4

```
Upgrade this Spring Boot project to version 4.0. Scan everything and
give me a phased plan.
```

### Scan and assess migration scope

```
Scan this project and tell me what it would take to migrate to
Spring Boot 4. Don't make changes yet.
```

### Fix deprecation warnings first

```
This project is on Spring Boot 3.2. Upgrade to 3.5 first and fix
all deprecation warnings before we go to 4.0.
```

### Jackson 3 migration only

```
We're already on Spring Boot 4.0 but still using Jackson 2
compatibility mode. Help me migrate to Jackson 3.
```

### Quick scan with the helper script

```
Run the parse-spring-project script on this project and tell me
what needs to change.
```

## Included References

| File | Description |
|------|-------------|
| **migration-guide.md** | Condensed reference for all Spring Boot 4.0 breaking changes: removed features, package relocations, property renames, ecosystem version matrix |
| **starter-renames.md** | Complete list of renamed starters with Maven and Gradle before/after examples |
| **jackson3-migration.md** | Detailed Jackson 3 migration: group ID changes, annotation renames, class renames, property changes, temporary compatibility path |

## Included Scripts

| File | Description |
|------|-------------|
| **parse-spring-project.js** | Node.js scanner that reads project files and detects Spring Boot version, dependencies, deprecated APIs, and configuration properties to rename. Outputs summary or JSON format |

### Script Usage

```bash
# Summary report (default)
node scripts/parse-spring-project.js --path /path/to/project

# JSON output (for programmatic use)
node scripts/parse-spring-project.js --path /path/to/project --format json
```
