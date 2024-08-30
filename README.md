# flow-log-parser

## Overview

This Python program parses flow log data, maps each row to a tag based on a lookup table, and generates an output CSV file containing the count of matches for each tag and each port/protocol combination.

## Assumptions

- **Input File Format**:
1. The flow log files should follow the default format (version 2). Example format:
  ```plaintext
  2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK
  2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 23 49154 6 15 12000 1620140761 1620140821 REJECT OK
  ```
2. The lookup table should be defined in a CSV file with three columns: `dstport`, `protocol`, and `tag`. The `protocol` must be a string (e.g., `tcp`, `udp`, `icmp`). Example format:
  ```csv
  dstport,protocol,tag
  25,tcp,sv_P1
  68,udp,sv_P2
  23,tcp,sv_P1
  ```
3. The protocol numbers mapping is based on the official IANA protocol numbers list: [IANA Protocol Numbers](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml)

- **Input File Size**:
1. The flow log file size can be up to 10 MB
2. The lookup file can have up to 10000 mappings

- **Output File Format**:
1. The tags can map to more than one port, protocol combinations
2. The matches should be case-insensitive
3. The output is saved in CSV format. Example format:
  ```csv
  dstport,protocol,tag
  Tag Counts:
  Tag,Count
  sv_P1 ,2
  email ,2
  Untagged,8
  ----------------------------------------------------
  Port/Protocol Combination Counts: 
  Port,Protocol,Count
  49153,tcp,1
  49154,tcp,1
  49155,tcp,1
  49156,tcp,1
  ...
  ```

## Requirements

  - Python 3.x 

## Usage

### Command-Line Execution

You can run the script from the command line by specifying the lookup table file, flow logs file, and output file as arguments:

```bash
python flow_log_parser.py <lookup_table_file> <flow_logs_file> <output_file>
```

### Generating Test Data

You can generate sample data and expected outputs as follows:

```bash
python generate_test_data.py
```
