import json
from pathlib import Path

import pandas as pd

from config import (
    TEAM_NAME,
    COMP_ID,
    SEASON_ID,
    SB_MATCHES_DIR,
    SB_EVENTS_DIR,
    OUT_EVENTS_RAW,
)

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def get_team_name(team_obj: dict) -> str:
    return (
        team_obj.get("home_team_name")
        or team_obj.get("away_team_name")
        or team_obj.get("name")
        or ""
    )

def extract_team_matches(matches: list, team_name: str) -> list:
    out = []
    for m in matches:
        home = m.get("home_team", {})
        away = m.get("away_team", {})
        home_name = get_team_name(home)
        away_name = get_team_name(away)
        if home_name == team_name or away_name == team_name:
            out.append(m)
    return out


def main():
    matches_path = SB_MATCHES_DIR / str(COMP_ID) / f"{SEASON_ID}.json"
    if not matches_path.exists():
        raise FileNotFoundError(f"Missing matches file: {matches_path}")

    matches = load_json(matches_path)
    team_matches = extract_team_matches(matches, TEAM_NAME)

    if len(team_matches) == 0:
        raise FileNotFoundError(f"No matches found for team: {TEAM_NAME}")

    # Load and normalize events
    all_events = []

    for m in team_matches:
        match_id = m.get("match_id")
        ev_path = SB_EVENTS_DIR / f"{match_id}.json"

        if not ev_path.exists():
            raise FileNotFoundError(f"Missing event file for: {match_id}")

        events = load_json(ev_path)
        event_list = pd.json_normalize(events)

        # add match metadata
        event_list["match_id"] = match_id
        event_list["match_date"] = m.get("match_date")
        event_list["home_team"] = m.get("home_team", {}).get("home_team_name") or m.get("home_team", {}).get("name")
        event_list["away_team"] = m.get("away_team", {}).get("away_team_name") or m.get("away_team", {}).get("name")
        event_list["home_score"] = m.get("home_score")
        event_list["away_score"] = m.get("away_score")

        all_events.append(event_list)

    events_raw = pd.concat(all_events, ignore_index=True)

    # Save
    OUT_EVENTS_RAW.parent.mkdir(parents=True, exist_ok=True)
    events_raw.to_csv(OUT_EVENTS_RAW)

    # Delete non-related events for cleaning space
    team_match_ids = {m.get("match_id") for m in team_matches}

    all_event_files = list(SB_EVENTS_DIR.glob("*.json"))

    for file_path in all_event_files:
        file_match_id = int(file_path.stem)

        if file_match_id not in team_match_ids:
            file_path.unlink()


if __name__ == "__main__":
    main()