import sys
import os
import subprocess

def run_test(n_limit):
  subprocess.run(['./run_all_tests.sh', str(n_limit)])

if __name__ == "__main__":
  for limit in range(1, 2002, 1000):
    print(f"Running tests for limit: {limit}")
    run_test(limit)
    print(f"Tests completed for limit: {limit}")