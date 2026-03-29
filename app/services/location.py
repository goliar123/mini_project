import streamlit as st
from streamlit_js_eval import get_geolocation


def update_location_from_browser() -> bool:
    if st.session_state.location_locked:
        return False

    try:
        loc = get_geolocation()
        if not loc:
            return False

        st.session_state.map_lat = loc["coords"]["latitude"]
        st.session_state.map_lng = loc["coords"]["longitude"]
        st.session_state.location_locked = True
        return True
    except Exception:
        return False
