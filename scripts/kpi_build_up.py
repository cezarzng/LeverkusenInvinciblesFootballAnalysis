# scripts/kpi_build_up.py
import pandas as pd

from scripts.config import (
    TEAM_NAME,
    OUT_EVENTS_CLEAN,
    OUTPUT_DATASETS,
    PROG_MIN_X_ADVANCE,
)

OUT_PROGRESSIONS = OUTPUT_DATASETS / "build_up_progressions.csv"
OUT_TOP_PLAYERS = OUTPUT_DATASETS / "build_up_top_progressive_players.csv"


def main():
    df = pd.read_csv(OUT_EVENTS_CLEAN)
    df = df[df["team.name"] == TEAM_NAME].copy()
    df = df[df["type.name"].isin(["Pass", "Carry"])].copy()

    # end coords per type
    df["end_x"] = df.apply(
        lambda r: r["pass_end_x"] if r["type.name"] == "Pass" else r["carry_end_x"],
        axis=1,
    )
    df["end_y"] = df.apply(
        lambda r: r["pass_end_y"] if r["type.name"] == "Pass" else r["carry_end_y"],
        axis=1,
    )

    # keep only rows that have coords
    df = df.dropna(subset=["x", "y", "end_x", "end_y"]).copy()

    # progression
    df["dx"] = df["end_x"] - df["x"]
    df["dy"] = df["end_y"] - df["y"]

    # keep only forward progressions
    df = df[df["dx"] > 0].copy()

    df["is_progressive"] = df["dx"] >= PROG_MIN_X_ADVANCE

    # save dataset for heatmaps
    keep_cols = [
        "match_id", 
        "match_date", 
        "minute",
        "type.name", 
        "player.name",
        "x", 
        "y", 
        "end_x", 
        "end_y",
        "dx", 
        "dy",
        "is_progressive",
    ]
    df[keep_cols].to_csv(OUT_PROGRESSIONS, index=False, encoding="utf-8-sig")

    # top players
    top = (
        df[df["is_progressive"] == True]
        .groupby(["player.name", "type.name"])
        .size()
        .unstack(fill_value=0)
    )

    if "Pass" not in top.columns:
        top["Pass"] = 0
    if "Carry" not in top.columns:
        top["Carry"] = 0

    top["total_progressive"] = top["Pass"] + top["Carry"]
    top = top.sort_values("total_progressive", ascending=False).reset_index()
    top = top.rename(columns={"Pass": "progressive_passes", "Carry": "progressive_carries"})

    top.to_csv(OUT_TOP_PLAYERS, index=False, encoding="utf-8-sig")

    print("Saved:")
    print("-", OUT_PROGRESSIONS)
    print("-", OUT_TOP_PLAYERS)


if __name__ == "__main__":
    main()