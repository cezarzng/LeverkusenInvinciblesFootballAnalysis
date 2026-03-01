import pandas as pd

from config import (
    TEAM_NAME,
    OUT_EVENTS_CLEAN,
    OUTPUT_DATASETS,
    OPP_PENALTY_BOX_X,
    PENALTY_BOX_Y_MIN,
    PENALTY_BOX_Y_MAX,
    LATE_GAME_MINUTE,
)

OUT_OFFENSE_SEASON = OUTPUT_DATASETS / "kpi_offense_seasonsummary.csv"
OUT_SHOTS_VIZ = OUTPUT_DATASETS / "shots_leverkusen.csv"
OUT_PASSES_VIZ = OUTPUT_DATASETS / "passes_leverkusen.csv"


def in_opp_box(end_x, end_y):
    return (
        (end_x >= OPP_PENALTY_BOX_X) &
        (end_y >= PENALTY_BOX_Y_MIN) &
        (end_y <= PENALTY_BOX_Y_MAX)
    )


def main():
    df = pd.read_csv(OUT_EVENTS_CLEAN)

    # Keep only Leverkusen events
    df = df[df["team.name"] == TEAM_NAME].copy()

    # SHOTS
    shots = df[df["type.name"] == "Shot"].copy()

    shots["is_goal"] = shots["shot.outcome.name"].fillna("") == "Goal"

    shots["is_shot_in_box"] = (
        (shots["x"] >= OPP_PENALTY_BOX_X) &
        (shots["y"] >= PENALTY_BOX_Y_MIN) &
        (shots["y"] <= PENALTY_BOX_Y_MAX)
    )

    shots["is_late_goal"] = shots["is_goal"] & (shots["minute"] >= LATE_GAME_MINUTE)

    shots["shot_type"] = shots["shot.type.name"].fillna("Unknown")
    shots["is_set_piece_shot"] = shots["shot_type"].isin(["Free Kick", "Corner", "Penalty"])
    shots["is_set_piece_goal"] = shots["is_goal"] & shots["is_set_piece_shot"]

    # Save shot dataset for visualizations
    shots_viz_cols = [
        "match_id", 
        "match_date", 
        "minute",
        "player.name",
        "x", 
        "y",
        "shot.statsbomb_xg",
        "shot.outcome.name",
        "shot.type.name",
        "is_goal",
        "is_shot_in_box",
    ]
    shots[shots_viz_cols].to_csv(OUT_SHOTS_VIZ, index=False, encoding="utf-8-sig")

    # PASSES
    passes = df[df["type.name"] == "Pass"].copy()

    if "pass.cross" in passes.columns:
        passes["is_cross"] = passes["pass.cross"].astype(str).str.lower().isin(["true", "1"])
    else:
        passes["is_cross"] = False

    passes["is_pass_into_box"] = in_opp_box(passes["pass_end_x"], passes["pass_end_y"])

    passes_viz_cols = [
        "match_id", 
        "match_date", 
        "minute",
        "player.name",
        "x", 
        "y",
        "pass_end_x", 
        "pass_end_y",
        "is_cross",
        "is_pass_into_box",
    ]
    existing = [c for c in passes_viz_cols if c in passes.columns]
    passes[existing].to_csv(OUT_PASSES_VIZ, index=False, encoding="utf-8-sig")

    # SEASON SUMMARY
    n_matches = df["match_id"].nunique()

    summary = {
        "matches": n_matches,
        "shots_total": int(len(shots)),
        "xg_total": float(shots["shot.statsbomb_xg"].sum()),
        "goals_total": int(shots["is_goal"].sum()),
        "shots_in_box_total": int(shots["is_shot_in_box"].sum()),
        "shots_in_box_pct": float(
            shots["is_shot_in_box"].sum() / len(shots) if len(shots) else 0
        ),
        "crosses_total": int(passes["is_cross"].sum()),
        "passes_into_box_total": int(passes["is_pass_into_box"].sum()),
        "set_piece_shots_total": int(shots["is_set_piece_shot"].sum()),
        "set_piece_goals_total": int(shots["is_set_piece_goal"].sum()),
        "late_goals_75plus": int(shots["is_late_goal"].sum()),
        "shots_per_match": float(len(shots) / n_matches if n_matches else 0),
        "xg_per_match": float(shots["shot.statsbomb_xg"].sum() / n_matches if n_matches else 0),
        "goals_per_match": float(shots["is_goal"].sum() / n_matches if n_matches else 0),
        "conversion_goals_per_xg": float(
            shots["is_goal"].sum() / shots["shot.statsbomb_xg"].sum()
            if shots["shot.statsbomb_xg"].sum() else 0
        ),
    }

    pd.DataFrame([summary]).to_csv(
        OUT_OFFENSE_SEASON,
        index=False,
        encoding="utf-8-sig"
    )

    print("Saved:")
    print(" -", OUT_OFFENSE_SEASON)
    print(" -", OUT_SHOTS_VIZ)
    print(" -", OUT_PASSES_VIZ)


if __name__ == "__main__":
    main()