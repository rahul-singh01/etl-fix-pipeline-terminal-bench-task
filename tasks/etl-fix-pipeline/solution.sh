#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <input-log> <output-csv>"
  exit 2
fi

infile="$1"
outfile="$2"
mkdir -p "$(dirname "$outfile")"

echo "ip,total_bytes" > "$outfile"

# Use awk with regex to capture IP and bytes robustly (handles quoted requests and '-' bytes)
gawk 'BEGIN { FS = "\n" }
{
  # Common Log Format: IP ... "REQUEST" STATUS BYTES
  # Extract IP and bytes using regex anchored to line end
  if (match($0, /^([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).*" [0-9]{3} ([0-9-]+)$/, m)) {
    ip = m[1]
    bytes = (m[2] == "-" ? 0 : m[2] + 0)
    sum[ip] += bytes
  }
}
END {
  for (i in sum) {
    printf "%s,%d\n", i, sum[i]
  }
}' "$infile" \
  | sort -t, -k2,2nr -k1,1 \
  >> "$outfile"
