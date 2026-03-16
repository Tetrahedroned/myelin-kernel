import threading
import random
import os
import time
import collections
import statistics
from myelin_kernel import MyelinKernel

# Shared data structures for latency collection
store_latencies = collections.deque()
retrieve_latencies = collections.deque()
latencies_lock = threading.Lock()


import argparse


def store_worker(memory, store_ops_per_thread):

    for _ in range(store_ops_per_thread):
        start_op = time.perf_counter()
        memory.store(
            "knowledge",
            f"fact_{random.randint(1,200)}",
            weight=0.5
        )
        end_op = time.perf_counter()
        with latencies_lock:
            store_latencies.append(end_op - start_op)


def retrieve_worker(memory, retrieve_ops_per_thread):

    for _ in range(retrieve_ops_per_thread):
        start_op = time.perf_counter()
        memory.retrieve(limit=5)
        end_op = time.perf_counter()
        with latencies_lock:
            retrieve_latencies.append(end_op - start_op)


def main():
    parser = argparse.ArgumentParser(description="Myelin Kernel Stress Test Benchmark.")
    parser.add_argument("--threads", type=int, default=10,
                        help="Number of concurrent threads for store and retrieve operations.")
    parser.add_argument("--store_ops", type=int, default=1000,
                        help="Number of store operations per thread.")
    parser.add_argument("--retrieve_ops", type=int, default=1000,
                        help="Number of retrieve operations per thread.")
    args = parser.parse_args()

    num_threads = args.threads
    store_ops_per_thread = args.store_ops
    retrieve_ops_per_thread = args.retrieve_ops

    memory = MyelinKernel()

    threads = []

    start_time = time.perf_counter()

    for _ in range(num_threads):
        t = threading.Thread(target=store_worker, args=(memory, store_ops_per_thread))
        threads.append(t)

    for _ in range(num_threads):
        t = threading.Thread(target=retrieve_worker, args=(memory, retrieve_ops_per_thread))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(f"\nTotal benchmark time: {total_time:.2f} seconds")
    print(f"Total Store Operations: {num_threads * store_ops_per_thread}")
    print(f"Total Retrieve Operations: {num_threads * retrieve_ops_per_thread}")


    # Calculate and print latencies
    if store_latencies:
        store_latencies_ms = [l * 1000 for l in store_latencies]
        print("\nStore Operation Latencies (ms):")
        print(f"  p50: {statistics.median(store_latencies_ms):.3f}")
        print(f"  p95: {statistics.quantiles(store_latencies_ms, n=100)[94]:.3f}")
        print(f"  p99: {statistics.quantiles(store_latencies_ms, n=100)[98]:.3f}")
    else:
        print("\nNo store operations recorded.")

    if retrieve_latencies:
        retrieve_latencies_ms = [l * 1000 for l in retrieve_latencies]
        print("\nRetrieve Operation Latencies (ms):")
        print(f"  p50: {statistics.median(retrieve_latencies_ms):.3f}")
        print(f"  p95: {statistics.quantiles(retrieve_latencies_ms, n=100)[94]:.3f}")
        print(f"  p99: {statistics.quantiles(retrieve_latencies_ms, n=100)[98]:.3f}")
    else:
        print("\nNo retrieve operations recorded.")

    print("\nIntegrity check:")
    print(memory.verify_integrity())

    os.remove(memory.db_path) # Clean up the database file
    memory.close()


if __name__ == "__main__":
    main()