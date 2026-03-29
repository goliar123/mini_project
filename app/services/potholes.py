from typing import Any, Optional

import pandas as pd
import streamlit as st

from app.config import COORD_ROUNDING


def _extract_coordinates(record: dict) -> Optional[tuple[float, float]]:
    latitude = record.get("latitude", record.get("lat"))
    longitude = record.get("longitude", record.get("lng"))
    if latitude is None or longitude is None:
        return None

    try:
        lat = float(latitude)
        lng = float(longitude)
    except (TypeError, ValueError):
        return None

    if not pd.notna(lat) or not pd.notna(lng):
        return None

    # Ignore placeholder coordinates where GPS lock did not happen.
    if lat == 0.0 and lng == 0.0:
        return None

    return lat, lng


def _normalize_record(
    record_id: str,
    record_value: dict,
    reporter_uid: Optional[str],
    source_path: str,
) -> Optional[dict]:
    coords = _extract_coordinates(record_value)
    if not coords:
        return None

    latitude, longitude = coords
    normalized = dict(record_value)
    normalized["id"] = record_id
    normalized["reporter_uid"] = reporter_uid
    normalized["source_path"] = source_path
    normalized["latitude"] = latitude
    normalized["longitude"] = longitude
    normalized["lat"] = latitude
    normalized["lng"] = longitude
    normalized["lon"] = longitude
    if "confidence" not in normalized:
        normalized["confidence"] = 0.0
    return normalized


def flatten_pothole_records(
    flat_data: Optional[dict], users_data: Optional[dict]
) -> pd.DataFrame:
    rows: list[dict] = []

    if isinstance(flat_data, dict):
        for record_id, record_value in flat_data.items():
            if not isinstance(record_value, dict):
                continue
            normalized = _normalize_record(
                record_id=str(record_id),
                record_value=record_value,
                reporter_uid=None,
                source_path=f"/potholes/{record_id}",
            )
            if normalized:
                rows.append(normalized)

    if isinstance(users_data, dict):
        for uid, user_info in users_data.items():
            if not isinstance(user_info, dict):
                continue

            potholes = user_info.get("potholes")
            if not isinstance(potholes, dict):
                continue

            for record_id, record_value in potholes.items():
                if not isinstance(record_value, dict):
                    continue
                normalized = _normalize_record(
                    record_id=str(record_id),
                    record_value=record_value,
                    reporter_uid=str(uid),
                    source_path=f"/users/{uid}/potholes/{record_id}",
                )
                if normalized:
                    rows.append(normalized)

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    return df.sort_values(by=["latitude", "longitude"]).reset_index(drop=True)


@st.cache_data(ttl=5, show_spinner=False)
def get_data() -> pd.DataFrame:
    try:
        from app.data.firebase_client import potholes_ref, users_ref

        flat_data = potholes_ref().get()
        users_data = users_ref().get()
        return flatten_pothole_records(flat_data=flat_data, users_data=users_data)
    except Exception:
        return pd.DataFrame()


def delete_cluster(target_lat: float, target_lng: float) -> int:
    try:
        from app.data.firebase_client import potholes_ref, users_ref

        deleted_count = 0
        rounded_target_lat = round(target_lat, COORD_ROUNDING)
        rounded_target_lng = round(target_lng, COORD_ROUNDING)

        flat_data = potholes_ref().get()
        if isinstance(flat_data, dict):
            flat_updates = {}
            for key, value in flat_data.items():
                if not isinstance(value, dict):
                    continue

                coords = _extract_coordinates(value)
                if not coords:
                    continue

                lat, lng = coords
                if round(lat, COORD_ROUNDING) == rounded_target_lat and round(
                    lng, COORD_ROUNDING
                ) == rounded_target_lng:
                    flat_updates[key] = None

            if flat_updates:
                potholes_ref().update(flat_updates)
                deleted_count += len(flat_updates)

        users_data = users_ref().get()
        if isinstance(users_data, dict):
            user_updates = {}
            for uid, user_info in users_data.items():
                if not isinstance(user_info, dict):
                    continue

                potholes = user_info.get("potholes")
                if not isinstance(potholes, dict):
                    continue

                for key, value in potholes.items():
                    if not isinstance(value, dict):
                        continue

                    coords = _extract_coordinates(value)
                    if not coords:
                        continue

                    lat, lng = coords
                    if round(lat, COORD_ROUNDING) == rounded_target_lat and round(
                        lng, COORD_ROUNDING
                    ) == rounded_target_lng:
                        user_updates[f"{uid}/potholes/{key}"] = None

            if user_updates:
                users_ref().update(user_updates)
                deleted_count += len(user_updates)

        if deleted_count > 0:
            get_data.clear()
        return deleted_count
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
