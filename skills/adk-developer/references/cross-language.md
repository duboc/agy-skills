# ADK Across Languages

ADK is available in Python, Java, Go, and TypeScript. The core model is identical -- agents, tools, state, callbacks -- but each language has its own idioms.

## At a Glance

| Aspect | Python | Java | Go | TypeScript |
|--------|--------|------|----|------------|
| Package | `google-adk` | `com.google.adk:google-adk` | `google.golang.org/adk` | `@google/adk` |
| Minimum runtime | 3.10+ | 17+ | 1.24+ | Node.js 24+ |
| How you define agents | Constructor kwargs | Builder chain | Struct literal | Constructor object |
| How you define tools | Typed function + docstring | Static method + `@Schema` | Struct implementing `tool.Tool` | `FunctionTool` + Zod schema |
| Entry point | `root_agent` variable | `ROOT_AGENT` static field | `main()` function | `export rootAgent` |
| Test runner | `InMemoryRunner` (async) | `InMemoryRunner` (RxJava) | Launcher | `InMemoryRunner` |
| Dev server | `adk run` / `adk web` | Maven + AdkWebServer | `go run` | `npx adk run` / `npx adk web` |

---

## Java

### Project Layout

```
my-agent/
├── src/main/java/com/myorg/agent/
│   ├── OrderAgent.java
│   └── tools/
│       └── InventoryTools.java
├── pom.xml
└── .env
```

### Maven Dependencies

```xml
<dependencies>
    <dependency>
        <groupId>com.google.adk</groupId>
        <artifactId>google-adk</artifactId>
        <version>0.5.0</version>
    </dependency>
    <dependency>
        <groupId>com.google.adk</groupId>
        <artifactId>google-adk-dev</artifactId>
        <version>0.5.0</version>
    </dependency>
</dependencies>
```

### Defining Agents (Builder Pattern)

```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.BaseAgent;
import com.google.adk.tools.FunctionTool;

public class OrderAgent {
    public static final BaseAgent ROOT_AGENT = createAgent();

    private static BaseAgent createAgent() {
        return LlmAgent.builder()
            .name("order_agent")
            .model("gemini-2.5-flash")
            .description("Processes and tracks customer orders")
            .instruction("Help customers with their orders...")
            .tools(FunctionTool.create(InventoryTools.class, "checkStock"))
            .build();
    }
}
```

### Defining Tools (`@Schema` Annotations)

```java
import io.swagger.v3.oas.annotations.media.Schema;
import java.util.Map;

public class InventoryTools {
    @Schema(description = "Check stock availability for a product in a warehouse")
    public static Map<String, Object> checkStock(
        @Schema(name = "sku", description = "Product SKU identifier") String sku,
        @Schema(name = "warehouse", description = "Warehouse location code") String warehouse
    ) {
        int qty = InventoryDB.getQuantity(sku, warehouse);
        return Map.of("sku", sku, "warehouse", warehouse, "quantity", qty, "in_stock", qty > 0);
    }
}
```

### Multi-Agent Composition

```java
LlmAgent validator = LlmAgent.builder()
    .name("order_validator")
    .model("gemini-2.5-flash")
    .instruction("Validate order details for completeness.")
    .outputKey("validation_result")
    .build();

LlmAgent processor = LlmAgent.builder()
    .name("order_processor")
    .model("gemini-2.5-flash")
    .instruction("Process the validated order.")
    .build();

SequentialAgent workflow = SequentialAgent.builder()
    .name("order_workflow")
    .subAgents(validator, processor)
    .build();
```

### Running Tests

```java
import com.google.adk.runner.InMemoryRunner;
import io.reactivex.rxjava3.core.Flowable;

InMemoryRunner runner = new InMemoryRunner(ROOT_AGENT);
Session session = runner.sessionService()
    .createSession("test_app", "test_user").blockingGet();

Content input = Content.fromParts(Part.fromText("Check stock for SKU-100"));
Flowable<Event> events = runner.runAsync("test_user", session.id(), input);
events.blockingForEach(e -> System.out.println(e.stringifyContent()));
```

### Running the Agent

```bash
# CLI mode
mvn compile exec:java -Dexec.mainClass="com.myorg.agent.OrderAgent"

# Web UI
mvn compile exec:java -Dexec.mainClass="com.google.adk.web.AdkWebServer" \
    -Dexec.args="--adk.agents.source-dir=target --server.port=8000"
```

### MCP Integration (Java)

```java
import com.google.adk.tools.mcp.McpToolset;
import com.google.adk.tools.mcp.SseServerParameters;

SseServerParameters params = SseServerParameters.builder()
    .url("http://localhost:5000/mcp/").build();
McpToolset.McpToolsAndToolsetResult result =
    McpToolset.fromServer(params, new ObjectMapper()).get();
```

---

## Go

### Project Layout

```
my-agent/
├── main.go
├── tools.go
├── go.mod
└── .env
```

### Setup

```bash
go mod init myorg.com/order-agent
go get google.golang.org/adk
go mod tidy
```

### Defining Agents (Struct Config)

