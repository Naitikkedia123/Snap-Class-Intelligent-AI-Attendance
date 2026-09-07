import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students


# =========================================================
# LOAD DLIB MODELS
# =========================================================

@st.cache_resource
def load_dlib_models():

    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec


# =========================================================
# GET FACE EMBEDDINGS
# =========================================================

def get_face_embeddings(image_np):

    detector, sp, facerec = load_dlib_models()

    faces = detector(image_np, 1)

    encodings = []

    for face in faces:

        shape = sp(image_np, face)

        face_descriptor = facerec.compute_face_descriptor(
            image_np,
            shape,
            1
        )

        encodings.append(
            np.array(
                face_descriptor,
                dtype=np.float64
            )
        )

    return encodings


# =========================================================
# FACE DISTANCE
# =========================================================

def face_distance(known_embedding, unknown_embedding):

    known_embedding = np.asarray(
        known_embedding,
        dtype=np.float64
    )

    unknown_embedding = np.asarray(
        unknown_embedding,
        dtype=np.float64
    )

    return np.linalg.norm(
        known_embedding - unknown_embedding
    )


# =========================================================
# LOGIN FACE RECOGNITION
# =========================================================

def recognize_student_login(image_np, threshold=0.45):

    """
    Used ONLY for student FaceID login.

    Does NOT use SVM.

    The captured face is compared directly against
    every student's stored face embedding.

    A student is accepted ONLY when the closest
    face distance is below the login threshold.
    """

    # -----------------------------------------------------
    # Detect face
    # -----------------------------------------------------

    encodings = get_face_embeddings(image_np)

    # Exactly one face must be present
    if len(encodings) != 1:
        return None, len(encodings), None

    captured_embedding = encodings[0]

    # -----------------------------------------------------
    # Get all registered students
    # -----------------------------------------------------

    students = get_all_students()

    if not students:
        return None, 1, None

    best_student = None
    best_distance = float("inf")

    # -----------------------------------------------------
    # Compare captured face with every student
    # -----------------------------------------------------

    for student in students:

        stored_embedding = student.get(
            "face_embedding"
        )

        # Skip students without a face embedding
        if not stored_embedding:
            continue

        stored_embedding = np.asarray(
            stored_embedding,
            dtype=np.float64
        )

        # Skip invalid embeddings
        if stored_embedding.shape != (128,):
            continue

        distance = face_distance(
            stored_embedding,
            captured_embedding
        )

        print(
            f"LOGIN | "
            f"{student['name']} | "
            f"distance = {distance:.4f}"
        )

        # Keep the closest student
        if distance < best_distance:

            best_distance = distance
            best_student = student

    # -----------------------------------------------------
    # No valid embedding found
    # -----------------------------------------------------

    if best_student is None:

        print(
            "LOGIN | No valid student embedding found"
        )

        return None, 1, None

    # -----------------------------------------------------
    # Print best match
    # -----------------------------------------------------

    print(
        f"LOGIN | Best match = "
        f"{best_student['name']} | "
        f"distance = {best_distance:.4f} | "
        f"threshold = {threshold}"
    )

    # -----------------------------------------------------
    # IMPORTANT:
    #
    # Being the closest student is NOT enough.
    #
    # The distance must pass the threshold.
    # -----------------------------------------------------

    if best_distance <= threshold:

        return (
            best_student,
            1,
            best_distance
        )

    # -----------------------------------------------------
    # Face is too different.
    # Treat it as a new/unrecognized student.
    # -----------------------------------------------------

    return (
        None,
        1,
        best_distance
    )


# =========================================================
# TRAIN CLASSIFIER
# =========================================================

@st.cache_resource
def get_trained_model():

    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:

        embedding = student.get(
            "face_embedding"
        )

        if embedding:

            embedding = np.asarray(
                embedding,
                dtype=np.float64
            )

            # Make sure embedding is actually
            # 128-dimensional
            if embedding.shape == (128,):

                X.append(embedding)

                y.append(
                    student.get("student_id")
                )

    if len(X) == 0:
        return None

    unique_students = list(
        set(y)
    )

    # =====================================================
    # ONLY ONE STUDENT
    # =====================================================

    if len(unique_students) < 2:

        return {
            "clf": None,
            "X": X,
            "y": y
        }

    # =====================================================
    # MULTIPLE STUDENTS
    # =====================================================

    clf = SVC(
        kernel="linear",
        probability=True,
        class_weight="balanced"
    )

    clf.fit(X, y)

    return {
        "clf": clf,
        "X": X,
        "y": y
    }


# =========================================================
# RETRAIN CLASSIFIER
# =========================================================

def train_classifier():

    st.cache_resource.clear()

    model_data = get_trained_model()

    return bool(model_data)


# =========================================================
# ATTENDANCE RECOGNITION
# =========================================================

def predict_attendance(class_image_np):

    encodings = get_face_embeddings(
        class_image_np
    )

    detected_student = {}

    model_data = get_trained_model()

    if not model_data:

        return (
            detected_student,
            [],
            len(encodings)
        )

    clf = model_data["clf"]

    X_train = model_data["X"]
    y_train = model_data["y"]

    all_students = sorted(
        list(set(y_train))
    )

    # =====================================================
    # ATTENDANCE THRESHOLD
    #
    # KEEP THIS SEPARATE FROM LOGIN THRESHOLD
    # =====================================================

    RECOGNITION_THRESHOLD = 0.50

    for encoding in encodings:

        predicted_id = None

        # =================================================
        # ONLY ONE STUDENT
        # =================================================

        if len(all_students) == 1:

            student_id = all_students[0]

            student_embeddings = [
                X_train[i]
                for i, sid in enumerate(y_train)
                if sid == student_id
            ]

            distances = [
                face_distance(
                    stored_embedding,
                    encoding
                )
                for stored_embedding in student_embeddings
            ]

            best_match_score = min(
                distances
            )

            if (
                best_match_score
                <= RECOGNITION_THRESHOLD
            ):

                predicted_id = student_id

        # =================================================
        # MULTIPLE STUDENTS
        # =================================================

        else:

            predicted_id = clf.predict(
                [encoding]
            )[0]

            predicted_id = int(
                predicted_id
            )

            student_embeddings = [
                X_train[i]
                for i, sid in enumerate(y_train)
                if sid == predicted_id
            ]

            distances = [
                face_distance(
                    stored_embedding,
                    encoding
                )
                for stored_embedding in student_embeddings
            ]

            best_match_score = min(
                distances
            )

            if (
                best_match_score
                > RECOGNITION_THRESHOLD
            ):

                predicted_id = None

        # =================================================
        # ACCEPT
        # =================================================

        if predicted_id is not None:

            detected_student[
                predicted_id
            ] = True

    return (
        detected_student,
        all_students,
        len(encodings)
    )