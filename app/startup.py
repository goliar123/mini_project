import streamlit as st

from app.config import DEFAULT_MAP_LAT, DEFAULT_MAP_LNG


def configure_page() -> None:
    st.set_page_config(
        page_title="Live Pothole Map",
        layout="wide",
        page_icon="⚠️",
        initial_sidebar_state="expanded",
    )


def init_session_state() -> None:
    defaults = {
        "logged_in": False,
        "selected_pothole": None,
        "dark_mode": False,
        "current_user": None,
        "current_role": None,
        "show_auth_panel": False,
        "severity_filters": ["Low", "Medium", "High"],
        "map_view_mode": "heatmap",
        "last_map_view_mode": "heatmap",
        "is_resolving": False,
        "resolution_log": [],
        "map_lat": DEFAULT_MAP_LAT,
        "map_lng": DEFAULT_MAP_LNG,
        "location_locked": False,
        "show_dashboard_sidebar": False,
        "show_resolve_panel": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
