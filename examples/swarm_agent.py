from myelin_kernel import MyelinKernel

"""
Purpose: Demonstrates multi-agent shared memory.
Multiple agents interact with the same Myelin database and reinforce useful insights collectively.
"""
import threading
import random
import time


AGENT_COUNT = 3
STEPS = 10


insights = [
    "Breaking tasks into steps improves reasoning.",
    "Shared memory allows agents to learn collectively.",
    "Frequent retrieval strengthens important knowledge.",
    "Reflection converts experience into reusable insight.",
]


def agent_worker(agent_id, memory):

    for _ in range(STEPS):

        insight = random.choice(insights)

        memory.reflect_and_store(insight)

        recalled = memory.retrieve(limit=3)

        print(f"\nAgent {agent_id} reflection:", insight)

        print(f"Agent {agent_id} recalls:")

        for r in recalled:
            print("-", r)

        time.sleep(random.uniform(0.1, 0.5))


def main():

    memory = MyelinKernel()

    threads = []

    for i in range(AGENT_COUNT):

        t = threading.Thread(target=agent_worker, args=(i + 1, memory))

        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("\nFinal shared memories:")

    for m in memory.retrieve(limit=10):
        print("-", m)

    memory.close()


if __name__ == "__main__":
    main()