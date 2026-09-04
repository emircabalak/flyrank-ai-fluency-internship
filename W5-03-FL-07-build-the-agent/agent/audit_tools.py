"""Computational helpers the auditor calls. These measure, they do not judge.

Every verdict in a report is written by the agent after reading this output. Nothing here
decides anything, which is deliberate: I want the judgment in the part I can argue with.
"""

import itertools

import numpy as np
import pandas as pd


def structure(df):
    out = []
    for c in df.columns:
        s = df[c]
        zeros = int((s == 0).sum()) if pd.api.types.is_numeric_dtype(s) else 0
        out.append(
            dict(
                column=c,
                dtype=str(s.dtype),
                nulls=int(s.isna().sum()),
                distinct=int(s.nunique(dropna=True)),
                zeros=zeros,
                sample_min=s.min() if pd.api.types.is_numeric_dtype(s) else "",
                sample_max=s.max() if pd.api.types.is_numeric_dtype(s) else "",
            )
        )
    return pd.DataFrame(out)


def single_column_signal(df, label):
    y = df[label]
    rows = []
    for c in df.columns:
        if c == label:
            continue
        s = df[c]
        if pd.api.types.is_numeric_dtype(s):
            rows.append(dict(column=c, corr=round(float(s.corr(y)), 4)))
        else:
            g = y.groupby(s.astype("string")).mean()
            spread = float(g.max() - g.min()) if len(g) > 1 else 0.0
            rows.append(dict(column=c, corr=np.nan, label_rate_spread=round(spread, 4)))
    return pd.DataFrame(rows).sort_values("corr", key=lambda s: s.abs(), ascending=False)


def pair_reconstruction(df, label, threshold, min_coverage=0.8):
    """Every ordered pair of numeric columns, tested as a ratio against the label threshold.

    A high agreement means the two columns together rebuild the quantity the label is a
    threshold on, which no single-column check will ever surface.
    """
    y = df[label]
    # Guessing the majority class already scores this. Any agreement at or near the baseline
    # is nothing, and without it on the page a 0.70 looks like a finding when it is chance.
    baseline = float(max(y.mean(), 1 - y.mean()))
    num = [c for c in df.select_dtypes("number").columns if c != label]
    found = []
    for a, b in itertools.permutations(num, 2):
        r = df[a] / df[b].replace(0, np.nan)
        m = r.notna() & y.notna()
        if m.sum() < len(df) * min_coverage:
            continue
        agree = float(((r[m] < threshold).astype(float) == y[m]).mean())
        found.append(
            dict(
                numerator=a,
                denominator=b,
                agreement=round(agree, 4),
                over_baseline=round(agree - baseline, 4),
                rows=int(m.sum()),
            )
        )
    out = pd.DataFrame(found).sort_values("agreement", ascending=False).reset_index(drop=True)
    out.attrs["baseline"] = round(baseline, 4)
    return out


def sentinel_check(df):
    """A zero that is really a missing marker usually sits apart from the rest of the
    distribution. This flags numeric columns whose zeros look implanted rather than earned."""
    rows = []
    for c in df.select_dtypes("number").columns:
        s = df[c].dropna()
        z = int((s == 0).sum())
        if z == 0:
            continue
        nonzero = s[s != 0]
        gap = float(nonzero.min()) if len(nonzero) else float("nan")
        rows.append(
            dict(
                column=c,
                zeros=z,
                zero_share=round(z / len(s), 4),
                smallest_nonzero=round(gap, 4),
                looks_like_sentinel=bool(gap > 1.0 and z / len(s) > 0.01),
            )
        )
    return pd.DataFrame(rows)


def three_state_flags(df):
    rows = []
    for c in df.columns:
        vals = set(df[c].dropna().unique().tolist())
        if vals <= {True, False} and df[c].isna().any():
            rows.append(dict(column=c, nulls=int(df[c].isna().sum()), note="true/false/null"))
    return pd.DataFrame(rows)


def population_check(df, label, entity, time_col):
    """Is the row set itself selected on something from the outcome window?

    An unfiltered panel has a roughly rectangular shape per entity. Rows dropped in a pattern
    that tracks the outcome show up as an uneven per-entity count and a label rate that moves
    with it.
    """
    per = df.groupby(entity).agg(rows=(time_col, "count"), label_rate=(label, "mean"))
    months = df[time_col].nunique()
    return dict(
        entities=int(len(per)),
        distinct_periods=int(months),
        rows=int(len(df)),
        rows_if_rectangular=int(len(per) * months),
        completeness=round(len(df) / (len(per) * months), 4),
        rows_per_entity_min=int(per["rows"].min()),
        rows_per_entity_max=int(per["rows"].max()),
        corr_rows_vs_label_rate=round(float(per["rows"].corr(per["label_rate"])), 4),
        overall_label_rate=round(float(df[label].mean()), 4),
    )


def report(path, label, threshold, entity="client_id", time_col="month"):
    df = pd.read_csv(path)
    print(f"### {path}   {len(df)} rows, {len(df.columns)} columns\n")
    print("-- structure --");            print(structure(df).to_string(index=False), "\n")
    print("-- single-column signal --"); print(single_column_signal(df, label).to_string(index=False), "\n")
    pr = pair_reconstruction(df, label, threshold)
    print(f"-- pair reconstruction, top 5 (majority-class baseline {pr.attrs['baseline']}) --")
    print(pr.head(5).to_string(index=False), "\n")
    print("-- sentinel candidates --");  print(sentinel_check(df).to_string(index=False), "\n")
    print("-- three-state flags --")
    tsf = three_state_flags(df)
    print((tsf.to_string(index=False) if len(tsf) else "  none"), "\n")
    print("-- population --")
    for k, v in population_check(df, label, entity, time_col).items():
        print(f"   {k:28s} {v}")
    return df
