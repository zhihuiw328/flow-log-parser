import sys
import csv

class FlowLogParser:
    def __init__(self):
        self.lookup_table = {}
        self.tag_count = {}
        self.port_protocol_count = {}
        self.protocol_map = {
            "1": "icmp",
            "6": "tcp",
            "17": "udp",
        }

    def load_lookup_table(self, lookup_table_file):
        with open(lookup_table_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                normalized_row = {key.strip(): value for key, value in row.items()}
                key = (normalized_row["dstport"].lower(), normalized_row["protocol"].lower())
                self.lookup_table[key] = normalized_row["tag"]
    
    def parse_flow_logs(self, flow_log_file):
        with open(flow_log_file, "r") as file:
            for line in file:
                parts = line.split()
                if len(parts) != 14:
                    # flow log format error, pass this line
                    continue

                dstport = parts[6].strip()
                protocol = parts[7].strip()
                protocol = self.protocol_map[protocol]

                key = (dstport, protocol)
                tag = self.lookup_table.get(key, "Untagged")
                
                self.tag_count[tag] = self.tag_count.get(tag, 0) + 1
                self.port_protocol_count[key] = self.port_protocol_count.get(key, 0) + 1
    
    def write_output(self, output_file):
        with open(output_file, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["Tag Counts:"])
            writer.writerow(["Tag", "Count"])
            for tag, count in self.tag_count.items():
                if tag != "Untagged":
                    writer.writerow([tag, count])
            
            if "Untagged" in self.tag_count:
                writer.writerow(["Untagged", self.tag_count["Untagged"]])

            writer.writerow(["----------------------------------------------------"])
            writer.writerow(["Port/Protocol Combination Counts: "])
            writer.writerow(["Port", "Protocol", "Count"])
            for (port, protocol), count in self.port_protocol_count.items():
                writer.writerow([port, protocol, count])



def main():
    if len(sys.argv) != 4:
        print("Usage: python flow_log_parser.py <lookup_table_file> <flow_logs_file> <output_file>")
        sys.exit(1)

    lookup_table_file = sys.argv[1]
    flow_logs_file = sys.argv[2]
    output_file = sys.argv[3]

    parser = FlowLogParser()
    parser.load_lookup_table(lookup_table_file)
    parser.parse_flow_logs(flow_logs_file)
    parser.write_output(output_file)
    
    

if __name__ == "__main__":
    main()
                