import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_modules():
    detector=dlib.get_frontal_face_detector()
    
    sp=dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    
    
    facerec=dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    
    return detector, sp, facerec

def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_modules()

    # Remove alpha channel if present
    if image_np.shape[-1] == 4:
        image_np = image_np[:, :, :3]

    # Detect faces
    faces = detector(image_np, 2)

    encodings = []

    for face in faces:
        shape = sp(image_np, face)

        face_descriptor = facerec.compute_face_descriptor(
            image_np,
            shape,
            1
        )

        encodings.append(np.array(face_descriptor))

    return encodings

@st.cache_resource
def get_trained_model():
    X=[]
    y=[]
    
    student_db=get_all_students()
    
    if not student_db:
        return None
    
    for student in student_db:
        embedding=student.get("face_embedding")
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))
            
    if len(X)==0:
        return 0
    
    clf = SVC(kernel='linear', probability=True, class_weight='balanced')
    
    try:
        clf.fit(X, y)
    except ValueError:
        pass
    
    return {'clf':clf, 'X':X, 'y':y}

def train_classifier():
    st.cache_resource.clear()
    model_data=get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np):
    encodings=get_face_embeddings(class_image_np)
    
    detected_student={}
    
    model_data=get_trained_model()
    
    if not model_data:
        return detected_student, [], len(encodings)
    
    clf=model_data['clf']
    X_train=model_data['X']
    y_train=model_data['y']
    
    all_students=sorted(list(set(y_train)))
    
    for encoding in encodings:
        if len(all_students) >= 2:
            predicted_id=int(clf.predict([encoding])[0])
        else:
            predicted_id=int(all_students[0])
        
        
        student_embedding=X_train[y_train.index(predicted_id)]
        
        best_match_score=np.linalg.norm(student_embedding - encoding)
        
        resemblance_threshold=0.6
        
        if best_match_score <= resemblance_threshold:
            detected_student[predicted_id]=True
        
    return detected_student, all_students, len(encodings)

def identify_student(image_np, threshold=0.5, margin=0.08):

    encodings = get_face_embeddings(image_np)

    if len(encodings) == 0:
        return None, None, 0

    if len(encodings) > 1:
        return None, None, len(encodings)

    new_encoding = encodings[0]

    students = get_all_students()

    matches = []

    for student in students:

        stored_embedding = student.get("face_embedding")

        if stored_embedding:
            stored_embedding = np.array(stored_embedding)

            distance = np.linalg.norm(
                new_encoding - stored_embedding
            )

            matches.append((distance, student))

    if not matches:
        return None, None, 1

    # Sort from smallest distance to largest
    matches.sort(key=lambda x: x[0])

    best_distance, best_student = matches[0]

    # Check threshold
    if best_distance > threshold:
        return None, best_distance, 1

    # Check ambiguity with second closest student
    if len(matches) > 1:
        second_distance, _ = matches[1]

        if second_distance - best_distance < margin:
            return None, best_distance, 1

    return best_student, best_distance, 1




    