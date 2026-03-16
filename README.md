# Myelin Kernel

A minimalist memory substrate for autonomous AI agents.

Myelin Kernel is a lightweight, thread-safe reinforcement memory layer inspired by how biological myelin strengthens neural pathways. It allows AI systems to store, reinforce, decay, and retrieve knowledge over time using a simple SQLite database.

The goal is not to replace vector databases or RAG systems, but to provide a persistent cognitive memory layer that improves reasoning across sessions.

---

## Why Myelin?

Most AI tools are stateless. Every conversation starts from zero.

Myelin Kernel introduces a simple idea:

Useful knowledge should get stronger when used.  
Unused knowledge should slowly fade.

This produces a memory system that naturally surfaces the most useful insights.

---

## Core Features

- Reinforcement-based memory scoring
- Thread-safe SQLite backend
- Identity layer for stable principles
- Knowledge layer for learned experience
- Honeypot layer for tamper detection
- Gentle decay of unused knowledge
- Integrity verification via hashing
- Markdown transparency export
- Zero external dependencies

---

## Architecture

Agent / LLM  
   ↓  
Myelin Kernel  
   ↓  
SQLite Memory Store  
   ↓  
Markdown Transparency Export

Memory is organized into three layers:

| Layer | Purpose |
|------|------|
| identity | stable system principles |
| knowledge | learned experiences |
| honeypot | decoy entries for tamper detection |

---

## Installation

Clone the repository:

git clone https://github.com/Tetrahedroned/myelin-kernel.git  
cd myelin-kernel

No external dependencies are required.

Python 3.9 or higher recommended.

---

## Quick Start

```python
from myelin_kernel import MyelinKernel

memory = MyelinKernel()

memory.reflect_and_store(
    "Agents improve when reflection compresses work into reusable knowledge."
)

results = memory.retrieve(limit=5)

print(results)

memory.export_to_markdown()

memory.close()
```

---

## Performance & Reliability

The Myelin Kernel is designed for **lightweight, persistent memory** in autonomous agents, prioritizing **data integrity** and **biologically inspired reinforcement learning** over raw throughput of traditional databases.

### System Health Status

**Status:** ✅ **Operational** - All core functionalities and integrity checks passed under stress.

### Benchmark Analysis (v0.1)

A multi-threaded stress test (10 concurrent store, 10 concurrent retrieve threads; 1,000 operations each) was conducted to assess performance and reliability.

**Key Findings:**

*   **Total Benchmark Time:** 21.72 seconds for 20,000 operations.
*   **Data Integrity:** Passed. Concurrent operations did not corrupt the database.
*   **SHA-256 Hashing Cost:** Negligible (approx. 0.004 ms per write for typical content), not a performance bottleneck.
*   **SQLite WAL Mode:** While WAL mode enhances read concurrency, the `MyelinKernel`'s global `threading.Lock` serializes all database operations, mitigating WAL's benefits for multi-threaded *write* contention within the application. The lock ensures safety but limits true parallel writes.

**Tail Latency Analysis (ms):**

| Operation | p50 (Median) | p95 | p99 |
| :-------- | :----------- | :-- | :-- |
| Store     | 0.072        | 20.573 | 37.222 |
| Retrieve  | 21.187       | 37.898 | 55.967 |

*   **Store Latency:** Most writes are extremely fast (median 0.072 ms), but tail latencies (p95, p99) indicate occasional spikes, likely due to lock contention, disk I/O, or handling of duplicate entries.
*   **Retrieve Latency:** Retrieval without a specific query is more computationally intensive, involving full table scans, scoring, and sorting. This results in higher latencies across the board (median 21.187 ms).

### Projected Behavior at Larger Scales

The current retrieve method performs scoring and sorting across all
non-honeypot entries when no query is provided. This results in
O(N log N) complexity.

For small knowledge bases (hundreds to a few thousand entries) this
remains very fast. For much larger datasets, agents should use the
`query` parameter so SQLite can leverage indexed filtering.

### Technical Comparison: Myelin Kernel vs. Alternatives

