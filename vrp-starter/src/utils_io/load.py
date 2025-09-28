from pathlib import Path
import pandas as pd

REQUIRED_STOPS = ["stop_id","name","lat","lon","demand","service_min","tw_start","tw_end"]
REQUIRED_VEH   = ["vehicle_id","start_lat","start_lon","end_lat","end_lon","capacity","shift_start","shift_end","max_distance_km"]
REQUIRED_MAT   = ["from_id","to_id","distance_km","travel_min"]

def _require_cols(df: pd.DataFrame, cols: list, label: str):
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"{label} に必要な列が足りません: {missing}")

def load_stops(data_dir: Path) -> pd.DataFrame:
    p = Path(data_dir) / "stops.csv"
    df = pd.read_csv(p)
    _require_cols(df, REQUIRED_STOPS, "stops.csv")
    return df

def load_vehicles(data_dir: Path) -> pd.DataFrame:
    p = Path(data_dir) / "vehicles.csv"
    df = pd.read_csv(p)
    _require_cols(df, REQUIRED_VEH, "vehicles.csv")
    return df

def load_matrix_optional(data_dir: Path) -> pd.DataFrame | None:
    p = Path(data_dir) / "matrix.csv"
    if not p.exists():
        return None
    df = pd.read_csv(p)
    _require_cols(df, REQUIRED_MAT, "matrix.csv")
    return df
