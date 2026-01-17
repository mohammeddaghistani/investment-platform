import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import qrcode
from io import BytesIO
from datetime import datetime
import plotly.express as px

# ==========================================
# 1. إعدادات الصفحة والهوية البصرية
# ==========================================
st.set_page_config(page_title="منصة إستدامة للاستثمار العقاري", layout="wide")

# استايل مخصص لتحسين المظهر
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1, h2, h3 { color: #1e3d59; font-family: 'Arial'; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. قاعدة بيانات الأنشطة والضوابط النظامية
# ==========================================
ACTIVITIES_DB = {
    "التجارية": {"method": "المتبقي", "max_term": 50, "grace_max": 0.10, "suitability": ["مركز المدينة", "محور رئيسي"]},
    "الصناعية": {"method": "السوق", "max_term": 25, "grace_max": 0.10, "suitability": ["منطقة صناعية"]},
    "الصحية": {"method": "الدخل", "max_term": 25, "grace_max": 0.10, "suitability": ["حي سكني", "مركز المدينة"]},
    "التعليمية": {"method": "الدخل", "max_term": 25, "grace_max": 0.10, "suitability": ["حي سكني"]},
    "السياحية": {"method": "المتبقي", "max_term": 50, "grace_max": 0.10, "suitability": ["واجهة بحرية", "مركز المدينة"]},
    "الرياضية والترفيهية": {"method": "الدخل", "max_term": 30, "grace_max": 0.10, "suitability": ["محور رئيسي", "واجهة بحرية"]},
    "الزراعية والحيوانية": {"method": "السوق", "max_term": 20, "grace_max": 0.05, "suitability": ["منطقة طرفية"]},
    "الاجتماعية": {"method": "التكلفة", "max_term": 25, "grace_max": 0.10, "suitability": ["حي سكني"]},
    "النقل": {"method": "السوق", "max_term": 20, "grace_max": 0.05, "suitability": ["محور رئيسي"]},
    "المالية": {"method": "السوق", "max_term": 15, "grace_max": 0.05, "suitability": ["مركز المدينة"]},
    "المركبات": {"method": "السوق", "max_term": 15, "grace_max": 0.05, "suitability": ["منطقة صناعية", "محور رئيسي"]},
    "الصيانة والتركيب": {"method": "السوق", "max_term": 10, "grace_max": 0.05, "suitability": ["منطقة صناعية"]},
    "التشييد وإدارة العقارات": {"method": "الدخل", "max_term": 20, "grace_max": 0.05, "suitability": ["محور رئيسي"]},
    "الخدمات العامة": {"method": "التكلفة", "max_term": 25, "grace_max": 0.10, "suitability": ["مركز المدينة", "حي سكني"]},
    "الملبوسات والمنسوجات": {"method": "السوق", "max_term": 10, "grace_max": 0.05, "suitability": ["مركز المدينة"]},
    "المرافق العامة": {"method": "التكلفة", "max_term": 50, "grace_max": 0.10, "suitability": ["محور رئيسي"]},
}

# ==========================================
# 3. المحركات المنطقية (Logic Engines)
# ==========================================

def calculate_valuation(activity, gdv, capex, revenue, term, grace):
    """حساب القيمة العادلة والنمو الخماسي (المادة 26)"""
    method = ACTIVITIES_DB[activity]["method"]
    if method == "المتبقي":
        soft_costs = capex * 0.12
        profit = gdv * 0.18
        land_value = max(gdv - (capex + soft_costs + profit), 0)
        base_rent = land_value * 0.08
    elif method == "الدخل":
        base_rent = revenue * 0.25
    else: # أسلوب السوق/التكلفة
        base_rent = (capex * 0.07) + (revenue * 0.10)
    
    # بناء جدول التدفقات النقدية
    cash_flows = []
    current_rent = base_rent
    for y in range(1, term + 1):
        if y <= grace:
            cash_flows.append(0)
        else:
            if y > 1 and (y - 1) % 5 == 0: # الزيادة النظامية كل 5 سنوات
                current_rent *= 1.05
            cash_flows.append(current_rent)
    return base_rent, cash_flows

def get_suitability_score(activity, location, demand):
    """حساب درجة الملاءمة من 100"""
    score = 50
    if location in ACTIVITIES_DB[activity]["suitability"]: score += 35
    if demand == "نمو قوي": score += 15
    elif demand == "انخفاض": score -= 20
    return min(max(score, 0), 100)

# ==========================================
# 4. بناء واجهة الاستخدام (Main UI)
# ==========================================

st.title("🏛️ منظومة إستدامة | التخطيط الاستراتيجي العقاري")
st.markdown("---")

# القائمة الجانبية للمدخلات العامة
with st.sidebar:
    st.header("⚙️ إعدادات المحاكاة")
    selected_act = st.selectbox("نوع النشاط الاستثماري", list(ACTIVITIES_DB.keys()))
    loc_type = st.selectbox("طبيعة الموقع الجغرافي", ["مركز المدينة", "محور رئيسي", "حي سكني", "واجهة بحرية", "منطقة صناعية"])
    demand_level = st.select_slider("بيئة الطلب السوقي", options=["انخفاض", "مستقر", "نمو قوي"], value="مستقر")
    st.divider()
    st.header("👥 المحرك الديموغرافي")
    current_pop = st.number_input("السكان في محيط الموقع", value=25000)
    growth_rate = st.slider("معدل النمو السنوي (%)", 0.0, 5.0, 2.5) / 100

# التبويبات الرئيسية
tab_radar, tab_finance, tab_kpi, tab_output = st.tabs([
    "🎯 رادار الملاءمة", "💰 التقييم المالي", "📊 لوحة التحكم", "📄 الوثائق الرسمية"
])

# --- التبويب الأول: رادار الملاءمة والطلب ---
with tab_radar:
    col1, col2 = st.columns([1, 1])
    with col1:
        score = get_suitability_score(selected_act, loc_type, demand_level)
        st.subheader("درجة الملاءمة الاستراتيجية")
        st.metric("Suitability Score", f"{score}/100")
        st.progress(score / 100)
        
        future_pop = current_pop * ((1 + growth_rate) ** 10)
        st.info(f"💡 السكان المتوقع بعد 10 سنوات: {int(future_pop):,} نسمة")

    with col2:
        st.subheader("تحليل فجوة الاحتياج")
        standards = {"الصحية": 5000, "التعليمية": 3000, "التجارية": 1500}
        needed = future_pop / standards.get(selected_act, 4000)
        st.write(f"الاحتياج المستقبلي لـ {selected_act}: **{int(needed)} وحدة**")
        

# --- التبويب الثاني: التقييم المالي والمفاضلة ---
with tab_finance:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("مدخلات التقييم (وفق الدليل)")
        gdv = st.number_input("القيمة التطويرية النهائية (GDV)", value=50000000)
        capex = st.number_input("تكاليف التشييد (CAPEX)", value=30000000)
        term = st.slider("مدة العقد (سنة)", 5, ACTIVITIES_DB[selected_act]["max_term"], 25)
        grace = st.slider("فترة السماح (سنوات)", 0, int(term * 0.10), 2)
        
        rent, schedule = calculate_valuation(selected_act, gdv, capex, 5000000, term, grace)
        st.success(f"الأجرة السنوية العادلة: {rent:,.2f} ﷼")

    with c2:
        st.subheader("استشراف التدفقات النقدية (25 سنة)")
        st.area_chart(schedule, color="#1e3d59")
        

# --- التبويب الثالث: لوحة التحكم (KPIs) ---
with tab_kpi:
    st.subheader("📈 تحليل استرداد القيمة في المحفظة العقارية")
    # بيانات افتراضية بناءً على ملف الـ 1800 عقد
    kpi_data = pd.DataFrame({
        'النشاط': ['تجاري', 'سياحي', 'تعليمي', 'صحي', 'صناعي'],
        'الإيراد الحالي': [120, 90, 40, 55, 70],
        'الإيراد العادل المستهدف': [155, 130, 52, 65, 85]
    })
    kpi_data['الفجوة المستردة'] = kpi_data['الإيراد العادل المستهدف'] - kpi_data['الإيراد الحالي']
    
    fig = px.bar(kpi_data, x='النشاط', y=['الإيراد الحالي', 'الفجوة المستردة'], 
                 title="فرص استرداد الأرباح (بالمليون ريال)", barmode='stack',
                 color_discrete_sequence=['#1e3d59', '#d35400'])
    st.plotly_chart(fig, use_container_width=True)
    

# --- التبويب الرابع: الوثائق والموثوقية ---
with tab_output:
    st.subheader("📑 إصدار مسودة خطاب إعادة التقييم")
    contract_id = st.text_input("رقم العقد المستهدف", "30040868948")
    
    letter_template = f"""
    إلى مستثمر نشاط {selected_act}،
    بناءً على دليل سياسات التقييم 2023 ولائحة التصرف بالعقارات البلدية، 
    نحيطكم علماً بأن الأجرة السنوية العادلة للعقد رقم {contract_id} 
    قد تم تحديثها لتصبح {rent:,.2f} ﷼ سنوياً، مع مراعاة الزيادات الدورية (المادة 26).
    """
    st.text_area("نص الإشعار:", letter_template, height=150)
    
    st.divider()
    st.subheader("🔐 رمز موثوقية التقييم (QR Code)")
    qr_content = f"Contract: {contract_id} | Fair Rent: {rent:,.0f} | Date: {datetime.now().date()}"
    qr = qrcode.make(qr_content)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    st.image(buf.getvalue(), caption="امسح الرمز للتحقق من بيانات التقييم على السحابة")

st.markdown("---")
st.center = st.caption("منصة إستدامة | جميع الحقوق محفوظة لقطاع التخطيط الاستراتيجي والاستثمار")
