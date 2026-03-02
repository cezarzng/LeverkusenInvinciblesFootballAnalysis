import pandas as pd
import matplotlib.pyplot as plt

from scripts.config import OTHERSTATS_DIR, OUTPUT_FIGURES, TEAM_NAME

FILE = OTHERSTATS_DIR / "expected_goals_team.csv"

FIG_CONVERSION = OUTPUT_FIGURES / "league_conversion_rate.png"
FIG_GOALS = OUTPUT_FIGURES / "league_goals_scored.png"


def main():
    OUTPUT_FIGURES.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(FILE, encoding="utf-8-sig")

    df["conversion_rate"] = df["Goals"] / df["Expected Goals"]

    # ====================================================
    # 1) CONVERSION RATE
    # ====================================================
    df_conv = df.sort_values("conversion_rate", ascending=False)

    fig, ax = plt.subplots(figsize=(12, 6))

    colors = ["red" if t == TEAM_NAME else "grey" for t in df_conv["Team"]]

    bars = ax.bar(df_conv["Team"], df_conv["conversion_rate"], color=colors)
    ax.bar_label(bars, fmt="%.2f")

    league_average = df_conv["conversion_rate"].mean()

    ax.axhline(league_average, linestyle="--", color="blue", label="League Avg")
    ax.legend()
    ax.set_title("Bundesliga 23/24 - Conversion Rate (Goals / xG)")
    ax.set_ylabel("Goals / xG")
    ax.set_xticklabels(df_conv["Team"], rotation=90)

    print(f"League average: {league_average}")

    fig.tight_layout()
    fig.savefig(FIG_CONVERSION, dpi=200)
    plt.close(fig)

    # ====================================================
    # 2) TOTAL GOALS SCORED
    # ====================================================
    df_goals = df.sort_values("Goals", ascending=False)

    fig, ax = plt.subplots(figsize=(12, 6))

    colors = ["red" if t == TEAM_NAME else "grey" for t in df_goals["Team"]]

    barsgoals = ax.bar(df_goals["Team"], df_goals["Goals"], color=colors)
    ax.bar_label(barsgoals, fmt="%.2f")

    ax.set_title("Bundesliga 23/24 - Goals Scored")
    ax.set_ylabel("Goals")
    ax.set_xticklabels(df_goals["Team"], rotation=90)

    fig.tight_layout()
    fig.savefig(FIG_GOALS, dpi=200)
    plt.close(fig)

    print("Saved:")
    print("-", FIG_CONVERSION)
    print("-", FIG_GOALS)


if __name__ == "__main__":
    main()