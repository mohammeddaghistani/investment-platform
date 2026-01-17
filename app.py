# app.py
import streamlit as st
from core.auth import login_gate
from ui.theme import apply_theme
from ui.pages import page_suitability, page_valuation, page_portfolio, page_reports

def main():
    st.set_page_config(page_title="منصة إستدامة", layout="wide")
    apply_theme()

    user = login_gate()   # يرجع user dict أو يوقف التطبيق
    st.sidebar.success(f"مرحباً بك: {user['name']}")

    tabs = st.tabs(["🚀 الملاءمة والديموغرافيا", "💰 التقييم (المادة 26)", "📊 تحليل المحفظة", "📄 التقارير والتحقق"])
    with tabs[0]:
        page_suitability()
    with tabs[1]:
        page_valuation()
    with tabs[2]:
        page_portfolio()
    with tabs[3]:
        page_reports()

if __name__ == "__main__":
    main()
