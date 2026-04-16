"""
TeamCapacity Hub
================
A full-featured internal project & capacity management dashboard.

HOW TO RUN:
-----------
1. Install dependencies:
   pip install streamlit pandas plotly

2. Run:
   streamlit run team_capacity_hub_full.py

3. Open: http://localhost:8501
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, datetime, timedelta
import re

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TeamCapacity Hub",
    page_icon="🗂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp { background: #f4f6fb; }

/* ── Nav tabs ── */
.nav-container {
    display: flex; gap: 4px; background: #fff;
    border-radius: 12px; padding: 6px;
    box-shadow: 0 1px 4px rgba(0,0,0,.08);
    margin-bottom: 28px;
}
.nav-btn {
    flex: 1; padding: 10px 0; border: none; border-radius: 8px;
    font-family: 'DM Sans', sans-serif; font-size: 0.82rem;
    font-weight: 600; cursor: pointer; transition: all .2s;
    background: transparent; color: #6b7280; letter-spacing: .3px;
}
.nav-btn.active {
    background: #1e293b; color: #fff;
    box-shadow: 0 2px 8px rgba(30,41,59,.25);
}
.nav-btn:hover:not(.active) { background: #f1f5f9; color: #1e293b; }

/* ── Page header ── */
.page-header {
    font-family: 'DM Sans', sans-serif; font-size: 1.55rem;
    font-weight: 700; color: #0f172a; margin-bottom: 4px;
}
.page-sub {
    font-size: 0.82rem; color: #94a3b8; margin-bottom: 24px;
    font-family: 'DM Mono', monospace;
}

/* ── Section card ── */
.section-card {
    background: #fff; border-radius: 12px; padding: 24px 28px;
    margin-bottom: 20px; border: 1px solid #e8edf5;
    box-shadow: 0 1px 3px rgba(0,0,0,.04);
}
.section-label {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 1.5px;
    text-transform: uppercase; color: #64748b;
    margin-bottom: 16px; padding-bottom: 8px;
    border-bottom: 1px solid #f1f5f9;
}

/* ── KPI cards ── */
.kpi-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 24px; }
.kpi-card {
    background: #fff; border-radius: 12px; padding: 20px 22px;
    border: 1px solid #e8edf5; box-shadow: 0 1px 3px rgba(0,0,0,.04);
    position: relative; overflow: hidden;
}
.kpi-card::after {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 3px;
}
.kpi-card.blue::after   { background: #3b82f6; }
.kpi-card.green::after  { background: #22c55e; }
.kpi-card.amber::after  { background: #f59e0b; }
.kpi-card.slate::after  { background: #64748b; }
.kpi-label { font-size: 0.7rem; font-weight: 600; letter-spacing: 1px;
             text-transform: uppercase; color: #94a3b8; margin-bottom: 8px; }
.kpi-value { font-size: 2rem; font-weight: 700; color: #0f172a;
             font-family: 'DM Mono', monospace; line-height: 1; }
.kpi-sub   { font-size: 0.72rem; color: #94a3b8; margin-top: 6px; }

/* ── Status badges ── */
.badge {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 0.7rem; font-weight: 600; letter-spacing: .3px;
}
.badge-green   { background: #dcfce7; color: #166534; }
.badge-red     { background: #fee2e2; color: #991b1b; }
.badge-amber   { background: #fef3c7; color: #92400e; }
.badge-blue    { background: #dbeafe; color: #1e40af; }
.badge-slate   { background: #f1f5f9; color: #475569; }
.badge-purple  { background: #ede9fe; color: #5b21b6; }

/* ── Util bar ── */
.util-bar-bg {
    background: #f1f5f9; border-radius: 4px; height: 8px;
    overflow: hidden; margin-top: 6px;
}
.util-bar-fill { height: 100%; border-radius: 4px; transition: width .4s; }

/* ── Filter row ── */
.filter-row {
    background: #fff; border-radius: 10px; padding: 16px 20px;
    margin-bottom: 20px; border: 1px solid #e8edf5;
    display: flex; gap: 12px; flex-wrap: wrap; align-items: flex-end;
}

/* ── Table ── */
.styled-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
.styled-table th {
    background: #f8fafc; color: #64748b; font-weight: 600;
    font-size: 0.68rem; letter-spacing: .8px; text-transform: uppercase;
    padding: 10px 14px; border-bottom: 1px solid #e2e8f0; text-align: left;
}
.styled-table td {
    padding: 10px 14px; border-bottom: 1px solid #f1f5f9;
    color: #334155; vertical-align: middle;
}
.styled-table tr:hover td { background: #f8fafc; }

/* ── Buttons ── */
.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important; border-radius: 8px !important;
    font-size: 0.82rem !important;
}

/* ── Form inputs ── */
.stTextInput input, .stNumberInput input, .stSelectbox > div > div,
.stDateInput input {
    border-radius: 8px !important;
    border-color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Divider ── */
hr { border: none; border-top: 1px solid #e8edf5; margin: 20px 0; }

/* ── Confirmation box ── */
.confirm-box {
    background: #f0fdf4; border: 1px solid #bbf7d0;
    border-radius: 10px; padding: 14px 18px; color: #166534;
    font-size: 0.82rem; font-weight: 500; margin-top: 12px;
}
.warn-box {
    background: #fff7ed; border: 1px solid #fed7aa;
    border-radius: 10px; padding: 14px 18px; color: #9a3412;
    font-size: 0.82rem; font-weight: 500; margin-top: 12px;
}
</style>
""", unsafe_allow_html=True)


