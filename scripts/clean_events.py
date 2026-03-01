import ast
import pandas as pd

from config import (
    OUT_EVENTS_RAW,
    OUT_EVENTS_CLEAN,
    EVENT_TYPES_KEEP,
)

def parse_point(v):
    if isinstance(v, list) and len(v) >= 2:
        return v
    if isinstance(v, str) and v.startswith("[") and v.endswith("]"):
        try:
            parsed = ast.literal_eval(v)
            if isinstance(parsed, list) and len(parsed) >= 2:
                return parsed
        except Exception:
            return None
    return None

def split_location(df, src_col, out_x, out_y):
    if src_col not in df.columns:
        df[out_x] = pd.NA
        df[out_y] = pd.NA
        return df

    pts = df[src_col].apply(parse_point)
    df[out_x] = pts.apply(lambda _: _[0] if isinstance(_, list) else pd.NA)
    df[out_y] = pts.apply(lambda _: _[1] if isinstance(_, list) else pd.NA)
    return df

def main():
    df = pd.read_csv(OUT_EVENTS_RAW)

    # Keep only relevant event types
    if "type.name" in df.columns:
        df = df[df["type.name"].isin(EVENT_TYPES_KEEP)].copy()

    wanted_cols = [
        "match_id",
        "match_date",
        "minute",
        "second",
        "period",
        "type.name",
        "team.name",
        "player.name",
        "possession_team.name",
        "play_pattern.name",
        "location",
        "pass.end_location",
        "carry.end_location",
        "shot.statsbomb_xg",
        "shot.outcome.name",
        "shot.type.name",
        "pass.cross",
        "pass.outcome.name",
        "pass.height.name",
        "pass.type.name",
        "duel.type.name",
        "duel.outcome.name",
        "home_team",
        "away_team",
        "home_score",
        "away_score",
    ]
    existing = [c for c in wanted_cols if c in df.columns]
    df = df[existing].copy()

    # start location
    df = split_location(df, "location", "x", "y")

    # end location
    df = split_location(df, "pass.end_location", "pass_end_x", "pass_end_y")
    df = split_location(df, "carry.end_location", "carry_end_x", "carry_end_y")


    for col in ["minute", "second", "period", "x", "y", "pass_end_x", "pass_end_y", "carry_end_x", "carry_end_y", "shot.statsbomb_xg"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Save
    df.to_csv(OUT_EVENTS_CLEAN, index=False, encoding="utf-8-sig")
    print(f"Saved: {OUT_EVENTS_CLEAN}")

if __name__ == "__main__":
    main()