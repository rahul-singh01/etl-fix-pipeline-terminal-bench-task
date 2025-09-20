# ETL Fix Pipeline - Terminal-Bench Task

## Summary
**Task ID:** (5) etl-fix-pipeline  
**Domain:** Terminal-Heavy ETL / Data Workloads  
**Description:** Fix a broken shell script that processes webserver access logs to aggregate response bytes per client IP and produce a properly formatted CSV report.

## The Challenge
You are given a baseline shell script (`processor.sh`) that is **intentionally broken**. Your mission is to fix it so that it correctly processes Common Log Format webserver logs and produces accurate CSV reports of bytes transferred per client IP.

## Quick Start

### **For Solvers (Docker - Recommended)**
```bash
# Build and test
docker build -t etl-task .
docker run --rm etl-task ./run-tests.sh  # Should fail (baseline broken)

# Test your fixed processor.sh
docker run --rm -v "$(pwd)/processor.sh:/workspace/processor.sh" etl-task ./run-tests.sh
```

### **For Task Authors (Local Development)**
```bash
# Virtual environment approach
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Verify oracle works (should pass 100%)
cp solution.sh processor.sh && ./run-tests.sh

# Verify baseline fails
git checkout processor.sh && ./run-tests.sh
deactivate
```

## Task Objectives

### **Expected Output Format**
```csv
ip,total_bytes
192.168.0.1,200
127.0.0.1,150
10.0.0.2,0
```

### **Acceptance Criteria**
- **AC1**: Produces CSV file with header `"ip,total_bytes"`
- **AC2**: Correctly aggregates bytes per IP (treat `'-'` as `0`)
- **AC3**: Handles requests containing spaces or commas in quotes
- **AC4**: Ignores malformed or empty lines without crashing
- **AC5**: Output sorted by `total_bytes` desc, tie-break by `ip` asc
- **AC6**: All provided sample inputs covered by tests (≥6 tests)

## Project Structure
```
etl-fix-pipeline/
├── Dockerfile                 # Container environment
├── task.yaml                  # Complete task specification
├── run-tests.sh               # Test execution entrypoint
├── requirements.txt           # Python testing dependencies
├── processor.sh               # BROKEN baseline script (YOUR TARGET)
├── solution.sh                # Oracle reference solution
├── tests/test_outputs.py      # 6 comprehensive test cases
└── data/                      # Sample webserver log files
    ├── access_simple.log      # Basic Common Log Format entries
    ├── access_quoted.log      # Requests with quoted commas/spaces
    ├── access_dashbytes.log   # Responses with '-' byte counts
    ├── access_malformed.log   # Invalid/corrupted log lines
    └── access_blank.log       # Empty lines and edge cases
```

## Known Issues in Baseline
The broken `processor.sh` has several bugs:
- ❌ No CSV header output
- ❌ Naive field parsing breaks on quoted requests  
- ❌ Incorrect sorting (alphabetical instead of numerical)
- ❌ No handling of malformed lines
- ❌ Fragile field position assumptions

## Development Guidelines
- **Allowed Tools**: bash, awk/gawk, coreutils, sed, sort (no Python for core ETL)
- **Key Challenge**: Robust Common Log Format parsing with regex
- **Performance**: < 10 minutes runtime, reasonable memory usage
- **Testing**: 6 deterministic tests covering all edge cases

## Caveats
- Baseline `processor.sh` is intentionally broken (fails all tests)
- Core logic must use shell/awk (no Python)
- Oracle solution (`solution.sh`) is excluded from Docker runtime
- Tests require deterministic, offline execution

## Terminal-Bench Evaluation Checklist
- ✅ Domain chosen: Terminal-Heavy ETL / Data Workloads
- ✅ Self-contained task.yaml with Context, Objectives, Constraints (max_agent_timeout_sec: 300, max_test_timeout_sec: 120), Acceptance Criteria → Tests mapping, Inputs/Materials, Outputs
- ✅ ≥6 deterministic tests covering criteria + edge cases; clear failure messages
- ✅ run-tests.sh works and exits non-zero on any failure
- ✅ Oracle passes 100%; baseline fails (~0%)
- ✅ Core workload not Python (tests may be Python)
- ✅ No network access; all inputs bundled; versions pinned; no privileged Docker flags
- ✅ Reproducible build (Dockerfile pins toolchain/deps); runtime < 10 minutes; reasonable memory
- ✅ Solution not copied/invoked in runtime/tests
- ✅ README.md ≤1 page: summary, domain, quickstart, caveats, and this checklist
- ✅ Zip structure exactly as specified under tasks/<task-id>/
- ✅ Determinism check: repeated runs yield identical results
