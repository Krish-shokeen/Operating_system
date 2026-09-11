# FCFS and Non-Preemptive SJF Scheduling

def validate_processes(processes):
    """Validate all process input values."""
    if not processes:
        print("Error: No processes entered.")
        return False

    ids = set()

    for pid, at, bt in processes:

        if pid in ids:
            print(f"Error: Duplicate Process ID {pid}")
            return False

        ids.add(pid)

        if at < 0:
            print(f"Error: Arrival Time of {pid} cannot be negative.")
            return False

        if bt <= 0:
            print(f"Error: Burst Time of {pid} must be greater than 0.")
            return False

    return True


# ---------------- FCFS ----------------

def fcfs(processes):
    # Preserve original data
    data = processes.copy()

    # FCFS: sort according to arrival time
    data.sort(key=lambda x: x[1])

    time = 0
    sequence = []

    for pid, at, bt in data:

        # CPU idle
        if time < at:
            sequence.append(("IDLE", time, at))
            time = at

        start = time
        end = time + bt

        sequence.append((pid, start, end))

        time = end

    return sequence


# ---------------- SJF ----------------

def sjf(processes):
    # Preserve original data
    data = processes.copy()

    remaining = data.copy()

    time = 0
    sequence = []

    while remaining:

        # Select processes that have arrived
        available = [
            p for p in remaining
            if p[1] <= time
        ]

        # If no process has arrived
        if not available:

            next_arrival = min(p[1] for p in remaining)

            sequence.append(("IDLE", time, next_arrival))

            time = next_arrival
            continue

        # Non-preemptive SJF
        # Tie-breaking:
        # 1. Shortest Burst Time
        # 2. Earlier Arrival Time
        # 3. Process ID
        selected = min(
            available,
            key=lambda x: (x[2], x[1], x[0])
        )

        pid, at, bt = selected

        start = time
        end = time + bt

        sequence.append((pid, start, end))

        time = end

        remaining.remove(selected)

    return sequence


# ---------------- Display ----------------

def display(title, sequence):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)

    print("\nExecution Sequence:")

    for pid, start, end in sequence:
        if pid == "IDLE":
            print(f"CPU IDLE : {start} -> {end}")
        else:
            print(f"{pid} : {start} -> {end}")

    print("\nStart/End Intervals:")

    for pid, start, end in sequence:
        print(f"{pid:5} | Start = {start:3} | End = {end:3}")


# ---------------- Main Program ----------------

print("=" * 50)
print("       FCFS AND SJF CPU SCHEDULING")
print("=" * 50)

try:
    n = int(input("\nEnter number of processes: "))

    if n <= 0:
        print("Error: Number of processes must be greater than 0.")
        exit()

    processes = []

    print("\nEnter process details:")

    for i in range(n):

        print(f"\nProcess {i + 1}")

        pid = input("Process ID: ").strip()

        if not pid:
            print("Error: Process ID cannot be empty.")
            exit()

        at = int(input("Arrival Time: "))
        bt = int(input("Burst Time: "))

        processes.append((pid, at, bt))

except ValueError:
    print("Error: Please enter valid numeric values.")
    exit()


# Validate input
if validate_processes(processes):

    print("\nInput data accepted successfully.")

    # Display original data
    print("\nOriginal Process Data:")
    print("PID\tArrival\tBurst")

    for pid, at, bt in processes:
        print(f"{pid}\t{at}\t{bt}")

    # Same dataset used for both algorithms
    fcfs_result = fcfs(processes)
    sjf_result = sjf(processes)

    # Display results
    display("FCFS SCHEDULING", fcfs_result)
    display("NON-PREEMPTIVE SJF SCHEDULING", sjf_result)

    print("\n" + "=" * 50)
    print("Both algorithms used the SAME process dataset.")
    print("=" * 50)