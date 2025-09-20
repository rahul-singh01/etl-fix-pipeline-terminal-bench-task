#!/usr/bin/env bash
set -euo pipefail

# WRONG: assumes bytes is always $10 and does not produce header, does not sort correctly
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <input-log> <output-csv>"
  exit 2
fi

infile="$1"
outfile="$2"
mkdir -p "$(dirname "$outfile")"

# naive extraction (buggy for quoted requests and certain log shapes)
awk '{ ip=$1; bytes=$10; if(bytes=="-") bytes=0; print ip "," bytes }' "$infile" \
  | sort \
  | awk -F, '{ arr[$1] += $2 } END { for (i in arr) print i "," arr[i] }' \
  > "$outfile"
