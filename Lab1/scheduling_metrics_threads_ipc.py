import threading
import multiprocessing
from collections import deque


# ============================================================
# SCHEDULING FUNCTIONS
# ============================================================

def fcfs(processes):
    data = sorted(processes, key=lambda x: (x[1], x[0]))
    time = 0
    sequence = []

    for pid, at, bt, priority in data:

        if time < at:
            sequence.append(("IDLE", time, at))
            time = at

        start = time
        time += bt

        sequence.append((pid, start, time))

    return sequence


def sjf(processes):
    remaining = processes.copy()
    sequence = []
    time = 0

    while remaining:

        available = [
            p for p in remaining
            if p[1] <= time
        ]

        if not available:
            next_arrival = min(p[1] for p in remaining)

            sequence.append(
                ("IDLE", time, next_arrival)
            )

            time = next_arrival
            continue

        # Non-preemptive SJF
        # Tie: Burst Time -> Arrival Time -> PID
        selected = min(
            available,
            key=lambda x: (x[2], x[1], x[0])
        )

        pid, at, bt, priority = selected

        start = time
        time += bt

        sequence.append(
            (pid, start, time)
        )

        remaining.remove(selected)

    return sequence


def priority_scheduling(processes):
    remaining = processes.copy()
    sequence = []
    time = 0

    # Lower priority number = higher priority

    while remaining:

        available = [
            p for p in remaining
            if p[1] <= time
        ]

        if not available:
            next_arrival = min(p[1] for p in remaining)

            sequence.append(
                ("IDLE", time, next_arrival)
            )

            time = next_arrival
            continue

        # Priority -> Arrival Time -> PID
        selected = min(
            available,
            key=lambda x: (x[3], x[1], x[0])
        )

        pid, at, bt, priority = selected

        start = time
        time += bt

        sequence.append(
            (pid, start, time)
        )

        remaining.remove(selected)

    return sequence


def round_robin(processes, quantum):
    remaining_bt = {
        p[0]: p[2]
        for p in processes
    }

    arrival = {
        p[0]: p[1]
        for p in processes
    }

    original_order = {
        p[0]: i
        for i, p in enumerate(processes)
    }

    sorted_processes = sorted(
        processes,
        key=lambda x: (x[1], original_order[x[0]])
    )

    ready_queue = deque()
    sequence = []

    time = 0
    next_process = 0
    completed = 0
    n = len(processes)

    while completed < n:

        # Add newly arrived processes
        while (
            next_process < n
            and sorted_processes[next_process][1] <= time
        ):
            ready_queue.append(
                sorted_processes[next_process][0]
            )

            next_process += 1

        # CPU idle
        if not ready_queue:

            next_arrival = sorted_processes[next_process][1]

            sequence.append(
                ("IDLE", time, next_arrival)
            )

            time = next_arrival
            continue

        # FIFO
        pid = ready_queue.popleft()

        start = time

        execution = min(
            quantum,
            remaining_bt[pid]
        )

        time += execution

        remaining_bt[pid] -= execution

        # Record every RR execution slice
        sequence.append(
            (pid, start, time)
        )

        # Add newly arrived processes
        while (
            next_process < n
            and sorted_processes[next_process][1] <= time
        ):
            ready_queue.append(
                sorted_processes[next_process][0]
            )

            next_process += 1

        # Put unfinished process back
        if remaining_bt[pid] > 0:
            ready_queue.append(pid)
        else:
            completed += 1

    return sequence


# ============================================================
# CALCULATE SCHEDULING METRICS
# ============================================================

def calculate_metrics(processes, sequence):

    process_info = {
        p[0]: p
        for p in processes
    }

    completion_time = {}
    first_start = {}

    for pid, start, end in sequence:

        if pid == "IDLE":
            continue

        # First time process gets CPU
        if pid not in first_start:
            first_start[pid] = start

        # Last execution end = Completion Time
        completion_time[pid] = end

    metrics = {}

    total_tat = 0
    total_wt = 0
    total_rt = 0

    for pid, at, bt, priority in processes:

        ct = completion_time[pid]

        # Turnaround Time
        tat = ct - at

        # Waiting Time
        wt = tat - bt

        # Response Time
        rt = first_start[pid] - at

        metrics[pid] = (ct, tat, wt, rt)

        total_tat += tat
        total_wt += wt
        total_rt += rt

    n = len(processes)

    averages = (
        total_tat / n,
        total_wt / n,
        total_rt / n
    )

    return metrics, averages


