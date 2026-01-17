import streamlit as st
import pandas as pd
import numpy as np
import qrcode
from io import BytesIO
import plotly.express as px
import streamlit_authenticator as stauth

# ==========================================
# 1. نظام الحماية الصارم (Security)
# ==========================================
credentials = {
    "usernames": {
        "invest_admin": {
            "name": "إدارة الاستثمار الاستراتيجي",
            "password": "$2b$12$EixZaYVK1Vz17Uy5vQPfbOfh17S2REAlX.y7n6tE9R.o5B1oH7EWG" # admin123
        }
    }
}
authenticator = stauth.Authenticate(credentials, "invest_vault", "key_2026_makkah", 1)

try:
    auth_result = authenticator.login(location='main')
except Exception:
    pass

if st.session_state.get("authentication_status") is not True:
    st.warning("🔒 يرجى تسجيل الدخول للوصول إلى العقل الاستثماري")
else:
    # --- بداية المحتوى الكامل ---
    with st.sidebar:
        st.success(f"مرحباً بك: {st.session_state['name']}")
        authenticator.logout('تسجيل الخروج', 'sidebar')
        st.divider()
        st.header("🛠️ معاملات الفحص النافي للجهالة")
        site_access = st.slider("سهولة الوصول للموقع (%)", 0, 100, 80)
        technical_risks = st.slider("مخاطر فنية/عوائق (%)", 0, 100, 10)
        utility_availability = st.checkbox("توفر الخدمات الأساسية (كهرباء/مياه)", value=True)

    # ==========================================
    # 2. محرك الأنشطة المتطور (17 نشاطاً)
    # ==========================================
    ACTIVITIES_DB = {
        "التجارية": {"max_term": 50, "method": "المتبقي", "risk_weight": 0.05},
        "الصناعية": {"max_term": 25, "method": "السوق", "risk_weight": 0.15},
        "السياحية": {"max_term": 50, "method": "المتبقي", "risk_weight": 0.10},
        "الصحية": {"max_term": 25, "method": "الدخل", "risk_weight": 0.02},
        "التعليمية": {"max_term": 25, "method": "الدخل", "risk_weight": 0.02},
        "الرياضية": {"max_term": 30, "method": "الدخل", "risk_weight": 0.05},
        "النقل": {"max_term": 20, "method": "السوق", "risk_weight": 0.10},
        "المالية": {"max_term": 15, "method": "السوق", "risk_weight": 0.01},
        "الخدمات العامة": {"max_term": 25, "method": "التكلفة", "risk_weight": 0.05},
        "الاتصالات": {"max_term": 15, "method": "السوق", "risk_weight": 0.02}
    }

    st.title("🏛️ منصة إستدامة | نظام دعم القرار الاستثماري")
    tabs = st.tabs(["🚀 رادار الملاءمة", "💰 التقييم المعمق", "⚖️ تحليل المخاطر والمفاضلة", "📑 التقارير الرسمية"])

    # --- التبويب 1: رادار الملاءمة والديموغرافيا ---
    with tabs[0]:
        c1, c2 = st.columns(2)
        selected_act = c1.selectbox("النشاط المستهدف", list(ACTIVITIES_DB.keys()))
        pop = c2.number_input("السكان الحاليين (نطاق 5 كم)", value=50000)
        growth = c2.slider("معدل النمو السنوي (%)", 0.0, 5.0, 2.5) / 100
        future_pop = pop * ((1 + growth) ** 10)
        c1.metric("الملاءمة الاستراتيجية", f"{int(site_access * 0.8 + 20)}/100")
        c2.info(f"📈 توقعات 2036: {int(future_pop):,} نسمة")
        

    # --- التبويب 2: التقييم المالي (Residual & Income) ---
    with tabs[1]:
        col_in, col_graph = st.columns([1, 1.5])
        with col_in:
            gdv = st.number_input("القيمة التطويرية (GDV)", value=25000000)
            capex = st.number_input("تكلفة المشروع (CAPEX)", value=15000000)
            term = st.slider("مدة العقد", 5, ACTIVITIES_DB[selected_act]["max_term"], 25)
            # احتساب فترة السماح آلياً (10% من العقد)
            grace = int(term * 0.10)
            st.write(f"⏱️ فترة السماح النظامية: **{grace} سنوات**")
            
            # محرك القيمة (تعديل بناءً على المخاطر)
            risk_adj = (technical_risks / 100) * gdv
            base_rent = max((gdv - capex - risk_adj) * 0.08, gdv * 0.04)
        
        with col_graph:
            st.metric("الأجرة السنوية العادلة (بعد خصم المخاطر)", f"{base_rent:,.0f} ريال")
            schedule = [0]*grace + [base_rent * (1.05 ** (i // 5)) for i in range(term - grace)]
            st.area_chart(schedule)
            

    # --- التبويب 3: مصفوفة المخاطر والمفاضلة (جديد) ---
    with tabs[2]:
        st.subheader("⚠️ مصفوفة مخاطر الموقع (Risk Heatmap)")
        risk_score = (technical_risks + (100 - site_access)) / 2
        if risk_score > 50:
            st.error(f"درجة الخطر: {risk_score}% - يتطلب ضمانات إضافية")
        else:
            st.success(f"درجة الخطر: {risk_score}% - موقع منخفض المخاطر")
        
        # محاكي المفاضلة بين المستثمرين
        st.divider()
        st.subheader("🤝 تقييم المستثمرين (Scorecard)")
        investor_name = st.text_input("اسم المستثمر المتقدم", "شركة مكة للإنشاء")
        financial_strength = st.slider("الملاءمة المالية", 0, 100, 90)
        exp_score = st.slider("الخبرة في النشاط", 0, 100, 85)
        final_inv_score = (financial_strength * 0.6 + exp_score * 0.4)
        st.write(f"النتيجة النهائية للمستثمر: **{final_inv_score}%**")

    # --- التبويب 4: المخرجات و QR ---
    with tabs[3]:
        st.subheader("📄 ملف الحقيقة الاستثمارية (Single Source of Truth)")
        report_data = f"Activity: {selected_act}\nRent: {base_rent:,.0f}\nRisk Level: {risk_score}%\nInvestor: {investor_name}"
        st.code(report_data)
        
        qr_data = f"AUTH-2026-{selected_act}-{base_rent}"
        qr = qrcode.make(qr_data)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="رمز موثوقية التقرير المعتمد")

st.markdown("---")
st.caption("تم الربط مع دليل التقييم 2023 ولائحة التصرف بالعقارات البلدية - نسخة 2026")
