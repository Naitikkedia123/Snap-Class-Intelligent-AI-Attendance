import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home


def home_screen():

    header_home()
    style_background_home()
    style_base_layout()

    # Slightly larger text and buttons for the Home page only
    st.markdown(
        """
        <style>
            [data-testid="stButton"] > button {
                font-size: 1.05rem !important;
                min-height: 52px !important;
                border-radius: 16px !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="large")

    # =====================================================
    # STUDENT
    # =====================================================

    with col1:

        with st.container(horizontal_alignment="center"):
            st.markdown(
                "<h2 style='color:black; text-align:center;'>I'm Student</h2>",
                unsafe_allow_html=True
            )

        with st.container(horizontal_alignment="center"):
            st.image(
                "https://i.ibb.co/844D9Lrt/mascot-student.png",
                width=120
            )

        with st.container(horizontal_alignment="center"):
            if st.button(
                'Student Portal',
                type='primary',
                icon=':material/arrow_outward:',
                icon_position='right',
                width=240,
                key='student_portal'
            ):
                st.session_state['login_type'] = 'student'
                st.rerun()

    # =====================================================
    # TEACHER
    # =====================================================

    with col2:

        with st.container(horizontal_alignment="center"):
            st.markdown(
                "<h2 style='color:black; text-align:center;'>I'm Teacher</h2>",
                unsafe_allow_html=True
            )

        with st.container(horizontal_alignment="center"):
            st.image(
                "https://i.ibb.co/CsmQQV6X/mascot-prof.png",
                width=145
            )

        with st.container(horizontal_alignment="center"):
            if st.button(
                'Teacher Portal',
                type='primary',
                icon=':material/arrow_outward:',
                icon_position='right',
                width=240,
                key='teacher_portal'
            ):
                st.session_state['login_type'] = 'teacher'
                st.rerun()

    footer_home()