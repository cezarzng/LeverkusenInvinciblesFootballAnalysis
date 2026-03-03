# visualizations/viz_build_up.py
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

from scripts.config import OUTPUT_FIGURES, OUTPUT_DATASETS

PROG_FILE = OUTPUT_DATASETS / "build_up_progressions.csv"
TOP_FILE = OUTPUT_DATASETS / "build_up_top_progressive_players.csv"

FIG_HEATMAP = OUTPUT_FIGURES / "build_up_progression_heatmap.png"
FIG_TOP_PLAYERS = OUTPUT_FIGURES / "build_up_top_progressive_players.png"


def main():
    OUTPUT_FIGURES.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(PROG_FILE)
    top = pd.read_csv(TOP_FILE).head(12)
   
    # -----------------------
    # Heatmap – Avg progression actions per match per area
    # -----------------------
    pitch = Pitch(pitch_type="statsbomb")
    fig, ax = plt.subplots(figsize=(12, 8))
    pitch.draw(ax=ax)

    ax.set_title("Build-up - Avg progression actions per match", fontsize=14)

    df_prog = df[df["is_progressive"] == True].copy()

    matches = df_prog["match_id"].nunique()

    bins = (24, 16)

    bin_count = pitch.bin_statistic(
       df_prog["x"], df_prog["y"],
       statistic="count",
       bins=bins
    )

    bin_count["statistic"] = bin_count["statistic"] / matches

    hm = pitch.heatmap(bin_count, ax=ax, alpha=0.9)

    cbar = fig.colorbar(hm, ax=ax, shrink=0.8)
    cbar.set_label("Avg progression actions per match")

    fig.savefig(FIG_HEATMAP, dpi=200, bbox_inches="tight")
    plt.close(fig)

    # -----------------------
    # 2) Top progressive players
    # -----------------------
    fig, ax = plt.subplots(figsize=(10, 6))

    names = top["player.name"]
    ax.barh(names, top["progressive_passes"], alpha=0.7, label="Progressive passes")
    ax.barh(names, top["progressive_carries"], alpha=0.7, left=top["progressive_passes"], label="Progressive carries")

    ax.set_title("Top progressive players")
    ax.set_xlabel("Count (progressive actions)")
    ax.invert_yaxis()
    ax.legend()

    fig.tight_layout()
    fig.savefig(FIG_TOP_PLAYERS, dpi=200)
    plt.close(fig)

    print("Saved:")
    print("-", FIG_HEATMAP)
    print("-", FIG_TOP_PLAYERS)

if __name__ == "__main__":
    main()