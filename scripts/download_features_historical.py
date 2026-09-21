#!/usr/bin/env python3
"""Download environmental feature sources: historical mode."""
import sys
from feature_download import main

if __name__ == "__main__":
    sys.exit(main(mode="historical"))
