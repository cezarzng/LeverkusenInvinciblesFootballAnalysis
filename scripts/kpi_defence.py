import pandas as pd

from config import (
    TEAM_NAME,
    OUT_EVENTS_CLEAN,
    OUTPUT_DATASETS,
    FINAL_THIRD_X,
)

OUT_RECOVERIES = OUTPUT_DATASETS / "defense_recoveries.csv"
OUT_TOP_RECOVERIES = OUTPUT_DATASETS / "defense_top_recoveries.csv"
OUT_TOP_PRESSURES = OUTPUT_DATASETS / "defense_top_pressures.csv"
OUT_TOP_DUELS_WON = OUTPUT_DATASETS / "defense_top_duels_won.csv"

def main():
    df = pd.read_csv(OUT_EVENTS_CLEAN)
    df = df[df["team.name"] == TEAM_NAME].copy()

    # ---- RECOVERIES ----
    rec = df[df["type.name"] == "Ball Recovery"].copy()
    rec = rec.dropna(subset=["x", "y"])

    rec["is_high_recovery"] = rec["x"] >= FINAL_THIRD_X

    # dataset for heatmap
    keep_cols = ["match_id", "match_date", "minute", "player.name", "x", "y", "is_high_recovery"]
    OUT_RECOVERIES.parent.mkdir(parents=True, exist_ok=True)
    rec[keep_cols].to_csv(OUT_RECOVERIES, index=False, encoding="utf-8-sig")

    # top recoveries
    top_rec = (
        rec.groupby("player.name")
        .size()
        .sort_values(ascending=False)
        .reset_index(name="recoveries")
    )
    OUT_TOP_RECOVERIES.parent.mkdir(parents=True, exist_ok=True)
    top_rec.to_csv(OUT_TOP_RECOVERIES, index=False, encoding="utf-8-sig")

    # ---- PRESSURES ----
    pres = df[df["type.name"] == "Pressure"].copy()
    pres = pres.dropna(subset=["x", "y"])
    pres["is_high_pressure"] = pres["x"] >= FINAL_THIRD_X

    top_pres = (
        pres.groupby("player.name")
        .size()
        .sort_values(ascending=False)
        .reset_index(name="pressures")
    )
    top_pres.to_csv(OUT_TOP_PRESSURES, index=False, encoding="utf-8-sig")

    # ---- DUELS ----
    duels = df[df["type.name"] == "Duel"].copy()
    duels = duels.dropna(subset=["x", "y"])

    if "duel.outcome.name" in duels.columns:
        outcome = duels["duel.outcome.name"].fillna("").astype(str).str.lower()
        duels["is_duel_won"] = outcome.str.contains("won")
    else:
        duels["is_duel_won"] = False

    top_duels_won = (
        duels[duels["is_duel_won"] == True]
        .groupby("player.name")
        .size()
        .sort_values(ascending=False)
        .reset_index(name="duels_won")
    )

    top_duels_won.to_csv(OUT_TOP_DUELS_WON, index=False, encoding="utf-8-sig")

    print("Saved:")
    print("-", OUT_RECOVERIES)
    print("-", OUT_TOP_RECOVERIES)
    print("-", OUT_TOP_PRESSURES)
    print("-", OUT_TOP_DUELS_WON)


if __name__ == "__main__":
    main()