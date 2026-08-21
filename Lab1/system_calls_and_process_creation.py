import os
import subprocess
import multiprocessing


def child_process_work():
    # Child process
    # 2. Display Process ID and Parent Process ID
    print("\n[Child Process]")
    print("Child PID       :", os.getpid())
    print("Parent PID      :", os.getppid())
    # 4. Execute a harmless Windows command
    print("\nExecuting command:")
    subprocess.run(["cmd", "/c", "echo Hello from child process"])


if __name__ == "__main__":
    # 1. Create a child process
    print("\n[Parent Process]")
    print("Parent PID      :", os.getpid())

    p = multiprocessing.Process(target=child_process_work)
    p.start()
    print("Child PID       :", p.pid)

    # 3. Wait for child process to complete
    p.join()
    print("Child process completed.")

    # 5. Create, write, read and close a test file
    print("\n[File Operations]")
    filename = "os_test.txt"
    try:
        # Create and write
        fd = os.open(filename, os.O_CREAT | os.O_WRONLY | os.O_BINARY)
        os.write(fd, b"Operating Systems System Call Test\n")
        os.close(fd)
        print("File created and written successfully.")

        # Open and read
        fd = os.open(filename, os.O_RDONLY | os.O_BINARY)
        data = os.read(fd, 1024)
        os.close(fd)
        print("File contents:", data.decode())
    except OSError as e:
        print("File operation error:", e)

    # 7. Handle an invalid path
    print("\n[Error Handling]")
    try:
        fd = os.open("C:\\invalid\\path\\test.txt", os.O_RDONLY)
        os.close(fd)
    except OSError as e:
        print("Expected error - invalid path:", e)

    print("\n=== PROGRAM COMPLETED ===")