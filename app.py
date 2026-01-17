import streamlit as st

from core.auth import login_gate, sidebar_user_box
from core.state import ensure_defaults
from ui.theme import apply_theme
from ui.pages import page_suitability, page_valuation, page_portfolio, page_reports


def main():
    st.set_page_config(page_title="منصة إستدامة | الاستثمار والتقييم العقاري", layout="wide")
    apply_theme()
    ensure_defaults()

    # Login gate (stops execution until authenticated)
    user = login_gate()

    with st.sidebar:
        sidebar_user_box(user)

    st.title("🏛️ منصة إستدامة | منظومة الاستثمار والتقييم العقاري")
    tabs = st.tabs(["🚀 الملاءمة والديموغرافيا", "💰 التقييم (المادة 26)", "📊 تحليل المحفظة", "📄 التقارير والتحقق"])

    with tabs[0]:
        page_suitability()

    with tabs[1]:
        page_valuation()

    with tabs[2]:
        page_portfolio()

    with tabs[3]:
        page_reports()

    st.markdown("---")
    st.caption("منصة إستدامة | النسخة الاستراتيجية الكاملة - مكة المكرمة 2026")


if __name__ == "__main__":
    main()
