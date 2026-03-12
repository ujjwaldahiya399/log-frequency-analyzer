from collections import Counter,defaultdict
from parser import parse_file

def countIPs(entries):
    """count requests per IP address"""
    return Counter(entry['ip'] for entry in entries)

def count_status_codes(entries):
    """count occurances for each status type """
    return Counter(entry['status'] for entry in entries)

def count_methods(entries):
    """count number of occurances for each HTTP method"""
    return Counter(entry["method"] for entry in entries)

def count_paths(entries):
    """count how many time each URL path is requested"""
    return Counter(entry['path'] for entry in entries)

def count_status_groups(entries):
    """Group status codes into 2xx, 3xx, 4xx, 5xx."""
    groups = Counter()
    for entry in entries:
        group = f"{entry['status'] // 100}xx"
        groups[group] += 1
    return groups

def top_n(counter,n=5):
    """Return top n most common items from a counter"""
    return counter.most_common(n)



def request_per_hour(entries):
    """Count total requests for each hour of the day."""
    hourly = Counter()
    for entry in entries:
        hour = entry['datetime'].strftime("%H:00")
        hourly[hour] += 1
    return hourly

def errors_per_hour(entries):
    """Count only 4xx and 5xx responses per hour."""
    hourly = Counter()
    for entry in entries:
        if entry['status'] >= 400:
            hour = entry['datetime'].strftime("%H:00")
            hourly[hour] += 1
    return hourly

def requests_per_hour_by_status(entries):
    """Break down requests per hour into status groups (2xx, 4xx, 5xx etc.)"""
    breakdown = defaultdict(Counter)
    for entry in entries:
        hour = entry['datetime'].strftime("%H:00")
        group = f"{entry['status'] // 100}xx"
        breakdown[hour][group] += 1
    return breakdown


def print_hourly_report(entries):
    """Print a visual hourly traffic report with a bar chart in terminal."""
    hourly = request_per_hour(entries)
    errors = errors_per_hour(entries)

    print("\n--- Requests Per Hour ---")
    print(f"  {'Hour':<8} {'Requests':<12} {'Errors':<10} {'Traffic Bar'}")
    print(f"  {'-'*55}")

    for hour in sorted(hourly.keys()):
        total = hourly[hour]
        error = errors.get(hour, 0)
        bar = '█' * total          # one block per request
        print(f"  {hour:<8} {total:<12} {error:<10} {bar}")

def top_error_ips(entries, n=5):
    """Top IPs that triggered the most 4xx/5xx errors."""
    error_entries = [e for e in entries if e['status'] >= 400]
    return Counter(e['ip'] for e in error_entries).most_common(n)


def top_404_urls(entries, n=5):
    """Top URLs that returned 404 Not Found."""
    not_found = [e for e in entries if e['status'] == 404]
    return Counter(e['path'] for e in not_found).most_common(n)


def top_500_urls(entries, n=5):
    """Top URLs that returned 500 Internal Server Error."""
    server_errors = [e for e in entries if e['status'] == 500]
    return Counter(e['path'] for e in server_errors).most_common(n)


def top_ips_by_method(entries, method='POST', n=5):
    """Top IPs using a specific HTTP method (default: POST)."""
    filtered = [e for e in entries if e['method'] == method]
    return Counter(e['ip'] for e in filtered).most_common(n)


def top_active_users(entries, n=5):
    """Top authenticated users by request count (ignores anonymous)."""
    authenticated = [e for e in entries if e['user'] is not None]
    return Counter(e['user'] for e in authenticated).most_common(n)


def suspicious_ips(entries, threshold=10):
    suspects = []

    # Group all entries by IP
    from collections import defaultdict
    ip_entries = defaultdict(list)
    for e in entries:
        ip_entries[e['ip']].append(e)

    for ip, reqs in ip_entries.items():
        total         = len(reqs)
        error_count   = sum(1 for e in reqs if e['status'] >= 400)
        not_found     = sum(1 for e in reqs if e['status'] == 404)
        unauthorized  = sum(1 for e in reqs if e['status'] == 401)

        reasons = []

        if total >= threshold:
            reasons.append(f"{total} total requests")
        if not_found >= 3:
            reasons.append(f"{not_found} x 404 (scanning?)")
        if unauthorized >= 2:
            reasons.append(f"{unauthorized} x 401 (brute force?)")
        if error_count >= 5:
            reasons.append(f"{error_count} errors triggered")

        if reasons:
            suspects.append((ip, reasons))

    return suspects





def print_patterns_report(entries, n=5):
    """Print a full patterns report."""

    print(f"\n--- Top {n} IPs with Errors (4xx/5xx) ---")
    for ip, count in top_error_ips(entries, n):
        print(f"  {ip:<20} {count} errors")

    print(f"\n--- Top {n} 404 URLs ---")
    for path, count in top_404_urls(entries, n):
        print(f"  {path:<30} {count} times")

    print(f"\n--- Top {n} 500 URLs ---")
    for path, count in top_500_urls(entries, n):
        print(f"  {path:<30} {count} times")

    print(f"\n--- Top {n} POST IPs ---")
    for ip, count in top_ips_by_method(entries, 'POST', n):
        print(f"  {ip:<20} {count} POST requests")

    print(f"\n--- Top {n} Active Users ---")
    for user, count in top_active_users(entries, n):
        print(f"  {user:<20} {count} requests")

    print(f"\n--- Suspicious IPs (10+ requests) ---")
    suspects = suspicious_ips(entries, threshold=10)
    if suspects:
        for ip, reasons in sorted(suspects, key=lambda x: len(x[1]), reverse=True):
            print(f"  ⚠️  {ip:<20} → {', '.join(reasons)}")
    else:
        print("  None found.")
"""Test """

if __name__ == "__main__":
    entries = parse_file("access.log")

    print("\n--- Top 5 IPs ---")
    for ip, count in top_n(countIPs(entries)):
        print(f"  {ip:<20} {count} requests")

    print("\n--- Status Codes ---")
    for status, count in top_n(count_status_codes(entries)):
        print(f"  {status}    {count} times")

    print("\n--- HTTP Methods ---")
    for method, count in top_n(count_methods(entries)):
        print(f"  {method:<10} {count} times")

    print("\n--- Top 5 URLs ---")
    for path, count in top_n(count_paths(entries)):
        print(f"  {path:<30} {count} times")

    print("\n--- Status Groups ---")
    for group, count in sorted(count_status_groups(entries).items()):
        print(f"  {group}    {count} responses")

    # New Step 4 output
    print_hourly_report(entries)

    print("\n--- Errors Per Hour (4xx + 5xx) ---")
    for hour, count in sorted(errors_per_hour(entries).items()):
        print(f"  {hour}   {count} errors")

    # New Step 5 output
    print_patterns_report(entries, n=5)