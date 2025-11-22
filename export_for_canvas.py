# save as export_for_canvas.py
import json, numpy as np, pandas as pd
from pathlib import Path
from typing import Optional, List

def export_for_canvas(common_path: str,
                      out_json: str = "race_canvas.json",
                      session_filter: Optional[List[str]] = None,
                      downsample: int = 5):
    df = pd.read_parquet(common_path) if common_path.endswith(".parquet") else pd.read_csv(common_path)

    # required columns
    need = ["meta_session","vehicle_number","t_rel","meta_time"]
    missing = [c for c in need if c not in df.columns]
    if missing:
        raise ValueError(f"missing column(s): {missing}")

    # lat/lon detection (keep your names)
    if "lat" in df.columns and "lon" in df.columns:
        LAT, LON = "lat", "lon"
    elif "VBOX_Lat_Min" in df.columns and "VBOX_Long_Minutes" in df.columns:
        LAT, LON = "VBOX_Lat_Min", "VBOX_Long_Minutes"
    else:
        raise ValueError("No lat/lon found: need either (lat,lon) or (VBOX_Lat_Min,VBOX_Long_Minutes)")

    df["meta_session"] = df["meta_session"].astype(str)
    df["vehicle_number"] = df["vehicle_number"].astype(str)
    df = df.dropna(subset=[LAT, LON, "t_rel"]).sort_values(["meta_session","vehicle_number","t_rel"])

    if session_filter:
        df = df[df["meta_session"].isin(session_filter)]

    data = {"sessions": {}}
    step = max(1, int(downsample))

    for sess, g_s in df.groupby("meta_session", sort=False):
        # projection origin per session
        lat_med = g_s[LAT].median()
        lon_med = g_s[LON].median()
        lat0_rad = np.deg2rad(lat_med)
        m_per_deg_lat = 110_540.0
        m_per_deg_lon = 111_320.0 * float(np.cos(lat0_rad))

        def proj_x(series): return (series - lon_med) * m_per_deg_lon
        def proj_y(series): return (series - lat_med) * m_per_deg_lat

        sess_obj = {"cars": {}, "meta": {"lat0": float(lat_med), "lon0": float(lon_med)}}

        for vid, g in g_s.groupby("vehicle_number", sort=False):
            # Downsample in time order
            h = g.iloc[::step, :].copy()

            # Build base car object
            x = proj_x(h[LON].values).astype("float32")
            y = proj_y(h[LAT].values).astype("float32")
            t = pd.to_numeric(h["t_rel"], errors="coerce").values.astype("float32")
            car_obj = {"t": t.tolist(), "x": x.tolist(), "y": y.tolist()}

            # Optional lap change arrays
            if "lap" in h.columns:
                laps = pd.to_numeric(h["lap"], errors="coerce").ffill().fillna(0).astype(int).values
                # indices where lap value changes (including first)
                change_idx = np.flatnonzero(np.r_[True, laps[1:] != laps[:-1]])
                if change_idx.size > 0:
                    lap_t = t[change_idx].astype("float32")
                    lap_v = laps[change_idx].astype("int32")
                    car_obj["lap_t"] = lap_t.tolist()
                    car_obj["lap_v"] = lap_v.tolist()

            sess_obj["cars"][vid] = car_obj

        data["sessions"][sess] = sess_obj

    Path(out_json).write_text(json.dumps(data), encoding="utf-8")
    print(f"Wrote {out_json}  | sessions={len(data['sessions'])}  cars={sum(len(s['cars']) for s in data['sessions'].values())}")


# usage example:
export_for_canvas('simulation-data/common.parquet', out_json="race_canvas.json", downsample=5)
