"""
Memory Profiling Utilities

Tools for monitoring and optimizing memory usage during data extraction.
"""

import psutil
import os
from loguru import logger
from functools import wraps
from typing import Callable
import gc


class MemoryMonitor:
    """Monitor memory usage during execution."""

    def __init__(self):
        """Initialize memory monitor."""
        self.process = psutil.Process(os.getpid())
        self.initial_memory = self.get_memory_usage()

    def get_memory_usage(self) -> float:
        """
        Get current memory usage in MB.

        Returns:
            float: Memory usage in megabytes
        """
        return self.process.memory_info().rss / 1024 / 1024

    def get_memory_percent(self) -> float:
        """
        Get memory usage as percentage of total system memory.

        Returns:
            float: Memory usage percentage
        """
        return self.process.memory_percent()

    def log_memory_usage(self, label: str = ""):
        """
        Log current memory usage.

        Args:
            label: Optional label for the log message
        """
        current_memory = self.get_memory_usage()
        memory_percent = self.get_memory_percent()
        memory_delta = current_memory - self.initial_memory

        logger.info(
            f"Memory {label}: {current_memory:.2f} MB "
            f"({memory_percent:.1f}% of system) "
            f"[Δ {memory_delta:+.2f} MB]"
        )

    def check_memory_threshold(self, threshold_mb: float = 1000) -> bool:
        """
        Check if memory usage exceeds threshold.

        Args:
            threshold_mb: Memory threshold in megabytes

        Returns:
            bool: True if memory usage exceeds threshold
        """
        current_memory = self.get_memory_usage()
        if current_memory > threshold_mb:
            logger.warning(
                f"Memory usage ({current_memory:.2f} MB) exceeds threshold ({threshold_mb} MB)"
            )
            return True
        return False

    def force_garbage_collection(self):
        """Force garbage collection and log memory freed."""
        before = self.get_memory_usage()
        gc.collect()
        after = self.get_memory_usage()
        freed = before - after

        logger.info(f"Garbage collection freed {freed:.2f} MB")
        return freed


def memory_profile(func: Callable) -> Callable:
    """
    Decorator to profile memory usage of a function.

    Args:
        func: Function to profile

    Returns:
        Wrapped function with memory profiling
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        monitor = MemoryMonitor()

        logger.info(f"Starting {func.__name__}")
        monitor.log_memory_usage("before")

        try:
            result = func(*args, **kwargs)

            monitor.log_memory_usage("after")
            return result

        except Exception as e:
            monitor.log_memory_usage("on error")
            raise

        finally:
            # Force garbage collection
            monitor.force_garbage_collection()

    return wrapper


def get_system_memory_info():
    """
    Get system memory information.

    Returns:
        dict: System memory statistics
    """
    virtual_mem = psutil.virtual_memory()

    info = {
        "total_mb": virtual_mem.total / 1024 / 1024,
        "available_mb": virtual_mem.available / 1024 / 1024,
        "used_mb": virtual_mem.used / 1024 / 1024,
        "percent_used": virtual_mem.percent,
        "free_mb": virtual_mem.free / 1024 / 1024,
    }

    return info


def log_system_memory():
    """Log system memory information."""
    info = get_system_memory_info()

    logger.info("System Memory:")
    logger.info(f"  Total: {info['total_mb']:.2f} MB")
    logger.info(f"  Available: {info['available_mb']:.2f} MB")
    logger.info(f"  Used: {info['used_mb']:.2f} MB ({info['percent_used']:.1f}%)")
    logger.info(f"  Free: {info['free_mb']:.2f} MB")


def optimize_memory_settings():
    """
    Optimize Python memory settings for large-scale processing.

    Returns:
        dict: Applied settings
    """
    import sys

    settings = {}

    # Set garbage collection thresholds
    # More aggressive garbage collection
    gc.set_threshold(700, 10, 10)  # Default is (700, 10, 10)
    settings["gc_threshold"] = gc.get_threshold()

    # Log settings
    logger.info("Memory optimization settings applied:")
    logger.info(f"  GC threshold: {settings['gc_threshold']}")
    logger.info(f"  Python recursion limit: {sys.getrecursionlimit()}")

    return settings


class MemoryLimitExceeded(Exception):
    """Exception raised when memory limit is exceeded."""

    pass


class MemoryGuard:
    """
    Context manager to guard against excessive memory usage.

    Example:
        with MemoryGuard(max_memory_mb=500):
            # Your memory-intensive code here
            process_large_dataset()
    """

    def __init__(self, max_memory_mb: float = 1000, check_interval: int = 10):
        """
        Initialize memory guard.

        Args:
            max_memory_mb: Maximum allowed memory in MB
            check_interval: Check memory every N operations
        """
        self.max_memory_mb = max_memory_mb
        self.check_interval = check_interval
        self.monitor = MemoryMonitor()
        self.operation_count = 0

    def __enter__(self):
        """Enter context."""
        self.monitor.log_memory_usage("guard start")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context."""
        self.monitor.log_memory_usage("guard end")
        self.monitor.force_garbage_collection()

    def check(self):
        """Check if memory usage is within limits."""
        self.operation_count += 1

        if self.operation_count % self.check_interval == 0:
            current_memory = self.monitor.get_memory_usage()

            if current_memory > self.max_memory_mb:
                raise MemoryLimitExceeded(
                    f"Memory usage ({current_memory:.2f} MB) exceeds limit ({self.max_memory_mb} MB)"
                )
