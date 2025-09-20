import subprocess
import tempfile
import os
import filecmp
import textwrap
import pytest

TASK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROCESSOR = os.path.join(TASK_DIR, "processor.sh")

def run_proc(input_rel, expected_content):
    outdir = tempfile.mkdtemp(prefix="etltest_")
    outfile = os.path.join(outdir, "top_ips.csv")
    cmd = ["bash", PROCESSOR, os.path.join(TASK_DIR, input_rel), outfile]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise AssertionError(f"processor.sh exited {res.returncode}\nstderr:\n{res.stderr}")
    with open(outfile, "r") as f:
        got = f.read().strip()
    expected = textwrap.dedent(expected_content).strip()
    assert got == expected, f"\nExpected:\n{expected}\n\nGot:\n{got}\n"

def test_simple_aggregation():
    expected = """\
    ip,total_bytes
    192.168.0.1,200
    127.0.0.1,150
    """
    run_proc("data/access_simple.log", expected)

def test_quoted_request_handling():
    expected = """\
    ip,total_bytes
    10.0.0.1,300
    127.0.0.1,100
    """
    run_proc("data/access_quoted.log", expected)

def test_dash_bytes_treated_as_zero():
    expected = """\
    ip,total_bytes
    192.168.0.1,200
    10.0.0.2,0
    """
    run_proc("data/access_dashbytes.log", expected)

def test_ignore_malformed_lines():
    expected = """\
    ip,total_bytes
    127.0.0.1,100
    """
    run_proc("data/access_malformed.log", expected)

def test_blank_lines_ignored():
    expected = """\
    ip,total_bytes
    127.0.0.1,50
    """
    run_proc("data/access_blank.log", expected)

def test_large_repeat_aggregation():
    # Generate a temporary input with repeated lines to test aggregation determinism and sum
    tmp_in = os.path.join(TASK_DIR, "data", "temp_repeat.log")
    with open(tmp_in, "w") as f:
        for _ in range(100):
            f.write('203.0.113.5 - - [10/Oct/2020:14:00:00 -0700] "GET /x HTTP/1.1" 200 7\n')
    expected = """\
    ip,total_bytes
    203.0.113.5,700
    """
    run_proc("data/temp_repeat.log", expected)
    os.remove(tmp_in)
