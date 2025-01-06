import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import numpy as np
import streamlit as st
from analytics_service import viz_kpi 
from analytics_service import viz_sroi 
from analytics_service import viz_roi
from analytics_service import viz_cba
from conv import convert_pdf_to_txt

# analytics_service = AnalyticsService('AIzaSyBfRpWgkylVc9WmMyy_chmQyehXLEFMbA4')
# Color palette
COLORS = {
    'primary': '#00725c',    # Dark teal
    'secondary': '#99aa67',  # Sage green
    'accent': '#ea9423',     # Orange
    'background': '#dfeae4',  # Light mint
    'white': '#ffffff'       # White
}

value = 0.87  # Value should be between 0 and 1

# Function to create a custom progress bar
def render_progress_bar(value):
    value_percent = value * 100
    bar_html = f"""
    <div style="position: relative; width: 100%; height: 30px; background-color: #e0e0e0; border-radius: 5px;">
        <div style="width: {value_percent}%; height: 100%; background-color: #4caf50; border-radius: 5px;"></div>
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: black; font-weight: bold;">
            {value_percent:.2f}%
        </div>
    </div>
    """
    st.markdown(bar_html, unsafe_allow_html=True)


# Set page config
st.set_page_config(
    page_title="Proposal Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for styling with new colors
st.markdown(f"""
    <style>
    .main {{
        background-color: {COLORS['white']};
    }}
    .stButton>button {{
        background-color: {COLORS['primary']};
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
        width: 100%;
    }}
    .stButton>button:hover {{
        background-color: {COLORS['secondary']};
    }}
    .css-1d391kg {{
        background-color: {COLORS['white']};
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    .proposal-card {{
        background-color: {COLORS['white']};
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid {COLORS['primary']};
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin: 10px 0;
        cursor: pointer;
    }}
    .proposal-card:hover {{
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-left: 4px solid {COLORS['secondary']};
    }}
    .stSidebar {{
        background-color: {COLORS['background']};
    }}
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Logo implementation
    try:
        # Replace 'logo.png' with your actual logo file path
        logo = Image.open('logo.png')
        # Resize logo if needed
        logo = logo.resize((200, 165))  # Adjust size as needed
        st.image(logo, use_column_width=True)
    except FileNotFoundError:
        st.error("Please place your logo.png file in the same directory as this script")
    
    # Navigation
    st.markdown(f"""
        <div style='background-color: {COLORS["primary"]}; padding: 10px; border-radius: 10px;'>
    """, unsafe_allow_html=True)
    selected = st.radio(
    label="",
    options=["Dashboard", "Analytics", "Settings"],
    index=0,
    key="nav",
    label_visibility="collapsed"
)

# Style the radio buttons with custom CSS
st.markdown(f"""
    <style>
    div[data-testid="stRadio"] label span {{
        color: {COLORS["primary"]} !important;
        font-weight: 500;
    }}
    </style>
""", unsafe_allow_html=True)
    


# Main content
def main():
    # Header with new color scheme
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown(f"""
            <h1 style='color: {COLORS["primary"]}'>Proposal Analysis Dashboard</h1>
        """, unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.markdown("### Analysis Controls")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate Rankings"):
            # Streamlit app
            

            # Add your logic for generating rankings
            
            st.success("Rankings generated successfully!")
            st.info("Processing uploaded file(s)...")
            for uploaded_file in uploaded_files:
                try:
                    # Convert the uploaded file to text and save it to session state
                    text_content = convert_pdf_to_txt(uploaded_file)
                    
            #         st.title("Progress Bar Example")
            # st.write("sustainable development score")

            # render_progress_bar(value)
            #         # st.success(f"Successfully converted: {uploaded_file.name}")
                    # st.markdown(f"### Analysis for {uploaded_file.name}")
                    
                    # # Store text content in session state
                    # st.session_state[f"text_{uploaded_file.name}"] = text_content
                    
                    # st.write("Click a button below to view specific analysis:")
                    # st.session_state[f"selected_file"] = uploaded_file.name
                except Exception as e:
                    st.error(f"An error occurred while processing {uploaded_file.name}: {e}")

        if st.button("Generate Statistics"):
            st.info("Processing uploaded file(s)...")
            for uploaded_file in uploaded_files:
                    try:
                        # Convert the uploaded file to text and save it to session state
                        text_content = convert_pdf_to_txt(uploaded_file)
                        st.success(f"Successfully converted: {uploaded_file.name}")
                        st.markdown(f"### Analysis for {uploaded_file.name}")
                        
                        # Store text content in session state
                        st.session_state[f"text_{uploaded_file.name}"] = text_content
                        
                        st.write("Click a button below to view specific analysis:")
                        st.session_state[f"selected_file"] = uploaded_file.name

                    except Exception as e:
                        st.error(f"An error occurred while processing {uploaded_file.name}: {e}")

            # Check if a file was selected and stored in session state
        if "selected_file" in st.session_state:
                file_name = st.session_state["selected_file"]
                text_content = st.session_state[f"text_{file_name}"]

                # Show individual analysis options
                if st.button("Show KPI stats"):
                    res = viz_kpi(text_content)
                    st.write(res)

                if st.button("Show CBA"):
                    res = viz_cba(text_content)
                    st.write(res)

                if st.button("Show SROI"):
                    res = viz_sroi(text_content)
                    st.write(res)

                if st.button("Show ROI"):
                    res = viz_roi(text_content)
                    st.write(res)

                    
        ##################################################################
        # INTEGRATE ESG CODE 🐕
        
        st.markdown("### Proposal Rankings")
        sample_rankings = [
            {"name": "Proposal A", "score": 95},
            {"name": "Proposal B", "score": 87},
        ]

        for rank, proposal in enumerate(sample_rankings, 1):
            with st.container():
                st.markdown(f"""
                    <div class='proposal-card'>
                        <h3 style='color: {COLORS["primary"]};'>#{rank} - {proposal['name']}</h3>
                        <p style='color: {COLORS["secondary"]};'>Score: {proposal['score']}</p>
                    </div>
                """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()