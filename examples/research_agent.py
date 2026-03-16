from myelin_kernel import MyelinKernel

"""
Purpose: Simulates an agent performing research and storing discovered knowledge.
"""


def research_topic(topic):

    findings = [
        "SQLite supports WAL mode for concurrent reads.",
        "Thread locks are required when sharing SQLite connections.",
        "Logarithmic reinforcement prevents runaway scoring."
    ]

    return findings


def main():

    memory = MyelinKernel()

    topic = "SQLite concurrency"

    print("\nResearching:", topic)

    results = research_topic(topic)

    for fact in results:

        memory.store(
            "knowledge",
            fact,
            weight=0.7
        )

    print("\nStored findings.")

    print("\nTop retrieved knowledge:")

    for m in memory.retrieve(limit=5):
        print("-", m)

    memory.close()


if __name__ == "__main__":
    main()