# ── Sample data ───────────────────────────────────────────────────────────────
SAMPLE_PROJECTS = [
    {
        "project_id": "PRJ-001", "project_name": "Website Redesign",
        "project_status": "In Progress", "approval_status": "Approved",
        "bu": "Marketing", "volume": 1500,
        "primary_owner": "Sarah Kim", "project_lead": "Alice Chen",
        "stakeholder": "John Reeves", "execution_team_member": "Alice Chen",
        "planned_start": date(2026, 2, 1), "planned_end": date(2026, 4, 30),
        "actual_start": date(2026, 2, 3), "actual_end": None,
        "effort_required": 120, "actual_effort": 85,
        "space_growth": "High", "revenue_growth": "Medium",
        "reference_link": "https://sharepoint.com/sites/website-redesign",
        "csat_link": "", "csat_sent": "Not Sent", "csat_completed": "Pending",
    },
    {
        "project_id": "PRJ-002", "project_name": "API Integration – CRM",
        "project_status": "Completed", "approval_status": "Approved",
        "bu": "Engineering", "volume": 800,
        "primary_owner": "Tom Walsh", "project_lead": "Bob Martins",
        "stakeholder": "Linda Park", "execution_team_member": "Bob Martins",
        "planned_start": date(2026, 1, 10), "planned_end": date(2026, 3, 10),
        "actual_start": date(2026, 1, 12), "actual_end": date(2026, 3, 8),
        "effort_required": 80, "actual_effort": 76,
        "space_growth": "Low", "revenue_growth": "High",
        "reference_link": "https://onenote.com/api-integration",
        "csat_link": "https://forms.office.com/csat-001",
        "csat_sent": "Not Sent", "csat_completed": "Pending",
    },
    {
        "project_id": "PRJ-003", "project_name": "Mobile App v2",
        "project_status": "In Progress", "approval_status": "Approved",
        "bu": "Product", "volume": 3200,
        "primary_owner": "Priya Nair", "project_lead": "Clara Osei",
        "stakeholder": "Mark Ellison", "execution_team_member": "Clara Osei",
        "planned_start": date(2026, 1, 20), "planned_end": date(2026, 3, 31),
        "actual_start": date(2026, 1, 22), "actual_end": None,
        "effort_required": 160, "actual_effort": 140,
        "space_growth": "High", "revenue_growth": "High",
        "reference_link": "https://sharepoint.com/sites/mobile-v2",
        "csat_link": "", "csat_sent": "Not Sent", "csat_completed": "Pending",
    },
    {
        "project_id": "PRJ-004", "project_name": "Data Pipeline Automation",
        "project_status": "On Hold", "approval_status": "Pending",
        "bu": "Data", "volume": 500,
        "primary_owner": "David Park", "project_lead": "David Park",
        "stakeholder": "Rachel Stone", "execution_team_member": "Alice Chen",
        "planned_start": date(2026, 3, 1), "planned_end": date(2026, 5, 1),
        "actual_start": None, "actual_end": None,
        "effort_required": 60, "actual_effort": 10,
        "space_growth": "Medium", "revenue_growth": "Low",
        "reference_link": "",
        "csat_link": "", "csat_sent": "Not Sent", "csat_completed": "Pending",
    },
    {
        "project_id": "PRJ-005", "project_name": "Internal Analytics Dashboard",
        "project_status": "Completed", "approval_status": "Approved",
        "bu": "Operations", "volume": 200,
        "primary_owner": "Sarah Kim", "project_lead": "Bob Martins",
        "stakeholder": "John Reeves", "execution_team_member": "Bob Martins",
        "planned_start": date(2026, 1, 5), "planned_end": date(2026, 2, 28),
        "actual_start": date(2026, 1, 5), "actual_end": date(2026, 2, 25),
        "effort_required": 45, "actual_effort": 42,
        "space_growth": "Low", "revenue_growth": "Medium",
        "reference_link": "https://sharepoint.com/analytics-dash",
        "csat_link": "https://forms.office.com/csat-005",
        "csat_sent": "Sent", "csat_completed": "Completed",
    },
]

