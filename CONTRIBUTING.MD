# Contributing to Myelin Kernel

Thanks for taking a look at Myelin Kernel.

I built this project as an experiment in lightweight reinforcement-based memory for AI systems. I'm sharing it so others can explore it, test it, and push its limits.

If you find it useful or interesting, contributions and experiments are welcome.

---

# Ways You Can Contribute

## Stress Testing

One of the most valuable contributions is simply pushing the system.

Ideas to try:

- high thread counts
- large memory databases
- heavy duplicate knowledge
- simultaneous store and retrieval operations
- long running reinforcement loops

If something breaks, open an Issue and include reproduction steps.

---

## Benchmarking

Performance data is extremely useful.

Examples:

- retrieval latency
- database growth over time
- reinforcement behavior stability
- token savings when used with LLM prompts

If you publish benchmarks, please include:

- system specs
- Python version
- database size
- thread count
- benchmark script

---

## Agent Experiments

The `examples` folder is intentionally simple.

It's meant as a sandbox for experimenting with how agents might use persistent memory.

Interesting experiments might include:

- multi-agent collaboration
- knowledge consolidation
- memory pruning strategies
- retrieval scoring improvements
- long-term autonomous agents

Feel free to share experiments as pull requests or discussions.

---

## Code Improvements

Areas where improvements might be useful:

- concurrency handling
- scoring models
- decay mechanisms
- export formats
- integration helpers

Please keep changes focused and avoid unnecessary dependencies.

---

# Pull Request Guidelines

If you submit a pull request:

1. Keep changes small and focused
2. Explain what the change does
3. Add tests when possible
4. Avoid introducing heavy dependencies

The goal is to keep Myelin Kernel lightweight and easy to understand.

---

# Reporting Issues

If you run into a bug, please include:

- reproduction steps
- operating system
- Python version
- database size
- thread configuration

This makes it much easier to track down problems.

---

# Project Philosophy

Myelin Kernel is intentionally small.

It is not meant to be a full agent framework.  
It is a **memory layer** that can sit underneath agents.

My goal is to keep it:

- lightweight
- dependency free
- easy to integrate
- easy to experiment with

---

Thanks for taking the time to explore it.