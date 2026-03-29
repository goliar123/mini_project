import streamlit as st

from app.auth.session import login, logout, register_user

SEVERITY_OPTIONS = ["Low", "Medium", "High"]
MAP_VIEW_OPTIONS = ["heatmap", "scatter"]
LOCAL_HISTORY_TOLERANCE = 0.003


def _show_toast(message: str, success: bool) -> None:
    color = "#10B981" if success else "#EF4444"
    border = "#059669" if success else "#B91C1C"
    st.markdown(
        f"""<style>div[data-testid=\"stToast\"] {{background-color: {color} !important; border: 1px solid {border} !important;}}</style>""",
        unsafe_allow_html=True,
    )
    st.toast(message)


def render_home_page() -> None:
    st.markdown(
        '''
        <div class='landing-topbar'>
            <div class='landing-topbar-brand'>Road Safety Command</div>
            <a class='landing-login-link' href='#secure-login'>Login</a>
        </div>
        <section class="claude-hero-container">
            <div class="claude-hero-topline">Road Safety Command</div>
            <div class="claude-hero-text">
                <h1 class='headline-title claude-hero-title'>Good afternoon</h1>
                <p class="claude-hero-subtitle">
                    Welcome back to the Road Safety Command. Access your unified dashboard to resolve active clusters and view municipal metrics.
                </p>
            </div>
            <section class="preview-shell">
                <div class="preview-head">
                    <div class="preview-kicker">Coming Next</div>
                    <div class="preview-meta">Preview upcoming capabilities before sign-in</div>
                </div>
                <div class="preview-scroll" role="region" aria-label="Upcoming feature previews">
                    <article class="preview-item">
                        <div class="preview-chip preview-chip-progress">In Progress</div>
                        <h3>Predictive Cluster Forecast</h3>
                        <p>Anticipate pothole growth by area using historical density trends and weather overlays.</p>
                    </article>
                    <article class="preview-item">
                        <div class="preview-chip preview-chip-soon">Soon</div>
                        <h3>Ward-Level Maintenance Timeline</h3>
                        <p>Track pending and resolved operations by ward with clearer public-works accountability.</p>
                    </article>
                    <article class="preview-item">
                        <div class="preview-chip preview-chip-progress">In Progress</div>
                        <h3>Smart Priority Queue</h3>
                        <p>Auto-rank incidents using severity, report volume, and nearby road criticality signals.</p>
                    </article>
                    <article class="preview-item">
                        <div class="preview-chip preview-chip-soon">Soon</div>
                        <h3>Field Team Dispatch Panel</h3>
                        <p>Push selected clusters directly to maintenance crews with status sync and audit history.</p>
                    </article>
                    <article class="preview-item">
                        <div class="preview-chip preview-chip-soon">Soon</div>
                        <h3>Citizen Report Digest</h3>
                        <p>Summarize complaint hotspots into actionable briefings for daily operations review.</p>
                    </article>
                    <article class="preview-item">
                        <div class="preview-chip preview-chip-progress">In Progress</div>
                        <h3>Live Resolution Performance</h3>
                        <p>Measure turnaround time, closure quality, and repeat-incident rates in one compact view.</p>
                    </article>
                </div>
            </section>
        </section>
        ''', unsafe_allow_html=True
    )
    
    left, right = st.columns([0.45, 0.55], gap="large")
    with left:
        st.markdown("<div id='secure-login'></div>", unsafe_allow_html=True)
        st.markdown("<div class='auth-alignment-wrapper'>", unsafe_allow_html=True)
        st.markdown(
            '''
            <section class='auth-stage'>
                <div class='auth-panel'>
                    <div class='auth-title'>Secure Access</div>
                    <div class='auth-subtitle'>Sign in to unlock operational dashboards and incident workflows.</div>
            ''',
            unsafe_allow_html=True,
        )
        login_tab, register_tab = st.tabs(["Login", "Register"])

        with login_tab:
            username = st.text_input("Username", key="home_login_username")
            password = st.text_input("Password", type="password", key="home_login_password")
            if st.button("Login", type="primary", use_container_width=True, key="home_login_btn"):
                success, message = login(st.session_state, username, password)
                _show_toast(message, success)
                if success:
                    st.session_state.show_auth_panel = False
                    st.rerun()

        with register_tab:
            st.caption("Admin accounts cannot be registered.")
            username = st.text_input("New Username", key="home_register_username")
            password = st.text_input("New Password", type="password", key="home_register_password")
            confirm = st.text_input("Confirm Password", type="password", key="home_register_confirm")
            if st.button("Create Account", type="secondary", use_container_width=True, key="home_register_btn"):
                success, message = register_user(username, password, confirm)
                _show_toast(message, success)

        st.markdown("</div></section>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(
            '''
            <div class='claude-grid-visual'>
                <div class='cg-card cg-card-large'>
                    <div class='cg-icon'>*</div>
                    <div class='cg-title'>Density Heatmap Intelligence</div>
                    <div class='cg-desc'>Analyze massive road clusters instantly, spotting critical infrastructure decay before it affects transit corridors.</div>
                </div>
                <div class='cg-card'>
                    <div class='cg-icon'>+</div>
                    <div class='cg-title'>Audit Trails</div>
                    <div class='cg-desc'>Track resolution events transparently.</div>
                </div>
                <div class='cg-card'>
                    <div class='cg-icon'>#</div>
                    <div class='cg-title'>Role Framework</div>
                    <div class='cg-desc'>Granular admin permissions.</div>
                </div>
                <div class='cg-card cg-card-wide'>
                    <div class='cg-icon'>~</div>
                    <div class='cg-title'>High-Speed Action Panels</div>
                    <div class='cg-desc'>Switch to scatter mode to target and mark immediate repairs directly from the active command overlay.</div>
                </div>
            </div>
            ''', unsafe_allow_html=True
        )

