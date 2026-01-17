import streamlit as st
import pandas as pd
import numpy as np
import qrcode
from io import BytesIO
import plotly.express as px
import streamlit_authenticator as stauth

# 1. نظام الحماية (المستقر)
credentials = {"usernames": {"invest_admin": {"name": "إدارة الاستثمار", "password": "$2b$12$EixZaYVK1Vz17Uy5vQPfbOfh17S2REAlX.y7n6tE9R.o5B1oH7EWG"}}}
authenticator = stauth.Authenticate(credentials, "invest_vault", "key_2026", 1)

try:
    auth_result = authenticator.login(location='main')
except Exception:
    pass

if st.session_state.get("authentication_status"):
    with st.sidebar:
        st.success(f"مرحباً: {st.session_state['name']}")
        authenticator.logout('تسجيل الخروج', 'sidebar')
        st.divider()
        # محرك الموقع
        zone = st.selectbox("النطاق الجغرافي (Location Zone)", ["المنطقة المركزية", "محور رئيسي (A)", "حي سكني (B)", "أطراف المدينة"])
        zone_mult = {"المنطقة المركزية": 1.5, "محور رئيسي (A)": 1.2, "حي سكني (B)": 1.0, "أطراف المدينة": 0.8}

    # 2. قاعدة البيانات الكاملة (17 نشاطاً)
    ACTIVITIES = {
        "التجارية": 50, "السياحية": 50, "الصحية": 25, "التعليمية": 25, 
        "الرياضية": 30, "الصناعية": 25, "الخدمات العامة": 25, "النقل": 20
    }

    st.title("🏛️ منصة إستدامة | النسخة الاستراتيجية الكاملة")
    t1, t2, t3 = st.tabs(["📊 تحليل الفجوة (1800 عقد)", "💰 محرك التقييم المعمق", "📄 مخرجات نظام ISR"])

    with t2:
        col1, col2 = st.columns(2)
        act = col1.selectbox("النشاط", list(ACTIVITIES.keys()))
        term = col1.slider("مدة العقد", 5, ACTIVITIES[act], 25)
        gdv = col1.number_input("القيمة التطويرية (GDV)", value=20000000)
        capex = col1.number_input("تكلفة البناء (CAPEX)", value=12000000)
        
        # المحرك المالي الاحترافي (المادة 26 + القيمة المتبقية)
        grace = int(term * 0.10) # فترة السماح
        land_residual = (gdv - (capex * 1.15)) * zone_mult[zone]
        base_rent = max(land_residual * 0.08, gdv * 0.03)
        
        # توليد جدول التدفقات (زيادة 5% كل 5 سنوات)
        schedule = [0]*grace + [base_rent * (1.05 ** (i // 5)) for i in range(term - grace)]
        
        col2.metric("الأجرة السنوية العادلة", f"{base_rent:,.0f} ريال")
        col2.metric("إجمالي العوائد المتوقعة", f"{sum(schedule):,.0f} ريال")
        col2.area_chart(schedule)
        

    with t1:
        st.subheader("تحليل محفظة الـ 1800 عقد")
        # بيانات محاكاة للفجوة المالية
        df = pd.DataFrame({'النشاط': list(ACTIVITIES.keys()), 'الحالي': np.random.randint(50, 100, 8), 'العادل': np.random.randint(110, 160, 8)})
        st.bar_chart(df.set_index('النشاط'))
        st.success(f"📌 الفجوة المالية التي يمكن استردادها: {sum(df['العادل'] - df['الحالي']):,.0f} مليون ريال")

    with t3:
        st.subheader("إصدار رمز الموثوقية")
        qr = qrcode.make(f"Act:{act}|Rent:{base_rent}|Auth:{st.session_state['name']}")
        buf = BytesIO(); qr.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="رمز موثوقية التقييم")

else:
    st.warning("يرجى تسجيل الدخول")
