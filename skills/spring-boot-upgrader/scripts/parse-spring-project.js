#!/usr/bin/env node

/**
 * Spring Boot Project Scanner
 *
 * Scans a Spring Boot project to detect the current version, dependencies,
 * and configuration patterns. Outputs a migration summary, JSON, or shell
 * commands for the upgrade.
 *
 * Usage:
 *   node parse-spring-project.js [--path <dir>] [--format summary|json|shell]
 */

const fs = require('fs');
const path = require('path');

// ---------------------------------------------------------------------------
// CLI Arguments
// ---------------------------------------------------------------------------
const args = process.argv.slice(2);
let projectPath = process.cwd();
let format = 'summary';

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--path' && args[i + 1]) projectPath = args[++i];
  if (args[i] === '--format' && args[i + 1]) format = args[++i];
}

// ---------------------------------------------------------------------------
// File Scanner
// ---------------------------------------------------------------------------
const SCAN_FILES = [
  'pom.xml',
  'build.gradle',
  'build.gradle.kts',
  'application.properties',
  'application.yml',
  'application.yaml',
  'src/main/resources/application.properties',
  'src/main/resources/application.yml',
  'src/main/resources/application.yaml',
  'Dockerfile',
  'docker-compose.yml',
  'docker-compose.yaml',
  '.mvn/wrapper/maven-wrapper.properties',
  'gradle/wrapper/gradle-wrapper.properties',
  'src/main/resources/META-INF/spring.factories',
  'src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports',
];

function scanFiles(basePath) {
  const results = [];
  for (const relative of SCAN_FILES) {
    const full = path.join(basePath, relative);
    if (fs.existsSync(full)) {
      try {
        results.push({ path: relative, content: fs.readFileSync(full, 'utf-8') });
      } catch { /* skip unreadable */ }
    }
  }
  // Also scan Java source files for import patterns (first 50 files)
  const srcDirs = ['src/main/java', 'src/test/java'];
  for (const dir of srcDirs) {
    const fullDir = path.join(basePath, dir);
    if (fs.existsSync(fullDir)) {
      walkJavaFiles(fullDir, results, 50);
    }
  }
  return results;
}

function walkJavaFiles(dir, results, limit) {
  if (results.length >= limit + SCAN_FILES.length) return;
  let entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return; }
  for (const entry of entries) {
    if (results.length >= limit + SCAN_FILES.length) return;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walkJavaFiles(full, results, limit);
    } else if (entry.name.endsWith('.java') || entry.name.endsWith('.kt')) {
      try {
        results.push({ path: full, content: fs.readFileSync(full, 'utf-8') });
      } catch { /* skip */ }
    }
  }
}

