# System Design Framework

Follow this structured approach when designing any system.

## 1. Requirements Gathering
Clarify the boundaries of the problem before designing solutions.
- **Functional Requirements:** What must the system do? (e.g., "Users can post a tweet", "Users can view a timeline").
- **Non-Functional Requirements:** Constraints on the system's behavior (Scale, latency, availability, consistency vs. availability, cost).
- **Constraints:** Team size, timeline to launch, existing technology stack, regulatory requirements.

## 2. High-Level Design
Establish the big picture.
- **Component Diagram:** Outline the major services (API Gateway, Auth Service, Core App, Database).
- **Data Flow:** How does a request travel through the system?
- **API Contracts:** High-level definition of how clients talk to the system.
- **Storage Choices:** Initial selection of databases/caches based on read/write patterns.

## 3. Deep Dive
Examine the critical components in detail.
- **Data Model Design:** Schema definitions, normalization vs denormalization, indexing strategies.
- **API Endpoint Design:** Detailed REST paths, GraphQL mutations, or gRPC definitions. Payload structures.
- **Caching Strategy:** Where to cache (CDN, application level, database level), cache invalidation policies (TTL, LRU).
- **Queue/Event Design:** Asynchronous processing (Kafka, SQS, RabbitMQ), event sourcing, pub/sub models.
- **Error Handling:** Retry logic (exponential backoff, jitter), circuit breakers, dead-letter queues.

## 4. Scale and Reliability
Ensure the system survives production traffic.
- **Load Estimation:** Back-of-the-envelope calculations for Requests Per Second (RPS), storage requirements, and bandwidth.
- **Scaling Strategies:** Horizontal (adding nodes) vs Vertical (bigger machines). Database sharding and replication.
- **Failover and Redundancy:** Multi-AZ deployments, active-passive vs active-active database setups.
- **Observability:** Key metrics to track, monitoring, and alerting strategies.

## 5. Trade-off Analysis
Every decision has a cost. Make them explicit.
- **Consistency vs. Availability:** (CAP Theorem) What happens during a network partition?
- **Complexity vs. Time-to-Market:** Is a microservice architecture justified for a V1 MVP?
- **Cost vs. Performance:** Evaluating the cost of caching and multi-region redundancy against the required latency.
- **Future Considerations:** Identify specific bottlenecks that will break first as the system scales (e.g., "The relational DB will handle up to 10M users, after which we will need to shard").