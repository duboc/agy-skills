# Spring Boot 4.0 — Starter Renames

## Renamed Starters

These starters have been renamed. The old names still work in 4.0 but are deprecated and will be removed in a future release.

| Old Starter | New Starter | Notes |
|------------|-------------|-------|
| `spring-boot-starter-web` | `spring-boot-starter-webmvc` | Aligns with Spring MVC module name |
| `spring-boot-starter-web-services` | `spring-boot-starter-webservices` | Hyphen removed |
| `spring-boot-starter-aop` | `spring-boot-starter-aspectj` | Aligns with underlying technology |
| `spring-boot-starter-oauth2-client` | `spring-boot-starter-security-oauth2-client` | Grouped under security |
| `spring-boot-starter-oauth2-resource-server` | `spring-boot-starter-security-oauth2-resource-server` | Grouped under security |
| `spring-boot-starter-oauth2-authorization-server` | `spring-boot-starter-security-oauth2-authorization-server` | Grouped under security |

## New Required Starters

These starters are now required for features that previously worked via transitive dependencies:

| Feature | New Required Starter | Replaces |
|---------|---------------------|----------|
| Flyway database migrations | `spring-boot-starter-flyway` | Just adding `flyway-core` dependency |
| Liquibase database migrations | `spring-boot-starter-liquibase` | Just adding `liquibase-core` dependency |
| Spring Batch with DB metadata | `spring-boot-starter-batch-jdbc` | `spring-boot-starter-batch` (now in-memory only) |

## Classic Starters (Backward Compatibility)

For a temporary compatibility bridge, use these starters to restore the pre-4.0 flat classpath:

| Starter | Purpose |
|---------|---------|
| `spring-boot-starter-classic` | All modules on classpath like pre-4.0 |
| `spring-boot-starter-test-classic` | Test modules on classpath like pre-4.0 |

**Strategy**: Add classic starters first, get the build passing, then incrementally replace with modular starters.

## WAR Deployment on Tomcat

| Old Dependency | New Dependency |
|---------------|---------------|
| `spring-boot-starter-tomcat` (provided) | `spring-boot-starter-tomcat-runtime` (provided) |

## Maven / Gradle Examples

### Maven — Before

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-oauth2-resource-server</artifactId>
</dependency>
```

### Maven — After

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webmvc</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security-oauth2-resource-server</artifactId>
</dependency>
```

### Gradle — Before

```groovy
implementation 'org.springframework.boot:spring-boot-starter-web'
implementation 'org.springframework.boot:spring-boot-starter-oauth2-resource-server'
```

### Gradle — After

```groovy
implementation 'org.springframework.boot:spring-boot-starter-webmvc'
implementation 'org.springframework.boot:spring-boot-starter-security-oauth2-resource-server'
```
