from collections import deque


# -------------------------------------------------
# NON-PREEMPTIVE PRIORITY SCHEDULING
# -------------------------------------------------
# Priority Convention:
# LOWER priority number = HIGHER priority
#
# Example:
# Priority 1 > Priority 2 > Priority 3
# -------------------------------------------------

def priority_scheduling(processes):
    remaining = processes.copy()
    time = 0
    sequence = []

    while remaining:

        # Find processes that have arrived
        available = [
            p for p in remaining
            if p[1] <= time
        ]

        # CPU is idle if no process is available
        if not available:
            next_arrival = min(p[1] for p in remaining)

            sequence.append(
                ("IDLE", time, next_arrival)
            )

            time = next_arrival
            continue

        # Select highest priority process
        # Tie-breaking:
        # 1. Priority
        # 2. Arrival Time
        # 3. Process ID
        selected = min(
            available,
            key=lambda x: (x[3], x[1], x[0])
        )

        pid, at, bt, priority = selected

        start = time
        end = time + bt

        sequence.append(
            (pid, start, end)
        )

        time = end
        remaining.remove(selected)

    return sequence


# -------------------------------------------------
# ROUND ROBIN SCHEDULING
# -------------------------------------------------

def round_robin(processes, quantum):

    # Store remaining burst time
    remaining_bt = {
        p[0]: p[2]
        for p in processes
    }

    # Store arrival times
    arrival_time = {
        p[0]: p[1]
        for p in processes
    }

    # Keep original process order
    process_order = {
        p[0]: i
        for i, p in enumerate(processes)
    }

    ready_queue = deque()
    sequence = []

    time = 0
    completed = 0
    n = len(processes)

    # Sort according to arrival time
    sorted_processes = sorted(
        processes,
        key=lambda x: (x[1], process_order[x[0]])
    )

    next_process = 0

    while completed < n:

        # Add newly arrived processes
        while (
            next_process < n
            and sorted_processes[next_process][1] <= time
        ):
            pid = sorted_processes[next_process][0]
            ready_queue.append(pid)
            next_process += 1

        # If ready queue is empty
        if not ready_queue:

            next_arrival = sorted_processes[next_process][1]

            sequence.append(
                ("IDLE", time, next_arrival)
            )

            time = next_arrival
            continue

        # FIFO ready queue
        pid = ready_queue.popleft()

        start = time

        # Execute for one time quantum
        execution_time = min(
            quantum,
            remaining_bt[pid]
        )

        time += execution_time
        remaining_bt[pid] -= execution_time

        # Record every execution slice
        sequence.append(
            (pid, start, time)
        )

        # Add processes that arrived during execution
        while (
            next_process < n
            and sorted_processes[next_process][1] <= time
        ):
            new_pid = sorted_processes[next_process][0]
            ready_queue.append(new_pid)
            next_process += 1

        # If process is not finished, put it back
        if remaining_bt[pid] > 0:
            ready_queue.append(pid)
        else:
            completed += 1

    return sequence


# -------------------------------------------------
# DISPLAY RESULTS
# -------------------------------------------------

def display(title, sequence):

    print("\n" + "=" * 55)
    print(title)
    print("=" * 55)

    print("\nExecution Sequence:")

    for pid, start, end in sequence:

        if pid == "IDLE":
            print(f"CPU IDLE : {start} -> {end}")
        else:
            print(f"{pid} : {start} -> {end}")

    print("\nExecution Intervals:")

    for pid, start, end in sequence:
        print(
            f"{pid:6} | Start = {start:3} | End = {end:3}"
        )


# -------------------------------------------------
# INPUT VALIDATION
# -------------------------------------------------

def validate_processes(processes):

    if not processes:
        print("Error: No processes entered.")
        return False

    ids = set()

    for pid, at, bt, priority in processes:

        if pid in ids:
            print(f"Error: Duplicate Process ID: {pid}")
            return False

        ids.add(pid)

        if at < 0:
            print(
                f"Error: Arrival Time of {pid} "
                "cannot be negative."
            )
            return False

        if bt <= 0:
            print(
                f"Error: Burst Time of {pid} "
                "must be greater than 0."
            )
            return False

        if priority <= 0:
            print(
                f"Error: Priority of {pid} "
                "must be greater than 0."
            )
            return False

    return True


# -------------------------------------------------
# MAIN PROGRAM
# -------------------------------------------------

print("=" * 55)
print("       PRIORITY AND ROUND ROBIN SCHEDULING")
print("=" * 55)

# Priority convention
print("\nPriority Convention:")
print("LOWER NUMBER = HIGHER PRIORITY")
print("Example: Priority 1 > Priority 2 > Priority 3")

try:

    n = int(input("\nEnter number of processes: "))

    if n <= 0:
        print("Error: Number of processes must be greater than 0.")
        exit()

    processes = []

    print("\nEnter Process Details:")

    for i in range(n):

        print(f"\nProcess {i + 1}")

        pid = input("Process ID: ").strip()

        if not pid:
            print("Error: Process ID cannot be empty.")
            exit()

        at = int(input("Arrival Time: "))
        bt = int(input("Burst Time: "))
        priority = int(input("Priority: "))

        processes.append(
            (pid, at, bt, priority)
        )

    # Round Robin Quantum
    quantum = int(
        input("\nEnter Round Robin Time Quantum: ")
    )

    if quantum <= 0:
        print("Error: Time Quantum must be greater than 0.")
        exit()

except ValueError:

    print("Error: Please enter valid numeric values.")
    exit()


# Validate all input
if validate_processes(processes):

    print("\nInput validation successful.")

    # -------------------------------------------------
    # ORIGINAL DATA
    # -------------------------------------------------

    print("\n" + "=" * 55)
    print("ORIGINAL PROCESS DATA")
    print("=" * 55)

    print("\nPID\tArrival\tBurst\tPriority")

    for pid, at, bt, priority in processes:

        print(
            f"{pid}\t{at}\t{bt}\t{priority}"
        )

    print("\nSelected Priority Convention:")
    print("Lower priority number = Higher priority")

    print("Round Robin Time Quantum:", quantum)

    # -------------------------------------------------
    # RUN BOTH ALGORITHMS
    # -------------------------------------------------

    priority_result = priority_scheduling(processes)

    rr_result = round_robin(
        processes,
        quantum
    )

    # -------------------------------------------------
    # DISPLAY RESULTS SEPARATELY
    # -------------------------------------------------

    display(
        "NON-PREEMPTIVE PRIORITY SCHEDULING",
        priority_result
    )

    display(
        "ROUND ROBIN SCHEDULING",
        rr_result
    )

    print("\n" + "=" * 55)
    print("Both algorithms completed successfully.")
    print("=" * 55)