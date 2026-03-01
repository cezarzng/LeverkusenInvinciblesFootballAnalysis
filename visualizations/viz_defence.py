import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

from scripts.config import OUTPUT_FIGURES, OUTPUT_DATASETS

REC_FILE = OUTPUT_DATASETS / "defense_recoveries.csv"
TOP_REC_FILE = OUTPUT_DATASETS / "defense_top_recoveries.csv"
TOP_PRES_FILE = OUTPUT_DATASETS / "defense_top_pressures.csv"
TOP_DUELS_FILE = OUTPUT_DATASETS / "defense_top_duels_won.csv"

FIG_REC_HEAT = OUTPUT_FIGURES / "defense_recoveries_heatmap.png"
FIG_TOP_REC = OUTPUT_FIGURES / "defense_top_recoveries.png"
FIG_TOP_PRES = OUTPUT_FIGURES / "defense_top_pressures.png"
FIG_TOP_DUELS = OUTPUT_FIGURES / "defense_top_duels_won.png"


def barh_top(df, name_col, value_col, title, xlabel, out_path, top_n=12):
    df = df[[name_col, value_col]].dropna().copy()
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
    df = df.dropna(subset=[value_col]).sort_values(value_col, ascending=False).head(top_n)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df[name_col], df[value_col])
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main():
    OUTPUT_FIGURES.mkdir(parents=True, exist_ok=True)

    rec = pd.read_csv(REC_FILE)
    top_rec = pd.read_csv(TOP_REC_FILE)
    top_pres = pd.read_csv(TOP_PRES_FILE)
    top_duels = pd.read_csv(TOP_DUELS_FILE)

    # -----------------------
    # 1) Heatmap recoveries
    # -----------------------
    pitch = Pitch(pitch_type="statsbomb")
    fig, ax = plt.subplots(figsize=(12, 8))
    pitch.draw(ax=ax)
    ax.set_title("Leverkusen 23/24 - Ball Recoveries", fontsize=14)

    # Avg recoveries
    matches = rec["match_id"].nunique() if "match_id" in rec.columns else 34
    bins = (12, 8)

    bin_count = pitch.bin_statistic(
        rec["x"], rec["y"],
        statistic="count",
        bins=bins
    )
    bin_count["statistic"] = bin_count["statistic"] / matches

    hm = pitch.heatmap(bin_count, ax=ax, alpha=0.9)
    cbar = fig.colorbar(hm, ax=ax, shrink=0.8)
    cbar.set_label("Avg recoveries")

    fig.savefig(FIG_REC_HEAT, dpi=200, bbox_inches="tight")
    plt.close(fig)

    # -----------------------
    # 2) Top recoveries
    # -----------------------
    barh_top(
        top_rec,
        name_col="player.name",
        value_col="recoveries",
        title="Top Players - Ball Recoveries",
        xlabel="Recoveries",
        out_path=FIG_TOP_REC,
        top_n=10,
    )

    # -----------------------
    # 3) Top duels won
    # -----------------------
    barh_top(
        top_duels,
        name_col="player.name",
        value_col="duels_won",
        title="Top Players - Duels Won",
        xlabel="Duels won",
        out_path=FIG_TOP_DUELS,
        top_n=10,
    )

    # -----------------------
    # 4) Top pressures
    # -----------------------
    barh_top(
        top_pres,
        name_col="player.name",
        value_col="pressures",
        title="Top Players - Pressures",
        xlabel="Pressures",
        out_path=FIG_TOP_PRES,
        top_n=10,
    )

    print("Saved figures:")
    print("-", FIG_REC_HEAT)
    print("-", FIG_TOP_REC)
    print("-", FIG_TOP_DUELS)
    print("-", FIG_TOP_PRES)


if __name__ == "__main__":
    main()