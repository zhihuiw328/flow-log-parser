import random
import time
import csv
from datetime import datetime, timedelta

lookup_map = {}
tag_count = {}
port_protocal_count = {}
protocal_map = {
    "1": "icmp",
    "6": "tcp",
    "17": "udp",
}

def generate_flow_logs(max_size_mb = 9):
    flow_logs = []
    eni_ids = ["eni-0a1b2c3d", "eni-4d3c2b1a", "eni-5e6f7g8h", "eni-9h8g7f6e", "eni-7i8j9k0l", "eni-6m7n8o9p", "eni-1a2b3c4d", "eni-5f6g7h8i", "eni-9k10l11m", "eni-2d2e2f3g", "eni-4h5i6j7k"]
    src_ips = [f"10.0.{i}.{j}" for i in range(0, 255) for j in range(1, 255)]
    dest_ips = [f"198.51.{i}.{j}" for i in range(100, 110) for j in range(1, 255)]
    ports = list(range(1, 65536))
    protocols = ["1", "6", "17"]  # 1 for ICMP, 6 for TCP, 17 for UDP
    actions = ["ACCEPT", "REJECT"]
    statuses = ["OK", "FAIL"]
    max_size_bytes = max_size_mb * 1024 * 1024
    # max_size_bytes = max_size_mb * 100
    current_size = 0
    start_time = datetime.now()

    while current_size < max_size_bytes:
        eni_id = random.choice(eni_ids)
        src_ip = random.choice(src_ips)
        dest_ip = random.choice(dest_ips)
        src_port = random.randint(1, 65535)
        dest_port = random.choice(ports)
        protocol = random.choice(protocols)
        packets = random.randint(5, 25)
        bytes_transferred = packets * random.randint(500, 2000)
        start_epoch = int(time.mktime(start_time.timetuple()))
        end_epoch = start_epoch + random.randint(60, 120)
        action = random.choice(actions)
        status = random.choice(statuses)
        
        flow_log = f"2 123456789012 {eni_id} {src_ip} {dest_ip} {src_port} {dest_port} {protocol} {packets} {bytes_transferred} {start_epoch} {end_epoch} {action} {status}"
        flow_logs.append(flow_log)
        current_size += len(flow_log.encode("utf-8")) + 1  # +1 for newline character
        start_time += timedelta(seconds=random.randint(1, 10))

        # calculate expected result
        key = (dest_port, protocal_map[str(protocol)])
        # print(key)
        # print(lookup_map)
        tag = lookup_map.get(key, "Untagged")
        
        tag_count[tag] = tag_count.get(tag, 0) + 1
        port_protocal_count[key] = port_protocal_count.get(key, 0) + 1

    return flow_logs

def generate_lookup_table(num_entries=10000):
    lookup_table = []
    ports = list(range(1, 65536))
    protocols = ["tcp", "udp", "icmp"]
    tags = [f"sv_P{i}" for i in range(1, 101)]

    for _ in range(num_entries):
        port = random.choice(ports)
        protocol = random.choice(protocols)
        tag = random.choice(tags)
        lookup_table.append({"dstport": port, "protocol": protocol, "tag": tag})
        lookup_map[(port, protocol)] = tag
    
    return lookup_table

def save_flow_logs_to_file(flow_logs, filename="generated_test_data/flow_logs.txt"):
    with open(filename, 'w') as file:
        for log in flow_logs:
            file.write(log + "\n")

def save_lookup_table_to_csv(lookup_table, filename="generated_test_data/lookup_table.csv"):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ["dstport", "protocol", "tag"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in lookup_table:
            writer.writerow(row)

def save_expected_result(filename="generated_test_data/expected_result.csv"):
    with open(filename, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Tag Counts:"])
        writer.writerow(["Tag", "Count"])
        for tag, count in tag_count.items():
            if tag != "Untagged":
                writer.writerow([tag, count])
        
        if "Untagged" in tag_count:
            writer.writerow(["Untagged", tag_count["Untagged"]])

        writer.writerow(["----------------------------------------------------"])
        writer.writerow(["Port/Protocol Combination Counts: "])
        writer.writerow(["Port", "Protocol", "Count"])
        for (port, protocol), count in port_protocal_count.items():
            writer.writerow([port, protocol, count])

# Generate the fake data
lookup_table = generate_lookup_table()
flow_logs = generate_flow_logs()

# Save the generated data to files
save_flow_logs_to_file(flow_logs)
save_lookup_table_to_csv(lookup_table)
save_expected_result()