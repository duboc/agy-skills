# System Design Capacity Estimation & Trade-Off Cheat Sheet

Use these back-of-the-envelope numbers, formulas, and distributed systems trade-off matrices when sizing and designing architectures.

---

## 1. Latency Numbers Every Engineer Should Know

| Operation | Typical Latency | Order of Magnitude |
|-----------|-----------------|--------------------|
| L1 / L2 CPU Cache reference | `1 ns – 4 ns` | Nanoseconds |
| Main Memory (RAM) reference | `100 ns` | `0.1 µs` |
| Redis / In-Memory Cache read (VPC) | `0.5 ms` | Sub-millisecond |
| SSD Random Read (`4 KB`) | `100 µs – 150 µs` | `0.15 ms` |
| Intra-Region Datacenter RTT (same zone/region) | `0.5 ms – 2 ms` | ~1 ms |
| Indexed Relational / NoSQL point read | `2 ms – 10 ms` | Single-digit ms |
| Cross-Region / Inter-Continental WAN RTT | `70 ms – 150 ms` | ~100 ms |
| LLM Token Generation (Time to First Token) | `250 ms – 1,200 ms` | ~0.5 s |

---

## 2. Back-of-the-Envelope Capacity Formulas

- **Seconds per Day**: `86,400 s` ($\approx 10^5$ seconds/day)
- **Requests per Second (RPS)**:
  $$\text{Average RPS} = \frac{\text{DAU} \times \text{Actions/User/Day}}{10^5}, \quad \text{Peak RPS} \approx 3 \times \text{Average RPS}$$
- **Bandwidth**:
  $$\text{Ingress/Egress (MB/s)} = \text{Peak RPS} \times \text{Avg Payload Size (MB)}$$
- **5-Year Storage**:
  $$\text{Storage (TB)} = \text{Daily New Records} \times \text{Record Size} \times 365 \times 5 \times \text{Replication Factor (3)}$$

---

## 3. Distributed Systems Trade-Off Matrix

| Architectural Decision | Option A | Option B | Selection Rule |
|------------------------|----------|----------|----------------|
| **Consistency Model (PACELC)** | Strong Consistency (`Spanner`, `Postgres` Primary) | Eventual Consistency (`DynamoDB`/`Firestore` multi-region) | Choose **Strong** for ledgers, inventory, and auth; **Eventual** for feeds, telemetry, and catalogs. |
| **Caching Pattern** | Cache-Aside (`Redis` + DB read fallback) | Write-Through / Read-Through | Choose **Cache-Aside** with TTL jitter + singleflight lock for read-heavy workloads (`>10:1` R:W). |
| **Async Decoupling** | Log-Based Broker (`Kafka`, `Pub/Sub`) | Task Queue (`Cloud Tasks`, `RabbitMQ`) | Choose **Log-Based** for multi-consumer event replay; **Task Queue** for per-job rate-limiting and retries. |
| **Rate Limiting** | Token Bucket (Edge Proxy / Redis Lua) | Sliding Window Counter | Combine **Signed Device Session + User Cooldown + CGNAT-safe IP Burst/Sustained** buckets. |
