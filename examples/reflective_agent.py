from myelin_kernel import MyelinKernel

"""
Purpose: Shows how an agent can convert experience into distilled insights before storing them.
"""


def run_task(memory):

    task = "Solve a complex problem step by step."

    print("\nTask:", task)

    result = "Breaking problems into smaller steps improves reasoning."

    print("Result:", result)

    memory.reflect_and_store(result)


def main():

    memory = MyelinKernel()

    run_task(memory)

    print("\nTop memories:")

    for m in memory.retrieve(limit=5):
        print("-", m)

    memory.close()


if __name__ == "__main__":
    main()