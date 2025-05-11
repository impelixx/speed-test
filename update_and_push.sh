#!/bin/bash
git pull
python3 report/run_tests.py
python3 report/generate_report.py
git add README.md report/*.png
git commit -m 'auto: update charts'
git push