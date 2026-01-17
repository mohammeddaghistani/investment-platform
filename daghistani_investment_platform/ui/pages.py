import streamlit as st
import pandas as pd
import plotly.express as px

from core.regulations import ACTIVITIES_DB, ZONE_MULT
from core.engine import ValuationInputs, compute_suitability, compute_future_population, compute_valuation
from core.qr import make_qr_png
from core.reporting import generate_official_pdf

def _sidebar_due_diligence():
    with st.sidebar:
        st.header("⚙️ معاملات الفحص (Due Diligence)")
        loc_zone = st.selectbox("نطاق الموقع الجغرافي", list(ZONE_MULT.keys()))
        land_area = st.number_input("مساحة الأرض (م2)", value=1000, min_value=1)
        tech_risks = st.slider("معامل المخاطر الفنية (%)", 0, 100, 10)
    return loc_zone, land_area, tech_risks

def page_suitability():
    loc_zone, land_area, tech_risks = _sidebar_due_diligence()
    c1, c2 = st.columns(2)
    selected_act = c1.selectbox("اختر النشاط الاستثماري", list(ACTIVITIES_DB.keys()), key="act_select")
    suit_score = compute_suitability(tech_risks)
    c1.metric("درجة ملاءمة الموقع", f"{suit_score}/100")
    c1.progress(suit_score / 100)

    pop = c2.number_input("السكان الحاليين (نطاق 5 كم)", value=50000, min_value=0)
    growth = c2.slider("معدل النمو السنوي (%)", 0.0, 5.0, 2.7) / 100
    future_pop = compute_future_population(pop, growth, years=10)
    c2.info(f"📈 السكان المتوقع لعام 2036: {future_pop:,} نسمة")

    st.session_state["inputs"].update({
        "loc_zone": loc_zone, "land_area": land_area, "tech_risks": tech_risks,
        "selected_act": selected_act, "pop": pop, "growth": growth,
    })

def page_valuation():
    loc_zone, land_area, tech_risks = _sidebar_due_diligence()
    selected_act = st.session_state["inputs"].get("selected_act") or st.selectbox(
        "اختر النشاط الاستثماري", list(ACTIVITIES_DB.keys()), key="act_select_2"
    )
    col_in, col_res = st.columns(2)
    with col_in:
        gdv = st.number_input("القيمة التطويرية (GDV) / م2", value=5000, min_value=0)
        capex = st.number_input("تكلفة البناء (CAPEX) / م2", value=3000, min_value=0)
        max_term = int(ACTIVITIES_DB[selected_act]["max_term"])
        term = st.slider("مدة العقد (سنة)", 5, max_term, min(25, max_term))
        grace_rate = float(ACTIVITIES_DB[selected_act]["grace_rate"])
        grace = int(term * grace_rate)
        st.write(f"⏱️ فترة السماح النظامية: **{grace} سنوات**")

    with col_res:
        inp = ValuationInputs(
            selected_act=selected_act, loc_zone=loc_zone, land_area=float(land_area),
            tech_risks=int(tech_risks), pop_current=int(st.session_state["inputs"].get("pop", 50000)),
            growth_rate=float(st.session_state["inputs"].get("growth", 0.027)),
            gdv_m2=float(gdv), capex_m2=float(capex), term_years=int(term),
            grace_rate=grace_rate, zone_multiplier=float(ZONE_MULT[loc_zone]),
        )
        out = compute_valuation(inp)
        if out["warning_low_gdv"]:
            st.warning("⚠️ القيمة التطويرية أقل من التكاليف التقديرية: تحقق من المدخلات (GDV/CAPEX).")
        st.metric("الأجرة السنوية العادلة", f"{out['base_rent']:,.0f} ريال")
        st.area_chart(out["schedule"])
        st.caption("الرسم يوضح فترة السماح ثم القفزات الإيجارية النظامية (5% كل 5 سنوات)")
        st.session_state["results"].update(out)
        st.session_state["inputs"].update({
            "loc_zone": loc_zone, "land_area": land_area, "tech_risks": tech_risks,
            "selected_act": selected_act, "gdv": gdv, "capex": capex, "term": term, "grace": out["grace"],
        })