| Feature / DB Type | Myelin Kernel | Raw SQLite | Local Redis | Vector DB (Chroma/FAISS) |
| :---------------- | :------------------------------- | :--------- | :---------- | :----------------------- |
| **Primary Use Case** | Persistent Reinforcement Memory for Agents | General-purpose Relational DB | In-memory Key-Value Store, Caching | Semantic Search, Embeddings |
| **Data Integrity** | ✅ Strong (SHA-256 hashing, WAL mode) | ✅ Strong (ACID properties) | ⚠️ Weak (in-memory, optional persistence) | ✅ Strong (for vector data) |
| **Concurrency** | ✅ Thread-safe (internal lock, WAL) | ✅ Good (WAL mode) | ✅ Excellent (single-threaded event loop) | ✅ Good (designed for concurrent access) |
| **Reinforcement Learning** | ✅ Built-in (weight, decay, retrieval count) | ❌ Requires custom logic | ❌ Requires custom logic | ❌ Requires custom logic |
| **Decay Mechanism** | ✅ Built-in (gentle, configurable) | ❌ Requires custom logic | ❌ Requires custom logic | ❌ Requires custom logic |
| **Dependency Footprint** | ✅ Zero external dependencies | ✅ Zero external dependencies | ⚠️ External server/client | ⚠️ Significant (NumPy, SciPy, etc.) |
| **"Biological" Analogy** | ✅ Direct (Myelin, decay, reinforcement) | ❌ None | ❌ None | ❌ None |
| **Best For Autonomous Agents** | ✅ Superior (cognitive memory layer) | ❌ Too low-level for cognitive features | ❌ Lacks persistence, cognitive features | ❌ Focus on embeddings, not reinforcement |

### Why Myelin Kernel is Superior for Autonomous Agents

The Myelin Kernel, offers a distinct advantage for autonomous agents by providing a **dedicated cognitive memory layer**. Unlike general-purpose databases or vector stores, Myelin Kernel directly integrates:

1.  **Biologically Inspired Reinforcement:** Knowledge is not static. It strengthens with use and gently decays when unused, mimicking natural learning processes. This ensures that the most relevant and frequently accessed insights naturally surface, improving an agent's "cognitive focus."
2.  **Built-in Data Integrity:** Every piece of stored knowledge is hashed, allowing for robust integrity verification. This is crucial for agents that rely on the trustworthiness of their internal knowledge base.
3.  **Minimalist & Dependency-Free:** Its zero-dependency nature makes it incredibly lightweight and easy to embed directly into any agent architecture without introducing complex external systems.
4.  **Focus on Distilled Insights:** It encourages agents to store compressed, high-value insights rather than raw data, leading to more efficient memory utilization and improved reasoning.

While other databases excel at specific tasks (e.g., raw data storage, caching, semantic search), Myelin Kernel fills a unique niche by providing the core mechanisms for an agent's evolving, self-organizing knowledge base.

---

## Example Use Cases

Myelin Kernel works well as a memory layer for:

- autonomous agents
- AI copilots
- research assistants
- coding agents
- personal knowledge systems
- reflection-based learning loops
---

## Stress Testing

Community testing is encouraged.

Suggested benchmark scenarios:
- multi-thread store operations
- concurrent retrieve operations
- duplicate memory reinforcement
- decay behavior under large datasets
- database integrity checks

Example stress test scripts are included in /benchmarks.

---

## Token ROI Experiments

One goal of Myelin Kernel is improving token efficiency.

Testers are encouraged to measure:
- prompt size reduction
- reasoning improvement across sessions
- retrieval relevance
- reinforcement stability

Share benchmark results in Issues or Discussions.

---

## Transparency Export

Myelin can export memory summaries as Markdown:
```
memory/
├─ CLAUDE.md
├─ principles.md
└─ decisions.md
```

These files allow humans to inspect what the system remembers.

The SQLite database remains the authoritative source of truth.

---

## Roadmap

Current version: v0.1
Future exploration areas may include:
- concept graph linking
- semantic clustering
- adaptive decay models
- multi-agent memory sharing

---

## Contributing

Community feedback is welcome.
Areas where contributions are valuable:
- stress testing
- benchmarking
- retrieval scoring experiments
- agent integrations

---

## License
MIT License

---

## Author
Created by MortisVivere  
© 2026