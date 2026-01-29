"""
Compare Memory Usage Between Extraction Methods

This script demonstrates the memory difference between standard and
memory-efficient extraction approaches.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.utils.memory_utils import MemoryMonitor, log_system_memory
from loguru import logger


def simulate_standard_approach(num_records: int = 1000):
    """
    Simulate standard extraction approach (accumulate in memory).

    Args:
        num_records: Number of records to simulate
    """
    logger.info(f"=== Simulating Standard Approach ({num_records} records) ===")

    monitor = MemoryMonitor()
    monitor.log_memory_usage("start")

    # Simulate accumulating data in memory
    results = []
    for i in range(num_records):
        # Simulate a record with 64 embeddings
        record = {
            "municipality_id": f"ID_{i}",
            "municipality_name": f"City_{i}",
            "state_name": f"State_{i % 27}",
            **{f"embedding_{j}": float(j) for j in range(64)},
            "extraction_date": "2026-01-28",
        }
        results.append(record)

        if (i + 1) % 100 == 0:
            monitor.log_memory_usage(f"after {i+1} records")

    logger.info(f"Total records in memory: {len(results)}")
    monitor.log_memory_usage("end (all in memory)")

    # Clear memory
    del results
    monitor.force_garbage_collection()
    monitor.log_memory_usage("after cleanup")


def simulate_efficient_approach(num_records: int = 1000):
    """
    Simulate memory-efficient extraction approach (streaming writes).

    Args:
        num_records: Number of records to simulate
    """
    logger.info(f"=== Simulating Memory-Efficient Approach ({num_records} records) ===")

    monitor = MemoryMonitor()
    monitor.log_memory_usage("start")

    # Simulate streaming writes
    import csv
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        fieldnames = ["municipality_id", "municipality_name", "state_name"]
        fieldnames.extend([f"embedding_{j}" for j in range(64)])
        fieldnames.append("extraction_date")

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(num_records):
            # Simulate a record
            record = {
                "municipality_id": f"ID_{i}",
                "municipality_name": f"City_{i}",
                "state_name": f"State_{i % 27}",
                **{f"embedding_{j}": float(j) for j in range(64)},
                "extraction_date": "2026-01-28",
            }

            # Write immediately
            writer.writerow(record)

            # Clear record from memory
            del record

            if (i + 1) % 100 == 0:
                monitor.log_memory_usage(f"after {i+1} records")
                f.flush()

            # Periodic garbage collection
            if (i + 1) % 50 == 0:
                monitor.force_garbage_collection()

    monitor.log_memory_usage("end (streaming)")
    logger.info(f"Data written to temporary file (not in memory)")


def main():
    """Run comparison."""
    logger.info("=" * 70)
    logger.info("Memory Usage Comparison: Standard vs Memory-Efficient")
    logger.info("=" * 70)

    # Show system memory
    log_system_memory()

    print("\n")

    # Test with different dataset sizes
    for num_records in [100, 500, 1000]:
        logger.info(f"\n{'='*70}")
        logger.info(f"Testing with {num_records} records")
        logger.info(f"{'='*70}\n")

        # Standard approach
        simulate_standard_approach(num_records)

        print("\n")

        # Efficient approach
        simulate_efficient_approach(num_records)

        print("\n")

    logger.info("=" * 70)
    logger.info("Comparison Complete")
    logger.info("=" * 70)
    logger.info("\nKey Observations:")
    logger.info("1. Standard approach: Memory grows with dataset size")
    logger.info("2. Efficient approach: Memory stays relatively constant")
    logger.info(
        "3. For large datasets (5000+ records), efficient approach is essential"
    )
    logger.info("\nRecommendation: Use extract_embeddings_efficient.py for production")


if __name__ == "__main__":
    main()
