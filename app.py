import streamlit as st
import pandas as pd
import numpy as np
import qrcode
from io import BytesIO
from datetime import datetime
import plotly.express as px
import streamlit_authenticator as stauth

# ==========================================
# 1. نظام الحماية المحدث (Compatible with v0.3.0+)
# ==========================================

# تعريف بيانات المستخدمين
names = ['إدارة الاستثمار', 'المدير التنفيذي']
usernames = ['invest_admin', 'ceo_makkah']
# ملاحظة: في النسخة الاحترافية يتم توليد الهاش مسبقاً، هنا نستخدم النسخة المبسطة للتوافق
passwords = ['admin123', 'ceo2025']

# تشفير كلمات المرور بالطريقة الصحيحة الجديدة
hashed_passwords = stauth.Hasher(passwords).generate()

credentials = {
    "usernames": {
        usernames[0]: {"name": names[0], "password": hashed_passwords[0]},
        usernames[1]: {"name": names[1], "password": hashed_passwords[1]}
    }
}

# إنشاء كائن المصادقة
authenticator = stauth.Authenticate(
    credentials,
    "investment_dashboard", # اسم الكوكي
    "auth_key_2026",        # مفتاح التوقيع
    cookie_expiry_days=1
)

# واجهة تسجيل الدخول
# ملاحظة: تم تعديل المسميات لتناسب التحديث الجديد للمكتبة
name, authentication_status, username = authenticator.login(location='main')

if authentication_status == False:
    st.error('اسم المستخدم أو كلمة المرور غير صحيحة')
elif authentication_status == None:
    st.warning('يرجى إدخال بيانات الدخول المعتمدة')
elif authentication_status:
    # --- بداية محتوى النظام المحمي ---
    
    with st.sidebar:
        st.success(f'مرحباً بك: {name}')
        authenticator.logout('تسجيل الخروج', 'sidebar')

    # ==========================================
    # 2. قاعدة البيانات والضوابط (جميع الأنشطة)
    # ==========================================
    ACTIVITIES_DB = {
        "التجارية": {"method": "المتبقي", "max_term": 50, "suitability": ["مركز المدينة", "محور رئيسي"]},
        "الصحية": {"method": "الدخل", "max_term": 25, "suitability": ["حي سكني"]},
        "التعليمية": {"method": "الدخل", "max_term": 25, "suitability": ["حي سكني"]},
        "السياحية": {"method": "المتبقي", "max_term": 50, "suitability": ["واجهة بحرية"]},
        "الصناعية": {"method": "السوق", "max_term": 25, "suitability": ["منطقة صناعية"]}
    }

    # ==========================================
    # 3. الواجهة الرسومية والتحليل
    # ==========================================
    st.title("🏛️ منصة إستدامة الاستثمارية (آمنة)")
    
    tab1, tab2, tab3 = st.tabs(["📊 لوحة التحكم", "💰 تقييم العقود", "📄 الوثائق المعتمدة"])

    with tab1:
        st.subheader("تحليل فجوة القيمة")
        kpi_df = pd.DataFrame({
            'النشاط': list(ACTIVITIES_DB.keys()),
            'الإيراد الحالي': [100, 55, 40, 80, 70],
            'الإيراد العادل': [145, 68, 55, 115, 88]
        })
        fig = px.bar(kpi_df, x='النشاط', y=['الإيراد الحالي', 'الإيراد العادل'], 
                     barmode='group', color_discrete_sequence=['#1e3d59', '#d35400'])
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        col_in, col_res = st.columns(2)
        with col_in:
            sel_act = st.selectbox("نوع النشاط الاستثماري", list(ACTIVITIES_DB.keys()))
            gdv = st.number_input("القيمة التطويرية (GDV)", value=10000000)
            capex = st.number_input("تكلفة الإنشاء (CAPEX)", value=6000000)
            term = st.slider("المدة", 5, 50, 25)
            # حساب مبسط للأجرة
            rent = (gdv - capex) * 0.08
        with col_res:
            st.metric("الأجرة السنوية العادلة المقدرة", f"{rent:,.0f} ريال")
            # رسم بياني للنمو
            st.line_chart([rent * (1.05 ** (i // 5)) for i in range(term)])

    with tab3:
        st.subheader("إصدار رمز الموثوقية")
        qr_str = f"Auditor: {name} | Activity: {sel_act} | Rent: {rent:,.0f}"
        qr = qrcode.make(qr_str)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="رمز موثوقية التقييم")

    st.markdown("---")
    st.caption("نظام التخطيط الاستراتيجي المؤمن - كافة الحقوق محفوظة 2026")

# --- نهاية النظام المحمي ---
