import streamlit as st

from core.auth import login_gate, sidebar_user_box
from core.state import ensure_defaults
from ui.theme import apply_theme
from ui.pages import page_suitability, page_valuation, page_portfolio, page_reports

ROLE_TABS = {
    "admin": ["🚀 الملاءمة والديموغرافيا", "💰 التقييم (المادة 26)", "📊 تحليل المحفظة", "📄 التقارير والتحقق"],
    "analyst": ["🚀 الملاءمة والديموغرافيا", "💰 التقييم (المادة 26)", "📄 التقارير والتحقق"],
    "viewer": ["📄 التقارير والتحقق"],
}

def main():
    st.set_page_config(page_title="منصة إستدامة | الاستثمار والتقييم العقاري", layout="wide")
    apply_theme()
    ensure_defaults()

    user = login_gate()
    with st.sidebar:
        sidebar_user_box(user)

    st.title("🏛️ منصة إستدامة | منظومة الاستثمار والتقييم العقاري")

    role = user.get("role", "viewer")
    tab_names = ROLE_TABS.get(role, ROLE_TABS["viewer"])
    tabs = st.tabs(tab_names)

    for i, name in enumerate(tab_names):
        with tabs[i]:
            if name.startswith("🚀"):
                page_suitability()
            elif name.startswith("💰"):
                page_valuation()
            elif name.startswith("📊"):
                page_portfolio()
            elif name.startswith("📄"):
                page_reports()

    st.markdown("---")
    st.caption("منصة إستدامة | النسخة الاستراتيجية الكاملة - مكة المكرمة 2026")

if __name__ == "__main__":
    main()
