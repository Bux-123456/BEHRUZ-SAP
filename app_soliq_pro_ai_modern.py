import os
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="SOLIQ PRO AI", page_icon="🧾", layout="wide")


# SOLIQ PRO AI dizayni: to‘q ko‘k fon, oq matn va yashil tugmalar
st.markdown("""
<style>
:root { --navy:#071B33; --panel:#102B4C; --panel2:#16365C; --green:#16A36A; --mint:#70E0AD; --line:#294B70; }
.stApp, [data-testid="stAppViewContainer"] { background: radial-gradient(circle at 75% 0%, #123C68 0%, #071B33 42%, #06172B 100%) !important; color:#F5F8FC !important; }
[data-testid="stHeader"] { background:rgba(7,27,51,.85) !important; }
[data-testid="stSidebar"], [data-testid="stSidebar"] > div { background:linear-gradient(180deg,#06172B,#0D2B4D) !important; border-right:1px solid #294B70; }
.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp p,.stApp label,.stApp li,.stApp [data-testid="stMetricLabel"],.stApp [data-testid="stMetricValue"],.stApp [data-testid="stCaptionContainer"] { color:#F5F8FC !important; }
.stApp h1 { letter-spacing:-1.2px; font-weight:800; }
[data-testid="stMetric"], [data-testid="stChatMessage"], [data-testid="stExpander"] { background:linear-gradient(145deg,rgba(22,54,92,.94),rgba(12,39,69,.94)) !important; border:1px solid var(--line) !important; border-radius:16px !important; padding:12px; }
[data-testid="stMetricValue"] { font-weight:750 !important; }
.stButton > button, [data-testid="stFormSubmitButton"] > button { background:linear-gradient(135deg,#16A36A,#0D8658) !important; color:white !important; border:1px solid #27BC80 !important; border-radius:11px !important; font-weight:650 !important; min-height:42px; transition:all .2s ease; }
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover { background:#128455 !important; border-color:#70E0AD !important; transform:translateY(-1px); }
.stTextInput input,.stTextArea textarea,[data-testid="stChatInput"] textarea { background:#F5F8FC !important; color:#10233D !important; border:1px solid #B7C9DD !important; border-radius:10px !important; }
[data-testid="stSelectbox"] div[data-baseweb="select"] { background:#F5F8FC !important; color:#10233D !important; border-radius:10px !important; }
[data-testid="stChatInput"] { border-color:#294B70 !important; }
.stApp a { color:#70E0AD !important; font-weight:550; }
hr { border-color:#294B70 !important; }
div[data-testid="stAlert"] { border-radius:12px !important; }
.hero-card { padding:28px 30px; border:1px solid #28517B; border-radius:22px; background:linear-gradient(115deg,rgba(18,58,99,.98),rgba(7,27,51,.94)); margin:4px 0 20px; box-shadow:0 16px 40px rgba(0,0,0,.18); }
.hero-kicker { display:inline-block; padding:5px 12px; border-radius:20px; background:rgba(22,163,106,.18); color:#8AF0BE; font-size:13px; font-weight:650; margin-bottom:10px; }
.hero-title { font-size:clamp(30px,4vw,48px); line-height:1.08; font-weight:850; color:#fff; letter-spacing:-1.4px; margin:0 0 10px; }
.hero-title span { color:#3DDB91; }
.hero-sub { font-size:17px; color:#D5E4F4; max-width:760px; margin:0 0 16px; }
.feature-row { display:flex; flex-wrap:wrap; gap:10px 22px; color:#DDEAF7; font-size:13px; }
.feature-row span:before { content:'✓'; display:inline-block; margin-right:7px; color:#75F0B5; font-weight:800; }
.section-label { font-size:22px; font-weight:750; margin:18px 0 10px; color:#fff; }
.quick-card { border:1px solid #2B5682; border-radius:16px; padding:16px 14px; min-height:112px; background:linear-gradient(145deg,rgba(19,57,96,.94),rgba(11,37,67,.96)); }
.quick-card strong { display:block; color:#fff; font-size:16px; margin-bottom:6px; }
.quick-card small { color:#C9D9E9; line-height:1.45; }
@media (max-width:700px) { .hero-card { padding:22px 18px; } .hero-title { font-size:30px; } }
</style>
""", unsafe_allow_html=True)

