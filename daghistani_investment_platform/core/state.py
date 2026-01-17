import streamlit as st

def ensure_defaults():
    st.session_state.setdefault("inputs", {})
    st.session_state.setdefault("results", {})
    st.session_state.setdefault("portfolio_df", None)
