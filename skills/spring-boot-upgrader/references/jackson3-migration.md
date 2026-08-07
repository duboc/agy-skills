# Jackson 3 Migration Reference

Jackson 3 is the single biggest breaking change in Spring Boot 4.0. It affects almost every Spring Boot application because Jackson is the default JSON serializer.

## Group ID and Package Changes

| Component | Jackson 2 | Jackson 3 |
|-----------|-----------|-----------|
| Core | `com.fasterxml.jackson.core:jackson-core` | `tools.jackson.core:jackson-core` |
| Databind | `com.fasterxml.jackson.core:jackson-databind` | `tools.jackson.core:jackson-databind` |
| Annotations | `com.fasterxml.jackson.core:jackson-annotations` | `com.fasterxml.jackson.core:jackson-annotations` (unchanged) |
| Datatype modules | `com.fasterxml.jackson.datatype:*` | `tools.jackson.datatype:*` |
| Dataformat modules | `com.fasterxml.jackson.dataformat:*` | `tools.jackson.dataformat:*` |

**Note**: `jackson-annotations` keeps the old group ID. Everything else moves to `tools.jackson`.

## Spring Boot Annotation Changes

| Jackson 2 (Boot 3.x) | Jackson 3 (Boot 4.0) |
|----------------------|---------------------|
| `@JsonComponent` | `@JacksonComponent` |
| `@JsonMixin` | `@JacksonMixin` |

## Spring Boot Class Renames

| Jackson 2 (Boot 3.x) | Jackson 3 (Boot 4.0) |
|----------------------|---------------------|
| `JsonObjectSerializer` | `ObjectValueSerializer` |
| `JsonValueDeserializer` | `ObjectValueDeserializer` |
| `Jackson2ObjectMapperBuilderCustomizer` | `JsonMapperBuilderCustomizer` |

## Configuration Property Changes

| Old Property | New Property |
|-------------|-------------|
| `spring.jackson.read.*` | `spring.jackson.json.read.*` |
| `spring.jackson.write.*` | `spring.jackson.json.write.*` |
| `spring.jackson.parser.*` | `spring.jackson.json.read.*` |

## Jackson 3 Behavioral Changes

Key differences from Jackson 2:

1. **Stricter type handling** — Jackson 3 is more strict about type resolution and may reject previously-accepted input.
2. **Module consolidation** — Some modules have been merged or renamed.
3. **ObjectMapper behavior** — Default settings have changed. Review any assumptions about default serialization/deserialization behavior.
4. **Auto-detection** — Jackson 3 auto-detects and registers all classpath modules. Disable with `spring.jackson.find-and-add-modules=false`.

## Temporary Jackson 2 Compatibility

If Jackson 3 migration is too disruptive to do in one pass, Spring Boot 4.0 provides a compatibility path:

### Step 1: Add the Jackson 2 compatibility module

**Maven:**
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-jackson2</artifactId>
</dependency>
```

**Gradle:**
```groovy
implementation 'org.springframework.boot:spring-boot-jackson2'
```

### Step 2: Configure Boot to use Jackson 2 defaults

```properties
spring.jackson.use-jackson2-defaults=true
```

### Step 3: Use the Jackson 2 property namespace

Jackson 2 properties are available under:
```properties
spring.jackson2.serialization.*
spring.jackson2.deserialization.*
```

**Important**: This is a temporary bridge. The `spring-boot-jackson2` module is deprecated and will be removed in a future Boot release. Plan to fully migrate to Jackson 3.

## Migration Checklist

- [ ] Update Jackson dependency group IDs in build file
- [ ] Replace `@JsonComponent` → `@JacksonComponent`
- [ ] Replace `@JsonMixin` → `@JacksonMixin`
- [ ] Replace `JsonObjectSerializer` → `ObjectValueSerializer`
- [ ] Replace `JsonValueDeserializer` → `ObjectValueDeserializer`
- [ ] Replace `Jackson2ObjectMapperBuilderCustomizer` → `JsonMapperBuilderCustomizer`
- [ ] Update `spring.jackson.read/write/parser` properties
- [ ] Review custom serializers/deserializers for behavioral changes
- [ ] Run full test suite with special attention to JSON tests
- [ ] Verify API responses match expected format
