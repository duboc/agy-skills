# Spring Boot 4.0 Migration Guide — Quick Reference

This is the condensed reference for the Spring Boot 4.0 migration. The full official guide lives at:
https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide

## Prerequisites

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| Java | 17 | 21 (LTS) |
| Kotlin | 2.2 | Latest 2.x |
| GraalVM native-image | 25 | Latest |
| Jakarta EE | 11 | 11 |
| Servlet | 6.1 | 6.1 |
| Spring Framework | 7.0 | Latest 7.x |

## Mandatory Migration Path

```
Spring Boot 1.x → 2.7.x → 3.5.x → 4.0.x
Spring Boot 2.x → 2.7.x → 3.5.x → 4.0.x
Spring Boot 3.x → 3.5.x → 4.0.x
```

**Never skip 3.5.x.** It is the bridge release that deprecates everything removed in 4.0.

## Features Removed in 4.0

| Feature | Replacement |
|---------|-------------|
| Undertow embedded server | Tomcat (default) or Jetty |
| Reactive Pulsar auto-configuration | Manual configuration |
| Embedded executable uber-jar scripts | `java -jar` |
| Spring Session Hazelcast (Boot-managed) | Hazelcast-managed module |
| Spring Session MongoDB (Boot-managed) | MongoDB-managed module |
| Spock integration | JUnit 5/6 |
| MockitoTestExecutionListener | `@ExtendWith(MockitoExtension.class)` |
| Spring Retry dependency management | Spring Framework 7 retry or explicit version |
| Classic uber-jar loader | Remove `CLASSIC` loader config |
| Binding to public fields | Use private fields + getters/setters |
| `alwaysApplyingNotNull()` on PropertyMapper | Use `always()` |

## Module Architecture Overhaul

Spring Boot 4.0 restructures into focused modules:

- **Modules**: `spring-boot-<technology>`
- **Packages**: `org.springframework.boot.<technology>`
- **Starters**: `spring-boot-starter-<technology>`
- **Test modules**: `spring-boot-<technology>-test`

**Tip**: Add `spring-boot-starter-classic` temporarily to restore the old flat classpath, then migrate incrementally.

## Package Relocations

| Old Package/Class | New Location |
|------------------|-------------|
| `o.s.b.BootstrapRegistry` | `o.s.b.bootstrap.BootstrapRegistry` |
| `o.s.b.env.EnvironmentPostProcessor` | `o.s.b.EnvironmentPostProcessor` |
| `o.s.b.test.web.client.TestRestTemplate` | `o.s.b.resttestclient.TestRestTemplate` |
| `o.s.b.test.autoconfigure.properties.PropertyMapping` | `o.s.b.test.context.PropertyMapping` |
| `@EntityScan` imports | `o.s.b.persistence.autoconfigure` |

## Configuration Property Changes

| Old Property | New Property |
|-------------|-------------|
| `spring.data.mongodb.host` | `spring.mongodb.host` |
| `spring.data.mongodb.port` | `spring.mongodb.port` |
| `spring.data.mongodb.database` | `spring.mongodb.database` |
| `spring.data.mongodb.uri` | `spring.mongodb.uri` |
| `spring.data.mongodb.username` | `spring.mongodb.username` |
| `spring.data.mongodb.password` | `spring.mongodb.password` |
| `spring.data.mongodb.ssl.enabled` | `spring.mongodb.ssl.enabled` |
| `spring.data.mongodb.ssl.bundle` | `spring.mongodb.ssl.bundle` |
| `spring.data.mongodb.replica-set-name` | `spring.mongodb.replica-set-name` |
| `spring.data.mongodb.authentication-database` | `spring.mongodb.authentication-database` |
| `spring.session.redis.*` | `spring.session.data.redis.*` |
| `spring.session.mongodb.*` | `spring.session.data.mongodb.*` |
| `spring.dao.exceptiontranslation.enabled` | `spring.persistence.exceptiontranslation.enabled` |
| `spring.kafka.retry.topic.backoff.random` | `spring.kafka.retry.topic.backoff.jitter` |
| `spring.jackson.read.*` | `spring.jackson.json.read.*` |
| `spring.jackson.write.*` | `spring.jackson.json.write.*` |
| `spring.jackson.parser.*` | `spring.jackson.json.read.*` |

## Test Framework Changes

| Old Pattern | New Pattern |
|------------|-------------|
| `@MockBean` | `@MockitoBean` |
| `@SpyBean` | `@MockitoSpyBean` |
| `@SpringBootTest` auto-provides MockMvc | Must add `@AutoConfigureMockMvc` |
| `@SpringBootTest` auto-provides TestRestTemplate | Must add `@AutoConfigureTestRestTemplate` |
| `@AutoConfigureMockMvc(webClientEnabled=false)` | `@AutoConfigureMockMvc(htmlUnit = @HtmlUnit(webClient = false))` |

## Ecosystem Version Matrix

| Component | Boot 3.5.x | Boot 4.0.x |
|-----------|-----------|-----------|
| Spring Framework | 6.2.x | 7.0.x |
| Spring Security | 6.4.x | 7.0.x |
| Spring Data | 2024.1 | 2025.1 |
| Spring Batch | 5.2.x | 6.0.x |
| Spring Kafka | 3.3.x | 4.0.x |
| Spring AMQP | 3.2.x | 4.0.x |
| Hibernate | 6.6.x | 7.x |
| Jackson | 2.18.x | 3.x |
| Elasticsearch client | 8.x | 9.x |
