import threading
import time


# 1. Create a single-threaded baseline workload
def single_threaded_baseline_workload():
    print("\n--- Single-Threaded Workload ---")
    
    start_time = time.time()

    total = 0
    for i in range(1, 10000001):
        total += i

    end_time = time.time()
    execution_time = end_time - start_time

    print("Single-threaded result:", total)
    print("Single-threaded execution time:", execution_time, "seconds")

    return execution_time


# 2. Divide the workload into independent tasks
def divide_workload_into_independent_tasks():
    tasks = [
        (1, 2500000),
        (2500001, 5000000),
        (5000001, 7500000),
        (7500001, 10000000)
    ]

    return tasks


# Worker function for each independent task
def worker_thread(start, end):
    thread_id = threading.get_ident()

    print(f"Thread {thread_id} started: {start} to {end}")

    total = 0
    for i in range(start, end + 1):
        total += i

    print(f"Thread {thread_id} completed: {start} to {end}")

    return total


# 3. Create multiple worker threads using Python
def create_multiple_worker_threads(tasks):
    threads = []

    for start, end in tasks:
        thread = threading.Thread(
            target=worker_thread,
            args=(start, end)
        )
        threads.append(thread)

    return threads


# 4. Display thread identifiers and execution progress
def display_thread_identifiers_and_execution_progress(threads):
    print("\n--- Starting Worker Threads ---")

    for thread in threads:
        thread.start()

    print("All worker threads have been started.")


# 5. Wait for all worker threads to complete
def wait_for_all_worker_threads_to_complete(threads):
    for thread in threads:
        thread.join()

    print("All worker threads have completed.")


# 6. Measure single-threaded and multithreaded execution time
def measure_single_threaded_and_multithreaded_execution_time():
    
    # Single-threaded execution
    single_time = single_threaded_baseline_workload()

    # Divide workload
    tasks = divide_workload_into_independent_tasks()

    # Create threads
    threads = create_multiple_worker_threads(tasks)

    # Multithreaded execution
    print("\n--- Multithreaded Workload ---")

    start_time = time.time()

    display_thread_identifiers_and_execution_progress(threads)
    wait_for_all_worker_threads_to_complete(threads)

    end_time = time.time()
    multi_time = end_time - start_time

    print("Multithreaded execution time:", multi_time, "seconds")

    return single_time, multi_time


# 7. Compare both versions using the same workload
def compare_both_versions_using_same_workload(single_time, multi_time):
    print("\n--- Execution Time Comparison ---")
    print("Single-threaded time:", single_time, "seconds")
    print("Multithreaded time:", multi_time, "seconds")

    if multi_time < single_time:
        print("Multithreaded execution was faster.")
    elif multi_time > single_time:
        print("Single-threaded execution was faster.")
    else:
        print("Both execution times were approximately equal.")


# 8. Explain user-level threads, kernel-level threads and common multithreading models
def explain_user_level_threads_kernel_level_threads_and_common_multithreading_models():
    print("\n--- Thread Models ---")

    print("""
User-Level Threads:
User-level threads are managed by a user-level thread library rather
than directly by the operating system kernel. They are fast to create
and manage, but a blocking system call can block the entire process.

Kernel-Level Threads:
Kernel-level threads are managed directly by the operating system.
The kernel schedules these threads independently and can execute
multiple threads in parallel on multiple CPU cores.

Common Multithreading Models:
1. Many-to-One:
   Many user threads are mapped to one kernel thread.

2. One-to-One:
   Each user thread is mapped to one kernel thread.

3. Many-to-Many:
   Many user threads are mapped to multiple kernel threads.
""")


# 9. Discuss responsiveness, resource sharing, concurrency, parallelism,
#    race conditions, deadlocks and overhead
def discuss_multithreading_concepts():
    print("\n--- Multithreading Concepts ---")

    print("""
Responsiveness:
Multithreading allows an application to remain responsive while
another thread performs a time-consuming task.

Resource Sharing:
Threads belonging to the same process share resources such as
memory, files and other process resources.

Concurrency:
Concurrency means multiple tasks make progress during overlapping
periods of time.

Parallelism:
Parallelism means multiple tasks actually execute at the same time,
usually on multiple CPU cores.

Race Condition:
A race condition occurs when multiple threads access shared data
and the final result depends on the order of execution.

Deadlock:
A deadlock occurs when two or more threads wait indefinitely for
resources held by each other.

Overhead:
Creating, scheduling and switching between threads requires
system resources and CPU time.
""")


# Main program
def main():
    print("===== THREAD CREATION, MODELS AND BENEFITS =====")

    # Requirements 1–7
    single_time, multi_time = (
        measure_single_threaded_and_multithreaded_execution_time()
    )

    compare_both_versions_using_same_workload(
        single_time,
        multi_time
    )

    # Requirement 8
    explain_user_level_threads_kernel_level_threads_and_common_multithreading_models()

    # Requirement 9
    discuss_multithreading_concepts()


if __name__ == "__main__":
    main()