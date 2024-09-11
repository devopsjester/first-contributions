#!/bin/bash

# Check if API_ACCESS_TOKEN is set
if [ -z "$API_ACCESS_TOKEN" ]; then
  echo "Error: API_ACCESS_TOKEN environment variable is not set."
  exit 1
fi

# Check if the organization name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <organization_name> [output_file]"
  exit 1
fi

ORG_NAME=$1
OUTPUT_FILE=$2

# Run the Python script
if [ -z "$OUTPUT_FILE" ]; then
  python3 graph_first_commit.py "$ORG_NAME"
else
  python3 graph_first_commit.py "$ORG_NAME" --output "$ORG_NAME-$OUTPUT_FILE"
fi