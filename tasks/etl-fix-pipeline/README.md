# ETL Fix Pipeline - Terminal-Bench Task

[![Terminal-Bench](https://img.shields.io/badge/Terminal--Bench-ETL%20Task-blue)](https://github.com/terminal-bench)
[![Shell](https://img.shields.io/badge/Shell-Bash%2FAWK-green)](https://www.gnu.org/software/bash/)
[![Tests](https://img.shields.io/badge/Tests-6%20Cases-brightgreen)](./tests/)

## Overview

This is a **Terminal-Bench** style engineering task that challenges you to fix a broken ETL (Extract, Transform, Load) shell script. The task simulates a real-world scenario where you need to debug and repair a data processing pipeline that aggregates webserver access logs.

### The Challenge

You are given a baseline shell script (`processor.sh`) that is **intentionally broken**. Your mission is to fix it so that it correctly processes Common Log Format webserver logs and produces accurate CSV reports of bytes transferred per client IP.

---

## Architecture & Tech Stack

### **Core Technologies**
- **Shell Scripting**: Bash for orchestration and control flow
- **Text Processing**: GNU AWK (gawk) for log parsing and aggregation
- **Data Sorting**: Unix `sort` command for deterministic ordering
- **Testing**: Python 3 + pytest for automated validation
- **Containerization**: Docker for reproducible environments

### **System Requirements**
- **Base OS**: Ubuntu 22.04 LTS
- **Runtime**: Bash 5.x, GNU AWK 5.x, Python 3.10+
- **Memory**: < 512MB for provided datasets
- **Execution Time**: < 10 minutes for all test cases

---

## 📁 Project Structure

```
etl-fix-pipeline/
├── Dockerfile                 # Container environment definition
├── task.yaml                  # Complete task specification
├── run-tests.sh               # Test execution entrypoint
├── requirements.txt           # Python testing dependencies
├── processor.sh               # BROKEN baseline script (YOUR TARGET)
├── solution.sh                # Oracle reference solution
├── tests/
│   └── test_outputs.py           # Comprehensive test suite (6 cases)
├── data/                      # Sample webserver log files
│   ├── access_simple.log         # Basic Common Log Format entries
│   ├── access_quoted.log         # Requests with quoted commas/spaces
│   ├── access_dashbytes.log      # Responses with '-' byte counts
│   ├── access_malformed.log      # Invalid/corrupted log lines
│   └── access_blank.log          # Empty lines and edge cases
└── README.md                  # This documentation
```

---

## File-by-File Analysis

### Dockerfile
**Purpose**: Defines the containerized environment for consistent testing and execution.

**Key Features**:
- **Base Image**: Ubuntu 22.04 for stability and compatibility
- **Essential Tools**: bash, gawk, coreutils, python3, pip
- **Security**: Non-interactive installation, minimal attack surface
- **Isolation**: Oracle solution (`solution.sh`) is **NOT** copied into runtime
- **Workspace**: All task files mounted at `/workspace`

**Tech Stack**: Docker, Ubuntu, APT package manager

### task.yaml
**Purpose**: Complete task specification following Terminal-Bench standards.

**Structure**:
- **Context**: Scenario description and problem background
- **Objective**: Precise requirements for the fixed script
- **Constraints**: Allowed tools, timeouts, and technical limitations
- **Acceptance Criteria**: 6 testable requirements (AC1-AC6)
- **I/O Specification**: Input files and expected output format

**Tech Stack**: YAML configuration, structured specification

### **processor.sh** (The Broken Baseline)
**Purpose**: Intentionally flawed ETL script that students must debug and fix.

**Current Issues**:
```bash
# WRONG: assumes bytes is always $10 and does not produce header
awk '{ ip=$1; bytes=$10; if(bytes=="-") bytes=0; print ip "," bytes }' "$infile"
```

**Known Bugs**:
- ❌ No CSV header output
- ❌ Naive field parsing breaks on quoted requests
- ❌ Incorrect sorting (alphabetical instead of numerical)
- ❌ No handling of malformed lines
- ❌ Fragile field position assumptions

**Tech Stack**: Bash, AWK (buggy implementation)

### ✅ **solution.sh** (Oracle Reference)
**Purpose**: Correct implementation demonstrating proper log parsing techniques.

**Key Techniques**:
```bash
# Robust regex-based parsing
if (match($0, /^([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).*" [0-9]{3} ([0-9-]+)$/, m)) {
    ip = m[1]
    bytes = (m[2] == "-" ? 0 : m[2] + 0)
    sum[ip] += bytes
}
```

**Advanced Features**:
- ✅ Regex-based field extraction
- ✅ Proper CSV header generation
- ✅ Numerical sorting with tie-breaking
- ✅ Graceful error handling
- ✅ Common Log Format compliance

**Tech Stack**: Bash, GNU AWK with regex matching, Unix sort

### **run-tests.sh**
**Purpose**: Test execution wrapper with environment setup.

**Functionality**:
```bash
# Install dependencies silently
python3 -m pip install --user -r requirements.txt >/dev/null 2>&1 || true

# Execute test suite
python3 -m pytest -q tests/test_outputs.py
```

**Features**:
- Dependency management
- Error handling and exit code propagation
- Quiet execution for clean output

**Tech Stack**: Bash, Python pip, pytest

### **requirements.txt**
**Purpose**: Python testing dependencies specification.

**Contents**:
```
pytest==7.4.0
```

**Rationale**: Pinned version for deterministic test execution across environments.

### **tests/test_outputs.py**
**Purpose**: Comprehensive test suite validating all acceptance criteria.

**Test Cases**:
1. **`test_simple_aggregation()`**: Basic IP byte aggregation
2. **`test_quoted_request_handling()`**: Requests with commas/spaces in quotes
3. **`test_dash_bytes_treated_as_zero()`**: Handling of '-' byte values
4. **`test_ignore_malformed_lines()`**: Graceful handling of invalid entries
5. **`test_blank_lines_ignored()`**: Empty line processing
6. **`test_large_repeat_aggregation()`**: Stress test with repeated data

**Testing Strategy**:
- **Black-box testing**: Validates observable outputs only
- **Deterministic**: No randomness or external dependencies
- **Comprehensive**: Edge cases and error conditions covered
- **Clear diagnostics**: Detailed failure messages with expected vs actual

**Tech Stack**: Python 3, pytest, subprocess, tempfile

### 📊 **Data Files**

#### **access_simple.log**
**Purpose**: Basic Common Log Format entries for fundamental testing.
```
127.0.0.1 - - [10/Oct/2020:13:55:36 -0700] "GET /index.html HTTP/1.1" 200 100
192.168.0.1 - - [10/Oct/2020:13:55:37 -0700] "GET /image.png HTTP/1.1" 200 200
```

#### **access_quoted.log**
**Purpose**: Tests parsing of requests containing commas and spaces.
```
10.0.0.1 - - [10/Oct/2020:13:55:39 -0700] "GET /path,with,comma HTTP/1.1" 200 300
```

#### **access_dashbytes.log**
**Purpose**: Tests handling of '-' in byte count field.
```
10.0.0.2 - - [10/Oct/2020:13:55:40 -0700] "GET /no-bytes HTTP/1.1" 200 -
```

#### **access_malformed.log**
**Purpose**: Tests resilience against corrupted log entries.
```
bad line not in CLF
127.0.0.1 - - [10/Oct/2020:13:55:36 -0700] "GET /index.html HTTP/1.1" 200 100
```

#### **access_blank.log**
**Purpose**: Tests handling of empty lines and whitespace.

---

## 🚀 Quick Start Guide

### **Option 1: Docker (Recommended)**
```bash
# Build the container
docker build -t etl-task .

# Run tests to see current failures
docker run --rm etl-task ./run-tests.sh

# Interactive debugging session
docker run --rm -it etl-task bash
```

### **Option 2: Local Development**
```bash
# Install test dependencies
pip3 install -r requirements.txt

# Run tests
./run-tests.sh

# Debug individual test cases
bash -x processor.sh data/access_simple.log /tmp/output.csv
cat /tmp/output.csv
```

---

## 🎯 Task Objectives

### **Primary Goal**
Fix `processor.sh` to correctly process webserver logs and generate CSV reports.

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

---

## Testing & Validation

### **Running Tests**
```bash
# Execute full test suite
./run-tests.sh

# Run specific test
python3 -m pytest tests/test_outputs.py::test_simple_aggregation -v

# Debug with verbose output
python3 -m pytest tests/test_outputs.py -v -s
```

### **Test Results Interpretation**
- **✅ PASSED**: All acceptance criteria met
- **❌ FAILED**: Specific failure with expected vs actual output
- **💥 ERROR**: Script execution failure or crash

### **Debugging Tips**
```bash
# Trace script execution
bash -x processor.sh data/access_simple.log /tmp/debug.csv

# Compare with oracle solution
./solution.sh data/access_simple.log /tmp/oracle.csv
diff /tmp/debug.csv /tmp/oracle.csv

# Validate individual log parsing
awk 'your_parsing_logic' data/access_simple.log
```

---

## 🛠️ Development Guidelines

### **Allowed Tools**
- ✅ **bash**: Script orchestration and control flow
- ✅ **awk/gawk**: Text processing and field extraction
- ✅ **coreutils**: sort, cut, grep, sed, etc.
- ❌ **Python**: Not allowed for core ETL logic (tests only)
- ❌ **External APIs**: Must work offline

### **Best Practices**
1. **Error Handling**: Use `set -euo pipefail` for robust scripts
2. **Field Parsing**: Use regex for reliable Common Log Format parsing
3. **Data Validation**: Handle edge cases gracefully
4. **Performance**: Optimize for reasonable execution time
5. **Maintainability**: Write clear, commented code

### **Common Pitfalls**
- **Field Position Assumptions**: CLF fields can vary with quoted content
- **Sorting Logic**: Ensure numerical sorting, not lexicographical
- **Header Generation**: Don't forget CSV header row
- **Error Propagation**: Handle malformed lines without script failure

---

## 📊 Performance Characteristics

### **Baseline Performance**
- **Dataset Size**: 5 sample files, ~1KB total
- **Execution Time**: < 1 second for all tests
- **Memory Usage**: < 10MB peak
- **Scalability**: Linear with log file size

### **Expected Improvements**
- **Correctness**: 0% → 100% test pass rate
- **Robustness**: Handle all edge cases gracefully
- **Maintainability**: Clean, readable parsing logic

---

## 🔧 Troubleshooting

### **Common Issues**

#### **Tests Fail with "No such file"**
```bash
# Ensure run-tests.sh is executable
chmod +x run-tests.sh

# Check file paths are correct
ls -la processor.sh data/
```

#### **AWK Parsing Errors**
```bash
# Test AWK syntax separately
echo "test line" | awk 'your_pattern { print "works" }'

# Use gawk for advanced regex features
gawk --version
```

#### **Sorting Issues**
```bash
# Test sort behavior
echo -e "192.168.1.1,100\n10.0.0.1,200" | sort -t, -k2,2nr -k1,1
```

#### **Docker Build Failures**
```bash
# Clean Docker cache
docker system prune -f

# Build with verbose output
docker build --no-cache -t etl-task .
```

---

## 📈 Success Metrics

### **Completion Criteria**
- ✅ All 6 tests pass (`./run-tests.sh` exits with code 0)
- ✅ Output matches expected CSV format exactly
- ✅ Script handles all edge cases gracefully
- ✅ Code is readable and maintainable

### **Quality Indicators**
- **Correctness**: 100% test pass rate
- **Robustness**: No crashes on malformed input
- **Performance**: Execution time < 10 seconds
- **Code Quality**: Clear logic and proper error handling

---

## 🤝 Contributing

This is a Terminal-Bench educational task. Focus on:
1. **Understanding** the Common Log Format specification
2. **Debugging** the existing broken implementation
3. **Implementing** robust parsing with AWK regex
4. **Testing** your solution against all provided cases

---

## 📚 References

- [Common Log Format Specification](https://en.wikipedia.org/wiki/Common_Log_Format)
- [GNU AWK Manual](https://www.gnu.org/software/gawk/manual/)
- [Bash Scripting Guide](https://tldp.org/LDP/abs/html/)

---

**Happy Debugging! 🐛→✨**
