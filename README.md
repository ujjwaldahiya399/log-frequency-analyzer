# 🔍 Log Frequency Analyzer

A command-line tool to analyze Apache/Nginx web server logs — built in Python.
Parses raw log files and surfaces traffic patterns, error trends, and suspicious
IP behavior through an interactive terminal interface.

---

## 📸 Demo
```
╔══════════════════════════════════════╗
║      🔍  Log Frequency Analyzer       ║
╚══════════════════════════════════════╝

  File: access.log  |  Entries: 150

  [1]  Top IPs              [5]  Hourly Traffic
  [2]  Status Codes         [6]  Error Analysis
  [3]  HTTP Methods         [7]  Suspicious IPs
  [4]  Top URLs             [8]  Change Top N
                            [9]  Load New File
                            [0]  Exit
```

---

## ✨ Features

- **IP Frequency Analysis** — identify most active clients
- **Status Code Breakdown** — group by 2xx, 3xx, 4xx, 5xx
- **HTTP Method Counter** — GET, POST, PUT, DELETE distribution
- **Top URL Paths** — find most and least requested endpoints
- **Hourly Traffic Report** — visualize traffic patterns across the day
- **Error Analysis** — surface broken endpoints and failing URLs
- **Suspicious IP Detection** — flag brute force attempts, scanners, and broken clients
- **Color-coded Terminal UI** — red for errors, yellow for warnings, green for success
- **Export to CSV** — save any report for further analysis

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3 | Core language |
| `re` | Regex parsing of raw log lines |
| `collections.Counter` | Frequency counting |
| `collections.defaultdict` | Grouped time-based analysis |
| `datetime` | Timestamp parsing and hourly grouping |
| `colorama` | Cross-platform terminal colors |
| `csv` | Exporting reports |

---

## 📂 Project Structure
```
log_analyzer/
├── parser.py       # Regex-based log line parser
├── analyzer.py     # Frequency counters and pattern detection
├── colors.py       # Colorama color helpers
├── cli.py          # Interactive CLI menu
├── access.log      # Sample Apache/Nginx access log
├── error.log       # Sample Nginx error log
└── requirements.txt
```

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/log-frequency-analyzer.git
cd log-frequency-analyzer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the analyzer
```bash
python cli.py
```

### 4. Enter the path to your log file when prompted
```
Enter path to log file: access.log
```

---

## 📊 Sample Output

### Suspicious IP Detection
```
--- Suspicious IPs (10+ requests) ---
  ⚠️  10.0.0.4        → 15 total requests, 15 errors triggered
  ⚠️  192.168.1.2     → 10 total requests, 6 x 401 (brute force?)
  ⚠️  192.168.1.1     → 12 total requests
```

### Hourly Traffic
```
--- Requests Per Hour ---
  Hour     Requests   Errors   Traffic Bar
  ──────────────────────────────────────────
  08:00    7          2        ███████
  09:00    13         3        █████████████
  10:00    11         3        ███████████
```

---

## 💡 What I Learned

- Parsing real-world unstructured text data using **regex named groups**
- Using `Counter` and `defaultdict` for efficient frequency analysis
- Detecting anomalous patterns with **threshold-based logic**
- Building a clean **interactive CLI** with input validation and screen management
- Structuring a Python project across multiple modules with separation of concerns

---

## 🔮 Future Improvements

- [ ] Support for combined log format variations
- [ ] Time-window based suspicious IP detection
- [ ] HTML report export
- [ ] Real-time log monitoring with `tail -f`
- [ ] Geolocation of IP addresses

---

## 📄 License

MIT License — feel free to use and modify.

---

*Built as a learning project to understand log analysis, regex parsing, and CLI development in Python.*