SYSTEM_PROMPT = """
Siz SOLIQ PRO AI — O‘zbekiston bo‘yicha professional buxgalteriya, moliya, soliq tahlili
va audit yordamchisisiz. Foydalanuvchiga o‘zbek tilida, aniq va tartibli javob bering.

Qoidalar:
1. Qonun moddasi, soliq stavkasi, muddat yoki imtiyozni ishonchli manbasiz uydirmang.
2. Qonunchilik o‘zgarishi mumkinligini hisobga oling. Zarur bo‘lsa, foydalanuvchidan soliq davri,
   soliq to‘lovchi maqomi, faoliyat turi va tegishli hujjatlarni aniqlashtiring.
3. Huquqiy javoblarda rasmiy manbalarni tekshirishni tavsiya qiling: https://lex.uz/ va
   https://soliq.uz/. Agar aniq manba yoki modda sizda tasdiqlanmagan bo‘lsa, buni ochiq ayting.
4. Hisob-kitobni formula, kiritilgan ma’lumotlar, taxminlar va natija ko‘rinishida ko‘rsating.
5. Buxgalteriya provodkasida debet, kredit, summa va operatsiya mazmunini alohida ko‘rsating.
   Schyot raqamini ishonchli tasdiqlay olmasangiz, uni taxmin qilmang.
6. Auditda aniqlangan holat, ehtimoliy xavf, dalil yetishmasligi va tavsiya etilgan keyingi qadamlarni ajrating.
7. Foydalanuvchining maxfiy ma’lumotlarini keraksiz so‘ramang. Parol, ERI kaliti, API kaliti yoki
   soliq tizimiga kirish tokenlarini chatga yuborishni so‘ramang.
8. Javob oxirida zarur bo‘lsa “Tekshirish kerak” bo‘limini qo‘shing.
9. Bu yordamchi professional tekshiruv o‘rnini bosmaydi; yakuniy soliq hisobotini yuborishdan oldin
   rasmiy manbalar va birlamchi hujjatlar bilan solishtirish kerak.
"""

def local_reply(question: str) -> str:
    q = question.lower().strip()
    if any(x in q for x in ["qqs", "qo‘shilgan qiymat", "qo'shilgan qiymat"]):
        return (
            "**QQS bo‘yicha tahlilni boshlash uchun** quyidagilar kerak:\n\n"
            "1. Soliq davri (oy/chorak va yil)\n"
            "2. Korxona QQS to‘lovchisi ekanligi\n"
            "3. Operatsiya turi: realizatsiya, xarid, import, eksport yoki tuzatish\n"
            "4. Summa QQS bilanmi yoki QQSsizmi\n"
            "5. Birlamchi hujjat turi\n\n"
            "Men hozir internetdagi qonunchilikni avtomatik tekshirmayapman. Amaldagi stavka, chegirma "
            "va muddatlarni **LexUZ yoki Soliq qo‘mitasining rasmiy manbasidan** tasdiqlash kerak. "
            "Ma’lumotlarni bersangiz, hisob-kitob jadvalini tuzib beraman."
        )
    if any(x in q for x in ["foyda solig", "foyda solig‘i", "foyda solig'i"]):
        return (
            "**Foyda solig‘i tahlili uchun** soliq davri, soliq to‘lovchi turi, jami daromadlar, "
            "chegiriladigan xarajatlar, chegirilmaydigan xarajatlar va mavjud imtiyozlar haqida ma’lumot kerak.\n\n"
            "Soddalashtirilgan ishchi tuzilma:\n"
            "- Soliq solinadigan foyda = tegishli qoidalarga muvofiq aniqlangan daromadlar − chegiriladigan xarajatlar ± soliq tuzatishlari\n"
            "- Soliq summasi = soliq bazasi × tegishli davr uchun tasdiqlangan stavka\n\n"
            "Bu umumiy tuzilma; aniq hisob-kitob uchun davrga tegishli qoidalarni tekshirish zarur."
        )
    if any(x in q for x in ["provodka", "debet", "kredit", "buxgalteriya yozuv"]):
        return (
            "**Provodka tuzish uchun** operatsiya mazmuni, hujjat turi, summa, QQS holati, "
            "korxonaning hisob siyosati va qo‘llaniladigan schyotlar rejasini yuboring.\n\n"
            "Natijani quyidagi shaklda beraman: sana | operatsiya | debet | kredit | summa | asoslovchi hujjat | izoh.\n"
            "Schyot raqamlarini tasdiqlash uchun tegishli schyotlar rejasi va hisob siyosati kerak."
        )
    if any(x in q for x in ["audit", "xavf", "tafovut", "tekshir"]):
        return (
            "**Audit tekshiruvi uchun** hujjat yoki operatsiyalar jadvalini shaxsiy ma’lumotlarni yashirgan holda yuboring.\n\n"
            "Tahlil quyidagicha tuziladi:\n"
            "1. Aniqlangan holat\n2. Dalil va hujjat\n3. Ehtimoliy soliq/buxgalteriya xavfi\n"
            "4. Yetishmayotgan ma’lumot\n5. Tavsiya etilgan tuzatish va qayta tekshirish.\n\n"
            "Bu dastlabki tahlil bo‘ladi; xulosa birlamchi hujjatlar va amaldagi me’yorlar bilan tasdiqlanishi kerak."
        )
    return (
        "SOLIQ PRO AI ishga tushdi, ammo hozir **API kaliti ulanmagan**, shuning uchun bu rejimda "
        "faqat boshlang‘ich yo‘riqnoma bera olaman.\n\n"
        "To‘liq AI javoblari uchun OpenAI API kalitini kompyuteringizda muhit o‘zgaruvchisi sifatida "
        "sozlang yoki `.env` faylini mahalliy kompyuterda yarating (bu loyiha `.env` faylini avtomatik o‘qimaydi). "
        "Sozlash bosqichlari README.md faylida bor.\n\n"
        "Savolingizni aniqroq yozing: soliq turi, soliq davri, korxona maqomi va operatsiya ma’lumotlari."
    )

