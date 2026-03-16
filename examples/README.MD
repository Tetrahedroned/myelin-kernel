# Myelin Kernel Example Agents

This directory contains small example agents that demonstrate how the Myelin Kernel can be used inside different reasoning and learning loops.

These examples are intentionally simple. Their purpose is to show how persistent memory can be integrated into agent behavior.

Each example highlights a different pattern of interaction with memory.

The general learning cycle looks like this:

experience → reflection → storage → retrieval → improved reasoning

Instead of saving entire conversations, agents compress useful insights into reusable memories.

---

# Example Agents

## simple_agent.py

Purpose

The simplest possible integration with Myelin Kernel.

This example demonstrates:

- storing knowledge
- retrieving memories
- exporting memory

Usage

python examples/simple_agent.py

What it demonstrates

The basic lifecycle of the memory system:

store → retrieve → export

This file acts as the **Hello World example** for Myelin.

---

## reflective_agent.py

Purpose

Shows how an agent can convert experience into distilled insights before storing them.

Example memory

Breaking complex problems into smaller steps improves reasoning.

Usage

python examples/reflective_agent.py

Why this matters

Reflected insights produce higher-quality memories that are easier to retrieve and reuse.

---

## research_agent.py

Purpose

Simulates an agent performing research and storing discovered knowledge.

Example stored knowledge

- SQLite supports WAL mode for concurrent reads
- Thread locks are needed when sharing SQLite connections

Usage

python examples/research_agent.py

Why this matters

Agents can build persistent knowledge bases across sessions.

---

## code_learning_agent.py

Purpose

Demonstrates how coding agents can remember solutions to engineering problems.

Example memory

Use `threading.Lock` when sharing SQLite connections.

Usage

python examples/code_learning_agent.py

Why this matters

Coding agents often rediscover the same fixes repeatedly. Persistent memory prevents that.

---

## self_improving_agent.py

Purpose

Exercises reinforcement behavior in the kernel.

The agent repeatedly:

- generates insights
- stores them
- retrieves existing knowledge

Usage

python examples/self_improving_agent.py

This example stresses:

- memory reinforcement
- retrieval ranking
- long-running loops

You can increase loop counts to stress the system further.

Why this matters

This example highlights how the kernel's reinforcement and decay mechanisms allow agents to prioritize and retain the most useful knowledge over long operational periods, leading to continuous self-improvement.

---

## swarm_agent.py

Purpose

Demonstrates **multi-agent shared memory**.

Multiple agents interact with the same Myelin database and reinforce useful insights collectively.

Each agent:

1. generates an insight
2. stores it
3. retrieves shared memories
4. reinforces important knowledge

Usage

python examples/swarm_agent.py

Why this matters

This example shows how Myelin can function as a **shared knowledge substrate for multiple agents**.

Instead of learning in isolation, agents contribute to a collective memory pool.

---

# Suggested Experiments

Developers are encouraged to modify the examples and observe how the kernel behaves.

Ideas to try:

- increase loop counts in the self-improving agent
- run multiple swarm agents simultaneously
- introduce duplicate insights and observe reinforcement behavior
- simulate long-running autonomous agents
- measure prompt token reduction when using retrieved memories

---

# Why These Examples Exist

These examples provide a **memory experimentation sandbox**.

They allow developers to explore how persistent reinforcement-based memory can improve autonomous agent systems while keeping the implementation easy to understand.
