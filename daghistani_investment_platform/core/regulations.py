ACTIVITIES_DB = {
    "التجارية": {"max_term": 50, "method": "المتبقي", "grace_rate": 0.10},
    "السياحية": {"max_term": 50, "method": "المتبقي", "grace_rate": 0.10},
    "الصحية": {"max_term": 25, "method": "الدخل", "grace_rate": 0.10},
    "التعليمية": {"max_term": 25, "method": "الدخل", "grace_rate": 0.10},
    "الصناعية": {"max_term": 25, "method": "السوق", "grace_rate": 0.10},
    "الرياضية والترفيهية": {"max_term": 30, "method": "الدخل", "grace_rate": 0.10},
    "الاجتماعية": {"max_term": 25, "method": "التكلفة", "grace_rate": 0.10},
    "الزراعية": {"max_term": 20, "method": "السوق", "grace_rate": 0.05},
    "النقل": {"max_term": 20, "method": "السوق", "grace_rate": 0.05},
    "المالية": {"max_term": 15, "method": "السوق", "grace_rate": 0.05},
    "الاتصالات": {"max_term": 15, "method": "السوق", "grace_rate": 0.05},
    "المركبات": {"max_term": 15, "method": "السوق", "grace_rate": 0.05},
    "الخدمات العامة": {"max_term": 25, "method": "التكلفة", "grace_rate": 0.10},
    "المرافق العامة": {"max_term": 50, "method": "التكلفة", "grace_rate": 0.10},
    "التشييد وإدارة العقارات": {"max_term": 20, "method": "الدخل", "grace_rate": 0.05},
    "الصيانة والتركيب": {"max_term": 10, "method": "السوق", "grace_rate": 0.05},
    "الملبوسات والمنسوجات": {"max_term": 10, "method": "السوق", "grace_rate": 0.05},
}

ZONE_MULT = {
    "المنطقة المركزية": 1.5,
    "محور رئيسي (A)": 1.3,
    "داخل الأحياء (B)": 1.0,
    "أطراف المدينة": 0.8,
}
