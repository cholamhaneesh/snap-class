import streamlit as st

def style_background_home():
    
    st.markdown('''
                    <style>
                        .stApp{
                            background: #5865F2 !important;
                        }
                        
                        .stApp div[data-testid="stColumn"]{
                            background-color: #E0E3FF !important;
                            padding:2.5rem !important;
                            border-radius: 5rem !important;
                        }
                    </style>
                    
                ''', unsafe_allow_html=True
                )

def style_base_layout():
    
    st.markdown('''
                    
                    
                    <style>
                        
                        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Outfit:wght@100..900&display=swap');
                        #MainMenu, footer, header{
                            visibility: hidden;
                        }
                        .block-container{
                            padding-top: 2vh ;
                        }
                        
                        [data-testid="stHeading"] *{
                            font-family: 'Climate Crisis', sans-serif !important;
                            font-size: 2rem !important;
                            line-height: 1.1 !important;
                            margin-bottom:0rem !important;
                            color: #1E293B !important;
                        }
                        
                        h3, h4, p, span{
                            font-family: 'Outfit', sans-serif;
                        }
                        
                        button{
                            border-radius: 1.5rem !important;
                            background: #5865F2 !important;
                            color: white !important;
                            padding: 10px 20px !important;
                            border: none !important;
                            transition: transform  0.25s ease-in-out !important;
                        }

                        button[kind="secondary"]{
                            border-radius: 1.5rem !important;
                            background: #EB459E !important;
                            color: white !important;
                            padding: 10px 20px !important;
                            border: none !important;
                            transition: transform  0.25s ease-in-out !important;
                        }
                        
                        button[kind="tertiary"]{
                            border-radius: 1.5rem !important;
                            background: black !important;
                            color: white !important;
                            padding: 10px 20px !important;
                            border: none !important;
                            transition: transform  0.25s ease-in-out !important;
                        }
                        
                        button:hover{
                            transform: scale(1.05) !important;
                        }
                        .logo-container{
                            display:flex; 
                            flex-direction:column; 
                            align-items: center; 
                            justify-content: center; 
                            margin-bottom:30px; 
                            margin-top:30px;
                        }
                        .logo,
                        .logo * {
                            font-family: 'Climate Crisis', sans-serif !important;
                            font-size: 3.5rem !important;
                            line-height: 0.9 !important;
                            margin-bottom:0rem !important;
                            color: #E0E3FF !important;
                            text-align: center !important;
                            margin: 0 !important;
                        }

                        .h2logo,
                        .h2logo * {
                            font-family: 'Climate Crisis', sans-serif !important;
                            font-size: 2rem !important;
                            line-height: 1.1 !important;
                            margin-bottom:0rem !important;
                        }
                        
                        /* Dataframe */
                        [data-testid="stDataFrame"],
                        [data-testid="stDataFrame"] > div,
                        [data-testid="stDataFrame"] > div > div,
                        [data-testid="stDataFrame"] [data-testid="stStyledDataFrameLite"] {
                            background-color: white !important;
                            border-radius: 12px !important;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
                            padding: 8px !important;
                        }

                        [data-testid="stDataFrame"] canvas {
                            background-color: white !important;
                        }

                        [data-testid="stDataFrame"] [role="grid"],
                        [data-testid="stDataFrame"] [role="table"] {
                            background-color: white !important;
                        }

                        [data-testid="stDataFrame"] [role="row"],
                        [data-testid="stDataFrame"] [role="row"]:hover {
                            background-color: white !important;
                        }

                        [data-testid="stDataFrame"] [role="columnheader"],
                        [data-testid="stDataFrame"] [role="gridcell"] {
                            background-color: white !important;
                            color: #1E293B !important;
                        }
                        
                        /* Text input labels */
                        [data-testid="stTextInput"] label,
                        [data-testid="stTextInput"] label p {
                            color: #1E293B !important;
                        }

                        /* Placeholder */
                        [data-testid="stTextInput"] input::placeholder {
                            color: #64748B !important;
                            opacity: 1 !important;
                        }
                        
                                                
                    </style>
                    
                    
                ''', unsafe_allow_html=True
                )
    
def style_background_dashboard():
    
    st.markdown('''
                    <style>
                        .stApp{
                            background: #E0E3FF !important;
                        }
                    </style>
                    
                ''', unsafe_allow_html=True
                )