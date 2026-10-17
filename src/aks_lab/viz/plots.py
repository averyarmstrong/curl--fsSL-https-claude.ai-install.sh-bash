"""Figure helpers. Every figure is saved with its parameter set embedded in the PNG metadata."""

from __future__ import annotations

import json
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

plt.rcParams.update({"figure.dpi": 130, "font.size": 9, "axes.grid": True, "grid.alpha": 0.3})


def save(fig, path, params: dict | None = None, title: str | None = None):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    meta = {"Software": "aks-lab", "Description": json.dumps(params or {}, default=str)[:60000]}
    if title:
        meta["Title"] = title
    fig.savefig(path, metadata=meta, bbox_inches="tight")
    plt.close(fig)
    return path


def band(df: pd.DataFrame, x: str, y: str, group: str | None = None, q=(0.05, 0.5, 0.95)):
    """Median and quantile band of y vs x (over seeds), optionally per group."""
    out = {}
    groups = [(None, df)] if group is None else df.groupby(group)
    for g, d in groups:
        agg = d.groupby(x)[y].quantile(list(q)).unstack()
        out[g] = agg
    return out


def plot_band(ax, df, x, y, group=None, label_fmt="{}", logx=False, **kw):
    for g, agg in band(df, x, y, group).items():
        xs = agg.index.values
        ax.plot(xs, agg[0.5].values, label=label_fmt.format(g) if g is not None else None, **kw)
        ax.fill_between(xs, agg[0.05].values, agg[0.95].values, alpha=0.2)
    if logx:
        ax.set_xscale("log")
    ax.set_xlabel(x)
    ax.set_ylabel(y)


def md_table(df: pd.DataFrame, cols: list[str], fmt: dict | None = None) -> str:
    fmt = fmt or {}
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        cells = []
        for c in cols:
            v = r[c]
            if isinstance(v, (float, np.floating)):
                cells.append(fmt.get(c, "{:.3g}").format(v))
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)