DEFAULT_AVAILABLE_HRS = {
    "Alice Chen": 160,
    "Bob Martins": 160,
    "Clara Osei": 120,
    "David Park": 140,
}

# ── Session state init ────────────────────────────────────────────────────────
if "projects" not in st.session_state:
    st.session_state.projects = SAMPLE_PROJECTS.copy()
if "available_hrs" not in st.session_state:
    st.session_state.available_hrs = DEFAULT_AVAILABLE_HRS.copy()
if "page" not in st.session_state:
    st.session_state.page = "intake"
if "csat_messages" not in st.session_state:
    st.session_state.csat_messages = {}


# ── Helpers ───────────────────────────────────────────────────────────────────
def get_df():
    return pd.DataFrame(st.session_state.projects)

def status_badge(val):
    mapping = {
        "Completed": "badge-green", "In Progress": "badge-blue",
        "On Hold": "badge-amber", "Not Started": "badge-slate",
        "Cancelled": "badge-red",
        "Approved": "badge-green", "Pending": "badge-amber", "Rejected": "badge-red",
        "On Track": "badge-green", "Delayed": "badge-red", "Completed On Time": "badge-purple",
        "Sent": "badge-green", "Not Sent": "badge-slate",
    }
    cls = mapping.get(val, "badge-slate")
    return f'<span class="badge {cls}">{val}</span>'

def delay_status(row):
    today = date.today()
    ae = row.get("actual_end")
    pe = row.get("planned_end")
    ps = row.get("project_status")
    if ae:
        return "Delayed" if ae > pe else "Completed On Time"
    if pe and today > pe and ps != "Completed":
        return "Delayed"
    return "On Track"

def effort_variance(row):
    return (row.get("actual_effort") or 0) - (row.get("effort_required") or 0)

def effort_pct(row):
    req = row.get("effort_required") or 0
    act = row.get("actual_effort") or 0
    if req == 0:
        return 0
    return round(act / req * 100, 1)

def is_valid_url(s):
    return s.startswith("http://") or s.startswith("https://") if s else True


# ── Navigation ────────────────────────────────────────────────────────────────
pages = [
    ("intake",    "📋 Project Intake"),
    ("capacity",  "📊 Capacity Dashboard"),
    ("tracker",   "🗂 Project Tracker"),
    ("csat",      "✅ CSAT & Closure"),
]

