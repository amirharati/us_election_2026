#!/usr/bin/env python3
"""Download cdc_nhsn feature sources in historical or current mode."""
import sys
from feature_download import main

if __name__ == "__main__":
    sys.exit(main(source="cdc_nhsn"))
