import pandas as pd

from app.services.potholes import (
    build_map_dataframe,
    flatten_pothole_records,
    get_color,
    get_severity,
)


def test_get_color_thresholds():
    assert get_color(10) == [234, 179, 8, 220]
    assert get_color(50) == [249, 115, 22, 220]
    assert get_color(151) == [239, 68, 68, 220]
    assert get_color(10, is_selected=True) == [34, 197, 94, 255]


def test_get_severity_thresholds():
    assert get_severity(10) == "Low"
    assert get_severity(50) == "Medium"
    assert get_severity(151) == "High"


def test_build_map_dataframe_groups_and_marks_selection():
    df = pd.DataFrame(
        [
            {"id": "a", "latitude": 10.12344, "longitude": 20.12344},
            {"id": "b", "latitude": 10.12343, "longitude": 20.12343},
            {"id": "c", "latitude": 11.00001, "longitude": 21.00001},
        ]
    )

    current_selection = {"lat": 10.1234, "lng": 20.1234}
    result = build_map_dataframe(df, current_selection=current_selection, logged_in=True)

    assert len(result) == 2
    first_group = result.iloc[0]
    assert first_group["report_count"] == 2
    assert first_group["height"] == 2
    assert first_group["radius"] > 0
    assert first_group["severity"] in ["Low", "Medium", "High"]
    assert first_group["color"] == [34, 197, 94, 255]


def test_flatten_pothole_records_supports_flat_and_nested_paths():
    flat_data = {
        "flat-1": {
            "lat": 17.4864094,
            "lng": 78.5689702,
            "status": "Pending",
            "cost": "₹7566",
        }
    }
    users_data = {
        "uid-1": {
            "potholes": {
                "nested-1": {
                    "latitude": 17.5201,
                    "longitude": 78.3602,
                    "duplicate": False,
                    "time": 1774796808071,
                }
            }
        }
    }

    df = flatten_pothole_records(flat_data=flat_data, users_data=users_data)

    assert len(df) == 2
    assert set(["latitude", "longitude", "lat", "lng", "lon"]).issubset(df.columns)

    flat_row = df[df["id"] == "flat-1"].iloc[0]
    assert flat_row["reporter_uid"] is None
    assert flat_row["lat"] == flat_row["latitude"]
    assert flat_row["lon"] == flat_row["longitude"]

    nested_row = df[df["id"] == "nested-1"].iloc[0]
    assert nested_row["reporter_uid"] == "uid-1"
    assert nested_row["source_path"] == "/users/uid-1/potholes/nested-1"


def test_flatten_pothole_records_skips_invalid_or_zero_coordinates():
    flat_data = {
        "bad-1": {"lat": "abc", "lng": 78.1},
        "bad-2": {"lat": 0.0, "lng": 0.0},
    }
    users_data = {
        "uid-1": {
            "potholes": {
                "bad-3": {"latitude": None, "longitude": 77.0},
            }
        }
    }

    df = flatten_pothole_records(flat_data=flat_data, users_data=users_data)
    assert df.empty
