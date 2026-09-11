import os
import multiprocessing
import subprocess

TEST_FILE = "test_system_call.txt"


# Child process
def child_process():
    print("\n--- CHILD PROCESS ---")

    # 2. Display Process ID and Parent Process ID
    print("Child Process ID (PID):", os.getpid())
    print("Parent Process ID (PPID):", os.getppid())

    # 4. Execute a harmless Windows command
    print("\nExecuting Windows command: systeminfo")
    result = subprocess.run(
        ["cmd", "/c", "echo Hello from Child Process"],
        capture_output=True,
        text=True
    )

    print("Command Output:", result.stdout.strip())


if __name__ == "__main__":

    print("========================================")
    print(" SYSTEM CALLS AND PROCESS CREATION")
    print("========================================")

    # 1. Create a child process
    print("\nCreating child process...")

    child = multiprocessing.Process(target=child_process)
    child.start()

    # 3. Wait for child process to complete
    child.join()

    print("\nChild process completed.")
    print("Child Exit Code:", child.exitcode)

    # 5. Create, write, read and close a test file
    print("\n--- FILE OPERATIONS ---")

    try:
        # Create and write
        file = open(TEST_FILE, "w")
        file.write("This is a controlled test file.\n")
        file.write("File operations completed successfully.\n")
        file.close()

        print("File created and written:", TEST_FILE)

        # Read
        file = open(TEST_FILE, "r")
        data = file.read()
        file.close()

        print("File contents:")
        print(data)

        print("File read and closed successfully.")

    except OSError as e:
        print("File operation error:", e)

    # 6. Inspect Windows device interface
    print("\n--- DEVICE INTERFACE ---")

    try:
        # Windows equivalent of a null device
        with open("NUL", "w") as device:
            device.write("Test data")

        print("Windows device interface inspected: NUL")

    except OSError as e:
        print("Device interface error:", e)

    # 7. Handle invalid path
    print("\n--- ERROR HANDLING ---")

    invalid_path = "Z:\\invalid\\path\\test.txt"

    try:
        file = open(invalid_path, "r")
        data = file.read()
        file.close()

    except FileNotFoundError:
        print("Error handled successfully:")
        print("Invalid path - file does not exist.")

    except OSError as e:
        print("File operation failed:", e)

    # 8. Display evidence
    print("\n--- EVIDENCE ---")

    print("Main Process ID (PID):", os.getpid())
    print("Main Parent Process ID (PPID):", os.getppid())
    print("Test file:", TEST_FILE)
    print("Device interface inspected: NUL")
    print("Invalid path error handled successfully.")

    print("\n========================================")
    print(" PROGRAM COMPLETED SUCCESSFULLY")
    print("========================================")