# ============================================================
# DISPLAY GANTT CHART
# ============================================================

def display_gantt(sequence):

    print("\nGANTT CHART")
    print("-" * 65)

    # Process blocks
    print("|", end="")

    for pid, start, end in sequence:
        print(f" {pid:^7} |", end="")

    print()

    # Exact time boundaries
    print(sequence[0][1], end="")

    for pid, start, end in sequence:
        print(f"{end:10}", end="")

    print()


# ============================================================
# DISPLAY METRICS
# ============================================================

def display_metrics(processes, sequence):

    metrics, averages = calculate_metrics(
        processes,
        sequence
    )

    print("\nSCHEDULING METRICS")
    print("-" * 70)

    print(
        f"{'PID':<8}"
        f"{'AT':<8}"
        f"{'BT':<8}"
        f"{'CT':<8}"
        f"{'TAT':<8}"
        f"{'WT':<8}"
        f"{'RT':<8}"
    )

    print("-" * 70)

    for pid, at, bt, priority in processes:

        ct, tat, wt, rt = metrics[pid]

        print(
            f"{pid:<8}"
            f"{at:<8}"
            f"{bt:<8}"
            f"{ct:<8}"
            f"{tat:<8}"
            f"{wt:<8}"
            f"{rt:<8}"
        )

    avg_tat, avg_wt, avg_rt = averages

    print("-" * 70)

    print(
        f"Average Turnaround Time : {avg_tat:.2f}"
    )

    print(
        f"Average Waiting Time    : {avg_wt:.2f}"
    )

    print(
        f"Average Response Time   : {avg_rt:.2f}"
    )


# ============================================================
# THREADING
# ============================================================

def thread_work(thread_number):

    print(
        f"Thread {thread_number} started"
        f" | Thread ID: {threading.get_ident()}"
    )

    # Simulated work
    total = 0

    for i in range(1, 100001):
        total += i

    print(
        f"Thread {thread_number} completed work."
        f" Result = {total}"
    )


def demonstrate_threads():

    print("\n")
    print("=" * 65)
    print("PYTHON THREADING")
    print("=" * 65)

    thread1 = threading.Thread(
        target=thread_work,
        args=(1,)
    )

    thread2 = threading.Thread(
        target=thread_work,
        args=(2,)
    )

    # Start threads
    thread1.start()
    thread2.start()

    # Wait for threads
    thread1.join()
    thread2.join()

    print("\nBoth threads completed successfully.")


# ============================================================
# IPC USING MULTIPROCESSING PIPE
# ============================================================

def sender_process(connection):

    message = "Hello from Sender Process"

    print(
        "\nSender Process ID:",
        multiprocessing.current_process().pid
    )

    print("Transmitted Message:", message)

    connection.send(message)

    connection.close()


def receiver_process(connection):

    message = connection.recv()

    print(
        "\nReceiver Process ID:",
        multiprocessing.current_process().pid
    )

    print("Received Message:", message)

    connection.close()


