from scapy.all import *
from scapy.layers.inet import TCP, IP

# Define the target IP and port
TARGET_IP = "127.0.0.1"  # Replace with the actual target IP
TARGET_PORT = 11000  # Replace with the target port


# Function to modify and retransmit packets
def intercept_and_modify(packet):
    if packet.haslayer(TCP) and packet.haslayer(Raw):  # Look for TCP packets with data
        print(f"Captured Packet: {packet.summary()}")

        # Extract the payload (TCP data)
        original_payload = packet[Raw].load
        print(f"Original Payload: {original_payload}")

        # Modify the payload (example: replace "hello" with "world")
        modified_payload = original_payload.replace(b"mvp", b"off")

        # Create a new packet with the modified payload
        new_packet = IP(src=packet[IP].src, dst=packet[IP].dst) / \
                     TCP(sport=packet[TCP].sport, dport=packet[TCP].dport, seq=packet[TCP].seq, ack=packet[TCP].ack,
                         flags="PA") / \
                     modified_payload
        print(packet[TCP].seq)

        # Recalculate checksums for IP and TCP layers
        del new_packet[IP].chksum
        del new_packet[TCP].chksum

        # Send the modified packet
        send(new_packet)
        #print(f"Modified Packet Sent: {modified_payload}")


# Sniff packets and apply the modification function
print(f"Sniffing packets on port {TARGET_PORT}...")
sniff(filter=f"tcp and port {TARGET_PORT} or tcp port 62626", prn=intercept_and_modify, store=0)