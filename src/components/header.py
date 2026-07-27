import streamlit as st

def header_home():
    
    
    logo_url="https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
        <div class='logo-container'>
            <img src='{logo_url}' style='height:100px;' />
            <h1 
                class='logo'
            >
                SNAP<br/>CLASS
            </h1>
        </div>
                """,
        unsafe_allow_html=True
                )
    