from pathlib import Path
import folium
import pandas as pd

def save_stops_map(stops: pd.DataFrame, out_html: Path):
    if stops.empty:
        raise ValueError("stops が空です")
    lat0 = stops["lat"].mean()
    lon0 = stops["lon"].mean()
    m = folium.Map(location=[lat0, lon0], zoom_start=12)
    for _, r in stops.iterrows():
        popup = f"{r['stop_id']} - {r['name']}<br>demand={r['demand']} | service={r['service_min']}min"
        folium.Marker(location=[r["lat"], r["lon"]], popup=popup).add_to(m)
    out_html.parent.mkdir(parents=True, exist_ok=True)
    m.save(str(out_html))
