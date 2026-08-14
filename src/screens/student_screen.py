import streamlit as st

from ui.base_layout import style_background_dashboard
from ui.base_layout import style_base_layout

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

from PIL import Image
import numpy as np
import time
from src.pipelines.face_pipiline import predict_attendance
from src.database.db import get_all_students
from src.pipelines.face_pipiline import get_face_embeddings
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import create_student
from src.pipelines.face_pipiline import train_classifier

def student_dashboard():
    st.header("Dashboard Header")
def student_screen():
    
    
    style_background_dashboard()
    style_base_layout()
    
    if "student_data" in st.session_state:
        student_dashboard()
        return
    c1,c2=st.columns(2, vertical_alignment="center", gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type="secondary", key='loginbackbtn', shortcut='control+backspace'):
            st.session_state['login_type']=None
            st.rerun()
        
    st.header('Login using FaceID', text_alignment='center')
    
    st.space()
    st.space()
    
    show_registration=False
    photo_source=st.camera_input("Position your face in the center")
    
    if photo_source:
        img=np.array(Image.open(photo_source))
        
        with st.spinner("AI is scanning..."):
            detected, all_ids, num_faces = predict_attendance(img)
            
            if num_faces==0:
                st.warning("Face not found")
            elif num_faces>1:
                st.warning("Multiple faces detected")
            else:
                if detected:
                    student_id=list(detected.keys())[0]
                    all_students=get_all_students()
                    student=next((s for s in all_students if s['student_id']==student_id), None)
                    
                    if student:
                        st.session_state.is_logged_in=True
                        st.session_state.user_role='student'
                        st.session_state.student_data=student
                        st.toast(f"Welcome Back {student['name']}!")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('Face not recognized! You might be a new student!')
                    show_registration=True
    
    if show_registration:
        with st.container(border=True):
            st.header("Register New Profile")
            new_name=st.text_input("Enter your name", placeholder='E.g Haneesh Cholam')
            
            st.subheader("Optional : Voice Enrollment")
            st.info("Enroll for voice only attendance")
            
            audio_data=None
            
            try:
                audio_data=st.audio_input("Record a short phrase like I am present, My name Haneesh.")
            except Exception as e:
                st.error("Audio Data Failed!")
                
            if st.button("Create Account", type='primary'):
                if new_name:
                    with st.spinner("Creating your profile..."):
                        img=np.array(Image.open(photo_source))
                        encodings=get_face_embeddings(img)
                        if encodings:
                            face_emb=encodings[0].tolist()
                            
                            voice_emb=None
                            if audio_data:
                                voice_emb=get_voice_embedding(audio_data.read())
                            
                            response_data=create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)
                            
                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in=True
                                st.session_state.user_role='student'
                                st.session_state.student_data=response_data[0]
                                st.toast(f'Profile created {new_name}!')
                                time.sleep(1)
                                st.rerun()
                        
                        else:
                            st.error("Could not capture your facial features for registration")
                            
                else:
                    st.warning("Please enter your name!")
                                    
                
    footer_dashboard()
    
