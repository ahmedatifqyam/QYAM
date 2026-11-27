#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص آلي: يبحث في app.js عن كل سطر يضع نصاً داخل innerHTML عبر قالب (template
literal) يحتوي على قيمة من state/req/إلخ، دون استخدام escH(...) لتنقيته في
نفس السطر. الهدف: اكتشاف أي موضع جديد يُدخل بيانات مستخدم دون تنقية قبل أي
نشر، بدل الاعتماد على فحص عيني فقط.

تنبيه: هذا فحص "احتمالي" (heuristic) لا قطعي — قد يُبلّغ عن أسطر سليمة فعلاً
(مثلاً نص ثابت لا يحمل بيانات مستخدم)، فكل نتيجة تحتاج مراجعة بشرية سريعة قبل
الحكم عليها، لا تصحيحاً أعمى.

الاستخدام: python3 tools/check_esch.py [مسار app.js]
المخرج: صفر إذا لم يجد شيئاً مريباً، وإلا يطبع الأسطر المرشّحة ويخرج بكود 1.
"""
import sys
import re

RISKY_FIELD = re.compile(r"\$\{[^}]*\.(name|reason|note|desc|title|detailedReason|purpose|address|email|phone)\b[^}]*\}")
HAS_ESCH = re.compile(r"escH\(")

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "app.js"
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    flagged = []
    for i, line in enumerate(lines, start=1):
        if "innerHTML" not in line:
            continue
        if not RISKY_FIELD.search(line):
            continue
        if HAS_ESCH.search(line):
            continue
        flagged.append((i, line.strip()[:160]))

    if not flagged:
        print("لا يوجد — كل مواضع innerHTML التي تحمل حقولاً شائعة الخطورة تستخدم escH() في نفس السطر.")
        return 0

    print(f"تنبيه: {len(flagged)} سطراً يحتاج مراجعة يدوية (قد يكون بعضها سليماً فعلاً):\n")
    for ln, text in flagged:
        print(f"  app.js:{ln}: {text}")
    return 1

if __name__ == "__main__":
    sys.exit(main())