```go
package main

import (
    "context"
    "log"
    "os"

    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/cmd/launcher"
    "google.golang.org/adk/cmd/launcher/full"
    "google.golang.org/adk/model/gemini"
    "google.golang.org/genai"
)

func main() {
    ctx := context.Background()

    model, err := gemini.NewModel(ctx, "gemini-2.5-flash",
        &genai.ClientConfig{APIKey: os.Getenv("GOOGLE_API_KEY")})
    if err != nil {
        log.Fatal(err)
    }

    agent, err := llmagent.New(llmagent.Config{
        Name:        "order_agent",
        Model:       model,
        Description: "Processes customer orders",
        Instruction: "Help customers with their orders...",
        Tools:       []tool.Tool{stockChecker},
    })
    if err != nil {
        log.Fatal(err)
    }

    l := full.NewLauncher()
    l.Start(ctx, launcher.Config{Agent: agent})
}
```

### Running

```bash
go run .                     # CLI mode
go run . web api webui       # Web UI on localhost:8080
```

---

## TypeScript

### Project Layout

```
my-agent/
├── agent.ts
├── tools.ts
├── package.json
└── .env
```

### Setup

```bash
mkdir my-agent && cd my-agent
npm init --yes
npm pkg set type="module"
npm pkg set main="agent.ts"
npm install @google/adk
npm install -D @google/adk-devtools
```

### Defining Agents

```typescript
import { LlmAgent, SequentialAgent } from '@google/adk';
import { checkStockTool, processOrderTool } from './tools';

const validator = new LlmAgent({
    name: 'order_validator',
    model: 'gemini-2.5-flash',
    instruction: 'Validate order details for completeness.',
    outputKey: 'validation',
});

const processor = new LlmAgent({
    name: 'order_processor',
    model: 'gemini-2.5-flash',
    instruction: 'Process validated orders. Read validation from state.',
    tools: [checkStockTool, processOrderTool],
});

export const rootAgent = new SequentialAgent({
    name: 'order_pipeline',
    subAgents: [validator, processor],
});
```

### Defining Tools (Zod Schemas)

```typescript
import { FunctionTool } from '@google/adk';
import { z } from 'zod';

export const checkStockTool = new FunctionTool({
    name: 'check_stock',
    description: 'Check product availability in a warehouse.',
    parameters: z.object({
        sku: z.string().describe('Product SKU identifier'),
        warehouse: z.string().default('main').describe('Warehouse location'),
    }),
    execute: async ({ sku, warehouse }) => {
        const qty = await db.getQuantity(sku, warehouse);
        return { sku, warehouse, quantity: qty, in_stock: qty > 0 };
    },
});
```

### Callbacks

```typescript
export const rootAgent = new LlmAgent({
    name: 'guarded_agent',
    model: 'gemini-2.5-flash',
    instruction: '...',
    tools: [checkStockTool],
    beforeToolCallback: (tool, args, toolContext) => {
        if (args.sku && !args.sku.startsWith('SKU-')) {
            return { error: 'Invalid SKU format. Must start with SKU-' };
        }
        return undefined;
    },
});
```

### Testing

```typescript
import { InMemoryRunner, isFinalResponse } from '@google/adk';
import { createUserContent } from '@google/genai';

const runner = new InMemoryRunner({ agent: rootAgent, appName: 'test' });
const session = await runner.sessionService.createSession({
    userId: 'tester', appName: 'test',
});

for await (const event of runner.runAsync({
    userId: 'tester',
    sessionId: session.id,
    newMessage: createUserContent('Check stock for SKU-100'),
})) {
    if (isFinalResponse(event)) {
        console.log(event.content?.parts?.[0]?.text);
    }
}
```

### Running

```bash
npx adk run agent.ts     # CLI mode
npx adk web              # Web UI
```

---

## Tool Definition Comparison

The same "check stock" tool across all four languages:

**Python** -- function + docstring:
```python
def check_stock(sku: str, warehouse: str = "main") -> dict:
    """Check product stock levels.
    Args:
        sku: Product SKU identifier.
        warehouse: Warehouse location.
    """
    return {"sku": sku, "quantity": 42}
```

**Java** -- static method + `@Schema`:
```java
@Schema(description = "Check product stock levels")
public static Map<String, Object> checkStock(
    @Schema(name = "sku", description = "Product SKU") String sku,
    @Schema(name = "warehouse", description = "Warehouse location") String warehouse
) { return Map.of("sku", sku, "quantity", 42); }
```

**TypeScript** -- `FunctionTool` + Zod:
```typescript
new FunctionTool({
    name: 'check_stock',
    description: 'Check product stock levels.',
    parameters: z.object({
        sku: z.string().describe('Product SKU'),
        warehouse: z.string().default('main'),
    }),
    execute: ({ sku }) => ({ sku, quantity: 42 }),
});
```

**Go** -- struct implementing `tool.Tool` interface (or built-in types like `geminitool.GoogleSearch{}`).

---

## Sample Repositories

Working examples for each language:
- **Python**: https://github.com/google/adk-samples/tree/main/python/agents
- **Java**: https://github.com/google/adk-samples/tree/main/java/agents
- **TypeScript**: https://github.com/google/adk-samples/tree/main/typescript/agents