nav_html = '<div class="nav-container">'
for key, label in pages:
    active = "active" if st.session_state.page == key else ""
    nav_html += f'<button class="nav-btn {active}" onclick="void(0)">{label}</button>'
nav_html += "</div>"

col_nav = st.columns(len(pages))
for i, (key, label) in enumerate(pages):
    with col_nav[i]:
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()

current = st.session_state.page


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — PROJECT INTAKE
# ══════════════════════════════════════════════════════════════════════════════
if current == "intake":
    st.markdown('<p class="page-header">Project Intake</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">// add a new project record</p>', unsafe_allow_html=True)

    with st.form("intake_form", clear_on_submit=True):

        # ── Section A ──
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">A · Project Overview</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            proj_id   = st.text_input("Project ID *", placeholder="PRJ-006")
            proj_name = st.text_input("Project Name *", placeholder="e.g. CRM Upgrade")
        with c2:
            proj_status  = st.selectbox("Project Status *",
                ["Not Started","In Progress","On Hold","Completed","Cancelled"])
            appr_status  = st.selectbox("Approval Status *",
                ["Pending","Approved","Rejected"])
        with c3:
            bu     = st.text_input("BU *", placeholder="e.g. Marketing")
            volume = st.number_input("Volume", min_value=0, value=0, step=100)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Section B ──
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">B · Ownership & Stakeholders</p>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: primary_owner = st.text_input("Primary Owner *")
        with c2: project_lead  = st.text_input("Project Lead *")
        with c3: stakeholder   = st.text_input("Stakeholder *")
        with c4: exec_member   = st.text_input("Execution Team Member *")
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Section C ──
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">C · Timeline</p>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: planned_start = st.date_input("Planned Start", value=None)
        with c2: planned_end   = st.date_input("Planned End",   value=None)
        with c3: actual_start  = st.date_input("Actual Start",  value=None)
        with c4: actual_end    = st.date_input("Actual End",    value=None)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Section D ──
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">D · Effort & Business Impact</p>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: effort_req    = st.number_input("Effort Required (hrs)", min_value=0.0, step=5.0)
        with c2: actual_effort = st.number_input("Actual Effort Logged (hrs)", min_value=0.0, step=5.0)
        with c3: space_growth  = st.selectbox("Space Growth Opportunity", ["Low","Medium","High"])
        with c4: rev_growth    = st.selectbox("Revenue Growth Opportunity", ["Low","Medium","High"])
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Section E ──
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">E · Links & References</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: ref_link  = st.text_input("Reference Link", placeholder="https://...")
        with c2: csat_link = st.text_input("CSAT Link",      placeholder="https://...")
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("💾 Save Project", use_container_width=True)

    if submitted:
        errors = []
        required = {"Project ID": proj_id, "Project Name": proj_name,
                    "BU": bu, "Stakeholder": stakeholder,
                    "Project Lead": project_lead, "Primary Owner": primary_owner,
                    "Execution Team Member": exec_member}
        for field, val in required.items():
            if not val.strip():
                errors.append(f"**{field}** is required.")

        existing_ids = [p["project_id"] for p in st.session_state.projects]
        if proj_id in existing_ids:
            errors.append(f"Project ID **{proj_id}** already exists.")

        if planned_start and planned_end and planned_end < planned_start:
            errors.append("Planned End Date cannot be before Planned Start Date.")
        if actual_start and actual_end and actual_end < actual_start:
            errors.append("Actual End Date cannot be before Actual Start Date.")
        if not is_valid_url(ref_link):
            errors.append("Reference Link must be a valid URL (https://...).")
        if not is_valid_url(csat_link):
            errors.append("CSAT Link must be a valid URL (https://...).")

        if errors:
            for e in errors:
                st.error(e)
        else:
            record = {
                "project_id": proj_id.strip(), "project_name": proj_name.strip(),
                "project_status": proj_status, "approval_status": appr_status,
                "bu": bu.strip(), "volume": volume,
                "primary_owner": primary_owner.strip(),
                "project_lead": project_lead.strip(),
                "stakeholder": stakeholder.strip(),
                "execution_team_member": exec_member.strip(),
                "planned_start": planned_start, "planned_end": planned_end,
                "actual_start": actual_start, "actual_end": actual_end,
                "effort_required": effort_req, "actual_effort": actual_effort,
                "space_growth": space_growth, "revenue_growth": rev_growth,
                "reference_link": ref_link.strip(), "csat_link": csat_link.strip(),
                "csat_sent": "Not Sent", "csat_completed": "Pending",
            }
            st.session_state.projects.append(record)
            st.success(f"✅ Project **{proj_id}** saved successfully!")

    # Recent projects preview
    st.markdown("---")
    st.markdown('<p class="section-label" style="color:#64748b;font-size:.7rem;'
                'letter-spacing:1.5px;text-transform:uppercase;font-weight:700;">'
                'Recent Projects</p>', unsafe_allow_html=True)
    df = get_df()
    if not df.empty:
        preview = df[["project_id","project_name","project_status","bu",
                       "project_lead","effort_required"]].tail(5)[::-1]
        st.dataframe(preview, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — CAPACITY DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif current == "capacity":
    st.markdown('<p class="page-header">Capacity Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">// team utilisation & effort analytics</p>', unsafe_allow_html=True)

    df = get_df()

    total_planned  = df["effort_required"].sum()
    total_actual   = df["actual_effort"].sum()
    active_count   = len(df[df["project_status"] == "In Progress"])
    complete_count = len(df[df["project_status"] == "Completed"])

    # KPI cards
    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card blue">
            <div class="kpi-label">Total Planned Effort</div>
            <div class="kpi-value">{total_planned:,.0f}</div>
            <div class="kpi-sub">hours required</div>
        </div>
        <div class="kpi-card green">
            <div class="kpi-label">Total Actual Effort</div>
            <div class="kpi-value">{total_actual:,.0f}</div>
            <div class="kpi-sub">hours logged</div>
        </div>
        <div class="kpi-card amber">
            <div class="kpi-label">Active Projects</div>
            <div class="kpi-value">{active_count}</div>
            <div class="kpi-sub">in progress</div>
        </div>
        <div class="kpi-card slate">
            <div class="kpi-label">Completed Projects</div>
            <div class="kpi-value">{complete_count}</div>
            <div class="kpi-sub">closed out</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Available hours editor + utilisation
    col_left, col_right = st.columns([3, 2])

    with col_right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">Available Hours per Member</p>', unsafe_allow_html=True)
        members_in_projects = df["execution_team_member"].dropna().unique().tolist()
        for m in members_in_projects:
            if m not in st.session_state.available_hrs:
                st.session_state.available_hrs[m] = 160
        for m in list(st.session_state.available_hrs.keys()):
            if m not in members_in_projects:
                del st.session_state.available_hrs[m]
        for m in members_in_projects:
            st.session_state.available_hrs[m] = st.number_input(
                m, min_value=0, max_value=500,
                value=st.session_state.available_hrs[m],
                step=8, key=f"avail_{m}"
            )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">Utilisation by Execution Team Member</p>',
                    unsafe_allow_html=True)

        member_grp = df.groupby("execution_team_member").agg(
            effort_required=("effort_required","sum"),
            actual_effort=("actual_effort","sum")
        ).reset_index()

        for _, row in member_grp.iterrows():
            m = row["execution_team_member"]
            avail = st.session_state.available_hrs.get(m, 160)
            util = (row["actual_effort"] / avail * 100) if avail > 0 else 0
            util_clamped = min(util, 100)
            bar_color = "#22c55e" if util <= 100 else "#ef4444"
            if util > 100:
                status_html = '<span class="badge badge-red">⚠ Overloaded</span>'
            elif util < 60:
                status_html = '<span class="badge badge-amber">◌ Underutilized</span>'
            else:
                status_html = '<span class="badge badge-green">✓ Balanced</span>'

            st.markdown(f"""
            <div style="margin-bottom:18px;">
                <div style="display:flex;justify-content:space-between;
                            align-items:center;margin-bottom:4px;">
                    <span style="font-weight:600;font-size:.85rem;color:#1e293b;">{m}</span>
                    {status_html}
                </div>
                <div style="display:flex;justify-content:space-between;
                            font-size:.72rem;color:#94a3b8;margin-bottom:4px;">
                    <span>{row['actual_effort']:.0f} hrs logged / {avail} available</span>
                    <span style="font-family:'DM Mono',monospace;font-weight:600;
                                 color:{'#ef4444' if util>100 else '#1e293b'};">{util:.1f}%</span>
                </div>
                <div class="util-bar-bg">
                    <div class="util-bar-fill"
                         style="width:{util_clamped}%;background:{bar_color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Charts row
    col1, col2, col3 = st.columns(3)

    with col1:
        # Available vs Allocated
        fig = go.Figure()
        members = list(member_grp["execution_team_member"])
        avail_vals = [st.session_state.available_hrs.get(m, 160) for m in members]
        alloc_vals = list(member_grp["actual_effort"])

        fig.add_trace(go.Bar(name="Available", x=members, y=avail_vals,
                             marker_color="#dbeafe", marker_line_width=0))
        fig.add_trace(go.Bar(name="Logged", x=members, y=alloc_vals,
                             marker_color="#3b82f6", marker_line_width=0))
        fig.update_layout(
            title="Available vs Logged Hours", barmode="group",
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="DM Sans", size=11, color="#64748b"),
            title_font=dict(size=13, color="#0f172a", family="DM Sans"),
            legend=dict(orientation="h", y=-0.25),
            margin=dict(l=10, r=10, t=40, b=10), height=280,
            xaxis=dict(tickfont=dict(size=9)),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Effort by member
        fig2 = px.bar(member_grp, x="execution_team_member",
                      y="effort_required", color="effort_required",
                      color_continuous_scale=["#dbeafe","#1d4ed8"],
                      labels={"effort_required":"Effort Required",
                               "execution_team_member":"Member"})
        fig2.update_layout(
            title="Effort Required by Member",
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="DM Sans", size=11, color="#64748b"),
            title_font=dict(size=13, color="#0f172a", family="DM Sans"),
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=40, b=10), height=280,
            xaxis=dict(tickfont=dict(size=9)),
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        # Project count by status
        status_counts = df["project_status"].value_counts().reset_index()
        status_counts.columns = ["status","count"]
        color_map = {
            "In Progress": "#3b82f6", "Completed": "#22c55e",
            "On Hold": "#f59e0b", "Not Started": "#94a3b8", "Cancelled": "#ef4444"
        }
        colors = [color_map.get(s, "#94a3b8") for s in status_counts["status"]]
        fig3 = go.Figure(go.Pie(
            labels=status_counts["status"], values=status_counts["count"],
            marker=dict(colors=colors, line=dict(color="#fff", width=2)),
            textinfo="label+value", hole=0.45,
        ))
        fig3.update_layout(
            title="Projects by Status",
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="DM Sans", size=11, color="#64748b"),
            title_font=dict(size=13, color="#0f172a", family="DM Sans"),
            showlegend=False,
            margin=dict(l=10, r=10, t=40, b=10), height=280,
        )
        st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — PROJECT TRACKER
# ══════════════════════════════════════════════════════════════════════════════
elif current == "tracker":
    st.markdown('<p class="page-header">Project Tracker</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">// filter, search and review all projects</p>',
                unsafe_allow_html=True)

    df = get_df()

    # Filters
    with st.expander("🔍 Filters", expanded=True):
        fc1, fc2, fc3, fc4, fc5 = st.columns(5)
        with fc1:
            f_bu = st.multiselect("BU", options=sorted(df["bu"].unique()), default=[])
        with fc2:
            f_status = st.multiselect("Project Status",
                options=sorted(df["project_status"].unique()), default=[])
        with fc3:
            f_appr = st.multiselect("Approval Status",
                options=sorted(df["approval_status"].unique()), default=[])
        with fc4:
            f_stake = st.multiselect("Stakeholder",
                options=sorted(df["stakeholder"].unique()), default=[])
        with fc5:
            f_exec = st.multiselect("Execution Member",
                options=sorted(df["execution_team_member"].unique()), default=[])

    filtered = df.copy()
    if f_bu:        filtered = filtered[filtered["bu"].isin(f_bu)]
    if f_status:    filtered = filtered[filtered["project_status"].isin(f_status)]
    if f_appr:      filtered = filtered[filtered["approval_status"].isin(f_appr)]
    if f_stake:     filtered = filtered[filtered["stakeholder"].isin(f_stake)]
    if f_exec:      filtered = filtered[filtered["execution_team_member"].isin(f_exec)]

    # Computed columns
    filtered["Effort Variance"]    = filtered.apply(effort_variance, axis=1)
    filtered["Effort Completion %"] = filtered.apply(effort_pct, axis=1)
    filtered["Delay Status"]        = filtered.apply(delay_status, axis=1)

    st.markdown(f"**{len(filtered)}** projects found")

    # Build HTML table
    columns = [
        ("project_id","Project ID"), ("project_name","Project Name"),
        ("project_status","Status"), ("approval_status","Approval"),
        ("bu","BU"), ("stakeholder","Stakeholder"),
        ("project_lead","Lead"), ("execution_team_member","Exec Member"),
        ("planned_start","Plan Start"), ("planned_end","Plan End"),
        ("actual_start","Act Start"), ("actual_end","Act End"),
        ("effort_required","Req Hrs"), ("actual_effort","Act Hrs"),
        ("Effort Variance","Variance"), ("Effort Completion %","Completion %"),
        ("Delay Status","Delay Status"),
        ("space_growth","Space Growth"), ("revenue_growth","Rev Growth"),
        ("reference_link","Reference"), ("csat_link","CSAT"),
    ]

    header_html = "".join(f"<th>{lbl}</th>" for _, lbl in columns)
    rows_html = ""
    for _, row in filtered.iterrows():
        cells = ""
        for col, _ in columns:
            val = row.get(col, "")
            if col in ("project_status","approval_status","Delay Status"):
                cells += f"<td>{status_badge(str(val)) if val else '—'}</td>"
            elif col in ("reference_link","csat_link"):
                if val:
                    cells += f'<td><a href="{val}" target="_blank" style="color:#3b82f6;font-size:.75rem;">🔗 Link</a></td>'
                else:
                    cells += "<td>—</td>"
            elif col == "Effort Variance":
                color = "#ef4444" if val > 0 else "#22c55e" if val < 0 else "#64748b"
                sign = "+" if val > 0 else ""
                cells += f'<td style="color:{color};font-weight:600;font-family:DM Mono,monospace;">{sign}{val:.0f}</td>'
            elif col == "Effort Completion %":
                cells += f'<td style="font-family:DM Mono,monospace;">{val:.1f}%</td>'
            elif val is None or val == "" or (isinstance(val, float) and pd.isna(val)):
                cells += "<td style='color:#cbd5e1;'>—</td>"
            else:
                cells += f"<td>{val}</td>"
        rows_html += f"<tr>{cells}</tr>"

    table_html = f"""
    <div style="overflow-x:auto;border-radius:12px;border:1px solid #e8edf5;
                box-shadow:0 1px 3px rgba(0,0,0,.04);">
        <table class="styled-table">
            <thead><tr>{header_html}</tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — CSAT & CLOSURE
# ══════════════════════════════════════════════════════════════════════════════
elif current == "csat":
    st.markdown('<p class="page-header">CSAT & Closure</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">// completed project follow-up & satisfaction tracking</p>',
                unsafe_allow_html=True)

    df = get_df()
    completed = df[df["project_status"] == "Completed"].copy()

    if completed.empty:
        st.info("No completed projects yet. Mark a project as Completed to see it here.")
    else:
        # Summary strip
        sent_count      = len(completed[completed["csat_sent"] == "Sent"])
        not_sent_count  = len(completed[completed["csat_sent"] != "Sent"])
        done_count      = len(completed[completed["csat_completed"] == "Completed"])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="kpi-card green" style="margin-bottom:20px;">
                <div class="kpi-label">Completed Projects</div>
                <div class="kpi-value">{len(completed)}</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="kpi-card blue" style="margin-bottom:20px;">
                <div class="kpi-label">CSAT Sent</div>
                <div class="kpi-value">{sent_count}</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="kpi-card amber" style="margin-bottom:20px;">
                <div class="kpi-label">CSAT Completed</div>
                <div class="kpi-value">{done_count}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

        for idx, row in completed.iterrows():
            pid   = row["project_id"]
            pname = row["project_name"]
            can_send = bool(row.get("csat_link"))

            with st.container():
                st.markdown(f"""
                <div class="section-card" style="margin-bottom:16px;">
                    <div style="display:flex;justify-content:space-between;
                                align-items:flex-start;margin-bottom:14px;">
                        <div>
                            <span style="font-family:'DM Mono',monospace;font-size:.72rem;
                                         color:#94a3b8;">{pid}</span>
                            <div style="font-size:1rem;font-weight:700;color:#0f172a;
                                        margin-top:2px;">{pname}</div>
                        </div>
                        <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;">
                            {status_badge(row['project_status'])}
                            {status_badge(row['csat_sent'])}
                            {status_badge(row['csat_completed'])}
                        </div>
                    </div>
                    <div style="display:grid;grid-template-columns:repeat(4,1fr);
                                gap:12px;font-size:.8rem;color:#64748b;">
                        <div><span style="font-weight:600;color:#1e293b;">Stakeholder</span><br>{row['stakeholder']}</div>
                        <div><span style="font-weight:600;color:#1e293b;">Project Lead</span><br>{row['project_lead']}</div>
                        <div><span style="font-weight:600;color:#1e293b;">CSAT Link</span><br>
                            {"<a href='" + row['csat_link'] + "' target='_blank' style='color:#3b82f6;'>🔗 Open Form</a>" if row['csat_link'] else "—"}
                        </div>
                        <div><span style="font-weight:600;color:#1e293b;">Effort</span><br>{row['actual_effort']:.0f} / {row['effort_required']:.0f} hrs</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                btn_col, msg_col = st.columns([1, 3])
                with btn_col:
                    btn_disabled = not can_send
                    btn_label = "📧 Send CSAT Email" if can_send else "⚠ No CSAT Link"
                    if st.button(btn_label, key=f"csat_btn_{pid}",
                                 disabled=btn_disabled, use_container_width=True):
                        # Simulate send
                        for i, p in enumerate(st.session_state.projects):
                            if p["project_id"] == pid:
                                st.session_state.projects[i]["csat_sent"] = "Sent"
                        st.session_state.csat_messages[pid] = "sent"
                        st.rerun()

                with msg_col:
                    if st.session_state.csat_messages.get(pid) == "sent":
                        st.markdown(f"""
                        <div class="confirm-box">
                            ✅ CSAT email trigger simulated for <strong>{pname}</strong>.
                            Status updated to <strong>Sent</strong>.
                        </div>
                        """, unsafe_allow_html=True)
                    elif not can_send:
                        st.markdown("""
                        <div class="warn-box">
                            ⚠ Add a CSAT Link in Project Intake to enable this action.
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;font-family:'DM Mono',monospace;font-size:.65rem;
            color:#cbd5e1;padding:24px 0 8px;">
    TeamCapacity Hub · internal prototype · data stored in session only
</div>
""", unsafe_allow_html=True)