def ask_openai(messages):
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
    input_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for item in messages:
        input_messages.append({"role": item["role"], "content": item["content"]})
    response = client.responses.create(model=model, input=input_messages)
    return response.output_text

st.markdown("""
<div class="hero-card">
  <div class="hero-kicker">O‘ZBEKISTON UCHUN • SOLIQ VA BUXGALTERIYA</div>
  <div class="hero-title">SOLIQ PRO <span>AI</span></div>
  <div class="hero-sub">Soliq, buxgalteriya, moliya va audit bo‘yicha ish jarayonlaringizga yordam beruvchi aqlli yordamchi.</div>
  <div class="feature-row"><span>Tartibli tushuntirishlar</span><span>Amaliy hisob-kitoblar</span><span>Rasmiy manbalarni eslatish</span></div>
</div>
""", unsafe_allow_html=True)

api_key_present = bool(os.environ.get("OPENAI_API_KEY"))
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Ishlash rejimi", "AI ulangan" if api_key_present else "Boshlang‘ich rejim")
with col2:
    st.metric("Til", "O‘zbek")
with col3:
    st.metric("Sana", datetime.now().strftime("%d.%m.%Y"))

st.markdown('<div class="section-label">Tezkor bo‘limlar</div>', unsafe_allow_html=True)
quick1, quick2, quick3, quick4 = st.columns(4)
with quick1:
    st.markdown('<div class="quick-card"><strong>％ QQS</strong><small>QQS bo‘yicha savollar va hisob-kitob tuzilmasi</small></div>', unsafe_allow_html=True)
with quick2:
    st.markdown('<div class="quick-card"><strong>▥ Foyda solig‘i</strong><small>Soliq bazasi va xarajatlarni tahlil qilish</small></div>', unsafe_allow_html=True)
with quick3:
    st.markdown('<div class="quick-card"><strong>▤ Provodkalar</strong><small>Debet, kredit va operatsiya izohi</small></div>', unsafe_allow_html=True)
with quick4:
    st.markdown('<div class="quick-card"><strong>✓ Audit</strong><small>Xavflar va tekshiruv bosqichlari</small></div>', unsafe_allow_html=True)

st.markdown('<div class="section-label">AI bilan maslahat</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🧾 SOLIQ PRO AI")
    st.caption("Soliq va buxgalteriya yordamchisi")
    st.header("Ish bo‘limlari")
    mode = st.selectbox("Yo‘nalishni tanlang", [
        "Umumiy maslahat", "Soliq hisob-kitobi", "Buxgalteriya provodkasi",
        "Soliq auditi", "Moliyaviy tahlil", "Hujjatni tahlil qilish"
    ])
    st.markdown("---")
    st.markdown("**Rasmiy manbalar**")
    st.markdown("- [LexUZ](https://lex.uz/)")
    st.markdown("- [Soliq qo‘mitasi](https://soliq.uz/)")
    st.markdown("- [AI SOLIQ](https://ai.soliq.uz/)")
    st.info("Muhim: amaldagi qonunchilik va stavkalarni rasmiy manbadan tekshiring.")
    st.caption("Bu prototip soliq hisobotini avtomatik yubormaydi va soliq tizimlariga ulanmagan.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Masalan: 2026-yil uchun QQS operatsiyasini tahlil qilib ber...")
if prompt:
    enriched_prompt = f"Tanlangan yo‘nalish: {mode}\nFoydalanuvchi savoli: {prompt}"
    st.session_state.messages.append({"role": "user", "content": enriched_prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Tahlil qilinmoqda..."):
            try:
                if api_key_present:
                    answer = ask_openai(st.session_state.messages)
                else:
                    answer = local_reply(prompt)
                st.markdown(answer)
            except Exception as exc:
                answer = (
                    "AI xizmatiga ulanishda xatolik yuz berdi. API kaliti, internet aloqasi va "
                    "model nomini tekshiring. Texnik tafsilot: " + str(exc)
                )
                st.error(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

if st.session_state.messages:
    if st.button("Suhbatni tozalash"):
        st.session_state.messages = []
        st.rerun()

st.markdown("---")
st.caption("SOLIQ PRO AI — 0.1 prototip. Hozircha rasmiy soliq API bilan integratsiya mavjud emas.")
