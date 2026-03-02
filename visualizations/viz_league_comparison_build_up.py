import pandas as pd
import matplotlib.pyplot as plt

from scripts.config import OTHERSTATS_DIR, OUTPUT_FIGURES, TEAM_NAME

FILE = OTHERSTATS_DIR / "expected_goals_team.csv"

POSSESSION_FILE = OTHERSTATS_DIR / "possession_percentage_team.csv"
PASS_ACC_FILE = OTHERSTATS_DIR / "accurate_pass_team.csv"

FIG_POSSESSION = OUTPUT_FIGURES / "league_possession_percentage.png"
FIG_PASS_ACC = OUTPUT_FIGURES / "league_pass_accuracy.png"


def main():
    OUTPUT_FIGURES.mkdir(parents=True, exist_ok=True)

    # -----------------------
    # POSSESSION %
    # -----------------------
    df_pos = pd.read_csv(POSSESSION_FILE, encoding="utf-8-sig")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors = ["red" if t == TEAM_NAME else "grey" for t in df_pos["Team"]]

    bars = ax.bar(df_pos["Team"], df_pos["Possession (%)"], color=colors)
    ax.bar_label(bars, fmt="%.0f%%")

    ax.set_title("Bundesliga 23/24 - Possesion (%)")
    ax.set_ylabel("Possesion (%)")
    ax.set_xticklabels(df_pos["Team"], rotation=90)

    fig.tight_layout()
    fig.savefig(FIG_POSSESSION, dpi=200)
    plt.close(fig)
    
    # -----------------------
    # PASS ACCURACY %
    # -----------------------
    df_acc = pd.read_csv(PASS_ACC_FILE, encoding="utf-8-sig")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors = ["red" if t == TEAM_NAME else "grey" for t in df_acc["Team"]]

    barsacc = ax.bar(df_acc["Team"], df_acc["Pass Success (%)"], color=colors)
    ax.bar_label(barsacc, fmt="%.0f%%")

    ax.set_title("Bundesliga 23/24 - Pass Accuracy (%)")
    ax.set_ylabel("Pass Accuracy (%)")
    ax.set_xticklabels(df_acc["Team"], rotation=90)

    fig.tight_layout()
    fig.savefig(FIG_PASS_ACC, dpi=200)
    plt.close(fig)

if __name__ == "__main__":
    main()