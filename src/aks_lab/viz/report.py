"""`make report`: regenerate every experiment's figures and tables from its parquet (no simulation)."""

from __future__ import annotations

import importlib.util
import pathlib
import sys

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[3]
EXP = ROOT / "experiments"


def main():
    sys.path.insert(0, str(EXP))
    done = []
    for d in sorted(p for p in EXP.iterdir() if p.is_dir() and p.name[:3].isdigit()):
        pq = d / "results" / "results.parquet"
        if not pq.exists():
            print(f"skip {d.name}: no results.parquet")
            continue
        spec = importlib.util.spec_from_file_location(f"run_{d.name}", d / "run.py")
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        m.analyse(pd.read_parquet(pq))
        done.append(d.name)
    sizing = ROOT / "reports" / "component_sizing.py"
    if sizing.exists():
        spec = importlib.util.spec_from_file_location("sizing", sizing)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        m.main()
    print("report regenerated for:", ", ".join(done))


if __name__ == "__main__":
    main()
