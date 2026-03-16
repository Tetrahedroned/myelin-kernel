from myelin_kernel import MyelinKernel

"""
Purpose: Demonstrates how coding agents can remember solutions to engineering problems.
"""


def learn_from_bug(memory):

    bug_solution = "Use threading.Lock when sharing SQLite connections."

    print("\nBug fixed.")

    memory.reflect_and_store(bug_solution)


def main():

    memory = MyelinKernel()

    learn_from_bug(memory)

    print("\nKnown solutions:")

    for m in memory.retrieve(limit=5):
        print("-", m)

    memory.close()


if __name__ == "__main__":
    main()