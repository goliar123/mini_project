import streamlit as st
from datetime import datetime

from app.data.firebase_client import initialize_firebase
from app.auth.user_store import set_user_map_view_mode
from app.auth.session import clear_persisted_auth, restore_auth_from_query_params
from app.services.location import update_location_from_browser
from app.services.potholes import delete_cluster, get_data
from app.startup import configure_page, init_session_state
from app.ui.layout import (
    render_admin_records_section,
    render_auth_panel,
    # render_contact_section,
    render_dashboard_command_bar,
    render_footer,
    render_header,
    render_home_page,
    render_resolve_panel,
    render_sidebar,
)
from app.ui.map_view import render_map
from app.ui.styles import get_theme, inject_global_styles


def run() -> None:
    configure_page()
    init_session_state()

    if not st.session_state.logged_in:
        restored = restore_auth_from_query_params(st.session_state)
        if not restored and "auth" in st.query_params:
            clear_persisted_auth()

    theme = get_theme(st.session_state.dark_mode)
    inject_global_styles(
        theme,
        show_sidebar=st.session_state.logged_in and st.session_state.show_dashboard_sidebar,
    )

    if not st.session_state.logged_in:
        render_home_page()
        render_auth_panel()
        # render_contact_section()
        render_footer()
        return

    initialize_firebase()

    # Update browser location once per session without forcing a full rerun.
    update_location_from_browser()

    previous_map_view_mode = st.session_state.map_view_mode
    command_actions = render_dashboard_command_bar()
    severity_filters = command_actions.get("severity_filters", ["Low", "Medium", "High"])
    map_view_mode = command_actions.get("map_view_mode", st.session_state.map_view_mode)

    if (
        st.session_state.current_role == "user"
        and st.session_state.current_user
        and map_view_mode != previous_map_view_mode
    ):
        set_user_map_view_mode(st.session_state.current_user, map_view_mode)
    st.session_state.map_view_mode = map_view_mode

    if st.session_state.show_dashboard_sidebar:
        render_sidebar(theme)

    df = get_data()
    total_active = len(df)
    render_header(total_active)

    if st.session_state.current_role == "admin":
        render_admin_records_section(df)

    if not st.session_state.selected_pothole:
        st.session_state.show_resolve_panel = False

    show_resolve_panel = bool(st.session_state.selected_pothole and st.session_state.show_resolve_panel)

    panel_actions = {"resolve": False}
    if show_resolve_panel:
        map_col, panel_col = st.columns([0.72, 0.28], gap="medium")
        with map_col:
            render_map(df, severity_filters=severity_filters, map_view_mode=map_view_mode, map_height=620)
        with panel_col:
            panel_actions = render_resolve_panel()
    else:
        render_map(df, severity_filters=severity_filters, map_view_mode=map_view_mode, map_height=700)

    # render_contact_section()
    render_footer()

    if (
        panel_actions.get("resolve")
        and st.session_state.selected_pothole
        and st.session_state.current_role == "admin"
    ):
        st.session_state.is_resolving = True
        selected = st.session_state.selected_pothole
        with st.spinner("Resolving pothole cluster..."):
            count = delete_cluster(selected["lat"], selected["lng"])
        st.session_state.is_resolving = False
        if count > 0:
            st.session_state.resolution_log.insert(
                0,
                {
                    "time": datetime.now().strftime("%H:%M"),
                    "user": st.session_state.current_user or "admin",
                    "count": count,
                    "lat": selected["lat"],
                    "lng": selected["lng"],
                },
            )
            st.session_state.resolution_log = st.session_state.resolution_log[:10]
            st.markdown(
                """<style>div[data-testid="stToast"] {background-color: #10B981 !important; border: 1px solid #059669 !important;}</style>""",
                unsafe_allow_html=True,
            )
            st.toast(f"Fixed {count} potholes")
            st.session_state.selected_pothole = None
            st.session_state.show_resolve_panel = False
            st.rerun()
        else:
            st.markdown(
                """<style>div[data-testid="stToast"] {background-color: #EF4444 !important; border: 1px solid #B91C1C !important;}</style>""",
                unsafe_allow_html=True,
            )
            st.toast("Could not resolve cluster. Please retry.")


run()
