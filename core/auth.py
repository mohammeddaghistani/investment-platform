import streamlit as st
import streamlit_authenticator as stauth

def login_gate():
    credentials = {
        "usernames": {
            "invest_admin": {
                "name": "إدارة الاستثمار الاستراتيجي",
                "password": st.secrets["auth"]["invest_admin_hash"],
            }
        }
    }

    authenticator = stauth.Authenticate(
        credentials,
        st.secrets["auth"]["cookie_name"],
        st.secrets["auth"]["cookie_key"],
        st.secrets["auth"]["cookie_expiry_days"],
    )

    authenticator.login(location="main")

    if st.session_state.get("authentication_status") is not True:
        st.warning("🔒 يرجى تسجيل الدخول للوصول إلى النظام المتكامل")
        st.stop()

    return {"name": st.session_state.get("name", "User"), "auth": authenticator}