def page_portfolio():
    st.subheader("📊 تحليل فجوة القيمة في المحفظة العقارية")
    st.info("يمكنك رفع ملف CSV/Excel للمحفظة، أو استخدام بيانات تجريبية (Mock).")
    up = st.file_uploader("رفع ملف المحفظة (CSV أو Excel)", type=["csv", "xlsx"])
    if up is not None:
        try:
            df = pd.read_csv(up) if up.name.lower().endswith(".csv") else pd.read_excel(up)
            st.session_state["portfolio_df"] = df
            st.success(f"تم تحميل الملف بنجاح: {up.name} (عدد الصفوف: {len(df):,})")
        except Exception as e:
            st.error(f"تعذر قراءة الملف: {e}")

    use_mock = st.toggle("استخدام بيانات تجريبية", value=(st.session_state["portfolio_df"] is None))
    if use_mock:
        df = pd.DataFrame({
            'القطاع': ['تجاري', 'سياحي', 'صحي', 'تعليمي', 'صناعي'],
            'الإيراد الحالي (M)': [120, 80, 45, 30, 65],
            'الإيراد العادل (M)': [155, 110, 58, 42, 85]
        })
    else:
        df = st.session_state["portfolio_df"]
        if df is None:
            st.warning("لم يتم رفع ملف بعد.")
            return

    if 'الإيراد العادل (M)' in df.columns and 'الإيراد الحالي (M)' in df.columns:
        df = df.copy()
        df['الفجوة المستردة'] = df['الإيراد العادل (M)'] - df['الإيراد الحالي (M)']
        xcol = 'القطاع' if 'القطاع' in df.columns else df.columns[0]
        fig = px.bar(df, x=xcol, y=['الإيراد الحالي (M)', 'الفجوة المستردة'], barmode='stack', title="فرص استرداد الأرباح السنوية")
        st.plotly_chart(fig, use_container_width=True)
        st.success(f"📌 إجمالي الإيرادات الإضافية الممكنة: {df['الفجوة المستردة'].sum():,.0f} مليون ريال سنوياً")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("ملفك لا يحتوي الأعمدة المطلوبة لتحليل الفجوة (الإيراد الحالي/العادل).")
        st.dataframe(df, use_container_width=True)

def page_reports():
    st.subheader("📄 إصدار تقرير التقييم المعتمد")
    contract_id = st.text_input("رقم العقد المستهدف", "30040868948")
    selected_act = st.session_state["inputs"].get("selected_act", "غير محدد")
    land_area = float(st.session_state["inputs"].get("land_area", 0) or 0)
    loc_zone = st.session_state["inputs"].get("loc_zone", "غير محدد")
    base_rent = float(st.session_state["results"].get("base_rent", 0) or 0)
    grace = int(st.session_state["results"].get("grace", 0) or 0)
    term = int(st.session_state["inputs"].get("term", 0) or 0)

    report_content = f"""إشعار تقييم استثماري - منصة إستدامة
-----------------------------------
رقم العقد: {contract_id}
النشاط: {selected_act}
مساحة الموقع: {land_area:,.0f} م2
نطاق الموقع: {loc_zone}
مدة العقد: {term} سنة
الأجرة السنوية المعتمدة: {base_rent:,.0f} ريال
فترة السماح: {grace} سنوات
الزيادة الدورية: 5% كل 5 سنوات (المادة 26)
-----------------------------------
تم هذا التقييم بناءً على دليل سياسات التقييم 2023 ولائحة التصرف بالعقارات البلدية."""
    st.code(report_content)

    qr_str = f"ID:{contract_id}|Rent:{base_rent:.0f}|Zone:{loc_zone}"
    qr_png = make_qr_png(qr_str)
    st.image(qr_png, caption="ختم الموثوقية الرقمي للتقييم")

    c1, c2 = st.columns(2)
    with c1:
        st.download_button("⬇️ تنزيل TXT", data=report_content.encode("utf-8"),
                           file_name=f"istidama_report_{contract_id}.txt", mime="text/plain")
    with c2:
        pdf_bytes = generate_official_pdf(
            report={"contract_id": contract_id, "activity": selected_act, "land_area": land_area,
                    "zone": loc_zone, "term_years": term, "grace_years": grace, "base_rent": base_rent},
            qr_png=qr_png,
        )
        st.download_button("⬇️ تنزيل PDF رسمي", data=pdf_bytes,
                           file_name=f"istidama_report_{contract_id}.pdf", mime="application/pdf")
