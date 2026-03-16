from myelin_kernel import MyelinKernel

"""
Purpose: The simplest possible integration with Myelin Kernel.
This example demonstrates:
- storing knowledge
- retrieving memories
- exporting memory
"""

def main():

    memory = MyelinKernel()

    print("\nAgent starting...\n")

    memory.reflect_and_store(
        "Reflection improves future reasoning."
    )

    memory.store(
        "knowledge",
        "SQLite provides lightweight persistent storage for agent memory.",
        weight=0.7
    )

    print("Top memories:")

    results = memory.retrieve(limit=5)

    for r in results:
        print("-", r)

    print("\nExporting memory snapshot...")

    memory.export_to_markdown()

    memory.close()

    print("\nAgent finished.\n")


if __name__ == "__main__":
    main()