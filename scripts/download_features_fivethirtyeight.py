#!/usr/bin/env python3
"""Import/download a verified legacy FiveThirtyEight approval archive."""
import sys
from feature_download import main

if __name__ == "__main__":
    sys.exit(main(source="fivethirtyeight"))
