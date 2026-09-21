#!/usr/bin/env python3
"""Download silver_bulletin feature sources in historical or current mode."""
import sys
from feature_download import main

if __name__ == "__main__":
    sys.exit(main(source="silver_bulletin"))
