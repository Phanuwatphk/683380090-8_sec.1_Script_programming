"""Shared Streamlit visual styling for the dashboard."""

from __future__ import annotations

import streamlit as st


def apply_dashboard_styles() -> None:
    """Apply the dashboard's visual system once per Streamlit run."""
    st.markdown(
        """
        <style>
        .stApp { --primary-color: #2563eb; --text-color: #132542; background: #f6f8fc; color: #132542; }
        [data-testid="stHeader"] { background: transparent; }
        [data-testid="stMain"] { color: #132542; }
        [data-testid="stMain"] [data-testid="stMetricLabel"] *,
        [data-testid="stMain"] [data-testid="stMetricValue"],
        [data-testid="stMain"] [data-testid="stMetricDelta"],
        [data-testid="stMain"] label,
        [data-testid="stMain"] [data-testid="stSelectbox"] *,
        [data-testid="stMain"] [data-testid="stTextInput"] * { color: #132542 !important; }
        [data-testid="stMain"] input, [data-testid="stMain"] [data-baseweb="select"] > div {
            background: #ffffff !important; color: #132542 !important; border-color: #c9d8ec !important;
        }
        [data-testid="stMain"] input::placeholder { color: #71819a !important; opacity: 1; }
        [data-testid="stMain"] .stButton > button,
        [data-testid="stMain"] [data-testid="stFormSubmitButton"] > button {
            min-height: 2.5rem; border-radius: .65rem; font-weight: 600;
            background: #ffffff; border: 1px solid #d6e1f0; color: #244a83 !important;
            transition: background .15s, border-color .15s;
        }
        [data-testid="stMain"] .stButton > button:hover {
            background: #edf4ff; border-color: #8bb3ef; color: #1d4ed8 !important;
        }
        [data-testid="stMain"] .stButton > button *,
        [data-testid="stMain"] [data-testid="stFormSubmitButton"] > button * { color: inherit !important; }
        [data-testid="stMain"] button[kind="primary"],
        [data-testid="stMain"] button[kind="primaryFormSubmit"] {
            background: #2563eb; border-color: #2563eb; color: #ffffff !important;
        }
        [data-testid="stMain"] .stButton > button:disabled {
            background: #e3eaf4; border-color: #e3eaf4; color: #71819a !important; opacity: 1;
        }
        [data-testid="stMain"] .stButton > button:disabled * { color: #71819a !important; }
        [data-testid="stSidebar"] { background: linear-gradient(180deg, #102947 0%, #071526 100%); }
        [data-testid="stSidebarContent"] {
            overflow: clip; overscroll-behavior: none;
            display: flex; flex-direction: column; justify-content: center;
        }
        [data-testid="stSidebarHeader"] { position: absolute; top: 0; left: 0; right: 0; }
        [data-testid="stSidebarUserContent"] { padding: 1.25rem 1rem; }
        [data-testid="stSidebar"] hr { margin: .75rem 0; }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p { color: #eef5ff !important; }
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] * { color: #a8bed7 !important; }
        [data-testid="stSidebar"] .stButton > button {
            justify-content: center; min-height: 2.75rem; padding: 0 .85rem; border: 1px solid transparent;
            border-radius: .55rem; background: transparent !important; color: #eef5ff !important;
            font-size: .94rem; transition: background .15s ease, border-color .15s ease;
        }
        [data-testid="stSidebar"] .stButton > button:hover,
        [data-testid="stSidebar"] .stButton > button:focus-visible {
            background: rgba(255, 255, 255, .16) !important; border-color: rgba(255, 255, 255, .18) !important;
            color: #ffffff !important;
        }
        [data-testid="stSidebar"] .stButton > button[kind="primary"] { background: #2563eb !important; color: #ffffff !important; }
        [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover { background: #1d4ed8 !important; }
        [data-testid="stSidebar"] .stButton > button[kind="secondary"] { color: #eef5ff !important; }
        [data-testid="stSidebar"] .stButton > button * { color: inherit !important; }
        [data-testid="stMain"] .block-container { max-width: 1400px; margin-inline: auto; padding: 3rem clamp(1.25rem, 4vw, 4rem) 3rem; }
        [data-testid="stMain"] h2, [data-testid="stMain"] h3 { color: #142644; letter-spacing: -.02em; }
        [data-testid="stMain"] h3 { font-size: 1.35rem; padding-top: .75rem; }
        .page-heading { padding-bottom: .75rem; }
        .page-kicker { color: #2563eb; font-size: .75rem; font-weight: 750; letter-spacing: .1em; text-transform: uppercase; }
        [data-testid="stMain"] h1.page-title { margin: .45rem 0 .6rem; padding: 0; color: #102542; font-size: 2.1rem; font-weight: 750; line-height: 1.2; letter-spacing: -.035em; }
        [data-testid="stMain"] p.page-subtitle { color: #63738c; margin: 0; font-size: .94rem; line-height: 1.65; }
        .sidebar-brand { color: #f6f9ff; font-size: 1.28rem; font-weight: 750; letter-spacing: -.02em; text-align: center; }
        .sidebar-label { color: #9db3cd; font-size: .82rem; margin-top: .25rem; text-align: center; }
        .hero-stat { background: linear-gradient(115deg, #102947, #245c9d); border-radius: 1rem; padding: 1.75rem 2rem; color: #f8fbff; margin: .25rem 0 .5rem; box-shadow: 0 8px 24px rgba(16, 41, 71, .1); }
        .hero-stat-label { color: #bcd4f4; font-size: .82rem; font-weight: 700; letter-spacing: .07em; text-transform: uppercase; }
        .hero-stat-value { color: #ffffff; font-size: 2.35rem; font-weight: 760; letter-spacing: -.04em; line-height: 1.2; margin-top: .35rem; }
        .hero-stat-note { color: #d4e4f8; font-size: .88rem; margin-top: .35rem; }
        .game-tile { background: #ffffff; border: 1px solid #dce7f5; border-radius: .9rem; overflow: hidden; box-shadow: 0 4px 14px rgba(28, 62, 106, .04); }
        [data-testid="stMain"] .game-cover { display: block; width: 100%; height: 10rem; object-fit: cover; border-radius: 0; background: #e8eef7; }
        [data-testid="stMain"] .game-cover--empty { display: grid; place-items: center; box-sizing: border-box; color: #60718a; font-size: .84rem; text-align: center; padding: 1rem; }
        .game-card { box-sizing: border-box; height: 10.75rem; padding: 1rem; }
        .game-name { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; color: #142644; font-weight: 700; font-size: .98rem; line-height: 1.4; height: 2.8em; overflow: hidden; }
        .game-meta { color: #60718a; font-size: .8rem; margin-top: .4rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .game-tags { display: flex; gap: .35rem; overflow: hidden; margin-top: .65rem; white-space: nowrap; }
        .tag { display: block; flex: 0 1 auto; min-width: 0; overflow: hidden; text-overflow: ellipsis; background: #edf4ff; color: #3264aa; border-radius: 999px; font-size: .72rem; padding: .18rem .48rem; }
        [data-testid="stMain"] a.genre-link { color: #3264aa; text-decoration: none; cursor: pointer; transition: background .15s, color .15s; }
        [data-testid="stMain"] a.genre-link:hover { background: #dbe9ff; color: #1d4ed8; text-decoration: none; }
        [data-testid="stMain"] a.genre-link:focus-visible { outline: 2px solid #2563eb; outline-offset: 2px; }
        .tag--muted { background: #f0f3f8; color: #71819a; }
        .empty-state { background: #ffffff; border: 1px dashed #b7c9e2; border-radius: 14px; padding: 3.5rem 1rem; text-align: center; color: #5c6f8a; }
        [data-testid="stMain"] .detail-cover { display: block; width: 100%; height: clamp(180px, 24vw, 300px); object-fit: cover; border-radius: 1rem; }
        .detail-stats { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1rem; }
        .detail-panel { background: #ffffff; border: 1px solid #dce7f5; border-radius: .9rem; padding: 1.25rem; min-width: 0; }
        .detail-label { color: #71819a; font-size: .8rem; margin-bottom: .65rem; }
        .detail-value { color: #142644; font-size: 1.2rem; line-height: 1.4; font-weight: 700; overflow-wrap: anywhere; }
        .detail-taxonomy { display: grid; grid-template-columns: 2fr 1fr; gap: 1rem; margin-top: 1rem; }
        .detail-developers { grid-column: 1 / -1; }
        .detail-section { background: #ffffff; border: 1px solid #dce7f5; border-radius: .9rem; padding: 1.25rem; min-width: 0; }
        [data-testid="stMain"] .detail-section h3 { margin: 0 0 1rem; padding: 0; font-size: 1rem; }
        .detail-tags { display: flex; flex-wrap: wrap; gap: .5rem; }
        .platform-tag { background: #f0f3f8; border: 1px solid #e2e8f0; border-radius: .45rem; padding: .35rem .65rem; color: #3d506d; font-size: .8rem; }
        .detail-tags .tag { padding: .35rem .65rem; font-size: .8rem; white-space: normal; }
        .detail-empty { color: #71819a; font-size: .85rem; }
        [data-testid="stMetric"] { background: #ffffff; border: 1px solid #dce7f5; border-radius: .9rem; padding: 1.25rem; }
        .st-key-statistics-metrics [data-testid="stHorizontalBlock"] { flex-wrap: wrap; }
        .st-key-statistics-metrics [data-testid="stColumn"] {
            flex: 1 1 150px !important; min-width: min(150px, 100%);
        }
        [data-testid="stForm"], [data-testid="stExpander"] {
            background: #ffffff; border: 1px solid #dce7f5; border-radius: .9rem;
        }
        .st-key-library-filters { background: #ffffff; border-radius: .9rem; }
        [data-testid="stMetricLabel"] p { white-space: normal; }
        @media (max-height: 560px) {
            [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] { gap: .5rem; }
            [data-testid="stSidebar"] .stButton > button { min-height: 2rem; }
            [data-testid="stSidebar"] hr { margin: .25rem 0; }
        }
        @media (max-width: 640px) {
            [data-testid="stMain"] .block-container { padding: 3.5rem 1rem 2rem; }
            [data-testid="stMain"] h1.page-title { font-size: 1.75rem; overflow-wrap: anywhere; }
            .hero-stat { padding: 1.25rem; }
            .hero-stat-value { font-size: 2rem; }
            .detail-stats { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .75rem; }
            .detail-taxonomy { grid-template-columns: 1fr; }
            .detail-panel, .detail-section { padding: 1rem; }
            .detail-value { font-size: 1.05rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
