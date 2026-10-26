#!/usr/bin/env python3
"""
Dead Internet Simulator - Main entry point
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))
import safe_random  # Safe random wrapper

from dead_internet_simulator.app import DeadInternetApp


def main():
    try:
        app = DeadInternetApp()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
