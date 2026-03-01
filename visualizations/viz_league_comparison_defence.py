import pandas as pd
import matplotlib.pyplot as plt

from scripts.config import OTHERSTATS_DIR, OUTPUT_FIGURES, TEAM_NAME

FILE_XGA = OTHERSTATS_DIR / "expected_goals_conceded_team.csv"
FILE_CS = OTHERSTATS_DIR / "clean_sheet_team.csv"
FILE_POSWON = OTHERSTATS_DIR / "possession_won_att_3rd_team.csv"

FIG_GOALS_CONC = OUTPUT_FIGURES / "league_goals_conceded.png"
FIG_CLEAN_SHEETS = OUTPUT_FIGURES / "league_clean_sheets.png"
FIG_POSWON = OUTPUT_FIGURES / "league_possession_won_att_3rd.png"
FIG_SCATTER = OUTPUT_FIGURES / "league_goals_conceded_vs_xga.png"


def pick_col(df, candidates):
    cols = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in cols:
            return cols[cand.lower()]
    raise ValueError(f"Missing columns. Tried: {candidates}. Available: {list(df.columns)}")


def bar_chart(df, team_col, value_col, title, ylabel, out_path, highlight=TEAM_NAME, ascending=False):
    df = df[[team_col, value_col]].copy()
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
    df = df.dropna(subset=[value_col])
    df = df.sort_values(value_col, ascending=ascending)

    colors = ["red" if t == highlight else "grey" for t in df[team_col]]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(df[team_col], df[value_col], color=colors)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xticklabels(df[team_col], rotation=90)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def main():
    OUTPUT_FIGURES.mkdir(parents=True, exist_ok=True)

    # -----------------------
    # 1) Goals conceded + xGA
    # -----------------------
    df_xga = pd.read_csv(FILE_XGA, encoding="utf-8-sig")

    team_col = pick_col(df_xga, ["Team", "team", "Squad", "squad"])
    goals_conc_col = pick_col(df_xga, ["Goals Conceded", "goals_conceded", "GA", "GoalsAgainst"])
    xga_col = pick_col(df_xga, ["xGA", "Expected Goals Against", "expected_goals_against", "Expected Goals Conceded"])

    bar_chart(
        df_xga, team_col, goals_conc_col,
        title="Bundesliga 23/24 - Goals Conceded",
        ylabel="Goals conceded",
        out_path=FIG_GOALS_CONC,
        ascending=True
    )

    # Scatter: Goals conceded vs xGA
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.scatter(df_xga[xga_col], df_xga[goals_conc_col], alpha=0.8)

    # highlight Leverkusen
    lev = df_xga[df_xga[team_col] == TEAM_NAME]
    if len(lev) == 1:
        lev_x = float(pd.to_numeric(lev[xga_col], errors="coerce").iloc[0])
        lev_y = float(pd.to_numeric(lev[goals_conc_col], errors="coerce").iloc[0])

    ax.scatter([lev_x], [lev_y], s=120)
    ax.annotate(TEAM_NAME, (lev_x, lev_y), xytext=(5, 5), textcoords="offset points")

    ax.set_title("Bundesliga 23/24 - Goals Conceded vs xGA")
    ax.set_xlabel("xGA")
    ax.set_ylabel("Goals conceded")

    fig.tight_layout()
    fig.savefig(FIG_SCATTER, dpi=200)
    plt.close(fig)

    # -----------------------
    # 2) Clean sheets
    # -----------------------
    df_cs = pd.read_csv(FILE_CS, encoding="utf-8-sig")
    team_col_cs = pick_col(df_cs, ["Team", "team", "Squad", "squad"])
    cs_col = pick_col(df_cs, ["Clean Sheets", "clean_sheets", "CS"])

    bar_chart(
        df_cs, team_col_cs, cs_col,
        title="Bundesliga 23/24 - Clean Sheets",
        ylabel="Clean sheets",
        out_path=FIG_CLEAN_SHEETS,
        ascending=False
    )

    # -----------------------
    # 3) Possession won in attacking third
    # -----------------------
    df_pw = pd.read_csv(FILE_POSWON, encoding="utf-8-sig")
    team_col_pw = pick_col(df_pw, ["Team", "team", "Squad", "squad"])
    pw_col = pick_col(df_pw, ["Possession Won Final 3rd per Match", "possession_won_att_3rd", "PossessionWonAtt3rd"])

    bar_chart(
        df_pw, team_col_pw, pw_col,
        title="Bundesliga 23/24 - Possession Won in Attacking 3rd",
        ylabel="Possession won",
        out_path=FIG_POSWON,
        ascending=False
    )

    print("Saved figures:")
    print("-", FIG_GOALS_CONC)
    print("-", FIG_SCATTER)
    print("-", FIG_CLEAN_SHEETS)
    print("-", FIG_POSWON)


if __name__ == "__main__":
    main()