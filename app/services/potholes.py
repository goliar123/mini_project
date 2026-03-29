from typing import Any, Optional

import pandas as pd
import streamlit as st

from app.config import COORD_ROUNDING


@st.cache_data(ttl=5, show_spinner=False)
def get_data() -> pd.DataFrame:
    try:
        from app.data.firebase_client import potholes_ref

        data = potholes_ref().get()
        if not data:
            return pd.DataFrame()

        rows = []
        for key, value in data.items():
            value["id"] = key
            if "confidence" not in value:
                value["confidence"] = 0.0
            rows.append(value)

        df = pd.DataFrame(rows)
        return df.sort_values(by=["latitude", "longitude"]).reset_index(drop=True)
    except Exception:
        return pd.DataFrame()


def delete_cluster(target_lat: float, target_lng: float) -> int:
    try:
        from app.data.firebase_client import potholes_ref

        data = potholes_ref().get()
        if not data:
            return 0

        keys_to_delete = []
        for key, value in data.items():
            if (
                round(value["latitude"], COORD_ROUNDING)
                == round(target_lat, COORD_ROUNDING)
                and round(value["longitude"], COORD_ROUNDING)
                == round(target_lng, COORD_ROUNDING)
            ):
                keys_to_delete.append(key)

        if not keys_to_delete:
            return 0

        updates = {key: None for key in keys_to_delete}
        potholes_ref().update(updates)
        get_data.clear()
        return len(keys_to_delete)
    except Exception:
        return 0


def get_color(count: int, is_selected: bool = False) -> list[int]:
    if is_selected:
        return [34, 197, 94, 255]
    if count > 150:
        return [239, 68, 68, 220]
    if count >= 50:
        return [249, 115, 22, 220]
    return [234, 179, 8, 220]


def get_severity(count: int) -> str:
    if count > 150:
        return "High"
    if count >= 50:
        return "Medium"
    return "Low"


def _is_selected(row: pd.Series, current_selection: Optional[dict], logged_in: bool) -> bool:
    if not (current_selection and logged_in):
        return False
    return (
        row["lat_round"] == current_selection["lat"]
        and row["lon_round"] == current_selection["lng"]
    )


def build_map_dataframe(
    df: pd.DataFrame, current_selection: Optional[dict], logged_in: bool
) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    working_df = df.copy()
    working_df["lat_round"] = working_df["latitude"].round(COORD_ROUNDING)
    working_df["lon_round"] = working_df["longitude"].round(COORD_ROUNDING)

    map_df = (
        working_df.groupby(["lat_round", "lon_round"])
        .size()
        .reset_index(name="report_count")
        .sort_values(by=["lat_round", "lon_round"])
        .reset_index(drop=True)
    )

    df_unique = working_df.drop_duplicates(subset=["lat_round", "lon_round"])[
        ["lat_round", "lon_round", "id"]
    ]
    map_df = pd.merge(map_df, df_unique, on=["lat_round", "lon_round"], how="left")

    map_df["color"] = map_df.apply(
        lambda row: get_color(
            row["report_count"], _is_selected(row, current_selection, logged_in)
        ),
        axis=1,
    )
    map_df["severity"] = map_df["report_count"].apply(get_severity)
    map_df["height"] = map_df["report_count"].clip(upper=100)
    map_df["radius"] = map_df["report_count"].clip(lower=1, upper=120) * 6

    return map_df


def extract_selection(event: Any, map_df: pd.DataFrame) -> Optional[dict]:
    if not event.selection or "objects" not in event.selection or not event.selection["objects"]:
        return None

    first_key = list(event.selection["objects"].keys())[0]
    selection_item = event.selection["objects"][first_key][0]

    row = None
    if isinstance(selection_item, dict):
        row = selection_item
    elif isinstance(selection_item, int) and selection_item < len(map_df):
        row = map_df.iloc[selection_item]

    if row is None:
        return None

    get_val = lambda r, k: r[k] if isinstance(r, dict) else r[k]
    return {
        "id": get_val(row, "id"),
        "count": get_val(row, "report_count"),
        "lat": get_val(row, "lat_round"),
        "lng": get_val(row, "lon_round"),
    }
