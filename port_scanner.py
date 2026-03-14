import socket
import threading
from datetime import datetime

print("===================================")
print("        Simple TCP Port Scanner    ")
print("===================================")

# input
target = input("Enter Target IP or Host: ")
start_port = int(input("Enter Start Port: "))
end_port = int(input("Enter End Port: "))

# resolve hostname
# computers communicate using ip , not domain names
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Hostname could not be resolved")
    exit()

print("\nScanning Target:", target_ip)
print("Scanning ports:", start_port, "to", end_port)
print("Scan started at:", datetime.now())
print("-----------------------------------")


# scan function
def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)

        result = sock.connect_ex((target_ip, port))

        if result == 0:
            message = f"Port {port} OPEN"
            print(message)
            

        else:
            message = f"Port {port} CLOSED"
            print(message)
            

        sock.close()

    except socket.timeout:
        message = f"Port {port} TIMEOUT"
        print(message)
       

    except socket.error:
        message = f"Port {port} ERROR"
        print(message)
        


threads = []

# create threads for scanning 
 # Thread runs port scanning tasks in parallel instead of one by one.
for port in range(start_port, end_port + 1):
    t = threading.Thread(target=scan_port, args=(port,))
    threads.append(t)
    t.start()

# wait for all threads to finish
for t in threads:
    t.join()

print("-----------------------------------")
print("Scan completed at:", datetime.now())


