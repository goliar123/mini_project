import pandas as pd
import pydeck as pdk
import streamlit as st

from app.services.potholes import build_map_dataframe, extract_selection


def _render_legend(map_view_mode: str, visible_clusters: int, active_filters: int) -> None:
    mode_label = "Heatmap" if map_view_mode == "heatmap" else "Scatter"
    st.markdown(
        f"""
        <div class='map-legend-shell'>
            <div class='map-legend-topline'>
                <div class='map-legend-stats'>
                    <span class='map-stat-pill'>Visible Clusters: <b>{visible_clusters}</b></span>
                    <span class='map-stat-pill'>Active Filters: <b>{active_filters}</b></span>
                </div>
                <span class='map-mode-label'>Mode: {mode_label}</span>
            </div>
            <div class='map-chip-row'>
                <span class='map-chip map-chip-low'>Low (1-49)</span>
                <span class='map-chip map-chip-medium'>Medium (50-150)</span>
                <span class='map-chip map-chip-high'>High (151+)</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _build_layers(map_df: pd.DataFrame, map_view_mode: str, is_interactive: bool) -> tuple[list, bool]:
    if map_view_mode == "heatmap":
        heat_layer = pdk.Layer(
            "HeatmapLayer",
            map_df,
            get_position=["lon_round", "lat_round"],
            get_weight="report_count",
            aggregation="SUM",
            threshold=0.04,
            radiusPixels=50,
            intensity=1,
            id="pothole_heatmap",
        )
        return [heat_layer], False

    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        map_df,
        get_position=["lon_round", "lat_round"],
        get_radius="radius",
        get_fill_color="color",
        stroked=True,
        get_line_color=[255, 255, 255, 90],
        line_width_min_pixels=1,
        pickable=is_interactive,
        auto_highlight=is_interactive,
        id="pothole_scatter",
    )
    return [scatter_layer], is_interactive


def _build_tooltip(allow_selection: bool) -> dict:
    if allow_selection:
        body = (
            "<div style='font-size:0.7rem; text-transform:uppercase; letter-spacing:1.1px; opacity:0.82;'>"
            "Cluster Details"
            "</div>"
            "<div style='font-size:1.05rem; font-weight:750; margin-top:2px;'>{report_count} reports</div>"
            "<div style='margin-top:6px; font-size:0.82rem; opacity:0.92;'>Severity <b>{severity}</b></div>"
        )
    else:
        body = (
            "<div style='font-size:0.7rem; text-transform:uppercase; letter-spacing:1.1px; opacity:0.82;'>"
            "Density View"
            "</div>"
            "<div style='font-size:1.02rem; font-weight:740; margin-top:2px;'>{report_count} reports</div>"
            "<div style='margin-top:6px; font-size:0.82rem; opacity:0.92;'>Zoom for finer cluster context</div>"
        )

    return {
        "html": body,
        "style": {
            "backgroundColor": "rgba(18, 24, 33, 0.92)",
            "color": "#F8FAFC",
            "fontFamily": "Lexend, sans-serif",
            "fontSize": "13px",
            "borderRadius": "12px",
            "padding": "10px 12px",
            "border": "1px solid rgba(148, 163, 184, 0.32)",
            "boxShadow": "0 10px 24px rgba(0, 0, 0, 0.28)",
        },
    }


def render_map(df: pd.DataFrame, severity_filters: list[str], map_view_mode: str, map_height: int = 680) -> None:
    if df.empty:
        st.info("No pothole data found. Verify Firebase credentials, database URL, and /potholes records.")
        return

    current_selection = st.session_state.selected_pothole
    is_interactive = st.session_state.logged_in
    map_df = build_map_dataframe(df, current_selection, is_interactive)
    map_df = map_df[map_df["severity"].isin(severity_filters)]

    _render_legend(
        map_view_mode=map_view_mode,
        visible_clusters=int(len(map_df)),
        active_filters=int(len(severity_filters)),
    )

    if map_df.empty:
        st.warning("No potholes match the selected severity filters.")
        return

    if (map_df["lat_round"] == 0).all() and (map_df["lon_round"] == 0).all():
        st.warning("All pothole reports currently have invalid GPS coordinates (0,0). Update data source to send real latitude/longitude.")
        return

    layers, allow_selection = _build_layers(map_df, map_view_mode, is_interactive)

    center_lat = st.session_state.map_lat
    center_lng = st.session_state.map_lng
    if not st.session_state.location_locked:
        center_lat = float(map_df["lat_round"].mean())
        center_lng = float(map_df["lon_round"].mean())

    view_state = pdk.ViewState(
        latitude=center_lat,
        longitude=center_lng,
        zoom=15.5,
        pitch=35 if map_view_mode == "scatter" else 0,
    )

    tooltip = _build_tooltip(allow_selection)

    selection_mode = "rerun" if allow_selection else "ignore"
    event = st.pydeck_chart(
        pdk.Deck(
            map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
            layers=layers,
            initial_view_state=view_state,
            tooltip=tooltip,
        ),
        on_select=selection_mode,
        selection_mode="single-object",
        use_container_width=True,
        height=map_height,
    )

    if not allow_selection:
        return

    new_selection = extract_selection(event, map_df)
    if new_selection and st.session_state.selected_pothole != new_selection:
        st.session_state.selected_pothole = new_selection
        st.session_state.show_resolve_panel = True
