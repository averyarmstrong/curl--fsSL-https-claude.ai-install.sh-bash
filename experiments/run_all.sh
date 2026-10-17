#!/bin/bash
# Sequential chain of every experiment (each resumes from its parquet). Logs in each results/.
cd "$(dirname "$0")/.."
W=${1:-4}
for d in 001_midsize_isoC_60mph_load_sweep 002_roads_speeds_vehicles 004_transmission_ratio 005_bias_ratio_travel 006_flywheel_tornado 003_class8; do
  echo "=== $(date -u +%H:%M:%S) start $d" >> experiments/chain.log
  python3 experiments/$d/run.py --workers $W > experiments/$d/results/stdout.log 2>&1 || echo "FAILED $d" >> experiments/chain.log
  echo "=== $(date -u +%H:%M:%S) end $d" >> experiments/chain.log
done
echo "=== CHAIN DONE" >> experiments/chain.log
