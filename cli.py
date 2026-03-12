import os
from colors import success, error, warning, info, highlight, color_status, color_bar
from parser import parse_file
from analyzer import (
    countIPs, count_status_codes, count_methods,
    count_paths, count_status_groups, top_n,
    print_hourly_report, print_patterns_report,
    top_error_ips, top_404_urls, top_500_urls,
    suspicious_ips
)


# ── Helpers ────────────────────────────────────────────────

def clear():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(filename, entry_count):
    print(info("╔══════════════════════════════════════╗"))
    print(info("║      🔍  Log Frequency Analyzer       ║"))
    print(info("╚══════════════════════════════════════╝"))
    print(f"\n  File: {highlight(filename)}  |  Entries: {highlight(entry_count)}\n")


def print_menu():
    print(info("  [1]  Top IPs"))
    print(info("  [2]  Status Codes"))
    print(info("  [3]  HTTP Methods"))
    print(info("  [4]  Top URLs"))
    print(info("  [5]  Hourly Traffic"))
    print(info("  [6]  Error Analysis"))
    print(info("  [7]  Suspicious IPs"))
    print(info("  [8]  Change Top N"))
    print(info("  [9]  Load New File"))
    print(info("  [0]  Exit"))
    print()


def pause():
    """Wait for user to press Enter before going back to menu."""
    input("\n  Press Enter to return to menu...")


def load_file():
    """Prompt user for a log file path and parse it."""
    while True:
        path = input("\n  Enter path to log file: ").strip()
        if os.path.exists(path):
            entries = parse_file(path)
            if entries:
                return path, entries
            print("  ⚠️  File parsed but no valid entries found. Try another.")
        else:
            print(f"  ❌ File not found: {path}")


# ── Menu Handlers ──────────────────────────────────────────

def show_top_ips(entries, n):
    counts = top_n(countIPs(entries), n)
    max_count = counts[0][1] if counts else 1
    print(info(f"\n--- Top {n} IPs ---"))
    for ip, count in counts:
        bar = color_bar(count, max_count)
        print(f"  {highlight(ip):<20} {count:>4} requests  {bar}")

def show_status_codes(entries, n):
    print(info(f"\n--- Top {n} Status Codes ---"))
    labels = {200: 'OK', 201: 'Created', 204: 'No Content',
              301: 'Moved', 304: 'Not Modified', 400: 'Bad Request',
              401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found',
              500: 'Server Error'}
    for status, count in top_n(count_status_codes(entries), n):
        label = labels.get(status, '')
        print(f"  {color_status(status)}  {label:<20} {highlight(count):>4} times")

    print(info(f"\n--- By Group ---"))
    groups = count_status_groups(entries)
    max_count = max(groups.values()) if groups else 1
    for group, count in sorted(groups.items()):
        bar = color_bar(count, max_count)
        print(f"  {info(group)}   {count:>4}  {bar}")

    print(f"\n--- By Group ---")
    for group, count in sorted(count_status_groups(entries).items()):
        bar = '█' * min(count, 40)
        print(f"  {group}   {count:>4}  {bar}")


def show_methods(entries, n):
    print(f"\n--- HTTP Methods ---")
    for method, count in top_n(count_methods(entries), n):
        bar = '█' * min(count, 40)
        print(f"  {method:<10} {count:>4}  {bar}")


def show_top_urls(entries, n):
    print(f"\n--- Top {n} Requested URLs ---")
    for path, count in top_n(count_paths(entries), n):
        print(f"  {path:<35} {count:>4} times")


def show_errors(entries, n):
    print(f"\n--- Top {n} IPs Causing Errors ---")
    for ip, count in top_error_ips(entries, n):
        print(f"  {ip:<20} {count:>4} errors")

    print(f"\n--- Top {n} 404 URLs ---")
    for path, count in top_404_urls(entries, n):
        print(f"  {path:<35} {count:>4} times")

    print(f"\n--- Top {n} 500 URLs ---")
    for path, count in top_500_urls(entries, n):
        print(f"  {path:<35} {count:>4} times")


def show_suspicious(entries):
    print(info(f"\n--- Suspicious IPs (10+ requests) ---"))
    suspects = suspicious_ips(entries, threshold=10)
    if suspects:
        for ip, reasons in sorted(suspects, key=lambda x: len(x[1]), reverse=True):
            print(f"  {warning('⚠️  ' + ip):<20} → {error(', '.join(reasons))}")
    else:
        print(f"  {success('✅ No suspicious IPs found.')}")


# ── Main Loop ──────────────────────────────────────────────

def main():
    clear()
    print("╔══════════════════════════════════════╗")
    print("║      🔍  Log Frequency Analyzer       ║")
    print("╚══════════════════════════════════════╝")

    # Load file on startup
    filename, entries = load_file()
    n = 5  # default top N

    while True:
        clear()
        print_header(filename, len(entries))
        print_menu()

        choice = input("  Enter choice: ").strip()

        if choice == '1':
            clear()
            show_top_ips(entries, n)
            pause()

        elif choice == '2':
            clear()
            show_status_codes(entries, n)
            pause()

        elif choice == '3':
            clear()
            show_methods(entries, n)
            pause()

        elif choice == '4':
            clear()
            show_top_urls(entries, n)
            pause()

        elif choice == '5':
            clear()
            print_hourly_report(entries)
            pause()

        elif choice == '6':
            clear()
            show_errors(entries, n)
            pause()

        elif choice == '7':
            clear()
            show_suspicious(entries)
            pause()

        elif choice == '8':
            try:
                n = int(input("  Enter new Top N value: ").strip())
                print(f"  ✅ Top N set to {n}")
            except ValueError:
                print("  ❌ Invalid number, keeping current value.")
            pause()

        elif choice == '9':
            filename, entries = load_file()
            print(f"  ✅ Loaded {len(entries)} entries from {filename}")
            pause()

        elif choice == '0':
            print("\n  Goodbye! 👋\n")
            break

        else:
            print("  ❌ Invalid choice, try again.")
            pause()


if __name__ == "__main__":
    main()