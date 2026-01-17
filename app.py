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
# 1. نظام الحماية وتسجيل الدخول (Security)
# ==========================================
# ملاحظة: في النسخة النهائية، يفضل وضع كلمات المرور في ملف سري (secrets.toml)
names = ['إدارة الاستثمار', 'المدير التنفيذي']
usernames = ['invest_admin', 'ceo_makkah']
# كلمات المرور مشفرة (هنا استخدمنا كلمات بسيطة للتوضيح)
passwords = ['admin123', 'admin2025'] 

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(
    {'usernames': {
        usernames[0]: {'name': names[0], 'password': hashed_passwords[0]},
        usernames[1]: {'name': names[1], 'password': hashed_passwords[1]}
    }},
    'investment_dashboard_cookie', 'auth_key', cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login('تسجيل الدخول للنظام الاستراتيجي', 'main')

if authentication_status == False:
    st.error('اسم المستخدم أو كلمة المرور غير صحيحة')
elif authentication_status == None:
    st.warning('يرجى إدخال بيانات الدخول المعتمدة')
elif authentication_status:
    # --- بداية محتوى النظام المحمي ---
    
    with st.sidebar:
        st.write(f'ترحيب: **{name}**')
        authenticator.logout('تسجيل الخروج', 'sidebar')

    # ==========================================
    # 2. قاعدة البيانات والضوابط (المدمجة سابقاً)
    # ==========================================
    ACTIVITIES_DB = {
        "التجارية": {"method": "المتبقي", "max_term": 50, "grace_max": 0.10, "suitability": ["مركز المدينة", "محور رئيسي"]},
        "الصناعية": {"method": "السوق", "max_term": 25, "grace_max": 0.10, "suitability": ["منطقة صناعية"]},
        "الصحية": {"method": "الدخل", "max_term": 25, "grace_max": 0.10, "suitability": ["حي سكوي", "مركز المدينة"]},
        "التعليمية": {"method": "الدخل", "max_term": 25, "grace_max": 0.10, "suitability": ["حي سكني"]},
        "السياحية": {"method": "المتبقي", "max_term": 50, "grace_max": 0.10, "suitability": ["واجهة بحرية", "مركز المدينة"]},
    }

    def calculate_valuation(activity, gdv, capex, revenue, term, grace):
        method = ACTIVITIES_DB[activity]["method"]
        if method == "المتبقي":
            land_value = max(gdv - (capex * 1.12 + gdv * 0.18), 0)
            base_rent = land_value * 0.08
        else:
            base_rent = revenue * 0.25
        
        cash_flows = []
        curr = base_rent
        for y in range(1, term + 1):
            if y <= grace: cash_flows.append(0)
            else:
                if y > 1 and (y - 1) % 5 == 0: curr *= 1.05
                cash_flows.append(curr)
        return base_rent, cash_flows

    # ==========================================
    # 3. الواجهة الرئيسية للوحة التحكم
    # ==========================================
    st.title("🏛️ منصة إستدامة | النسخة المؤمنة")
    
    tab_radar, tab_finance, tab_kpi, tab_output = st.tabs([
        "🎯 رادار الملاءمة", "💰 التقييم المالي", "📊 لوحة التحكم", "📄 الوثائق الرسمية"
    ])

    with tab_radar:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("⚙️ إعدادات الموقع والنشاط")
            selected_act = st.selectbox("نوع النشاط", list(ACTIVITIES_DB.keys()))
            loc_type = st.selectbox("الموقع الجغرافي", ["مركز المدينة", "حي سكني", "واجهة بحرية"])
            demand = st.select_slider("الطلب السوقي", ["انخفاض", "مستقر", "نمو قوي"], "مستقر")
        with col2:
            st.subheader("📈 الاستشراف الديموغرافي")
            pop = st.number_input("السكان الحاليين", value=15000)
            st.metric("السكان المتوقع (10 سنوات)", f"{int(pop * 1.3):,}")

    with tab_finance:
        c1, c2 = st.columns(2)
        with c1:
            gdv = st.number_input("القيمة التطويرية (GDV)", value=10000000)
            capex = st.number_input("التكلفة (CAPEX)", value=6000000)
            rent, schedule = calculate_valuation(selected_act, gdv, capex, 2000000, 25, 2)
            st.success(f"الأجرة العادلة المقدرة: {rent:,.0f} ريال")
        with c2:
            st.area_chart(schedule)

    with tab_kpi:
        st.subheader("📊 تحليل الفجوة المالية للمحفظة")
        kpi_df = pd.DataFrame({
            'النشاط': list(ACTIVITIES_DB.keys()),
            'الإيراد الحالي': [100, 40, 30, 25, 60],
            'الإيراد العادل': [135, 55, 42, 35, 95]
        })
        fig = px.bar(kpi_df, x='النشاط', y=['الإيراد الحالي', 'الإيراد العادل'], barmode='group')
        st.plotly_chart(fig, use_container_width=True)

    with tab_output:
        st.subheader("📄 إصدار الإخطارات الموثقة")
        if st.button("توليد كود QR للتقييم"):
            qr_data = f"Activity: {selected_act} | Rent: {rent:,.0f} | Auditor: {name}"
            qr = qrcode.make(qr_data)
            buf = BytesIO()
            qr.save(buf, format="PNG")
            st.image(buf.getvalue(), caption="امسح الرمز للتحقق من الصلاحية")

    st.caption("نظام مؤمن - إدارة التخطيط الاستراتيجي والاستثمار")

# --- نهاية النظام المحمي ---
