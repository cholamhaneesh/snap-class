import streamlit as st
import base64
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

def footer_home():
    image_path = ROOT_DIR / "utils" / "my_name_1.png"

    with open(image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()

    st.markdown(f"""
        <div style="margin-top:4rem; display:flex; gap:6px; justify-content:center; align-items:center">
            <p style="font-weight:bold; color:white; font-size:26px;">Created by</p>
            <img src="data:image/png;base64,{img_base64}" style="max-height:55px;" />
        </div>
    """, unsafe_allow_html=True)

def footer_dashboard():
    image_path = ROOT_DIR / "utils" / "my_name_2.png"

    with open(image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()

    st.markdown(f"""
        <div style="margin-top:4rem; display:flex; gap:6px; justify-content:center; align-items:center">
            <p style="font-weight:bold; color:black; font-size:26px;">Created by</p>
            <img src="data:image/png;base64,{img_base64}" style="max-height:55px;" />
        </div>
    """, unsafe_allow_html=True)
