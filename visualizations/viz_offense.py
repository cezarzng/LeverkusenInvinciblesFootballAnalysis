import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

from scripts.config import OUTPUT_FIGURES, OUTPUT_DATASETS

SHOTS_FILE = OUTPUT_DATASETS / "shots_leverkusen.csv"
PASSES_FILE = OUTPUT_DATASETS / "passes_leverkusen.csv"

FIG_SHOT_MAP = OUTPUT_FIGURES / "offense_shot_map.png"
FIG_CROSS_VS_BOX = OUTPUT_FIGURES / "offense_crosses_vs_passes_into_box.png"
FIG_SET_PIECES = OUTPUT_FIGURES / "offense_set_piece_goals.png"


def main():
    OUTPUT_FIGURES.mkdir(parents=True, exist_ok=True)

    shots = pd.read_csv(SHOTS_FILE)
    passes = pd.read_csv(PASSES_FILE)

    # -----------------------
    # 1) SHOTS MAP
    # -----------------------
    pitch = Pitch(pitch_type="statsbomb")

    fig, ax = plt.subplots(figsize=(12, 8))
    pitch.draw(ax=ax)
    ax.set_title("Bayer Leverkusen 2023/24 - Shot Map", fontsize=14)

    non_goals = shots[shots["is_goal"] == False].copy()
    goals = shots[shots["is_goal"] == True].copy()

    pitch.scatter(
        non_goals["x"], non_goals["y"],
        s=(non_goals["shot.statsbomb_xg"].fillna(0) * 800 + 10),
        ax=ax, alpha=0.35
    )

    pitch.scatter(
        goals["x"], goals["y"],
        s=(goals["shot.statsbomb_xg"].fillna(0) * 900 + 40),
        ax=ax, marker="*", alpha=0.9
    )

    fig.savefig(FIG_SHOT_MAP, dpi=200, bbox_inches="tight")
    plt.close(fig)

    # -----------------------
    # 2) CROSSES vs PASSES INTO BOX
    # -----------------------
    crosses = int(passes["is_cross"].sum()) if "is_cross" in passes.columns else 0
    passes_into_box = int(passes["is_pass_into_box"].sum()) if "is_pass_into_box" in passes.columns else 0

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(["Crosses", "Passes into box"], [crosses, passes_into_box])
    ax.set_title("Crosses vs Passes into Box")
    ax.set_ylabel("Count")
    fig.savefig(FIG_CROSS_VS_BOX, dpi=200, bbox_inches="tight")
    plt.close(fig)

    # -----------------------
    # 3) SET PIECE GOALS vs OPEN PLAY GOALS
    # -----------------------
    set_piece_goals = int(
        shots[(shots["is_goal"] == True) & (shots["shot.type.name"].isin(["Free Kick", "Corner", "Penalty"]))].shape[0]
    )
    total_goals = int(shots["is_goal"].sum())
    open_play_goals = max(total_goals - set_piece_goals, 0)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(["Open Play Goals", "Set Piece Goals"], [open_play_goals, set_piece_goals])
    ax.set_title("Goals: Open Play vs Set Pieces")
    ax.set_ylabel("Goals")
    fig.savefig(FIG_SET_PIECES, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print("Saved figures:")
    print(" -", FIG_SHOT_MAP)
    print(" -", FIG_CROSS_VS_BOX)
    print(" -", FIG_SET_PIECES)


if __name__ == "__main__":
    main()