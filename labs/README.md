# الذكاء الاصطناعي في السياسات العامة وتقديم الخدمات العامة: المختبرات

اثنا عشر مختبرًا لمقرر أكاديمية سدايا **LDS-EXE-301**، مدة كل منها 35 دقيقة. المختبرات صفحات إرشادية بالعربية: الهدف،
والملفات، وخطوات بدقائقها، وأسئلة تحقق، وتمرين إضافي ✱، ومفتاح للمدرّب في قسم «للمدرّب» في كل صفحة. لا كود يكتبه
المشارك؛ يشغّل برنامجين جاهزين فقط.

كل المختبرات في جهة واحدة: **وزارة الرعاية والتمكين**، وزارة افتراضية، وخدمتها **منحة تهيئة المسكن** ومساعدها «مُؤازِر».
المشروع الختامي على خدمة ثانية للوزارة نفسها، **بدل مقدّم الرعاية**. كل الأسماء والأرقام والجهات وهمية، وكل الملفات
اصطناعية ومنشورة مع المقرر، فهي «عامة».

## ما يحتاجه المشارك

- جدول بيانات يفتح ملفات CSV، ومحرر نصوص.
- [uv](https://docs.astral.sh/uv/) لتشغيل برنامج الاختبار والحاسبة على الجهاز أو في Colab. لا يُنزَّل أي نموذج على الجهاز.
- اختياري: حساب لدى مزوّد نماذج مستضافة بواجهة محادثة قياسية (عنوان ومفتاح واسم نموذج في `labs/testing/.env`
  المنسوخ من `labs/testing/.env.example`). من لا يملكه يستعمل `--recorded`.

## نقطة البداية والحل

كل مختبر يبدأ من ملفات مقدَّمة ولا يعتمد على مختبر آخر في اليوم نفسه. المختبر الذي يبني على يوم سابق يبدأ من ملف مرجعي
مقدَّم (السجلان المسجَّلان في `testing/recorded/`)، لا من عمل المشارك.

| المختبر | الصفحة | يبدأ من | الحل المرجعي |
|---|---|---|---|
| 1.1 | `D1_1_state_roles.html` | `d1/case_brief.txt`، `d1/policy_problem.txt`، `d1/ministry_actions.csv` | مفتاح الصفحة؛ `check.py 1.1` |
| 1.2 | `D1_2_instruments.html` | `d1/instrument_evidence.csv`، `d1/scoring_guide.txt`، `d1/team_draft_scores.csv` | مفتاح الصفحة؛ `check.py 1.2` |
| 1.3 | `D1_3_procurement_cost.html` | `d1/procurement_options.csv` | مفتاح الصفحة؛ `check.py 1.3` |
| 1.4 | `D1_4_public_value.html` | `d1/benefit_claims.csv` | مفتاح الصفحة؛ `check.py 1.4` |
| 2.1 | `D2_1_value_case.html` | `d2/draft_value_case.txt`، `d2/assumptions.csv`، بيانات الخدمة الشهرية، `tools/value_case.py` | مفتاح الصفحة؛ `check.py 2.1` |
| 2.2 | `D2_2_automation_limits.html` | `d2/journey_points.csv`، `d2/candidate_measures.csv`، بيانات الخدمة الشهرية | مفتاح الصفحة؛ `check.py 2.2` |
| 2.3 | `D2_3_bilingual_test.html` | `d2/test_cases.csv`، `d2/test_key.csv`، `d2/pass_rules.txt`، `d2/configurations.txt`، `testing/run_tests.py` | مفتاح الصفحة؛ `check.py 2.3` |
| 2.4 | `D2_4_test_report.html` | `testing/recorded/run_a.json`، `testing/recorded/run_b.json` | مفتاح الصفحة؛ `check.py 2.4` |
| 3.1 | `D3_1_inventory_record.html` | `d3/inventory_template.csv`، `d3/draft_transparency_record.txt`، السجل المسجَّل للإعداد B | مفتاح الصفحة؛ `check.py 3.1` |
| 3.2 | `D3_2_impact_assessment.html` | `d3/risk_register_draft.csv`، `d3/rmf_scale.txt` | مفتاح الصفحة؛ `check.py 3.2` |
| 3.3 | `D3_3_review_appeal.html` | `d3/pack_draft.csv`، `d3/appeal_route_draft.txt` | مفتاح الصفحة؛ `check.py 3.3` |
| 3.4 | `D3_4_competence_plan.html` | `d3/workforce_profile.csv`، `d3/occupation_cards.csv`، `d3/programme_results.csv` | مفتاح الصفحة؛ `check.py 3.4` |
| المشروع | `slides/capstone.html` | `files/capstone/`، `tools/value_case.py --service carers`، `testing/run_tests.py c` | `check.py capstone` (الأرقام وحدها) |

## تشغيل الحلول

```bash
uv run labs/solutions/check.py          # كل المختبرات وأرقام المشروع الختامي
uv run labs/solutions/check.py 2.1      # مختبر واحد
```

ملف واحد بلا اعتماديات خارجية. يطبع لكل مختبر ما أعاد حسابه و`PASS`، ولا يكتب شيئًا على القرص ولا يتصل بأي نموذج.

**ما يُشغَّل فعلًا:** كل حساب على الملفات: الأدوار والتعارضات، ودرجات الأدوات وتكلفة خمس سنوات، وتكلفة دورة الحياة،
وفرز المنافع، ودراسة القيمة وجدول التوزيع، وخطوط الأساس، وتصحيح الحالات بالقواعد المكتوبة وقاعدة القرار، ومستويات
المخاطر، ومشكلات جدول الضوابط، وفجوة الكفاءات.

**ما يُشغَّل بنموذج بديل:** إجابات المساعد في المختبرين 2.3 و2.4 والمختبر 3.1 والمشروع الختامي. السجلات في
`testing/recorded/` كتبها المقرر بسيناريو، فيها الأخطاء التي يقع فيها مساعد حقيقي، وليست مخرجات نموذج؛ وكل رقم في
مفاتيح هذه المختبرات وشرائح مراجعتها منها. مسار النموذج المستضاف في `run_tests.py` جُرِّب على خادم محلي يرد بالسجلات
نفسها، لا على نموذج حقيقي: مع نموذج حقيقي تختلف الأرقام، ويكتب المشارك ما ظهر له.

## الملفات

| الملف | ما هو | المزروع فيه |
|---|---|---|
| `d1/ministry_actions.csv` | أربعة عشر فعلًا للوزارة | ثلاثة تعارضات: A01 مع A02 وA03، وA04 مع A05، وA06 مع A07 |
| `d1/team_draft_scores.csv` | مسودة درجات الأدوات الثماني | أربع درجات تخالف دليل التقدير |
| `d1/procurement_options.csv` | ثلاثة خيارات شراء | الأرخص في السنة الأولى الأغلى في خمس سنوات |
| `d1/benefit_claims.csv` | ست عشرة منفعة مدعاة | ثلاثة أرقام تبنٍّ، وثلاثة عوائد خاصة، وخطران قُدّما منفعتين |
| `d2/draft_value_case.txt` | مسودة دراسة القيمة | سبعة أخطاء، منها عدّ الساعات مرتين وغياب موظفي المراجعة |
| `d2/enquiries_monthly.csv`، `d2/decisions_monthly.csv` | بيانات الخدمة الشهرية لسنة 2025 | فرق بين اللغتين وبين الفئات والمناطق |
| `d2/test_cases.csv`، `d2/test_key.csv` | أربعون حالة في عشرين زوجًا بمفتاحها | حالات سلامة وخصوصية حرجة، وجواب صحيح ناقص (T20) |
| `d3/draft_transparency_record.txt` | مسودة سجل الشفافية | سبعة أخطاء في سبعة سطور |
| `d3/risk_register_draft.csv` | عشرة مخاطر | خطأ ضرب في R02، ونقل إلى المزود، وقبولان قابلان للنقاش |
| `d3/pack_draft.csv`، `d3/appeal_route_draft.txt` | جدول الضوابط ومسودة التظلم | أربعة سطور تكسر المساءلة، وخمسة عيوب في طريق التظلم |
| `d3/workforce_profile.csv`، `d3/programme_results.csv` | القوى العاملة ونتائج برنامج سابق | نتائج نشاط تُقدَّم على أنها أثر |
| `capstone/` | خدمة بدل مقدّم الرعاية: موجز ومشكلة وبيانات وفرضيات وعشرون حالة | إخفاق خصوصية حرج (C18) يوقف الإطلاق |

## إعادة توليد الملفات

ملفات `files/` والسجلات في `testing/recorded/` مولّدة ببذرة ثابتة:

```bash
uv run labs/_tools/prepare_files.py
uv run labs/solutions/check.py
```

أعد تشغيل `check.py` بعد كل تغيير في المولّد. أرقام المثال الموازي في الشرائح (بطاقة النقل الميسّر) يطبعها
`uv run labs/_tools/parallel_example.py`.