def render_auth_panel() -> None:
    pass


def render_contact_section() -> None:
    st.markdown(
        """
        <section class='contact-shell'>
            <div class='contact-head'>
                <div class='contact-kicker'>Contact Page</div>
                <h2 class='contact-title'>Get Support And Escalate Field Incidents</h2>
            </div>
            <div class='contact-grid'>
                <article class='contact-card'>
                    <div class='contact-label'>Operations Desk</div>
                    <div class='contact-value'>support@roadsafety-command.local</div>
                    <div class='contact-value'>+91 40 1000 2200</div>
                    <div class='contact-copy'>Mon-Sat, 08:00-20:00 IST</div>
                </article>
                <article class='contact-card'>
                    <div class='contact-label'>Escalation</div>
                    <div class='contact-value'>dispatch@roadsafety-command.local</div>
                    <div class='contact-value'>+91 40 1000 2211</div>
                    <div class='contact-copy'>Critical clusters are triaged in under 15 minutes.</div>
                </article>
                <article class='contact-card'>
                    <div class='contact-label'>Support Channels</div>
                    <div class='contact-value'>Ops Chat: #roadsafety-live</div>
                    <div class='contact-value'>On-call: ward-response@roadsafety-command.local</div>
                    <div class='contact-copy'>Share location, severity, and cluster count for faster support.</div>
                </article>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown(
        """
        <footer class='page-footer'>
            <div class='page-footer-grid'>
                <section class='page-footer-card'>
                    <div class='page-footer-kicker'>Contact</div>
                    <div class='page-footer-title'>Road Safety Command Center</div>
                    <div class='page-footer-line'>support@roadsafety-command.local</div>
                    <div class='page-footer-line'>+91 40 1000 2200</div>
                    <div class='page-footer-line'>Mon-Sat, 8:00-20:00</div>
                </section>
                <section class='page-footer-card'>
                    <div class='page-footer-kicker'>Quick Links</div>
                    <a class='page-footer-link' href='#'>Operations Dashboard</a>
                    <a class='page-footer-link' href='#'>Issue Reporting</a>
                    <a class='page-footer-link' href='#'>Deployment Health</a>
                </section>
                <section class='page-footer-card'>
                    <div class='page-footer-kicker'>Governance</div>
                    <a class='page-footer-link' href='#'>Privacy Notice</a>
                    <a class='page-footer-link' href='#'>Terms Of Use</a>
                    <a class='page-footer-link' href='#'>Support SLA</a>
                </section>
            </div>
            <div class='page-footer-bottom'>
                <span>© 2026 Road Safety Command</span>
                <span>Operational Intelligence Console</span>
            </div>
        </footer>
        """,
        unsafe_allow_html=True,
    )

def render_header(total_active: int) -> None:
    left, right = st.columns([0.93, 0.07])
    with left:
        st.markdown(
            f"""
        <section class='dash-shell'>
            <div class='dash-copy'>
                <div class='dash-kicker'>Operations Dashboard</div>
                <h1 class='headline-title dash-title'>Integrated Pothole Detection and Maintenance System</h1>
            </div>
            <div class='headline-metrics'>
                <span class='active-count'>{total_active}</span>
                <span class='active-label'>Active Potholes</span>
            </div>
        </section>
        """,
            unsafe_allow_html=True,
        )

    with right:
        st.toggle("Dark Mode", key="dark_mode", label_visibility="collapsed")


def _render_map_view_selector_inline() -> str:
    current = st.session_state.map_view_mode if st.session_state.map_view_mode in MAP_VIEW_OPTIONS else "heatmap"
    selected = st.radio(
        "Mode",
        MAP_VIEW_OPTIONS,
        index=MAP_VIEW_OPTIONS.index(current),
        format_func=lambda value: "Heatmap" if value == "heatmap" else "Scatter",
        horizontal=True,
        key="dashboard_mode_radio",
    )
    return selected


def _render_severity_filter_inline() -> list[str]:
    selected = st.multiselect(
        "Severity",
        SEVERITY_OPTIONS,
        default=st.session_state.severity_filters,
        help="Filter map clusters by severity",
        key="dashboard_severity_multiselect",
    )
    return selected if selected else []


def render_dashboard_command_bar() -> dict:
    actions = {
        "severity_filters": st.session_state.severity_filters,
        "map_view_mode": st.session_state.map_view_mode,
    }

    st.markdown(
        """
        <div class='command-shell'>
            <div class='command-kicker'>Command Surface</div>
            <div class='command-sub'>Run map workflows here: mode, filter, inspect, and resolve.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([0.26, 0.52, 0.22])
    with c1:
        map_view_mode = _render_map_view_selector_inline()
        actions["map_view_mode"] = map_view_mode

        if st.session_state.last_map_view_mode != map_view_mode:
            target = "Heatmap" if map_view_mode == "heatmap" else "Scatter"
            st.markdown(
                f"<div class='mode-transition-note'>Switched to {target} view.</div>",
                unsafe_allow_html=True,
            )
            st.session_state.last_map_view_mode = map_view_mode

    with c2:
        severity_filters = _render_severity_filter_inline()
        st.session_state.severity_filters = severity_filters
        actions["severity_filters"] = severity_filters

    with c3:
        st.markdown("<div class='command-actions-title'>Panel And Account</div>", unsafe_allow_html=True)
        with st.container(border=True):
            panel_label = "Open Panel" if not st.session_state.show_dashboard_sidebar else "Hide Panel"
            if st.button(panel_label, type="secondary", use_container_width=True, key="toggle_dashboard_sidebar_btn"):
                st.session_state.show_dashboard_sidebar = not st.session_state.show_dashboard_sidebar
                st.rerun()

            if st.button("Log Out", type="secondary", use_container_width=True, key="dashboard_logout_btn"):
                logout(st.session_state)
                st.rerun()
            st.markdown("<div class='command-actions-note'>Workspace controls and account actions</div>", unsafe_allow_html=True)

    return actions


def _get_local_resolution_history(selected: dict, entries: list[dict]) -> list[dict]:
    lat = selected["lat"]
    lng = selected["lng"]
    return [
        item
        for item in entries
        if abs(item["lat"] - lat) <= LOCAL_HISTORY_TOLERANCE
        and abs(item["lng"] - lng) <= LOCAL_HISTORY_TOLERANCE
    ]


def render_resolve_panel() -> dict:
    actions = {"resolve": False}
    selected = st.session_state.selected_pothole
    if not selected:
        return actions

    st.markdown("<div class='panel-align-offset'></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <section class='resolve-panel-shell'>
            <div class='resolve-panel-head'>
                <div>
                    <div class='resolve-panel-kicker'>Resolve Panel</div>
                    <div class='resolve-panel-title'>{selected['count']} reports selected</div>
                </div>
                <div class='resolve-panel-meta'>({selected['lat']:.3f}, {selected['lng']:.3f})</div>
            </div>
            <div class='resolve-panel-note'>Use this panel to complete resolution without leaving the map context.</div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.current_role == "admin" and st.session_state.map_view_mode == "scatter":
        if st.session_state.is_resolving:
            st.button("Resolving...", type="primary", use_container_width=True, disabled=True, key="panel_resolve_disabled_btn")
        elif st.button("Mark as Resolved", type="primary", use_container_width=True, key="panel_resolve_btn"):
            actions["resolve"] = True
    elif st.session_state.current_role != "admin":
        st.info("View only. Only admin users can resolve clusters.")
    else:
        st.warning("Switch to Scatter mode to resolve this cluster.")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Clear", type="secondary", use_container_width=True, key="panel_clear_selection_btn"):
            st.session_state.selected_pothole = None
            st.session_state.show_resolve_panel = False
            st.rerun()
    with c2:
        if st.button("Close", type="secondary", use_container_width=True, key="panel_close_btn"):
            st.session_state.show_resolve_panel = False
            st.rerun()

    st.markdown("<div class='panel-history-kicker'>Nearby action history</div>", unsafe_allow_html=True)
    local_history = _get_local_resolution_history(selected, st.session_state.resolution_log)
    if not local_history:
        st.caption("No nearby actions yet for this cluster.")
    else:
        for item in local_history[:4]:
            st.markdown(
                f"""
                <div class='panel-history-item'>
                    <div class='panel-history-title'>{item['count']} potholes resolved</div>
                    <div class='panel-history-sub'>by {item['user']} at {item['time']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    return actions


def _render_recent_resolutions() -> None:
    st.sidebar.markdown("### Recent Resolved")
    entries = st.session_state.resolution_log[:5]
    if not entries:
        st.sidebar.caption("No potholes resolved yet.")
        return

    for item in entries:
        st.sidebar.markdown(
            f"""
            <div class='glass-card' style='margin-bottom:8px; padding:10px;'>
                <div class='log-title'>{item['count']} resolved</div>
                <div class='log-sub'>by {item['user']} at {item['time']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_sidebar(theme: dict) -> None:

    username = st.session_state.current_user or "user"
    role = (st.session_state.current_role or "user").title()

    st.sidebar.markdown(
        f"""
        <div class='glass-card sidebar-shell-card' style='margin: 10px 0 12px 0;'>
            <div class='meta-label'>Signed In As</div>
            <div class='meta-value'>{username}</div>
            <div class='meta-sub'>Role: {role}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected = st.session_state.selected_pothole
    if selected:
        c1, c2 = st.sidebar.columns(2)
        with c1:
            st.markdown(
                f"""
                <div class='bento-card sidebar-shell-card'>
                    <div class='small-label'>Latitude</div>
                    <div class='small-value'>{selected['lat']:.3f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f"""
                <div class='bento-card sidebar-shell-card'>
                    <div class='small-label'>Longitude</div>
                    <div class='small-value'>{selected['lng']:.3f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.sidebar.markdown(
            f"""
            <div class='bento-card sidebar-shell-card' style='margin-top:10px; margin-bottom:12px;'>
                <div class='small-label'>User Reports</div>
                <div style='font-size:2.1rem; font-weight:800; color:{theme['c_primary_btn']};'>{selected['count']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.sidebar.info("Resolve actions are available in the command surface above the map.")
    else:
        st.sidebar.markdown(
            """
            <div class='glass-card sidebar-shell-card' style='margin-bottom:10px;'>
                <p style='margin:0;' class='meta-sub'>Select a cluster in scatter mode to inspect and resolve.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    _render_recent_resolutions()

    if st.sidebar.button("Hide Panel", type="secondary", use_container_width=True, key="hide_sidebar_panel_btn"):
        st.session_state.show_dashboard_sidebar = False
        st.rerun()
