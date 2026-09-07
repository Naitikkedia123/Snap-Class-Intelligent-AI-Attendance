import streamlit as st


# ================================================================
# SNAPCLASS UI
#
# IMPORTANT:
# - This file changes styling only.
# - No screen, pipeline, database, session-state, or dialog logic
#   is changed.
# - Selectors are intentionally scoped so a style for one part of
#   Streamlit does not accidentally recolor another part.
# ================================================================


def style_background_home():

    st.markdown("""
        <style>

        /* --------------------------------------------------------
           HOME: page background
           -------------------------------------------------------- */
        .stApp {
            background:
                radial-gradient(circle at 12% 8%, rgba(255,255,255,.16), transparent 26%),
                radial-gradient(circle at 88% 90%, rgba(235,69,158,.10), transparent 28%),
                #5865F2 !important;
        }

        /* --------------------------------------------------------
           HOME: portal cards ONLY

           The home page contains the two mascot images. Using :has()
           makes this selector specific to those two cards, instead
           of styling every Streamlit column in the whole application.
           -------------------------------------------------------- */
        [data-testid="stHorizontalBlock"]:has(img[src*="mascot-student.png"]) {
            gap: 1.5rem !important;
        }

        [data-testid="stHorizontalBlock"]:has(img[src*="mascot-student.png"])
        > [data-testid="stColumn"] {
            background: #E0E3FF !important;
            border-radius: 2rem !important;
            padding: 2.5rem !important;
            border: 1px solid rgba(255,255,255,.55) !important;
            box-shadow: 0 14px 32px rgba(20,25,75,.14) !important;
        }

        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():

    st.markdown("""
        <style>

        /* --------------------------------------------------------
           DASHBOARD: page background
           No column/card styling here on purpose.
           -------------------------------------------------------- */
        .stApp {
            background:
                radial-gradient(circle at 0% 0%, rgba(88,101,242,.10), transparent 27%),
                radial-gradient(circle at 100% 100%, rgba(235,69,158,.07), transparent 27%),
                #E0E3FF !important;
        }

        </style>
    """, unsafe_allow_html=True)


def style_base_layout():

    st.markdown("""
        <style>

        /* ========================================================
           01. GLOBAL PAGE SHELL
           ======================================================== */

        @import url('https://fonts.googleapis.com/css2?family=Bowlby+One&family=Outfit:wght@100..900&display=swap');

        #MainMenu,
        footer,
        header {
            visibility: hidden;
        }

        .block-container {
            width: 100% !important;
            max-width: 1180px !important;
            padding-top: 1.5rem !important;
            padding-bottom: 1.5rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }


        /* ========================================================
           02. TYPOGRAPHY
           ======================================================== */

        h1,
        h2 {
            font-family: 'Bowlby One', sans-serif !important;
            color: #111111 !important;
        }

        h1 {
            font-size: 3.5rem !important;
            line-height: 1.08 !important;
            margin-bottom: 0 !important;
        }

        h2 {
            font-size: 2rem !important;
            line-height: 1.05 !important;
            margin-bottom: 0 !important;
        }

        h3,
        h4,
        p,
        label {
            font-family: 'Outfit', sans-serif !important;
        }

        h3,
        h4,
        p {
            color: #111111;
        }


        /* ========================================================
           03. STREAMLIT BUTTONS

           Only actual Streamlit button elements are targeted.
           The previous broad rules caused unrelated text/elements
           to inherit button colors.
           ======================================================== */

        [data-testid="stButton"] > button {
            width: 100% !important;
            min-height: 45px !important;
            border-radius: 1.35rem !important;
            padding: 0.65rem 1rem !important;
            border: none !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 600 !important;
            transition:
                transform .18s ease,
                box-shadow .18s ease,
                filter .18s ease !important;
            box-shadow: 0 7px 18px rgba(20, 25, 75, .10) !important;
        }

        /* Button label only */
        [data-testid="stButton"] > button p {
            margin: 0 !important;
            font-family: 'Outfit', sans-serif !important;
            color: inherit !important;
        }

        /* Button icon only */
        [data-testid="stButton"] > button svg {
            color: inherit !important;
            fill: currentColor !important;
        }

        /* Primary = SnapClass blue */
        [data-testid="stButton"] > button[kind="primary"] {
            background: #5865F2 !important;
            color: #FFFFFF !important;
        }

        /* Secondary = SnapClass pink */
        [data-testid="stButton"] > button[kind="secondary"] {
            background: #EB459E !important;
            color: #FFFFFF !important;
        }

        /* Tertiary = dark */
        [data-testid="stButton"] > button[kind="tertiary"] {
            background: #111111 !important;
            color: #FFFFFF !important;
        }

        [data-testid="stButton"] > button:hover:not(:disabled) {
            transform: translateY(-2px) !important;
            box-shadow: 0 11px 24px rgba(20, 25, 75, .16) !important;
            filter: brightness(1.02);
        }

        [data-testid="stButton"] > button:active:not(:disabled) {
            transform: translateY(0) !important;
        }

        /* Disabled buttons: still readable */
        [data-testid="stButton"] > button:disabled {
            opacity: .48 !important;
        }


        /* ========================================================
           04. TEXT INPUTS

           Used by teacher login/register and subject dialogs.
           This selector touches the input itself only.
           ======================================================== */

        input[type="text"],
        input[type="password"] {
            color: #111111 !important;
            -webkit-text-fill-color: #111111 !important;
            background: #FFFFFF !important;
            border: 1px solid rgba(17,17,17,.16) !important;
            border-radius: 12px !important;
            font-family: 'Outfit', sans-serif !important;
        }

        input[type="text"]::placeholder,
        input[type="password"]::placeholder {
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
            opacity: 1 !important;
        }

        input[type="text"]:focus,
        input[type="password"]:focus {
            border-color: #5865F2 !important;
            box-shadow: 0 0 0 2px rgba(88,101,242,.14) !important;
        }


        /* ========================================================
           05. SELECTBOX

           Used by teacher attendance subject selection.
           ======================================================== */

        [data-testid="stSelectbox"] [data-baseweb="select"] > div {
            background: #FFFFFF !important;
            border-radius: 12px !important;
            border: 1px solid rgba(17,17,17,.14) !important;
        }

        [data-testid="stSelectbox"] [data-baseweb="select"] span {
            color: #111111 !important;
            font-family: 'Outfit', sans-serif !important;
        }


        /* ========================================================
           06. CAMERA / AUDIO / FILE UPLOAD
           ======================================================== */

        [data-testid="stCameraInput"] label {
            color: #111111 !important;
            font-family: 'Outfit', sans-serif !important;
        }

        [data-testid="stFileUploaderDropzone"] {
            background: rgba(255,255,255,.72) !important;
            border: 1.5px dashed rgba(88,101,242,.40) !important;
            border-radius: 16px !important;
        }


        /* ========================================================
           07. USER REGISTRATION CONTAINER

           student_screen.py uses st.container(border=True).
           Only bordered Streamlit containers receive this polish.
           ======================================================== */

        [data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 20px !important;
            border: 1px solid rgba(17,17,17,.10) !important;
            box-shadow: 0 10px 28px rgba(20,25,75,.06) !important;
        }


        /* ========================================================
           08. DIALOGS

           All dialog files use @st.dialog().
           Make the dialog surface LIGHT and its content DARK.
           This fixes the black-background + black-text problem.
           ======================================================== */

        [data-testid="stDialog"] [role="dialog"] {
            background: #FFFFFF !important;
            color: #111111 !important;
            border-radius: 22px !important;
            border: 1px solid rgba(17,17,17,.10) !important;
            box-shadow: 0 25px 70px rgba(0,0,0,.24) !important;
        }

        /* Dialog headings and text */
        [data-testid="stDialog"] [role="dialog"] h1,
        [data-testid="stDialog"] [role="dialog"] h2,
        [data-testid="stDialog"] [role="dialog"] h3,
        [data-testid="stDialog"] [role="dialog"] h4,
        [data-testid="stDialog"] [role="dialog"] p,
        [data-testid="stDialog"] [role="dialog"] label {
            color: #111111 !important;
            font-family: 'Outfit', sans-serif !important;
        }

        /* Dialog headings can use the display font */
        [data-testid="stDialog"] [role="dialog"] h1,
        [data-testid="stDialog"] [role="dialog"] h2 {
            font-family: 'Bowlby One', sans-serif !important;
        }

        /* Dialog inputs */
        [data-testid="stDialog"] [role="dialog"] input[type="text"],
        [data-testid="stDialog"] [role="dialog"] input[type="password"] {
            color: #111111 !important;
            -webkit-text-fill-color: #111111 !important;
            background: #FFFFFF !important;
        }

        /* Dialog button labels */
        [data-testid="stDialog"] [role="dialog"] [data-testid="stButton"] > button p {
            color: inherit !important;
        }

        /* Dialog close button: keep close icon visible */
        [data-testid="stDialog"] [role="dialog"] button[aria-label="Close"] {
            color: #111111 !important;
            background: transparent !important;
            box-shadow: none !important;
        }


        /* ========================================================
           09. TOAST / SIDE POP-UPS

           Streamlit toast notifications use their own surface.
           Keep them light with dark text so the message does not
           disappear against a dark background.
           ======================================================== */

        [data-testid="stToast"],
        [data-testid="stToastContainer"] > div,
        .stToast {
            background: #FFFFFF !important;
            color: #111111 !important;
            border: 1px solid rgba(17,17,17,.10) !important;
            border-radius: 14px !important;
            box-shadow: 0 12px 32px rgba(0,0,0,.18) !important;
        }

        [data-testid="stToast"] p,
        [data-testid="stToast"] span,
        [data-testid="stToast"] div,
        .stToast p,
        .stToast span,
        .stToast div {
            color: #111111 !important;
            font-family: 'Outfit', sans-serif !important;
        }

        [data-testid="stToast"] button,
        .stToast button {
            color: #111111 !important;
            background: transparent !important;
            box-shadow: none !important;
        }


        /* ========================================================
           10. ATTENDANCE RESULT TABLE
           ======================================================== */

        [data-testid="stDataFrame"] {
            border-radius: 14px !important;
            overflow: hidden !important;
        }


        /* ========================================================
           11. IMAGE PRESENTATION
           ======================================================== */

        [data-testid="stImage"] img {
            border-radius: 14px !important;
        }


        /* ========================================================
           12. HOME-SPECIFIC POLISH

           style_background_home() is only executed on the home page.
           Do not add generic column-background rules here.
           ======================================================== */

        .home-portal-card {
            background: #E0E3FF;
            border-radius: 28px;
            padding: 2rem;
            box-shadow: 0 16px 38px rgba(20,25,75,.14);
        }


        /* ========================================================
           13. RESPONSIVE - TABLET

           We DO NOT force columns to stack here. Existing layouts
           remain intact.
           ======================================================== */

        @media (max-width: 900px) {

            .block-container {
                max-width: 100% !important;
                padding-left: 1.25rem !important;
                padding-right: 1.25rem !important;
                padding-top: 1.2rem !important;
            }

            h1 {
                font-size: 2.8rem !important;
            }

            h2 {
                font-size: 1.85rem !important;
            }

            [data-testid="stButton"] > button {
                min-height: 44px !important;
            }
        }


        /* ========================================================
           14. RESPONSIVE - PHONE

           Streamlit columns are allowed to wrap only on narrow
           screens. Desktop arrangement is not modified.
           ======================================================== */

        @media (max-width: 640px) {

            .block-container {
                padding-left: .75rem !important;
                padding-right: .75rem !important;
                padding-top: .8rem !important;
                padding-bottom: 1rem !important;
            }

            h1 {
                font-size: 2.25rem !important;
            }

            h2 {
                font-size: 1.65rem !important;
            }

            /* Existing horizontal groups wrap on phones */
            [data-testid="stHorizontalBlock"] {
                flex-wrap: wrap !important;
                row-gap: .65rem !important;
            }

            /* Never make a column narrower than a usable phone width */
            [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
                min-width: min(100%, 260px) !important;
            }

            /* Home portal cards become comfortable full-width cards */
            .home-portal-card {
                padding: 1.25rem;
                border-radius: 22px;
            }

            [data-testid="stButton"] > button {
                min-height: 44px !important;
                border-radius: 14px !important;
            }

            input[type="text"],
            input[type="password"] {
                min-height: 44px !important;
            }

            [data-testid="stDialog"] [role="dialog"] {
                width: calc(100vw - 1rem) !important;
                max-width: calc(100vw - 1rem) !important;
            }
        }


        /* ========================================================
           15. FOCUS / ACCESSIBILITY
           ======================================================== */

        [data-testid="stButton"] > button:focus-visible,
        input[type="text"]:focus-visible,
        input[type="password"]:focus-visible {
            outline: 3px solid rgba(88,101,242,.28) !important;
            outline-offset: 2px !important;
        }

        </style>
    """, unsafe_allow_html=True)
