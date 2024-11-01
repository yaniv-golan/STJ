#!/usr/bin/env python3

import argparse
import sys
from stjlib import StandardTranscriptionJSON

def main():
    parser = argparse.ArgumentParser(description="Validate an STJ file.")
    parser.add_argument('stj_file', help="Path to the STJ file to validate.")
    args = parser.parse_args()

    try:
        # Load and validate STJ file using stjlib
        stj = StandardTranscriptionJSON.from_file(args.stj_file, validate=False)
        validation_issues = stj.validate(raise_exception=False)
        
        if not validation_issues:
            print("Validation successful! No issues found.")
            sys.exit(0)
        
        # Print all validation issues in a readable format
        print("Validation failed. Found the following issues:")
        for i, issue in enumerate(validation_issues, 1):
            print(f"\n{i}. {issue}")
        
        sys.exit(1)
        
    except Exception as e:
        print(f"Error while processing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
