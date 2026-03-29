import pandas as pd

from app.services.potholes import build_map_dataframe, get_color, get_severity


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
