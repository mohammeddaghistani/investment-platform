import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import qrcode
from io import BytesIO
from datetime import datetime
import plotly.express as px
import streamlit_authenticator as stauth

# ==========================================
# 1. نظام الحماية المحدث (Security Update)
# ==========================================

# تعريف المستخدمين
config = {
    'credentials': {
        'usernames': {
            'invest_admin': {
                'name': 'إدارة الاستثمار',
                'password': 'admin123' # سيتم تشفيرها تلقائياً بواسطة المكتبة في الإصدارات الأحدث أو استبدلها بـ Hash
            },
            'ceo_makkah': {
                'name': 'المدير التنفيذي',
                'password': 'ceo2025'
            }
        }
    },
    'cookie': {
        'expiry_days': 1,
        'key': 'investment_signature_key',
        'name': 'investment_cookie'
    },
    'preauthorized': {
        'emails': ['admin@example.com']
    }
}

# تشفير كلمات المرور يدوياً لتجنب خطأ التحديث
Hasher = stauth.Hasher(['admin123', 'ceo2025'])
hashed_passwords = Hasher.generate()

# وضع الكلمات المشفرة في مكانها الصحيح
config['credentials']['usernames']['invest_admin']['password'] = hashed_passwords[0]
config['credentials']['usernames']['ceo_makkah']['password'] = hashed_passwords[1]

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# واجهة تسجيل الدخول
name, authentication_status, username = authenticator.login('تسجيل الدخول للنظام الاستراتيجي', 'main')

if authentication_status == False:
    st.error('اسم المستخدم أو كلمة المرور غير صحيحة')
elif authentication_status == None:
    st.warning('يرجى إدخال بيانات الدخول المعتمدة للوصول للملفات الاستثمارية')
elif authentication_status:
    # --- بداية محتوى النظام المحمي ---
    
    with st.sidebar:
        st.success(f'مرحباً بك: {name}')
        authenticator.logout('تسجيل الخروج', 'sidebar')

    # ==========================================
    # 2. محركات التقييم والأنشطة (المحدثة)
    # ==========================================
    ACTIVITIES_DB = {
        "التجارية": {"method": "المتبقي", "max_term": 50, "grace_max": 0.10, "suitability": ["مركز المدينة", "محور رئيسي"]},
        "الصحية": {"method": "الدخل", "max_term": 25, "grace_max": 0.10, "suitability": ["حي سكني"]},
        "السياحية": {"method": "المتبقي", "max_term": 50, "grace_max": 0.10, "suitability": ["واجهة بحرية"]},
        "التعليمية": {"method": "الدخل", "max_term": 25, "grace_max": 0.10, "suitability": ["حي سكني"]},
        "الصناعية": {"method": "السوق", "max_term": 25, "grace_max": 0.10, "suitability": ["منطقة صناعية"]}
    }

    def calculate_valuation(activity, gdv, capex, revenue, term, grace):
        method = ACTIVITIES_DB[activity]["method"]
        if method == "المتبقي":
            land_val = max(gdv - (capex * 1.12 + gdv * 0.18), 0)
            base_rent = land_val * 0.08
        else:
            base_rent = revenue * 0.25
        
        schedule = []
        curr = base_rent
        for y in range(1, term + 1):
            if y <= grace: schedule.append(0)
            else:
                if y > 1 and (y - 1) % 5 == 0: curr *= 1.05
                schedule.append(curr)
        return base_rent, schedule

    # ==========================================
    # 3. الواجهة الرسومية
    # ==========================================
    st.title("🏛️ منصة إستدامة الاستثمارية")
    
    tab1, tab2, tab3 = st.tabs(["📊 لوحة التحكم القيادية", "💰 تقييم العقود", "📄 الوثائق المعتمدة"])

    with tab1:
        st.subheader("تحليل فجوة القيمة (Gap Analysis)")
        kpi_df = pd.DataFrame({
            'النشاط': list(ACTIVITIES_DB.keys()),
            'الإيراد الحالي': [100, 55, 80, 40, 70],
            'الإيراد العادل': [135, 65, 110, 52, 85]
        })
        fig = px.bar(kpi_df, x='النشاط', y=['الإيراد الحالي', 'الإيراد العادل'], barmode='group',
                     color_discrete_sequence=['#1e3d59', '#d35400'])
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        col_in, col_res = st.columns(2)
        with col_in:
            sel_act = st.selectbox("نوع النشاط الاستثماري", list(ACTIVITIES_DB.keys()))
            gdv_in = st.number_input("القيمة التطويرية (GDV)", value=10000000)
            capex_in = st.number_input("تكلفة الإنشاء (CAPEX)", value=6000000)
            term_in = st.slider("المدة", 5, 50, 25)
            rent, sched = calculate_valuation(sel_act, gdv_in, capex_in, 2000000, term_in, 2)
        with col_res:
            st.metric("الأجرة السنوية العادلة", f"{rent:,.0f} ريال")
            st.area_chart(sched)

    with tab3:
        st.subheader("إصدار رمز الموثوقية")
        qr_str = f"Auditor: {name} | Activity: {sel_act} | Rent: {rent:,.0f}"
        qr = qrcode.make(qr_str)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="رمز موثوقية التقييم - منصة إستدامة")

    st.markdown("---")
    st.caption("نظام التخطيط الاستراتيجي المؤمن - كافة الحقوق محفوظة")
