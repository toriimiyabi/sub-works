import typer
from pathlib import Path
import csv, random, math
import pandas as pd
from io import StringIO
import yaml

from utils_io.load import load_stops, load_vehicles, load_matrix_optional  # type: ignore
from viz.map import save_stops_map  # type: ignore

app = typer.Typer(help="VRP Starter CLI")

# --------- ユーティリティ（設定読み込み） ---------
def read_cfg(path: Path) -> dict:
    if not path.exists():
        return {"data":{"dir":"data"}, "output":{"dir":"outputs"}}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

# --------- Day2: 合成データ生成 ---------
@app.command()
def gen(
    data_dir: str = typer.Option("data", help="CSVを出力するフォルダ"),
    stops: int = typer.Option(20, min=3, max=200, help="配送先の数"),
    vehicles: int = typer.Option(3, min=1, max=50, help="車両台数"),
    center_lat: float = typer.Option(35.6800, help="中心緯度（初期：東京駅あたり）"),
    center_lon: float = typer.Option(139.7600, help="中心経度"),
    spread_km: float = typer.Option(8.0, help="中心からの広がり（km）")
):
    """
    stops.csv / vehicles.csv の合成データを生成します。
    """
    ddir = Path(data_dir)
    ddir.mkdir(parents=True, exist_ok=True)

    # 緯度経度のランダム生成（簡易：1度 ≒ 111km）
    def jitter_latlon():
        dlat = (random.random() - 0.5) * (spread_km / 111.0) * 2
        dlon = (random.random() - 0.5) * (spread_km / (111.0*math.cos(math.radians(center_lat)))) * 2
        return center_lat + dlat, center_lon + dlon

    # stops.csv
    stops_rows = []
    for i in range(1, stops+1):
        lat, lon = jitter_latlon()
        demand = random.choice([5,8,10,12,15])
        service = random.choice([5,8,10,12])
        tw_s = random.choice([0, 540, 600])   # 0=制約なし、or 9:00/10:00開始
        tw_e = 1440 if tw_s == 0 else random.choice([900, 1020, 1080])  # 15:00/17:00/18:00
        stops_rows.append([f"S{i:03d}", f"Shop {i}", lat, lon, demand, service, tw_s, tw_e])

    with open(ddir/"stops.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["stop_id","name","lat","lon","demand","service_min","tw_start","tw_end"])
        w.writerows(stops_rows)

    # vehicles.csv（全車両は同じデポに戻る想定）
    veh_rows = []
    for v in range(1, vehicles+1):
        cap = random.choice([25,30,35])
        veh_rows.append([f"V{v:02d}", center_lat, center_lon, center_lat, center_lon, cap, 540, 1080, 300])
    with open(ddir/"vehicles.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["vehicle_id","start_lat","start_lon","end_lat","end_lon","capacity","shift_start","shift_end","max_distance_km"])
        w.writerows(veh_rows)

    typer.echo(f"generated: {ddir/'stops.csv'} , {ddir/'vehicles.csv'}")

# --------- Day2: CSV読み込み（検証） ---------
@app.command()
def load(
    data_dir: str = typer.Option("data", help="CSVフォルダ")
):
    """
    CSVを読み込んで件数を表示します。
    """
    ddir = Path(data_dir)
    stops = load_stops(ddir)
    veh   = load_vehicles(ddir)
    mtx   = load_matrix_optional(ddir)
    typer.echo(f"stops: {len(stops)} rows, vehicles: {len(veh)} rows, matrix: {0 if mtx is None else len(mtx)} rows")

# --------- Day2: ダミー地図を出力 ---------
@app.command()
def map(
    cfg: str = typer.Option("config.yml", help="設定ファイル"),
):
    """
    stops.csv を地図にプロットして outputs/map.html を作ります。
    """
    conf = read_cfg(Path(cfg))
    data_dir = Path(conf.get("data", {}).get("dir", "data"))
    out_dir  = Path(conf.get("output", {}).get("dir", "outputs"))
    out_dir.mkdir(parents=True, exist_ok=True)

    stops = load_stops(data_dir)
    out_html = out_dir / "map.html"
    save_stops_map(stops, out_html)
    typer.echo(f"saved: {out_html}")

# 既存のサンプルコマンド
@app.command()
def hello(name: str = "world"):
    """動作確認用のコマンド。"""
    typer.echo(f"Hello, {name}! VRP starter is ready.")

@app.command()
def info():
    """プロジェクトの説明を表示。"""
    typer.echo("VRP Starter: Day2 は CSV生成→読込→地図表示の土台を作ります。")

if __name__ == "__main__":
    app()
