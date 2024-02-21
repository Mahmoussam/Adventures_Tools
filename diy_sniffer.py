from scapy.all import *

def http_header(packet):
        http_packet=str(packet)
        
        if True:
                ret=GET_print(packet)
                #print(ret,'y')
                if 'User-Agent' in ret:
                    print(ret)
                    return ret
        else:
            return '##  NO GET ##'

def GET_print(packet1):
    ret = "***************************************GET PACKET****************************************************\n"
    ret += "\n".join(packet1.sprintf("{Raw:%Raw.load%}\n").split(r"\r\n"))
    ret += "*****************************************************************************************************\n"
    
    return ret
def packet_handler(packet):
    print(packet.summary())
    print(packet.show())
def packet_callback(packet):
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst

        if TCP in packet:
            protocol = "TCP"
            port_src = packet[TCP].sport
            port_dst = packet[TCP].dport
        elif UDP in packet:
            protocol = "UDP"
            port_src = packet[UDP].sport
            port_dst = packet[UDP].dport
        else:
            protocol = "Unknown"
            port_src = port_dst = "N/A"

        print(f"IP: {ip_src} -> {ip_dst}, Protocol: {protocol}, Source Port: {port_src}, Destination Port: {port_dst}")

def analyze_packet(packet):
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        protocol = packet[IP].proto

        if protocol == 6 and TCP in packet:
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            if(ip_dst=='192.168.1.6'):
                return
            if dst_port == 80:
                print(f"HTTP traffic  to {ip_dst}:{dst_port}")
            elif dst_port == 443:
                print(f"HTTPS traffic  to {ip_dst}:{dst_port}")
            else:
                print(f"TCP traffic  to {ip_dst}:{dst_port}")
        '''
        elif protocol == 17 and UDP in packet:
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport

            if dst_port == 53:
                print(f"DNS traffic from {ip_src}:{src_port} to {ip_dst}:{dst_port}")
            else:
                print(f"UDP traffic from {ip_src}:{src_port} to {ip_dst}:{dst_port}")
        '''
sniff(prn=analyze_packet)
#filter='ip host '
