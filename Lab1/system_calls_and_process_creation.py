import os
import subprocess

# 1. Create a child process
pid = os.fork()

if pid == 0:
    # Child process

    # 2. Display Process ID and Parent Process ID
    print("\n[Child Process]")
    print("Child PID       :", os.getpid())
    print("Parent PID      :", os.getppid())

    # 4. Execute a harmless Linux command
    print("\nExecuting Linux command:")
    subprocess.run(["echo", "Hello from child process"])

    os._exit(0)

else:
    # Parent process

    print("\n[Parent Process]")
    print("Parent PID      :", os.getpid())
    print("Child PID       :", pid)

    # 3. Wait for child process to complete
    os.waitpid(pid, 0)
    print("Child process completed.")

# 5. Create, write, read and close a test file
print("\n[File Operations]")

filename = "os_test.txt"

try:
    # Create and write
    fd = os.open(filename, os.O_CREAT | os.O_WRONLY)

    os.write(fd, b"Operating Systems System Call Test\n")
    os.close(fd)

    print("File created and written successfully.")

    # Open and read
    fd = os.open(filename, os.O_RDONLY)

    data = os.read(fd, 1024)
    os.close(fd)

    print("File contents:", data.decode())

except OSError as e:
    print("File operation error:", e)


# 7. Handle an invalid path
print("\n[Error Handling]")

try:
    fd = os.open("/invalid/path/test.txt", os.O_RDONLY)
    os.close(fd)

except OSError as e:
    print("Expected error - invalid path:", e)


print("\n=== PROGRAM COMPLETED ===")