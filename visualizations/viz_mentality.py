import pandas as pd
import matplotlib.pyplot as plt

from scripts.config import OUTPUT_FIGURES, OUTPUT_DATASETS

GOALS_INTERVAL_FILE = OUTPUT_DATASETS / "mentality_goals_by_interval.csv"
POINTS_80_FILE = OUTPUT_DATASETS / "mentality_points_after_80.csv"

FIG_GOALS_INTERVAL = OUTPUT_FIGURES / "mentality_goals_by_interval.png"
FIG_POINTS_80_VS_TOTAL = OUTPUT_FIGURES / "mentality_points_after_80_vs_total.png"


def main():
    OUTPUT_FIGURES.mkdir(parents=True, exist_ok=True)

    # -----------------------
    # 1) Goals by interval
    # -----------------------
    gi = pd.read_csv(GOALS_INTERVAL_FILE)
    order = ["0-30", "31-60", "61-80", "81-90+"]

    gi["interval"] = gi["interval"].astype(str)
    gi = gi.set_index("interval").reindex(order).fillna(0).reset_index()
    gi["goals_scored"] = pd.to_numeric(gi["goals_scored"], errors="coerce").fillna(0)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(gi["interval"], gi["goals_scored"])
    ax.set_title("Leverkusen 23/24 – Goals scored by minute interval")
    ax.set_xlabel("Minute interval")
    ax.set_ylabel("Goals scored")
    fig.tight_layout()
    fig.savefig(FIG_GOALS_INTERVAL, dpi=200, bbox_inches="tight")
    plt.close(fig)

    # -----------------------
    # 2) Points won after 80 vs total points
    # -----------------------
    p = pd.read_csv(POINTS_80_FILE)

    p["points_won_after_80"] = pd.to_numeric(p["points_won_after_80"], errors="coerce").fillna(0)
    p["points_final"] = pd.to_numeric(p["points_final"], errors="coerce").fillna(0)

    points_won_after_80 = float(p["points_won_after_80"].sum())
    total_points = float(p["points_final"].sum())

    fig, ax = plt.subplots(figsize=(7, 5))
    labels = ["Points won after 80'", "Total points (season)"]
    values = [points_won_after_80, total_points]

    ax.bar(labels, values)
    ax.set_title("Leverkusen 23/24 - Late points contribution")
    ax.set_ylabel("Points")
    fig.tight_layout()
    fig.savefig(FIG_POINTS_80_VS_TOTAL, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print("Saved figures:")
    print("-", FIG_GOALS_INTERVAL)
    print("-", FIG_POINTS_80_VS_TOTAL)


if __name__ == "__main__":
    main()