def demonstrate_ipc():

    print("\n")
    print("=" * 65)
    print("INTER-PROCESS COMMUNICATION USING PIPE")
    print("=" * 65)

    # Create pipe
    parent_connection, child_connection = multiprocessing.Pipe()

    sender = multiprocessing.Process(
        target=sender_process,
        args=(child_connection,)
    )

    receiver = multiprocessing.Process(
        target=receiver_process,
        args=(parent_connection,)
    )

    sender.start()
    receiver.start()

    sender.join()
    receiver.join()

    print("\nIPC communication completed.")
    print("IPC Method Used: multiprocessing.Pipe")
    print("Sender Role: Sends the message")
    print("Receiver Role: Receives the message")


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 65)
    print("   SCHEDULING METRICS, THREADS AND IPC")
    print("=" * 65)

    try:

        n = int(
            input("\nEnter number of processes: ")
        )

        if n <= 0:
            print("Error: Number of processes must be greater than 0.")
            exit()

        processes = []

        print("\nEnter process details:")

        for i in range(n):

            print(f"\nProcess {i + 1}")

            pid = input("Process ID: ").strip()

            at = int(
                input("Arrival Time: ")
            )

            bt = int(
                input("Burst Time: ")
            )

            priority = int(
                input("Priority: ")
            )

            if not pid:
                print("Error: Process ID cannot be empty.")
                exit()

            if at < 0:
                print("Error: Arrival Time cannot be negative.")
                exit()

            if bt <= 0:
                print("Error: Burst Time must be greater than 0.")
                exit()

            if priority <= 0:
                print("Error: Priority must be greater than 0.")
                exit()

            processes.append(
                (pid, at, bt, priority)
            )

        quantum = int(
            input("\nEnter Round Robin Time Quantum: ")
        )

        if quantum <= 0:
            print("Error: Time Quantum must be greater than 0.")
            exit()

    except ValueError:

        print("Error: Enter valid numeric values.")
        exit()

    # ========================================================
    # ORIGINAL DATA
    # ========================================================

    print("\n")
    print("=" * 65)
    print("ORIGINAL PROCESS DATA")
    print("=" * 65)

    print(
        f"{'PID':<8}"
        f"{'Arrival':<10}"
        f"{'Burst':<8}"
        f"{'Priority':<10}"
    )

    for pid, at, bt, priority in processes:

        print(
            f"{pid:<8}"
            f"{at:<10}"
            f"{bt:<8}"
            f"{priority:<10}"
        )

    # ========================================================
    # FCFS
    # ========================================================

    print("\n")
    print("=" * 65)
    print("FCFS SCHEDULING")
    print("=" * 65)

    fcfs_result = fcfs(processes)

    display_gantt(fcfs_result)

    display_metrics(
        processes,
        fcfs_result
    )

    # ========================================================
    # SJF
    # ========================================================

    print("\n")
    print("=" * 65)
    print("NON-PREEMPTIVE SJF")
    print("=" * 65)

    sjf_result = sjf(processes)

    display_gantt(sjf_result)

    display_metrics(
        processes,
        sjf_result
    )

    # ========================================================
    # PRIORITY
    # ========================================================

    print("\n")
    print("=" * 65)
    print("NON-PREEMPTIVE PRIORITY")
    print("=" * 65)

    print("Priority Convention:")
    print("Lower number = Higher priority")

    priority_result = priority_scheduling(processes)

    display_gantt(priority_result)

    display_metrics(
        processes,
        priority_result
    )

    # ========================================================
    # ROUND ROBIN
    # ========================================================

    print("\n")
    print("=" * 65)
    print("ROUND ROBIN")
    print("=" * 65)

    print("Time Quantum:", quantum)

    rr_result = round_robin(
        processes,
        quantum
    )

    display_gantt(rr_result)

    print("\nRound Robin Execution Slices:")

    for pid, start, end in rr_result:

        if pid == "IDLE":
            print(
                f"CPU IDLE : {start} -> {end}"
            )
        else:
            print(
                f"{pid} : {start} -> {end}"
            )

    display_metrics(
        processes,
        rr_result
    )

    # ========================================================
    # THREADS
    # ========================================================

    demonstrate_threads()

    # ========================================================
    # IPC
    # ========================================================

    demonstrate_ipc()

    # ========================================================
    # FINAL EXPLANATION
    # ========================================================

    print("\n")
    print("=" * 65)
    print("EXPLANATION")
    print("=" * 65)

    print("""
1. Scheduling Results:
   FCFS executes processes according to arrival order.
   SJF selects the shortest available process.
   Priority selects the process with the highest priority.
   Round Robin gives each process a fixed time quantum.

2. Scheduling Metrics:
   Completion Time (CT) = Time when process finishes.
   Turnaround Time (TAT) = CT - Arrival Time.
   Waiting Time (WT) = TAT - Burst Time.
   Response Time (RT) = First CPU Start - Arrival Time.

3. Benefits of Threads:
   Threads allow multiple tasks to execute concurrently.
   They are lightweight compared with separate processes
   and can share memory within the same process.

4. IPC Method:
   multiprocessing.Pipe is used for communication between
   two processes. One process acts as the sender and the
   other acts as the receiver.

5. Limitation of Pipe:
   A Pipe is mainly suitable for communication between a
   small number of related processes. It is not ideal for
   large-scale communication between many independent
   processes.
""")

    print("=" * 65)
    print("PROGRAM COMPLETED SUCCESSFULLY")
    print("=" * 65)