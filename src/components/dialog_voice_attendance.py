import streamlit as st
from src.database.config import supabase
from src.pipelines.voice_pipeline import process_bulk_audio
from datetime import datetime
import pandas as pd
from src.database.db import create_attendance
import time


@st.dialog("Voice Attendance")
def voice_attendance_dialog(selected_subject_id):
    st.write("Record audio of students saying I am present. Then AI will recognize the students")
    
    audio_data=None
    
    audio_data=st.audio_input("record classroom audio")
    
    if st.button("Analyze audio", width='stretch', type='primary'):
        with st.spinner("Processing audio data"):
            enrolled_res= supabase.table("subject_students").select("*, students(*)").eq("subject_id", selected_subject_id).execute()
            enrolled_students=enrolled_res.data
            
            if not enrolled_students:
                st.warning("No students enrolled in this course")
                return
            candidates_dict={
                s['students']['student_id'] : s['students']['voice_embedding']
                for s in enrolled_students if s['students'].get('voice_embedding')
            }
            
            if not candidates_dict:
                st.error('No enrolled students have voice profiles registered')
                return
            
            if audio_data is None:
                st.warning("Please record classroom audio first")
                return
            
            audio_bytes= audio_data.read()
            
            detected_scores=process_bulk_audio(audio_bytes, candidates_dict)
            
            results, attendance_to_log = [], []
            
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            
            
            for node in enrolled_students:
                student = node['students']

                voice_embedding = student.get('voice_embedding')

                if not voice_embedding:
                    results.append({
                        "Name": student['name'],
                        "ID": student['student_id'],
                        "Score": "-",
                        "Status": "No Voice Profile"
                    })
                    continue

                score = detected_scores.get(student['student_id'], 0.0)
                is_present = score > 0

                results.append({
                    "Name": student['name'],
                    "ID": student['student_id'],
                    "Score": f"{float(score):.3f}" if is_present else "-",
                    "Status": "Present" if is_present else "Absent"
                })

                attendance_to_log.append({
                    "student_id": student['student_id'],
                    "subject_id": selected_subject_id,
                    "timestamp": current_timestamp,
                    "is_present": bool(is_present)
                })
                
            st.session_state.voice_attendance_results=(pd.DataFrame(results), attendance_to_log)
            
    if st.session_state.get('voice_attendance_results'):
        st.divider()
        df_results, logs= st.session_state.voice_attendance_results
        st.write("Please review attendance before confirming.")
        st.dataframe(df_results, hide_index=True, width='stretch')
        
        col1, col2=st.columns(2)
        
        with col1:
            if st.button("Discard", width='stretch'):
                del st.session_state.voice_attendance_results
                st.rerun()
        
        with col2:
            if st.button("Confirm & Save", width='stretch', type='primary'):
                try:
                    create_attendance(logs)

                    # Delete the old voice attendance results
                    del st.session_state.voice_attendance_results

                    st.toast("Attendance taken")
                    time.sleep(1)
                    st.rerun()

                except Exception as e:
                    st.error("Sync failed!")