import dpkt
import csv

def pcap_to_csv(pcap_file, csv_file):
    """Converts a pcap file into a CSV file.

    Args:
        pcap_file: The path to the pcap file.
        csv_file: The path to the output CSV file.
    """

    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        with open(csv_file, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'src_ip', 'dst_ip', 'src_port', 'dst_port', 'protocol', 'info']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for ts, buf in pcap:
                eth = dpkt.ethernet.Ethernet(buf)
                if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                    continue

                ip = eth.data
                tcp = ip.data
                if tcp.sport or tcp.dport:
                    row = {
                        'timestamp': ts,
                        'src_ip': ip.src,
                        'dst_ip': ip.dst,
                        'src_port': tcp.sport,
                        'dst_port': tcp.dport,
                        'protocol': ip.p,
                        'info': tcp.data
                    }
                    writer.writerow(row)
                    print (row)

if __name__ == '__main__':
    pcap_file = 'capture.pcap'
    csv_file = 'cap1.csv'
    pcap_to_csv(pcap_file, csv_file)
