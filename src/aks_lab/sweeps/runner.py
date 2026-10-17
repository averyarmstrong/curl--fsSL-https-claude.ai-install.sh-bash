"""Parallel sweep runner: multiprocessing, incremental parquet, resumable, logged."""

from __future__ import annotations

import json
import logging
import os
import pathlib
import time
from multiprocessing import Pool

import pandas as pd

from .cases import case_id, run_case

log = logging.getLogger("aks_lab.sweeps")


def _setup_log(out_dir: pathlib.Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[logging.FileHandler(out_dir / "run.log"), logging.StreamHandler()])


def run_sweep(cases: list[dict], out_dir, workers: int | None = None, chunk: int = 8,
              resume: bool = True) -> pd.DataFrame:
    """Run all cases, appending results to <out_dir>/results.parquet as they finish."""
    out_dir = pathlib.Path(out_dir)
    _setup_log(out_dir)
    parquet = out_dir / "results.parquet"
    done: set[str] = set()
    rows: list[dict] = []
    if resume and parquet.exists():
        prev = pd.read_parquet(parquet)
        prev = prev[prev.get("error").isna()] if "error" in prev else prev
        done = set(prev["case_id"])
        rows = prev.to_dict("records")
        log.info("resuming: %d cases already done", len(done))
    todo = [c for c in cases if case_id(c) not in done]
    (out_dir / "cases.json").write_text(json.dumps(cases, indent=1, default=str))
    workers = workers or os.cpu_count() or 1
    log.info("sweep: %d cases (%d to run) on %d workers", len(cases), len(todo), workers)
    t0 = time.time()
    n_done, n_err = 0, 0
    with Pool(workers) as pool:
        for row in pool.imap_unordered(run_case, todo, chunksize=1):
            rows.append(row)
            n_done += 1
            if row.get("error"):
                n_err += 1
                log.warning("case %s failed: %s", row["case_id"], row["error"])
            if n_done % chunk == 0 or n_done == len(todo):
                pd.DataFrame(rows).to_parquet(parquet, index=False)
                el = time.time() - t0
                log.info("%d/%d done, %d errors, %.0f s elapsed, ~%.0f s left",
                         n_done, len(todo), n_err, el, el / n_done * (len(todo) - n_done))
    df = pd.DataFrame(rows)
    df.to_parquet(parquet, index=False)
    log.info("sweep finished: %d rows, %d errors, %.0f s", len(df), n_err, time.time() - t0)
    return df


def grid(**axes) -> list[dict]:
    """Cartesian product of keyword lists -> list of dicts."""
    import itertools
    keys = list(axes)
    return [dict(zip(keys, vals)) for vals in itertools.product(*[axes[k] for k in keys])]
