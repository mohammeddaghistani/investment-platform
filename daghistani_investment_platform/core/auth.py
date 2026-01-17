import streamlit as st
import streamlit_authenticator as stauth
from core.config import get_secret

def _credentials_from_secrets():
    usernames = get_secret("credentials.usernames", None)
    if not usernames:
        st.error(
            "Missing secrets: credentials.usernames.* (add users in Streamlit Secrets).\n"
            "See .streamlit/secrets.toml.example for the required structure."
        )
        st.stop()
    return {"usernames": dict(usernames)}

def _build_authenticator():
    credentials = _credentials_from_secrets()
    cookie_name = get_secret("auth.cookie_name", "invest_vault")
    cookie_key = get_secret("auth.cookie_key", "key_2026")
    cookie_expiry_days = int(get_secret("auth.cookie_expiry_days", 1))
    return stauth.Authenticate(credentials, cookie_name, cookie_key, cookie_expiry_days)

def login_gate():
    authenticator = _build_authenticator()
    try:
        authenticator.login(location="main")
    except Exception as e:
        st.error(f"Login error: {e}")
        st.stop()

    if st.session_state.get("authentication_status") is not True:
        st.warning("🔒 يرجى تسجيل الدخول للوصول إلى النظام المتكامل")
        st.stop()

    username = st.session_state.get("username", "")
    role = "viewer"
    try:
        role = authenticator.credentials["usernames"][username].get("role", "viewer")
    except Exception:
        role = "viewer"

    return {
        "name": st.session_state.get("name", "User"),
        "username": username,
        "role": role,
        "authenticator": authenticator,
    }

def sidebar_user_box(user: dict):
    st.success(f"مرحباً بك: {user.get('name', 'User')}")
    st.caption(f"الدور: **{user.get('role', 'viewer')}**")
    user["authenticator"].logout("تسجيل الخروج", "sidebar")
    st.divider()
