import streamlit as st
from PIL import Image
import numpy as np
import time

from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout
)

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card

from src.pipelines.face_pipeline import (
    get_face_embeddings,
    train_classifier,
    recognize_student_login
)

from src.pipelines.voice_pipeline import get_voice_embedding

from src.database.db import (
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject
)


def student_dashboard():

    student_data = st.session_state.student_data
    student_id = student_data["student_id"]

    # =====================================================
    # HEADER
    # =====================================================

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    with c1:
        header_dashboard()

    with c2:

        st.subheader(
            f"Welcome, {student_data['name']}"
        )

        if st.button(
            "Logout",
            type="secondary",
            key="student_logout_btn",
            shortcut="control+backspace"
        ):

            st.session_state["is_logged_in"] = False

            if "student_data" in st.session_state:
                del st.session_state["student_data"]

            st.rerun()

    st.space()

    # =====================================================
    # SUBJECT HEADER
    # =====================================================

    c1, c2 = st.columns(2)

    with c1:
        st.header("Your Enrolled Subjects")

    with c2:

        if st.button(
            "Enroll in Subject",
            type="primary",
            width="stretch",
            key="enroll_subject_btn"
        ):
            enroll_dialog()

    st.divider()

    # =====================================================
    # LOAD SUBJECTS AND ATTENDANCE
    # =====================================================

    with st.spinner("Loading your enrolled subjects.."):

        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    # =====================================================
    # CALCULATE ATTENDANCE STATISTICS
    # =====================================================

    stats_map = {}

    for log in logs:

        sid = log["subject_id"]

        if sid not in stats_map:

            stats_map[sid] = {
                "total": 0,
                "attended": 0
            }

        stats_map[sid]["total"] += 1

        if log.get("is_present"):
            stats_map[sid]["attended"] += 1

    # =====================================================
    # SUBJECT CARDS
    # =====================================================

    cols = st.columns(2)

    for i, sub_node in enumerate(subjects):

        sub = sub_node["subjects"]
        sid = sub["subject_id"]

        stats = stats_map.get(
            sid,
            {
                "total": 0,
                "attended": 0
            }
        )

        def unenroll_button(
            subject_id=sid,
            subject_name=sub["name"]
        ):

            if st.button(
                "Unenroll from this course",
                type="tertiary",
                width="stretch",
                icon=":material/delete_forever:",
                key=f"unenroll_{subject_id}"
            ):

                unenroll_student_to_subject(
                    student_id,
                    subject_id
                )

                st.toast(
                    f"Unenrolled from {subject_name} successfully!"
                )

                st.rerun()

        with cols[i % 2]:

            subject_card(
                name=sub["name"],
                code=sub["subject_code"],
                section=sub["section"],
                stats=[
                    ("📅", "Total", stats["total"]),
                    ("✅", "Attended", stats["attended"]),
                ],
                footer_callback=unenroll_button
            )

    footer_dashboard()


