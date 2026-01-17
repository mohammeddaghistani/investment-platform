# منصة إستدامة | مشروع Streamlit (نسخة متعددة الملفات)

## التشغيل محلياً
```bash
pip install -r requirements.txt
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# ضع hash كلمة المرور داخل .streamlit/secrets.toml
streamlit run app.py
```

## النشر على Streamlit Cloud
1) ارفع هذا المشروع إلى GitHub كما هو.
2) في Streamlit Cloud -> App Settings -> Secrets
   انسخ محتوى `.streamlit/secrets.toml.example` داخل Secrets (بعد تعبئة invest_admin_hash).
3) اجعل ملف التشغيل `app.py`.

> ملاحظة: المجلد `core/` يحتوي على `__init__.py` لتفادي ModuleNotFoundError.
