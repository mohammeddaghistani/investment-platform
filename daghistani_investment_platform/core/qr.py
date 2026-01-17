import qrcode
from io import BytesIO
import streamlit as st

@st.cache_data
def make_qr_png(payload: str) -> bytes:
    qr = qrcode.make(payload)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    return buf.getvalue()
