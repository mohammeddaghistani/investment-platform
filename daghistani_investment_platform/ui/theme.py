import streamlit as st

def apply_theme():
    st.markdown(
        """
        <style>
          .block-container { padding-top: 1.2rem; }
          h1, h2, h3, h4, h5, h6 { font-family: 'Segoe UI', Tahoma, Arial, sans-serif; }
          html, body, [class*="css"]  { direction: rtl; }
          .stTabs [data-baseweb="tab-list"] { gap: 8px; }
          .stMetric { border-radius: 14px; padding: 8px; }
        </style>
        """,
        unsafe_allow_html=True,
    )
