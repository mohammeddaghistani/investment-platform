import streamlit as st
import pandas as pd
import numpy as np
import qrcode
from io import BytesIO
from datetime import datetime
import plotly.express as px
import streamlit_authenticator as stauth

# ==========================================
# 1. نظام الحماية المحدث (حل مشكلة TypeError)
# ==========================================

# تعريف بيانات المستخدمين
config = {
    "credentials": {
        "usernames": {
            "invest_admin": {
                "name": "إدارة الاستثمار",
                "password": "admin123" # سيتم التعامل معها كهاش آلياً
            },
            "ceo_makkah": {
                "name": "المدير التنفيذي",
                "password": "ceo2025"
            }
        }
    },
    "cookie": {
        "expiry_days": 1,
        "key": "signature_key_2026",
        "name": "investment_cookie"
    },
    "preauthorized": {"emails": []}
}

# الطريقة الصحيحة والمحدثة لتشفير كلمات المرور في الإصدارات الجديدة
# نقوم بإنشاء كائن Hasher وتمرير كلمات المرور للحصول على الهاشات
passwords_to_hash = ['admin123', 'ceo2025']
hashed_passwords = stauth.Hasher(passwords_to_hash).generate()

# وضع الهاشات في إعدادات النظام
config['credentials']['usernames']['invest_admin']['password'] = hashed_passwords[0]
config['credentials']['usernames']['ceo_makkah']['password'] = hashed_passwords[1]

# إنشاء كائن المصادقة
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# واجهة تسجيل الدخول (استخدام القاموس مباشرة)
name, authentication_status, username = authenticator.login(location='main')

# التحقق من حالة الدخول
if authentication_status == False:
    st.error('خطأ: اسم المستخدم أو كلمة المرور غير صحيحة')
elif authentication_status == None:
    st.warning('🔒 يرجى إدخال بيانات الدخول المعتمدة للوصول لمنصة إستدامة')
elif authentication_status:
    
    # --- بداية محتوى النظام المحمي ---
    
    with st.sidebar:
        st.success(f'مرحباً بك: {name}')
        authenticator.logout('تسجيل الخروج', 'sidebar')

    # ==========================================
    # 2. قاعدة البيانات والضوابط الاستثمارية
    # ==========================================
    ACTIVITIES_DB = {
        "التجارية": {"method": "المتبقي", "max_term": 50, "suitability": ["مركز المدينة", "محور رئيسي"]},
        "الصحية": {"method": "الدخل", "max_term": 25, "suitability": ["حي سكني"]},
        "السياحية": {"method": "المتبقي", "max_term": 50, "suitability": ["واجهة بحرية"]},
        "التعليمية": {"method": "الدخل", "max_term": 25, "suitability": ["حي سكني"]},
        "الصناعية": {"method": "السوق", "max_term": 25, "suitability": ["منطقة صناعية"]}
    }

    # ==========================================
    # 3. واجهة العرض والتحليل (KPIs)
    # ==========================================
    st.title("🏛️ منصة إستدامة الاستثمارية (النسخة المؤمنة)")
    
    tab1, tab2, tab3 = st.tabs(["📊 لوحة التحكم", "💰 تقييم العقود", "📄 الوثائق المعتمدة"])

    with tab1:
        st.subheader("إجمالي الإيرادات والفجوة المالية")
        kpi_df = pd.DataFrame({
            'النشاط': list(ACTIVITIES_DB.keys()),
            'الإيراد الحالي (مليون)': [100, 55, 80, 40, 70],
            'الإيراد العادل (مليون)': [135, 65, 110, 52, 85]
        })
        fig = px.bar(kpi_df, x='النشاط', y=['الإيراد الحالي (مليون)', 'الإيراد العادل (مليون)'], 
                     barmode='group', color_discrete_sequence=['#1e3d59', '#d35400'])
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        col_in, col_res = st.columns(2)
        with col_in:
            sel_act = st.selectbox("نوع النشاط", list(ACTIVITIES_DB.keys()))
            gdv = st.number_input("القيمة التطويرية (GDV)", value=10000000)
            capex = st.number_input("تكلفة الإنشاء (CAPEX)", value=6000000)
            term = st.slider("المدة", 5, 50, 25)
            # معادلة مبسطة للأجرة العادلة
            rent = (gdv - capex) * 0.08
        with col_res:
            st.metric("الأجرة السنوية العادلة", f"{rent:,.0f} ريال")
            st.line_chart([rent * (1.05 ** (i // 5)) for i in range(term)])

    with tab3:
        st.subheader("إصدار رمز الموثوقية (Audit QR)")
        qr_str = f"Auditor: {name} | Activity: {sel_act} | Rent: {rent:,.0f}"
        qr = qrcode.make(qr_str)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="رمز التحقق من بيانات التقييم")

    st.markdown("---")
    st.caption("نظام التخطيط الاستراتيجي المؤمن - كافة الحقوق محفوظة 2026")

# --- نهاية النظام المحمي ---
