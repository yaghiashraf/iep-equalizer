import json
import os
from collections import defaultdict

LOG_FILE = "ab_test_logs.json"

def analyze_logs():
    if not os.path.exists(LOG_FILE):
        print("No data found.")
        return

    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except json.JSONDecodeError:
        print("Error reading log file.")
        return

    stats = defaultdict(lambda: {"total": 0, "conversions": 0, "total_latency": 0})

    for entry in logs:
        model = entry.get("model", "Unknown")
        stats[model]["total"] += 1
        stats[model]["conversions"] += entry.get("conversion", 0)
        stats[model]["total_latency"] += entry.get("latency", 0)

    print(f"\n{'='*40}")
    print(f"{'A/B TEST ANALYTICS DASHBOARD':^40}")
    print(f"{ '='*40}")
    
    print(f"\n{'-'*40}")
    print(f"{ 'Model':<20} | {'Conv Rate':<10} | {'Avg Latency':<10}")
    print(f"{'-'*40}")

    for model, data in stats.items():
        total = data["total"]
        if total > 0:
            conv_rate = (data["conversions"] / total) * 100
            avg_latency = data["total_latency"] / total
            print(f"{model:<20} | {conv_rate:>9.1f}% | {avg_latency:>9.4f}s")
        else:
             print(f"{model:<20} | {'N/A':>10} | {'N/A':>10}")
    print(f"{'-'*40}\n")

if __name__ == "__main__":
    analyze_logs()
