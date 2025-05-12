#!/bin/bash
git pull
python3 run_tests.py
python3 generate_report.py
git add README.md report/*.png
git commit -m 'auto: update charts'
git push
