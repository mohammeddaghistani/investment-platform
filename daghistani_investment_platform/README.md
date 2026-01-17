# منصة إستدامة | نسخة داخلية (Multiple Users + Roles + PDF)

## التشغيل محلياً
```bash
pip install -r requirements.txt
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# عدّل كلمات المرور (bcrypt hashes) داخل .streamlit/secrets.toml
streamlit run app.py
```

## النشر على Streamlit Cloud
1) ارفع المشروع إلى GitHub كما هو.
2) Streamlit Cloud -> App Settings -> Secrets
   الصق محتوى `.streamlit/secrets.toml.example` وعدّل hashes.
3) Main file path: `app.py`

## الأدوار (RBAC)
- admin: كل التبويبات
- analyst: الملاءمة + التقييم + التقارير
- viewer: التقارير فقط