def student_screen():

    # =====================================================
    # PAGE STYLING
    # =====================================================

    style_background_dashboard()
    style_base_layout()

    # =====================================================
    # ACCOUNT CREATION STATE
    # =====================================================

    if "creating_student_account" not in st.session_state:
        st.session_state["creating_student_account"] = False

    creating_account = st.session_state["creating_student_account"]

    # =====================================================
    # IF ALREADY LOGGED IN
    # =====================================================

    if "student_data" in st.session_state:

        student_dashboard()
        return

    # =====================================================
    # TOP HEADER
    # =====================================================

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    with c1:
        header_dashboard()

    with c2:

        if st.button(
            "Go back to Home",
            type="secondary",
            key="student_home_btn",
            shortcut="control+backspace",
            disabled=creating_account
        ):

            st.session_state["login_type"] = None
            st.rerun()

    # =====================================================
    # PAGE TITLE
    # =====================================================

    st.markdown(
        """
        <h2 style="
            text-align:center;
            color:black;
            font-family:Climate Crisis;
        ">
            Login using FaceID
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.space()
    st.space()

    show_registration = False

    # =====================================================
    # CAMERA LABEL CSS
    # =====================================================

    st.markdown(
        """
        <style>
            [data-testid="stCameraInput"] label {
                color: black !important;
                font-family: 'Outfit', sans-serif !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # CAMERA
    # =====================================================

    photo_source = st.camera_input(
        "Position your face in the center",
        disabled=creating_account
    )

    # =====================================================
    # FACE LOGIN
    # =====================================================

    if photo_source and not creating_account:

        img = np.array(
            Image.open(photo_source)
        )

        with st.spinner("AI is scanning.."):

            student, num_faces, distance = recognize_student_login(
                img,
                threshold=0.45
            )

        # -------------------------------------------------
        # NO FACE
        # -------------------------------------------------

        if num_faces == 0:

            st.warning(
                "Face not found! Please position your face clearly."
            )

        # -------------------------------------------------
        # MULTIPLE FACES
        # -------------------------------------------------

        elif num_faces > 1:

            st.warning(
                "Multiple faces found. "
                "Please make sure only your face is visible."
            )

        # -------------------------------------------------
        # ONE FACE
        # -------------------------------------------------

        else:

            # =============================================
            # FACE RECOGNIZED
            # =============================================

            if student:

                st.session_state["is_logged_in"] = True
                st.session_state["user_role"] = "student"
                st.session_state["student_data"] = student

                st.toast(
                    f"Welcome Back {student['name']}"
                )

                time.sleep(1)

                st.rerun()

            # =============================================
            # FACE NOT RECOGNIZED
            # =============================================

            else:

                st.info(
                    "Face not recognized! "
                    "You might be a new student."
                )

                show_registration = True

    # =====================================================
    # REGISTRATION
    # =====================================================

    if show_registration:

        with st.container(border=True):

            st.header("Register new Profile")

            new_name = st.text_input(
                "Enter your name",
                placeholder="E.g. Naitik Kedia",
                key="new_student_name"
            )

            st.subheader("Optional : Voice Enrollment")

            st.info(
                "Enroll your voice for voice-only attendance."
            )

            audio_data = None

            try:

                audio_data = st.audio_input(
                    'Record a short phrase like '
                    '"I am present, My name is Akash."'
                )

            except Exception as e:

                print(
                    "AUDIO INPUT ERROR:",
                    repr(e)
                )

                st.warning(
                    "Voice recording is unavailable. "
                    "You can continue with face registration."
                )

            # =================================================
            # CREATE ACCOUNT
            # =================================================

            create_account_clicked = st.button(
                "Create Account",
                type="primary",
                key="create_student_account_btn",
                disabled=False
            )

            if create_account_clicked:

                # ---------------------------------------------
                # VALIDATE NAME
                # ---------------------------------------------

                if not new_name.strip():

                    st.warning(
                        "Please enter your name!"
                    )

                    st.stop()

                # ---------------------------------------------
                # VALIDATE CAMERA
                # ---------------------------------------------

                if photo_source is None:

                    st.warning(
                        "Please capture your face first."
                    )

                    st.stop()

                # ---------------------------------------------
                # CREATION STARTS
                # ---------------------------------------------

                with st.spinner("Creating your profile..."):

                    try:

                        # =====================================
                        # READ IMAGE
                        # =====================================

                        img = np.array(
                            Image.open(photo_source)
                        )

                        # =====================================
                        # GET FACE EMBEDDINGS
                        # =====================================

                        encodings = get_face_embeddings(img)

                        # -------------------------------------
                        # NO FACE
                        # -------------------------------------

                        if len(encodings) == 0:

                            st.error(
                                "Could not detect your face. "
                                "Please capture another photo."
                            )

                            st.stop()

                        # -------------------------------------
                        # MULTIPLE FACES
                        # -------------------------------------

                        if len(encodings) > 1:

                            st.error(
                                "Multiple faces detected. "
                                "Please make sure only your face "
                                "is visible during registration."
                            )

                            st.stop()

                        # =====================================
                        # EXACTLY ONE FACE
                        # =====================================

                        face_emb = encodings[0].tolist()

                        # =====================================
                        # VOICE EMBEDDING
                        # =====================================

                        voice_emb = None

                        if audio_data is not None:

                            try:

                                voice_bytes = audio_data.read()

                                if voice_bytes:

                                    voice_emb = get_voice_embedding(
                                        voice_bytes
                                    )

                                    print(
                                        "VOICE EMBEDDING CREATED"
                                    )

                            except Exception as voice_error:

                                print(
                                    "VOICE EMBEDDING ERROR:",
                                    repr(voice_error)
                                )

                                st.warning(
                                    "Voice enrollment failed, "
                                    "but your face profile will "
                                    "still be created."
                                )

                                voice_emb = None

                        # =====================================
                        # CREATE DATABASE RECORD
                        # =====================================

                        try:

                            response_data = create_student(
                                new_name.strip(),
                                face_embedding=face_emb,
                                voice_embedding=voice_emb
                            )

                        except Exception as db_error:

                            print(
                                "DATABASE ERROR:",
                                repr(db_error)
                            )

                            st.error(
                                f"Could not create profile: "
                                f"{db_error}"
                            )

                            st.stop()

                        # =====================================
                        # DATABASE FAILURE
                        # =====================================

                        if not response_data:

                            st.error(
                                "Could not create the "
                                "student profile."
                            )

                            st.stop()

                        # =====================================
                        # TRAIN CLASSIFIER
                        # =====================================

                        try:

                            train_classifier()

                        except Exception as classifier_error:

                            print(
                                "CLASSIFIER ERROR:",
                                repr(classifier_error)
                            )

                            st.warning(
                                "Profile was created, but the "
                                "face classifier could not be rebuilt."
                            )

                        # =====================================
                        # LOGIN STUDENT
                        # =====================================

                        st.session_state[
                            "is_logged_in"
                        ] = True

                        st.session_state[
                            "user_role"
                        ] = "student"

                        st.session_state[
                            "student_data"
                        ] = response_data[0]

                        st.toast(
                            f"Profile Created! "
                            f"Hi {new_name.strip()}!"
                        )

                        time.sleep(1)

                        # Only rerun AFTER successful creation
                        st.rerun()

                    except Exception as e:

                        print(
                            "ACCOUNT CREATION ERROR:",
                            repr(e)
                        )

                        st.error(
                            f"Account creation failed: {e}"
                        )

                        st.stop()
    # =====================================================
    # FOOTER
    # =====================================================

    footer_dashboard()