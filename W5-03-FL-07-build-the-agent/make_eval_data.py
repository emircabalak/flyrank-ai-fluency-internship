"""Builds the six eval datasets for the leakage auditor.

Each case has a known ground truth, written down in evals/ground-truth.md. The point of
generating them rather than using real client data is that I can plant an exact failure and
then check whether the agent finds that one and only that one.
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(20260904)
OUT = "data"

N_CLIENTS = 120
MONTHS = 12


def base_panel():
    """One row per client per month, with plausible search-console style columns."""
    rows = []
    for c in range(N_CLIENTS):
        size = rng.lognormal(mean=6.0, sigma=1.1)
        start = rng.integers(0, 5)
        for m in range(MONTHS):
            if m < start:
                continue
            total_queries = max(20, int(size * rng.uniform(0.8, 1.2)))
            health = rng.beta(6, 3)
            queries_with_data = int(total_queries * np.clip(health + rng.normal(0, 0.06), 0.05, 1.0))
            impressions = int(total_queries * rng.uniform(8, 40))
            ctr = np.clip(rng.beta(2, 45), 0.001, 0.3)
            clicks = int(impressions * ctr)
            has_position = rng.random() > 0.12
            rows.append(
                dict(
                    client_id=f"c{c:03d}",
                    month=f"2025-{m + 1:02d}",
                    month_idx=m,
                    total_queries=total_queries,
                    queries_with_data=queries_with_data,
                    impressions=impressions,
                    clicks=clicks,
                    ctr_x100=round(ctr * 100 * 100, 2),
                    avg_position=round(rng.uniform(3, 40), 2) if has_position else 0.0,
                    gsc_data_start=f"2025-{start + 1:02d}",
                    is_ai_referral_available=rng.choice([True, False, None], p=[0.45, 0.35, 0.20]),
                )
            )
    return pd.DataFrame(rows)


def add_label(df):
    """Label at month M: does queries_with_data / total_queries drop below 0.6 at M+1."""
    df = df.sort_values(["client_id", "month_idx"]).reset_index(drop=True)
    df["_ratio"] = df["queries_with_data"] / df["total_queries"]
    df["_next_ratio"] = df.groupby("client_id")["_ratio"].shift(-1)
    df["label_visibility_drop"] = (df["_next_ratio"] < 0.6).astype("float")
    df.loc[df["_next_ratio"].isna(), "label_visibility_drop"] = np.nan
    return df.dropna(subset=["label_visibility_drop"]).reset_index(drop=True)


def case1_the_pair(df):
    """The real failure. Both components of the label ratio, from month M+1, under
    innocent names in what would have been two different source tables."""
    d = df.copy()
    nxt_qwd = d.groupby("client_id")["queries_with_data"].shift(-1)
    nxt_tot = d.groupby("client_id")["total_queries"].shift(-1)
    d["tracked_terms_returning"] = nxt_qwd          # numerator, from M+1
    d["term_universe_size"] = nxt_tot               # denominator, from M+1
    return d.dropna(subset=["tracked_terms_returning", "term_universe_size"]).reset_index(drop=True)


def case2_clean(df):
    """No leakage at all. Everything is observed at month M or earlier."""
    d = df.copy()
    d["clicks_prev_month"] = d.groupby("client_id")["clicks"].shift(1)
    d["impressions_prev_month"] = d.groupby("client_id")["impressions"].shift(1)
    d["months_of_history"] = d["month_idx"] - d.groupby("client_id")["month_idx"].transform("min")
    return d


def case3_obvious(df):
    """One column that is an arithmetic transform of the label itself."""
    d = df.copy()
    d["risk_score"] = d["label_visibility_drop"] * 100 + rng.normal(0, 0.4, len(d))
    return d


def case4_sentinel(df):
    """avg_position keeps its zeros meaning no data, and there is no data dictionary
    anywhere in the folder saying so. Nothing here leaks."""
    d = case2_clean(df)
    return d.drop(columns=["clicks_prev_month", "impressions_prev_month"])


def case5_population(df):
    """Every column is clean. The rows were filtered using a minimum-activity threshold
    computed over the outcome month, which is a population choice, not a column."""
    d = case2_clean(df)
    nxt_tot = d.groupby("client_id")["total_queries"].shift(-1)
    keep = nxt_tot >= 150
    return d[keep.fillna(False)].reset_index(drop=True)


def case6_backfill(df):
    """A column with a completely innocent name whose values were written after the
    outcome month closed. Undetectable from the values alone."""
    d = df.copy()
    nxt_ratio = d.groupby("client_id")["_ratio"].shift(-1)
    d["content_quality_index"] = (nxt_ratio * 70 + rng.normal(0, 9, len(d))).round(1)
    return d.dropna(subset=["content_quality_index"]).reset_index(drop=True)


DROP = ["_ratio", "_next_ratio", "month_idx"]

if __name__ == "__main__":
    panel = add_label(base_panel())
    cases = {
        "case1_pair.csv": case1_the_pair,
        "case2_clean.csv": case2_clean,
        "case3_obvious.csv": case3_obvious,
        "case4_sentinel.csv": case4_sentinel,
        "case5_population.csv": case5_population,
        "case6_backfill.csv": case6_backfill,
    }
    for name, fn in cases.items():
        out = fn(panel).drop(columns=DROP, errors="ignore")
        out.to_csv(f"{OUT}/{name}", index=False)
        print(f"{name:24s} {len(out):6d} rows  {len(out.columns):2d} cols")