// ---------------------------------------------------------------------------
// Version Detection
// ---------------------------------------------------------------------------
function detectSpringBootVersion(files) {
  for (const f of files) {
    // Maven parent version
    const mavenMatch = f.content.match(
      /spring-boot-starter-parent<\/artifactId>\s*<version>([^<]+)<\/version>/
    );
    if (mavenMatch) return mavenMatch[1];

    // Maven BOM version
    const bomMatch = f.content.match(
      /spring-boot-dependencies<\/artifactId>\s*<version>([^<]+)<\/version>/
    );
    if (bomMatch) return bomMatch[1];

    // Gradle plugin version
    const gradleMatch = f.content.match(
      /org\.springframework\.boot['"]\s*version\s*['"]([^'"]+)['"]/
    );
    if (gradleMatch) return gradleMatch[1];

    // Gradle Kotlin DSL
    const ktsMatch = f.content.match(
      /id\s*\(\s*["']org\.springframework\.boot["']\s*\)\s*version\s*["']([^"']+)["']/
    );
    if (ktsMatch) return ktsMatch[1];
  }
  return null;
}

function detectJavaVersion(files) {
  for (const f of files) {
    // Maven java.version property
    const mavenMatch = f.content.match(/<java\.version>(\d+)<\/java\.version>/);
    if (mavenMatch) return parseInt(mavenMatch[1], 10);

    // Maven source/target
    const sourceMatch = f.content.match(/<maven\.compiler\.source>(\d+)<\/maven\.compiler\.source>/);
    if (sourceMatch) return parseInt(sourceMatch[1], 10);

    // Gradle sourceCompatibility
    const gradleMatch = f.content.match(/sourceCompatibility\s*=\s*['"]?(\d+)/);
    if (gradleMatch) return parseInt(gradleMatch[1], 10);

    // Gradle Kotlin DSL
    const ktsMatch = f.content.match(/jvmToolchain\s*\(\s*(\d+)\s*\)/);
    if (ktsMatch) return parseInt(ktsMatch[1], 10);

    // Dockerfile
    const dockerMatch = f.content.match(/FROM\s+.*(?:openjdk|eclipse-temurin|amazoncorretto|liberica)[:-](\d+)/i);
    if (dockerMatch) return parseInt(dockerMatch[1], 10);
  }
  return null;
}

function detectBuildTool(files) {
  for (const f of files) {
    if (f.path === 'pom.xml') return 'maven';
    if (f.path === 'build.gradle' || f.path === 'build.gradle.kts') return 'gradle';
  }
  return 'unknown';
}

// ---------------------------------------------------------------------------
// Dependency Detection
// ---------------------------------------------------------------------------
const DEPENDENCY_PATTERNS = {
  'spring-security': {
    patterns: ['spring-boot-starter-security', 'spring-security', 'SecurityFilterChain', 'WebSecurityConfigurerAdapter', '@EnableWebSecurity'],
    label: 'Spring Security',
  },
  'spring-data-jpa': {
    patterns: ['spring-boot-starter-data-jpa', 'spring-data-jpa', '@Entity', 'JpaRepository', 'CrudRepository'],
    label: 'Spring Data JPA (Hibernate)',
  },
  'jackson': {
    patterns: ['jackson-databind', 'ObjectMapper', '@JsonProperty', '@JsonComponent', 'JsonSerializer', 'JsonDeserializer', '@JsonMixin'],
    label: 'Jackson',
  },
  'kafka': {
    patterns: ['spring-kafka', 'spring-boot-starter-kafka', '@KafkaListener', 'KafkaTemplate'],
    label: 'Spring Kafka',
  },
  'mongodb': {
    patterns: ['spring-boot-starter-data-mongodb', 'MongoRepository', 'MongoTemplate', '@Document'],
    label: 'Spring Data MongoDB',
  },
  'elasticsearch': {
    patterns: ['spring-boot-starter-data-elasticsearch', 'ElasticsearchRestTemplate', 'RestClient', '@Document'],
    label: 'Spring Data Elasticsearch',
  },
  'batch': {
    patterns: ['spring-boot-starter-batch', '@EnableBatchProcessing', 'JobBuilderFactory', 'StepBuilderFactory'],
    label: 'Spring Batch',
  },
  'amqp': {
    patterns: ['spring-boot-starter-amqp', 'RabbitTemplate', '@RabbitListener', 'spring-rabbit'],
    label: 'Spring AMQP (RabbitMQ)',
  },
  'flyway': {
    patterns: ['flyway-core', 'flyway-mysql', 'flyway-database', 'org.flywaydb'],
    label: 'Flyway',
  },
  'liquibase': {
    patterns: ['liquibase-core', 'org.liquibase'],
    label: 'Liquibase',
  },
  'oauth2-client': {
    patterns: ['spring-boot-starter-oauth2-client', 'oauth2Login', 'OAuth2AuthorizedClient'],
    label: 'OAuth2 Client',
  },
  'oauth2-resource-server': {
    patterns: ['spring-boot-starter-oauth2-resource-server', 'jwt()', 'opaqueToken()'],
    label: 'OAuth2 Resource Server',
  },
  'webflux': {
    patterns: ['spring-boot-starter-webflux', 'WebClient', '@EnableWebFlux', 'RouterFunction'],
    label: 'Spring WebFlux',
  },
  'undertow': {
    patterns: ['spring-boot-starter-undertow', 'undertow'],
    label: 'Undertow (REMOVED in 4.0)',
  },
  'spring-retry': {
    patterns: ['spring-retry', '@Retryable', '@EnableRetry', 'RetryTemplate'],
    label: 'Spring Retry (removed from BOM in 4.0)',
  },
};

function detectDependencies(files) {
  const combined = files.map(f => f.content).join('\n');
  const detected = {};

  for (const [key, config] of Object.entries(DEPENDENCY_PATTERNS)) {
    const matches = config.patterns.filter(p => combined.includes(p));
    if (matches.length > 0) {
      detected[key] = {
        label: config.label,
        matchedPatterns: matches,
        confidence: matches.length >= 2 ? 'high' : 'medium',
      };
    }
  }
  return detected;
}

// ---------------------------------------------------------------------------
// Deprecated API Detection
// ---------------------------------------------------------------------------
const DEPRECATED_APIS = {
  '@MockBean': { replacement: '@MockitoBean', since: '3.4', removedIn: '4.0' },
  '@SpyBean': { replacement: '@MockitoSpyBean', since: '3.4', removedIn: '4.0' },
  'WebSecurityConfigurerAdapter': { replacement: 'SecurityFilterChain bean', since: '2.7', removedIn: '3.0+' },
  'MockitoTestExecutionListener': { replacement: '@ExtendWith(MockitoExtension.class)', since: '3.4', removedIn: '4.0' },
  'alwaysApplyingNotNull': { replacement: 'always()', since: '3.5', removedIn: '4.0' },
  'spring.factories': { replacement: 'AutoConfiguration.imports', since: '3.0', removedIn: '4.0' },
  'javax.persistence': { replacement: 'jakarta.persistence', since: '3.0', removedIn: '3.0' },
  'javax.servlet': { replacement: 'jakarta.servlet', since: '3.0', removedIn: '3.0' },
  'com.fasterxml.jackson': { replacement: 'tools.jackson (Jackson 3)', since: '4.0', removedIn: '4.0' },
};

function detectDeprecatedAPIs(files) {
  const combined = files.map(f => f.content).join('\n');
  const found = [];

  for (const [pattern, info] of Object.entries(DEPRECATED_APIS)) {
    if (combined.includes(pattern)) {
      found.push({ pattern, ...info });
    }
  }
  return found;
}

// ---------------------------------------------------------------------------
// Configuration Property Detection
// ---------------------------------------------------------------------------
const RENAMED_PROPERTIES = [
  { old: 'spring.data.mongodb.host', new: 'spring.mongodb.host' },
  { old: 'spring.data.mongodb.port', new: 'spring.mongodb.port' },
  { old: 'spring.data.mongodb.database', new: 'spring.mongodb.database' },
  { old: 'spring.data.mongodb.uri', new: 'spring.mongodb.uri' },
  { old: 'spring.session.redis.', new: 'spring.session.data.redis.' },
  { old: 'spring.session.mongodb.', new: 'spring.session.data.mongodb.' },
  { old: 'spring.dao.exceptiontranslation.enabled', new: 'spring.persistence.exceptiontranslation.enabled' },
  { old: 'spring.kafka.retry.topic.backoff.random', new: 'spring.kafka.retry.topic.backoff.jitter' },
  { old: 'spring.jackson.read.', new: 'spring.jackson.json.read.' },
  { old: 'spring.jackson.write.', new: 'spring.jackson.json.write.' },
  { old: 'spring.jackson.parser.', new: 'spring.jackson.json.read.' },
];

function detectRenamedProperties(files) {
  const propsFiles = files.filter(f =>
    f.path.endsWith('.properties') || f.path.endsWith('.yml') || f.path.endsWith('.yaml')
  );
  const combined = propsFiles.map(f => f.content).join('\n');
  return RENAMED_PROPERTIES.filter(p => combined.includes(p.old));
}

// ---------------------------------------------------------------------------
// Migration Path
// ---------------------------------------------------------------------------
function parseMajorMinor(version) {
  if (!version) return null;
  const match = version.match(/^(\d+)\.(\d+)/);
  return match ? { major: parseInt(match[1], 10), minor: parseInt(match[2], 10) } : null;
}

function determineMigrationPath(version) {
  const v = parseMajorMinor(version);
  if (!v) return { hops: [], complexity: 'unknown' };

  if (v.major === 1) {
    return { hops: [`${version}`, '2.7.x', '3.5.x', '4.0.x'], complexity: 'very-high' };
  }
  if (v.major === 2 && v.minor < 7) {
    return { hops: [`${version}`, '2.7.x', '3.5.x', '4.0.x'], complexity: 'high' };
  }
  if (v.major === 2 && v.minor === 7) {
    return { hops: [`${version}`, '3.5.x', '4.0.x'], complexity: 'medium-high' };
  }
  if (v.major === 3 && v.minor < 5) {
    return { hops: [`${version}`, '3.5.x', '4.0.x'], complexity: 'medium' };
  }
  if (v.major === 3 && v.minor === 5) {
    return { hops: [`${version}`, '4.0.x'], complexity: 'low' };
  }
  if (v.major >= 4) {
    return { hops: [], complexity: 'none' };
  }
  return { hops: [], complexity: 'unknown' };
}

function classifyScope(version, deps, deprecatedAPIs) {
  const v = parseMajorMinor(version);
  if (!v) return 'unknown';
  if (v.major <= 2) return 'full-platform';

  const hasJacksonCustom = !!deps.jackson && deps.jackson.confidence === 'high';
  const hasHibernate = !!deps['spring-data-jpa'];

  if (v.major === 3 && v.minor < 5) return 'major';
  if (hasJacksonCustom || hasHibernate) return 'major';
  if (deprecatedAPIs.length > 2) return 'standard';
  return 'minimal';
}

// ---------------------------------------------------------------------------
// Output Formatters
// ---------------------------------------------------------------------------
function formatSummary(analysis) {
  const lines = [];
  lines.push('=== Spring Boot Upgrader: Project Analysis ===\n');

  // Version info
  lines.push('## Current State');
  lines.push(`  Spring Boot: ${analysis.version || 'not detected'}`);
  lines.push(`  Java:        ${analysis.javaVersion || 'not detected'}`);
  lines.push(`  Build tool:  ${analysis.buildTool}`);

  // Migration path
  lines.push('\n## Migration Path');
  if (analysis.migration.hops.length > 0) {
    lines.push(`  Route:      ${analysis.migration.hops.join(' → ')}`);
    lines.push(`  Complexity: ${analysis.migration.complexity}`);
    lines.push(`  Scope:      ${analysis.scope}`);
    lines.push(`  Phases:     ${analysis.migration.hops.length}`);
  } else if (analysis.migration.complexity === 'none') {
    lines.push('  Already on Spring Boot 4.x. No migration needed.');
  } else {
    lines.push('  Could not determine migration path.');
  }

  // Java upgrade needed?
  if (analysis.javaVersion && analysis.javaVersion < 17) {
    lines.push(`\n## ⚠ Java Upgrade Required`);
    lines.push(`  Current: Java ${analysis.javaVersion}`);
    lines.push(`  Required: Java 17+ (Java 21 recommended)`);
  }

  // Dependencies
  lines.push('\n## Detected Dependencies');
  const deps = Object.entries(analysis.dependencies);
  if (deps.length > 0) {
    for (const [, config] of deps) {
      lines.push(`  [${config.confidence === 'high' ? '!' : '?'}] ${config.label}`);
    }
  } else {
    lines.push('  No Spring-specific dependencies detected.');
  }

  // Deprecated APIs
  if (analysis.deprecatedAPIs.length > 0) {
    lines.push('\n## Deprecated APIs Found');
    for (const api of analysis.deprecatedAPIs) {
      lines.push(`  [!] ${api.pattern} → ${api.replacement} (deprecated ${api.since}, removed ${api.removedIn})`);
    }
  }

  // Properties to rename
  if (analysis.renamedProperties.length > 0) {
    lines.push('\n## Configuration Properties to Rename');
    for (const p of analysis.renamedProperties) {
      lines.push(`  ${p.old} → ${p.new}`);
    }
  }

  // Warnings
  lines.push('\n## Warnings');
  if (analysis.dependencies.undertow) {
    lines.push('  [!!] Undertow detected — REMOVED in Spring Boot 4.0. Must switch to Tomcat or Jetty.');
  }
  if (analysis.dependencies['spring-retry']) {
    lines.push('  [!!] Spring Retry detected — removed from Boot 4.0 BOM. Declare explicit version or migrate to Spring Framework 7 retry.');
  }
  if (analysis.dependencies.jackson) {
    lines.push('  [!] Jackson detected — Jackson 3 is a major breaking change. Review references/jackson3-migration.md.');
  }
  if (analysis.dependencies.batch) {
    lines.push('  [!] Spring Batch detected — default is now in-memory. Add spring-boot-starter-batch-jdbc for DB metadata.');
  }

  return lines.join('\n');
}

function formatJSON(analysis) {
  return JSON.stringify(analysis, null, 2);
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
function main() {
  const files = scanFiles(projectPath);

  if (files.length === 0) {
    console.error(`No project files found in ${projectPath}`);
    process.exit(1);
  }

  const version = detectSpringBootVersion(files);
  const javaVersion = detectJavaVersion(files);
  const buildTool = detectBuildTool(files);
  const dependencies = detectDependencies(files);
  const deprecatedAPIs = detectDeprecatedAPIs(files);
  const renamedProperties = detectRenamedProperties(files);
  const migration = determineMigrationPath(version);
  const scope = classifyScope(version, dependencies, deprecatedAPIs);

  const analysis = {
    version,
    javaVersion,
    buildTool,
    dependencies,
    deprecatedAPIs,
    renamedProperties,
    migration,
    scope,
  };

  switch (format) {
    case 'json':
      console.log(formatJSON(analysis));
      break;
    default:
      console.log(formatSummary(analysis));
  }
}

main();
