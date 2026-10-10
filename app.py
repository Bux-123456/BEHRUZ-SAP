import os
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="SOLIQ PRO AI", page_icon="🧾", layout="wide")


# SOLIQ PRO AI dizayni: to‘q ko‘k fon, oq matn va yashil tugmalar
st.markdown("""
<style>
/* Asosiy ilova va kontent foni */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"] {
    background-color: #142B4A !important;
    color: #FFFFFF !important;
}

/* Yon menyu */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background-color: #10233D !important;
}

/* Matnlar */
.stApp h1, .stApp h2, .stApp h3,
.stApp p, .stApp label, .stApp [data-testid="stMetricLabel"],
.stApp [data-testid="stMetricValue"], .stApp [data-testid="stCaptionContainer"] {
    color: #FFFFFF !important;
}

/* Chat xabarlari va kartochkalar */
[data-testid="stChatMessage"],
[data-testid="stMetric"],
[data-testid="stExpander"] {
    background-color: #1C385B !important;
    border: 1px solid #355477 !important;
    border-radius: 12px !important;
}

/* Asosiy tugmalar */
.stButton > button,
[data-testid="stFormSubmitButton"] > button {
    background-color: #16A36A !important;
    color: #FFFFFF !important;
    border: 1px solid #16A36A !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
}
.stButton > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {
    background-color: #128455 !important;
    border-color: #128455 !important;
}

/* Matn kiritish maydonlari */
.stTextInput input, .stTextArea textarea,
[data-testid="stChatInput"] textarea {
    background-color: #FFFFFF !important;
    color: #142B4A !important;
    border-radius: 8px !important;
}

/* Selectbox */
[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    color: #142B4A !important;
    border-radius: 8px !important;
}

/* Havolalar */
.stApp a { color: #70E0AD !important; }
hr { border-color: #355477 !important; }
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

st.title("🧾 SOLIQ PRO AI")
st.caption("Mahalliy kompyuteringizda ishlaydigan dastlabki prototip · O‘zbekiston soliq va buxgalteriya yordamchisi")

api_key_present = bool(os.environ.get("OPENAI_API_KEY"))
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Ishlash rejimi", "AI ulangan" if api_key_present else "Boshlang‘ich rejim")
with col2:
    st.metric("Til", "O‘zbek")
with col3:
    st.metric("Sana", datetime.now().strftime("%d.%m.%Y"))

with st.sidebar:
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
