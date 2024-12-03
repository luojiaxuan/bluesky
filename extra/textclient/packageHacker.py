from scapy.all import *
from scapy.layers.inet import IP, TCP

# Replace with your specific values
source_ip = "127.0.0.1"
target_ip = "127.0.0.1"
source_port = 49651
target_port = 11000
seq_num = 1299247620
ack_num = 2638130484


# Convert the hex payload to bytes
hex_payload = "01050035e9fc3c0105535441434b0009a87265736f206d7670"
payload_data = bytes.fromhex(hex_payload)
print(payload_data)
modified_payload = payload_data.replace(b"mvp",b"off")
print(modified_payload)
# Construct the packet
packet = IP(src=source_ip, dst=target_ip) / \
         TCP(sport=source_port, dport=target_port, flags="PA", seq=seq_num, ack=ack_num) / \
         modified_payload

print(packet)
# Send the packet
send(packet)
