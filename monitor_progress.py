"""
Real-time Progress Monitor for Satellite Data Collection

This script monitors the progress of the satellite data extraction in real-time.
Run this in a separate terminal while the main extraction script is running.

Usage:
    python monitor_progress.py
"""

import os
import time
import glob
from pathlib import Path
from datetime import datetime, timedelta
import sys


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def get_latest_output_file():
    """Find the most recent output CSV file."""
    output_dir = Path("data/processed")  # Files are saved here
    if not output_dir.exists():
        return None

    csv_files = list(output_dir.glob("municipality_embeddings_*.csv"))
    if not csv_files:
        return None

    # Get the most recent file
    latest_file = max(csv_files, key=lambda p: p.stat().st_mtime)
    return latest_file


def count_lines(file_path):
    """Count lines in a file (excluding header)."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return sum(1 for _ in f) - 1  # Subtract header
    except Exception:
        return 0


def get_file_size(file_path):
    """Get file size in MB."""
    try:
        size_bytes = file_path.stat().st_size
        return size_bytes / (1024 * 1024)  # Convert to MB
    except Exception:
        return 0


def format_time(seconds):
    """Format seconds into human-readable time."""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        return f"{hours}h {minutes}m"


def get_latest_log_entries(n=5):
    """Get the last N entries from the log file."""
    log_file = Path("logs/extraction.log")
    if not log_file.exists():
        return []

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return [line.strip() for line in lines[-n:]]
    except Exception:
        return []


def monitor_progress():
    """Main monitoring loop."""
    print("🛰️  Satellite Data Collection Monitor")
    print("=" * 80)
    print("\nSearching for active extraction process...\n")

    # Wait for output file to be created
    output_file = None
    for _ in range(10):
        output_file = get_latest_output_file()
        if output_file:
            break
        time.sleep(1)

    if not output_file:
        print("❌ No active extraction found!")
        print("\nMake sure the extraction script is running:")
        print(
            "   python src/1_collection/gee/extract_embeddings_efficient.py --mode streaming"
        )
        return

    print(f"✅ Found active extraction: {output_file.name}\n")
    print("Monitoring progress... (Press Ctrl+C to stop)\n")
    print("=" * 80)

    # Monitoring variables
    total_municipalities = 5570  # Approximate total for Brazil
    start_time = time.time()
    last_count = 0
    last_update_time = time.time()
    rates = []  # Track processing rates

    try:
        while True:
            clear_screen()

            # Get current stats
            current_count = count_lines(output_file)
            file_size = get_file_size(output_file)
            elapsed_time = time.time() - start_time

            # Calculate rate
            if current_count > last_count:
                time_diff = time.time() - last_update_time
                if time_diff > 0:
                    rate = (current_count - last_count) / time_diff
                    rates.append(rate)
                    if len(rates) > 10:  # Keep last 10 rates
                        rates.pop(0)
                last_count = current_count
                last_update_time = time.time()

            # Calculate average rate
            avg_rate = sum(rates) / len(rates) if rates else 0

            # Calculate estimates
            progress_pct = (
                (current_count / total_municipalities) * 100
                if total_municipalities > 0
                else 0
            )
            remaining = total_municipalities - current_count

            if avg_rate > 0:
                eta_seconds = remaining / avg_rate
                eta_time = datetime.now() + timedelta(seconds=eta_seconds)
            else:
                eta_seconds = 0
                eta_time = None

            # Display header
            print("🛰️  SATELLITE DATA COLLECTION MONITOR")
            print("=" * 80)
            print(f"📁 Output File: {output_file.name}")
            print(
                f"⏰ Started: {datetime.fromtimestamp(output_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}"
            )
            print("=" * 80)

            # Progress bar
            bar_length = 50
            filled_length = int(bar_length * progress_pct / 100)
            bar = "█" * filled_length + "░" * (bar_length - filled_length)
            print(f"\n📊 Progress: [{bar}] {progress_pct:.1f}%")

            # Statistics
            print(f"\n📈 Statistics:")
            print(
                f"   Municipalities Processed: {current_count:,} / {total_municipalities:,}"
            )
            print(f"   Remaining: {remaining:,}")
            print(f"   File Size: {file_size:.2f} MB")
            print(f"   Elapsed Time: {format_time(elapsed_time)}")

            if avg_rate > 0:
                print(f"\n⚡ Performance:")
                print(f"   Processing Rate: {avg_rate:.2f} municipalities/second")
                print(f"   Estimated Time Remaining: {format_time(eta_seconds)}")
                if eta_time:
                    print(
                        f"   Estimated Completion: {eta_time.strftime('%Y-%m-%d %H:%M:%S')}"
                    )

            # Recent activity
            print(f"\n📝 Recent Activity:")
            log_entries = get_latest_log_entries(5)
            for entry in log_entries:
                # Extract just the message part (after the log level)
                if "|" in entry:
                    parts = entry.split("|")
                    if len(parts) >= 3:
                        message = parts[-1].strip()
                        # Truncate if too long
                        if len(message) > 70:
                            message = message[:67] + "..."
                        print(f"   • {message}")

            # Status indicators
            print(f"\n💡 Status:")
            if current_count == 0:
                print("   ⏳ Initializing...")
            elif avg_rate > 0:
                print("   ✅ Running smoothly")
            else:
                print("   ⚠️  Waiting for updates...")

            print("\n" + "=" * 80)
            print("Press Ctrl+C to stop monitoring (extraction will continue)")
            print("=" * 80)

            # Update every 2 seconds
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n\n✅ Monitoring stopped. Extraction continues in background.")
        print(f"\n📊 Final Stats:")
        print(f"   Processed: {current_count:,} municipalities")
        print(f"   Progress: {progress_pct:.1f}%")
        print(f"   Output: {output_file}")
        print("\nTo resume monitoring, run: python monitor_progress.py")


if __name__ == "__main__":
    try:
        monitor_progress()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure the extraction script is running first!")
