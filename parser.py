import re
from datetime import datetime

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+)'
    r' \S+'
    r' (?P<user>\S+)'
    r' \[(?P<timestamp>[^\]]+)\]'
    r' "(?P<method>\S+)'
    r' (?P<path>\S+)'
    r' \S+"'
    r' (?P<status>\d{3})'
    r' (?P<size>\d+|-)'
)

def parse_line(line):
    """Parse a single log line. Returns a dict or None if no match."""
    print(line)
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None

    data = match.groupdict()

    # Convert status to int
    data['status'] = int(data['status'])

    # convert size to int
    data["size"] = int(data["size"]) if data["size"] != '-'else 0

    # Replace '-' user with None for clarity
    if data["user"] == '-':
        data['user'] = None

    # Parse timestamp into a datetime object
    data['datetime'] = datetime.strptime(data['timestamp'],"%d/%b/%Y:%H:%M:%S %z")

    return data

def parse_file(filepath):
    """Parse an entire log file. Returns a list of dicts."""
    entries = []
    skipped = 0

    with open(filepath, 'r') as f:
        for line in f:
            result = parse_line(line)
            if result:
                entries.append(result)
            else:
                skipped += 1

    print(" Parsed {len(entries)} entries.  Skipped {skipped} lines.")
    return entries


# ---- Quick test ----
if __name__ == "__main__":
    entries = parse_file("access.log")

    # Print the first 3 parsed entries
    for entry in entries[:3]:
        print(entry)