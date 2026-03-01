import pandas as pd

from config import (
    TEAM_NAME,
    OUT_EVENTS_CLEAN,
    SB_MATCHES_DIR,
    COMP_ID,
    SEASON_ID,
    OUTPUT_DATASETS,
)

OUT_GOALS_INTERVAL = OUTPUT_DATASETS / "mentality_goals_by_interval.csv"
OUT_POINTS_80 = OUTPUT_DATASETS / "mentality_points_after_80.csv"


def load_matches():
    path = SB_MATCHES_DIR / str(COMP_ID) / f"{SEASON_ID}.json"
    return pd.read_json(path)


def classify_interval(minute: float) -> str:
    if pd.isna(minute):
        return "Unknown"
    m = int(minute)
    if m <= 30:
        return "0-30"
    if m <= 60:
        return "31-60"
    if m <= 80:
        return "61-80"
    return "81-90+"


def points_from_result(result: str) -> int:
    if result == "W":
        return 3
    if result == "D":
        return 1
    return 0


def result_from_score(lv: int, opp: int) -> str:
    if lv > opp:
        return "W"
    if lv == opp:
        return "D"
    return "L"


def main():
    OUTPUT_DATASETS.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(OUT_EVENTS_CLEAN)

    # -----------------------
    # 1) Goals by minute interval
    # -----------------------
    shots = df[df["type.name"] == "Shot"].copy()
    shots = shots[shots["team.name"] == TEAM_NAME].copy()

    goals = shots[shots["shot.outcome.name"] == "Goal"].copy()

    goals["interval"] = goals["minute"].apply(classify_interval)
    goals_interval = goals.groupby("interval").size().reindex(["0-30", "31-60", "61-80", "81-90+"], fill_value=0)
    goals_interval = goals_interval.reset_index(name="goals_scored")

    goals_interval.to_csv(OUT_GOALS_INTERVAL, index=False, encoding="utf-8-sig")

    # -----------------------
    # 2) Points won after 80
    # -----------------------
    all_goals = df[(df["type.name"] == "Shot") & (df["shot.outcome.name"] == "Goal")].copy()

    all_goals["is_lv"] = all_goals["team.name"] == TEAM_NAME
    all_goals["is_leq_80"] = all_goals["minute"] <= 80

    # score at 80:
    g80_lv = all_goals[(all_goals["is_lv"]) & (all_goals["is_leq_80"])].groupby("match_id").size()
    g80_opp = all_goals[(~all_goals["is_lv"]) & (all_goals["is_leq_80"])].groupby("match_id").size()

    meta_cols = ["match_id", "home_team", "away_team", "home_score", "away_score"]
    if all(c in df.columns for c in meta_cols):
        match_meta = df[meta_cols].drop_duplicates(subset=["match_id"]).copy()
    else:
        raise ValueError(
            "Missing match metadata"
        )

    rows = []
    for _, m in match_meta.iterrows():
        match_id = int(m["match_id"])
        home = str(m["home_team"])
        away = str(m["away_team"])
        hs = int(m["home_score"])
        aas = int(m["away_score"])

        lv_is_home = (home == TEAM_NAME)
        final_lv = hs if lv_is_home else aas
        final_opp = aas if lv_is_home else hs

        lv80 = int(g80_lv.get(match_id, 0))
        opp80 = int(g80_opp.get(match_id, 0))

        res80 = result_from_score(lv80, opp80)
        res_final = result_from_score(final_lv, final_opp)

        pts80 = points_from_result(res80)
        pts_final = points_from_result(res_final)
        delta = pts_final - pts80

        rows.append({
            "match_id": match_id,
            "home_team": home,
            "away_team": away,
            "score_80": f"{lv80}-{opp80}",
            "score_final": f"{final_lv}-{final_opp}",
            "result_80": res80,
            "result_final": res_final,
            "points_at_80": pts80,
            "points_final": pts_final,
            "points_won_after_80": delta,
        })

    out = pd.DataFrame(rows)
    out.to_csv(OUT_POINTS_80, index=False, encoding="utf-8-sig")

    print("Saved:")
    print("-", OUT_GOALS_INTERVAL)
    print("-", OUT_POINTS_80)

if __name__ == "__main__":
    main()