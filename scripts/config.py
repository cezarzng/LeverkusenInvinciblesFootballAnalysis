from pathlib import Path

# =========================
# Project Paths
# =========================

ROOT = Path(__file__).parents[1]

DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"

# ---- StatsBomb ----
STATS_DIR = DATA_DIR / "statsbomb"
SB_COMPETITIONS = STATS_DIR / "competitions.json"
SB_MATCHES_DIR = STATS_DIR / "matches"
SB_EVENTS_DIR = STATS_DIR / "events"

# ---- Other Stats ----
OTHERSTATS_DIR = DATA_DIR / "otherstats" / "bundesliga23_24"

# ---- Output folders ----
OUTPUT_DATASETS = OUTPUT_DIR / "datasets"
OUTPUT_FIGURES = OUTPUT_DIR / "figures"

for folder in [OUTPUT_DATASETS, OUTPUT_FIGURES]:
    folder.mkdir(parents=True, exist_ok=True)

# =========================
# Competition & Team
# =========================

TEAM_NAME = "Bayer Leverkusen"
COMP_ID = 9
SEASON_ID = 281

# =========================
# Pitch Model (StatsBomb)
# =========================

PITCH_LENGTH = 120.0
PITCH_WIDTH = 80.0

# ---- Zones ----
FINAL_THIRD_X = 80.0
DEF_PENALTY_BOX_X = 18.0
OPP_PENALTY_BOX_X = 102.0
PENALTY_BOX_Y_MIN = 18.0
PENALTY_BOX_Y_MAX = 62.0

# =========================
# Time Definitions
# =========================

EARLY_GAME_MINUTE = 15
LATE_GAME_MINUTE = 75

# =========================
# Progressive Definitions
# =========================

PROG_DISTANCE_REDUCTION_PCT = 0.25
PROG_MIN_X_ADVANCE = 10.0
OWN_HALF_X_MAX = 60.0

# =========================
# Relevant Event Types
# =========================

EVENT_TYPES_KEEP = {
    "Shot",
    "Pass",
    "Carry",
    "Pressure",
    "Ball Recovery",
    "Interception",
    "Duel",
}

# =========================
# Output Files
# =========================

OUT_EVENTS_RAW = OUTPUT_DATASETS / "events_raw.csv"
OUT_EVENTS_CLEAN = OUTPUT_DATASETS / "events_clean.csv"