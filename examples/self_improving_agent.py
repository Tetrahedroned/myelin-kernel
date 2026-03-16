import random
import time
from myelin_kernel import MyelinKernel

"""
Purpose: Exercises reinforcement behavior in the kernel.
The agent repeatedly:
- generates insights
- stores them
- retrieves existing knowledge
"""


def main():
    # Using a dedicated demo DB
    memory = MyelinKernel("agent_demo.db")

    insights = [
        "Breaking tasks into steps improves reasoning.",
        "Retrieval of prior knowledge improves decision making.",
        "Reflection compresses experience into reusable insight.",
        "Frequent retrieval reinforces useful knowledge.",
    ]

    print("\n[STARTING SELF-IMPROVING LOOP]")

    for i in range(10):
        insight = random.choice(insights)
        print(f"\nStep {i + 1} | Agent Reflection: {insight}")

        # Store with high initial weight to simulate 'active focus'
        memory.reflect_and_store(insight)

        recalled = memory.retrieve(limit=3)
        print("Current Cognitive Focus:")
        for r in recalled:
            print(f" -> {r}")

        time.sleep(0.1)

    print("\n[FINAL TOP MEMORIES (Reinforced & Ranked)]")
    for m in memory.retrieve(limit=5):
        print(f" * {m}")

    memory.close()


if __name__ == "__main__":
    main()