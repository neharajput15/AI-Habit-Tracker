import streamlit as st


def apply_theme():

    # =====================================================
    # THEME MODE
    # =====================================================

    dark_mode = st.session_state.get("dark_mode", False)

    # =====================================================
    # LIGHT MODE COLORS
    # =====================================================

    if not dark_mode:

        bg = "#F7F5FF"
        card = "#FFFFFF"
        soft_card = "#EEE9FF"

        text = "#27233A"
        secondary = "#756F86"

        border = "#E3DDF2"

        input_bg = "#FFFFFF"
        input_text = "#27233A"

        primary = "#7C4DFF"
        primary_hover = "#6A3DE8"

    # =====================================================
    # DARK MODE COLORS
    # =====================================================

    else:

        bg = "#0F0B1A"
        card = "#1B152B"
        soft_card = "#241C38"

        text = "#FFFFFF"
        secondary = "#BDB5D0"

        border = "#3B3150"

        input_bg = "#171125"
        input_text = "#FFFFFF"

        primary = "#9B7BFF"
        primary_hover = "#8765F5"


    # =====================================================
    # GLOBAL CSS
    # =====================================================

    st.markdown(
        f"""
        <style>

        /* =================================================
           MAIN APPLICATION
           ================================================= */

        .stApp {{
            background-color: {bg} !important;
        }}

        [data-testid="stAppViewContainer"] {{
            background-color: {bg} !important;
        }}

        [data-testid="stMain"] {{
            background-color: {bg} !important;
        }}


        /* =================================================
           HEADER
           ================================================= */

        [data-testid="stHeader"] {{
            background-color: {bg} !important;
        }}


        /* =================================================
           HEADINGS
           ================================================= */

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {{
            color: {text} !important;
        }}


        /* =================================================
           NORMAL TEXT
           ================================================= */

        .stMarkdown p {{
            color: {text} !important;
        }}

        .stMarkdown li {{
            color: {text} !important;
        }}

        .stCaption {{
            color: {secondary} !important;
        }}

        [data-testid="stCaptionContainer"] {{
            color: {secondary} !important;
        }}


        /* =================================================
           SIDEBAR
           ================================================= */

        [data-testid="stSidebar"] {{
            background-color: {card} !important;
            border-right: 1px solid {border} !important;
        }}

        [data-testid="stSidebar"] * {{
            color: {text} !important;
        }}


        /* =================================================
           BUTTONS
           ================================================= */

        div.stButton {{
            width: auto !important;
        }}

        div.stButton > button {{
            width: auto !important;
            min-width: 100px !important;
            max-width: 240px !important;

            background-color: {primary} !important;
            color: #FFFFFF !important;

            border: none !important;
            border-radius: 10px !important;

            padding: 0.45rem 1rem !important;

            font-weight: 600 !important;

            transition: all 0.2s ease !important;
        }}

        div.stButton > button p {{
            color: #FFFFFF !important;
        }}

        div.stButton > button:hover {{
            background-color: {primary_hover} !important;
            color: #FFFFFF !important;

            transform: translateY(-1px);
        }}


        /* =================================================
           FORM SUBMIT BUTTON
           ================================================= */

        [data-testid="stFormSubmitButton"] {{
            width: auto !important;
        }}

        [data-testid="stFormSubmitButton"] button {{
            width: auto !important;
            min-width: 100px !important;

            background-color: {primary} !important;
            color: #FFFFFF !important;

            border: none !important;
            border-radius: 10px !important;

            font-weight: 600 !important;
        }}

        [data-testid="stFormSubmitButton"] button p {{
            color: #FFFFFF !important;
        }}

        [data-testid="stFormSubmitButton"] button:hover {{
            background-color: {primary_hover} !important;
        }}


        /* =================================================
           INPUT BOXES
           ================================================= */

        div[data-baseweb="input"] {{
            background-color: {input_bg} !important;
            border-radius: 9px !important;
            border-color: {border} !important;
        }}

        div[data-baseweb="input"] input {{
            background-color: {input_bg} !important;
            color: {input_text} !important;

            -webkit-text-fill-color: {input_text} !important;
        }}

        div[data-baseweb="input"] input::placeholder {{
            color: {secondary} !important;

            -webkit-text-fill-color: {secondary} !important;
        }}


        /* =================================================
           SELECT BOX
           ================================================= */

        div[data-baseweb="select"] {{
            background-color: {input_bg} !important;
            border-radius: 9px !important;
            border-color: {border} !important;
        }}

        div[data-baseweb="select"] * {{
            color: {input_text} !important;
        }}

        [role="listbox"] {{
            background-color: {card} !important;
            border: 1px solid {border} !important;
        }}

        [role="option"] {{
            background-color: {card} !important;
            color: {text} !important;
        }}

        [role="option"]:hover {{
            background-color: {soft_card} !important;
        }}


        /* =================================================
           TEXT AREA
           ================================================= */

        textarea {{
            background-color: {input_bg} !important;
            color: {input_text} !important;

            -webkit-text-fill-color: {input_text} !important;

            border: 1px solid {border} !important;
            border-radius: 9px !important;
        }}

        textarea::placeholder {{
            color: {secondary} !important;

            -webkit-text-fill-color: {secondary} !important;
        }}


        /* =================================================
           EXPANDERS
           ================================================= */

        [data-testid="stExpander"] {{
            background-color: {card} !important;

            border: 1px solid {border} !important;

            border-radius: 11px !important;

            margin-bottom: 12px !important;
        }}

        [data-testid="stExpander"] summary {{
            background-color: {card} !important;

            color: {text} !important;
        }}

        [data-testid="stExpander"] summary:hover {{
            background-color: {soft_card} !important;
        }}

        [data-testid="stExpander"] summary span {{
            color: {text} !important;
        }}

        [data-testid="stExpander"] p {{
            color: {text} !important;
        }}


        /* =================================================
           METRIC CARDS
           ================================================= */

        [data-testid="stMetric"] {{
            background-color: {card} !important;

            border: 1px solid {border} !important;

            border-radius: 13px !important;

            padding: 15px !important;
        }}

        [data-testid="stMetricLabel"] {{
            color: {secondary} !important;
        }}

        [data-testid="stMetricValue"] {{
            color: {text} !important;
        }}


        /* =================================================
           PROGRESS BAR
           ================================================= */

        [data-testid="stProgressBar"] {{
            background-color: {soft_card} !important;

            border-radius: 10px !important;
        }}

        [data-testid="stProgressBar"] > div > div {{
            background-color: {primary} !important;

            border-radius: 10px !important;
        }}


        /* =================================================
           TABS
           ================================================= */

        button[data-baseweb="tab"] {{
            color: {secondary} !important;
        }}

        button[data-baseweb="tab"][aria-selected="true"] {{
            color: {primary} !important;
        }}


        /* =================================================
           CHECKBOX
           ================================================= */

        [data-testid="stCheckbox"] label {{
            color: {text} !important;
        }}


        /* =================================================
           RADIO BUTTONS
           ================================================= */

        [data-testid="stRadio"] label {{
            color: {text} !important;
        }}


        /* =================================================
           TOGGLE
           ================================================= */

        [data-testid="stToggle"] label {{
            color: {text} !important;
        }}


        /* =================================================
           DIVIDERS
           ================================================= */

        hr {{
            border-color: {border} !important;
        }}


        /* =================================================
           ALERTS
           ================================================= */

        [data-testid="stAlert"] {{
            border-radius: 10px !important;
        }}


        /* =================================================
           LINKS
           ================================================= */

        a {{
            color: {primary} !important;
        }}


        /* =================================================
           CUSTOM PURPLE CARD
           ================================================= */

        .purple-card {{
            background-color: {card};

            border: 1px solid {border};

            border-radius: 14px;

            padding: 18px;

            margin-bottom: 15px;
        }}


        /* =================================================
           CUSTOM SOFT CARD
           ================================================= */

        .soft-purple-card {{
            background-color: {soft_card};

            border-radius: 12px;

            padding: 16px;

            margin-bottom: 12px;
        }}


        /* =================================================
           MOBILE
           ================================================= */

        @media (max-width: 768px) {{

            div.stButton > button {{
                max-width: 100% !important;
            }}

            [data-testid="stExpander"] {{
                width: 100% !important;
            }}

        }}

        </style>
        """,
        unsafe_allow_html=True
    )