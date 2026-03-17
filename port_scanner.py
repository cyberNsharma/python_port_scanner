import socket
import threading
import queue
from datetime import datetime

MAX_THREADS = 100
TIMEOUT = 1.5

print("===================================")
print("        Port Scanner    ")
print("===================================")

# Input
target = input("Enter Target IP or Host: ").strip()
start_port = int(input("Enter Start Port: "))
end_port = int(input("Enter End Port: "))

# Resolve hostname
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Hostname could not be resolved")
    exit()

print(f"\nScanning Target: {target_ip}")
print(f"Ports: {start_port} to {end_port}")
print(f"Scan started at: {datetime.now()}")
print("-----------------------------------")

# Queue & shared data
task_queue = queue.Queue()
results = {}
lock = threading.Lock()

# Worker function
def worker():
    while True:
        port = task_queue.get()
        if port is None:
            break

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(TIMEOUT)

            result = sock.connect_ex((target_ip, port))

            if result == 0:
                status = "OPEN"
            elif result in (111, 61, 10061):
                status = "CLOSED"
            else:
                status = "FILTERED"

        except socket.timeout:
            status = "TIMEOUT"
        except socket.error:
            status = "ERROR"
        finally:
            sock.close()

        with lock:
            results[port] = status
            print(f"Port {port:<5} {status}")

        task_queue.task_done()


# Create thread pool
threads = []
thread_count = min(MAX_THREADS, end_port - start_port + 1)

for _ in range(thread_count):
    t = threading.Thread(target=worker, daemon=True)
    t.start()
    threads.append(t)

# Add tasks
for port in range(start_port, end_port + 1):
    task_queue.put(port)

# Wait for completion
task_queue.join()

# Stop threads
for _ in threads:
    task_queue.put(None)

for t in threads:
    t.join()

# Summary
print("-----------------------------------")
print(f"Scan completed at: {datetime.now()}")

open_ports = [p for p, s in results.items() if s == "OPEN"]
print("OPEN ports:", open_ports if open_ports else "None")
