import streamlit as st

def get_secret(path: str, default=None):
    node = st.secrets
    try:
        for key in path.split("."):
            node = node[key]
        return node
    except Exception:
        return default
