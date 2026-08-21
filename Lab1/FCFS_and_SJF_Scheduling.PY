# FCFS and Non-Preemptive SJF Scheduling

# Taking number of processes
n = int(input("Enter number of processes: "))
processes = []

# Taking process details
for i in range(n):
    print("\nEnter details for Process", i + 1)
    pid = input("Process ID: ")
    at = int(input("Arrival Time: "))
    bt = int(input("Burst Time: "))

    # Simple validation
    if at < 0:
        print("Arrival Time cannot be negative.")
        exit()
    if bt <= 0:
        print("Burst Time must be greater than 0.")
        exit()

    processes.append([pid, at, bt])

# Keep a copy of original data
original = [p[:] for p in processes]

# =========================
# FCFS Scheduling
# =========================
fcfs = original[:]
# Sort according to Arrival Time
fcfs.sort(key=lambda x: x[1])

time = 0
print("\n\n===== FCFS =====")
print("Execution Sequence:")
for p in fcfs:
    pid = p[0]
    at = p[1]
    bt = p[2]

    # CPU is idle
    if time < at:
        print("IDLE:", time, "to", at)
        time = at

    start = time
    time = time + bt
    end = time
    print(pid, ":", start, "to", end)

# =========================
# Non-Preemptive SJF
# =========================
sjf = original[:]
completed = []
time = 0

print("\n\n===== SJF =====")
print("Execution Sequence:")
while len(completed) < n:
    available = []

    # Find processes that have arrived
    for p in sjf:
        if p not in completed and p[1] <= time:
            available.append(p)

    # If no process has arrived
    if len(available) == 0:
        # Find next process to arrive
        next_process = None
        for p in sjf:
            if p not in completed:
                if next_process is None or p[1] < next_process[1]:
                    next_process = p
        print("IDLE:", time, "to", next_process[1])
        time = next_process[1]
        continue

    # Find process with shortest burst time
    shortest = available[0]
    for p in available:
        if p[2] < shortest[2]:
            shortest = p

    pid = shortest[0]
    at = shortest[1]
    bt = shortest[2]
    start = time
    time = time + bt
    end = time
    print(pid, ":", start, "to", end)
    completed.append(shortest)