import os
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="SOLIQ PRO AI", page_icon="🧾", layout="wide", initial_sidebar_state="expanded")

# Xavfsiz tarzda Streamlit Cloud Secrets yoki muhit o‘zgaruvchisidan API kalitini olish
try:
    OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY", ""))
    OPENAI_MODEL = st.secrets.get("OPENAI_MODEL", os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"))
except Exception:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

st.markdown("""
<style>
:root { --navy:#07182D; --panel:#102B4C; --panel2:#16385F; --green:#16A36A; --mint:#72E5B0; --line:#294D75; --text:#F5F8FC; --muted:#B8CBE0; }
.stApp,[data-testid="stAppViewContainer"] { background:radial-gradient(ellipse at 75% 0%,#123B67 0%,#071B33 43%,#051426 100%) !important; color:var(--text) !important; }
[data-testid="stHeader"] { background:rgba(5,20,38,.78) !important; }
[data-testid="stSidebar"],[data-testid="stSidebar"] > div { background:linear-gradient(180deg,#061629,#0D2C4D) !important; border-right:1px solid var(--line); }
.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp p,.stApp label,.stApp li,.stApp [data-testid="stMetricLabel"],.stApp [data-testid="stMetricValue"],.stApp [data-testid="stCaptionContainer"] { color:var(--text) !important; }
.stApp h1 { font-weight:850 !important; letter-spacing:-1px; }
[data-testid="stMetric"],[data-testid="stExpander"] { background:linear-gradient(145deg,rgba(22,56,95,.96),rgba(10,35,62,.96)) !important; border:1px solid var(--line) !important; border-radius:16px !important; padding:12px; }
/* Chat xabarlari: yumaloq, o‘qilishi oson kartochkalar */
[data-testid="stChatMessage"] { background:linear-gradient(145deg,rgba(19,52,88,.96),rgba(10,31,55,.96)) !important; border:1px solid #2B5682 !important; border-radius:18px !important; padding:16px 18px !important; margin:12px 0 !important; box-shadow:0 8px 22px rgba(0,0,0,.12); }
[data-testid="stChatMessage"] p { line-height:1.7 !important; }
[data-testid="stChatMessage"] code { color:#D9FFE9 !important; background:#09213A !important; border-radius:5px; padding:2px 5px; }
[data-testid="stChatMessage"] a { color:#83F0BA !important; }
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] ul,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] ol { padding-left:1.4rem; }
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] table { width:100%; }
/* Chat yozish maydoni */
[data-testid="stChatInput"] { background:rgba(16,43,76,.98) !important; border:1px solid #3B6793 !important; border-radius:17px !important; padding:6px !important; box-shadow:0 8px 24px rgba(0,0,0,.15); }
[data-testid="stChatInput"] textarea { background:#F4F8FC !important; color:#10233D !important; border-radius:12px !important; min-height:54px !important; }
[data-testid="stChatInput"] button { background:linear-gradient(135deg,#16A36A,#0D8658) !important; border-radius:11px !important; }
/* Tezkor savollar uchun qulay tugmalar */
.stButton > button { white-space:normal !important; line-height:1.35 !important; }
.stSpinner > div { border-top-color:#72E5B0 !important; }
[data-testid="stMetricValue"] { font-weight:800 !important; }
.stButton > button,[data-testid="stFormSubmitButton"] > button { background:linear-gradient(135deg,#16A36A,#0D8658) !important; color:#fff !important; border:1px solid #28BD81 !important; border-radius:11px !important; font-weight:700 !important; min-height:42px; transition:all .18s ease; }
.stButton > button:hover,[data-testid="stFormSubmitButton"] > button:hover { background:#128455 !important; border-color:#75F0B5 !important; transform:translateY(-1px); }
.stTextInput input,.stTextArea textarea,[data-testid="stChatInput"] textarea { background:#F4F8FC !important; color:#10233D !important; border:1px solid #B7C9DD !important; border-radius:11px !important; }
[data-testid="stSelectbox"] div[data-baseweb="select"] { background:#F4F8FC !important; color:#10233D !important; border-radius:10px !important; }
[data-testid="stChatInput"] { border-color:#294D75 !important; }
.stApp a { color:#72E5B0 !important; font-weight:600; }
hr { border-color:var(--line) !important; }
div[data-testid="stAlert"] { border-radius:13px !important; }
.hero { padding:28px 30px; border:1px solid #2A5683; border-radius:23px; background:linear-gradient(115deg,rgba(18,58,99,.98),rgba(7,27,51,.94)); margin:4px 0 18px; box-shadow:0 16px 42px rgba(0,0,0,.18); }
.kicker { display:inline-block; padding:6px 12px; border-radius:30px; background:rgba(22,163,106,.18); color:#8AF0BE; font-size:12px; font-weight:750; letter-spacing:.4px; margin-bottom:12px; }
.hero-title { font-size:clamp(32px,4vw,49px); line-height:1.08; font-weight:900; color:#fff; letter-spacing:-1.5px; margin:0 0 10px; }
.hero-title span { color:#3DDB91; }
.hero-sub { font-size:17px; color:#D5E4F4; max-width:800px; margin:0 0 18px; }
.feature-row { display:flex; flex-wrap:wrap; gap:10px 22px; color:#DDEAF7; font-size:13px; }
.feature-row span:before { content:'✓'; display:inline-flex; align-items:center; justify-content:center; width:19px; height:19px; border-radius:50%; background:#087E58; color:#B8FFD9; margin-right:7px; font-weight:900; }
.section-title { font-size:22px; font-weight:800; margin:20px 0 10px; color:#fff; }
.quick-card { border:1px solid #2B5682; border-radius:17px; padding:16px 15px 14px; min-height:118px; background:linear-gradient(145deg,rgba(19,57,96,.97),rgba(11,37,67,.97)); }
.quick-card .icon { font-size:25px; margin-bottom:8px; }
.quick-card strong { display:block; color:#fff; font-size:16px; margin-bottom:6px; }
.quick-card small { color:#C9D9E9; line-height:1.45; font-size:12px; }
.chat-panel { padding:16px 18px; border:1px solid #2B5682; border-radius:18px; background:rgba(12,39,69,.6); margin:4px 0 12px; }
.status-dot { display:inline-block; width:9px; height:9px; border-radius:50%; background:#22D58A; margin-right:7px; }
.side-brand { font-size:22px; font-weight:850; letter-spacing:-.5px; }
.side-brand span { color:#3DDB91; }
.side-sub { color:#B8CBE0; font-size:12px; margin-top:-5px; }
.footer-note { color:#AFC3D9; font-size:12px; }
@media (max-width:750px) { .hero {padding:22px 18px;} .hero-title {font-size:31px;} .hero-sub {font-size:15px;} }
</style>
""", unsafe_allow_html=True)

SYSTEM_PROMPT = """
Siz SOLIQ PRO AI — O‘zbekiston bo‘yicha buxgalteriya, moliya, soliq tahlili va audit yordamchisisiz. Foydalanuvchiga o‘zbek tilida, aniq va tartibli javob bering.
Qoidalar:
1. Qonun moddasi, soliq stavkasi, muddat yoki imtiyozni ishonchli manbasiz uydirmang.
2. Qonunchilik o‘zgarishi mumkin. Zarur bo‘lsa soliq davri, soliq to‘lovchi maqomi, faoliyat turi va tegishli hujjatlarni aniqlashtiring.
3. Rasmiy manbalarni tavsiya qiling: https://lex.uz/ va https://soliq.uz/. Tasdiqlanmagan modda yoki manbani tasdiqlangandek ko‘rsatmang.
4. Hisob-kitobni formula, kiritilgan ma’lumotlar, taxminlar va natija ko‘rinishida bering.
5. Provodkada debet, kredit, summa va operatsiya mazmunini alohida ko‘rsating. Schyot raqamini bilmasangiz taxmin qilmang.
6. Auditda holat, dalil, ehtimoliy xavf, yetishmayotgan ma’lumot va keyingi qadamlarni ajrating.
7. Parol, ERI kaliti, API kaliti yoki soliq tizimi tokenlarini chatga yuborishni so‘ramang.
8. Zarur bo‘lsa “Tekshirish kerak” bo‘limini qo‘shing.
9. Yordamchi professional tekshiruv o‘rnini bosmaydi; yakuniy hisobotdan oldin rasmiy manbalar va birlamchi hujjatlar bilan solishtiring.
"""

MODE_PROMPTS = {
    "Umumiy maslahat": "Savolga umumiy va tushunarli javob bering.",
    "QQS hisob-kitobi": "QQS bo‘yicha davr, to‘lovchi maqomi, operatsiya turi va summa QQS bilan yoki QQSsiz ekanini aniqlang. Stavkani taxmin qilmang.",
    "Foyda solig‘i": "Daromad, chegiriladigan xarajatlar, soliq tuzatishlari va davrni ajrating. Tasdiqlanmagan stavkani ishlatmang.",
    "Buxgalteriya provodkasi": "Operatsiya, debet, kredit, summa, hujjat va izoh ustunlari bilan javob bering. Schyot raqamini taxmin qilmang.",
    "Soliq auditi": "Aniqlangan holat, dalil, xavf, yetishmayotgan ma’lumot va tavsiyani alohida bering.",
    "Moliyaviy tahlil": "Ko‘rsatkichlar, formulalar, davrlar va taxminlarni aniq ajrating.",
    "Hujjatni tahlil qilish": "Faqat berilgan matn yoki ma’lumotlarga tayaning; ko‘rinmayotgan faktlarni o‘ylab topmang. Maxfiy ma’lumotlarni yashirishni eslating."
}

def local_reply(question: str, mode: str) -> str:
    q = question.lower().strip()
    if mode == "QQS hisob-kitobi" or any(x in q for x in ["qqs", "qo‘shilgan qiymat", "qo'shilgan qiymat"]):
        return ("**QQS bo‘yicha tahlil**\n\nKerakli ma’lumotlar:\n1. Soliq davri (oy/chorak va yil)\n2. Korxonaning QQS to‘lovchisi maqomi\n3. Operatsiya turi: realizatsiya, xarid, import, eksport yoki tuzatish\n4. Summa QQS bilanmi yoki QQSsizmi\n5. Birlamchi hujjat turi\n\nMen bu rejimda qonunchilikni internetdan avtomatik tekshirmayman. Amaldagi stavka, chegirma va muddatlarni [LexUZ](https://lex.uz/) yoki [Soliq qo‘mitasi](https://soliq.uz/) manbasidan tasdiqlang.")
    if mode == "Foyda solig‘i" or any(x in q for x in ["foyda solig", "foyda solig‘i", "foyda solig'i"]):
        return ("**Foyda solig‘i tahlili**\n\nQuyidagilarni kiriting: soliq davri, korxona turi, jami daromad, chegiriladigan xarajatlar, chegirilmaydigan xarajatlar va imtiyozlar.\n\n- Ishchi soliq bazasi = tegishli qoidalarga muvofiq daromad − chegiriladigan xarajatlar ± soliq tuzatishlari\n- Soliq summasi = soliq bazasi × tegishli davr uchun tasdiqlangan stavka\n\nBu umumiy tuzilma; aniq hisob uchun davrga tegishli qoidalarni tekshirish zarur.")
    if mode == "Buxgalteriya provodkasi" or any(x in q for x in ["provodka", "debet", "kredit", "buxgalteriya yozuv"]):
        return ("**Provodka tayyorlash**\n\nOperatsiya mazmuni, sana, summa, QQS holati, hujjat turi va hisob siyosatini yuboring.\n\nNatija: sana | operatsiya | debet | kredit | summa | asoslovchi hujjat | izoh.\n\nSchyot raqamlarini tasdiqlash uchun tegishli schyotlar rejasi va hisob siyosati kerak.")
    if mode == "Soliq auditi" or any(x in q for x in ["audit", "xavf", "tafovut", "tekshir"]):
        return ("**Dastlabki audit tahlili**\n\nHujjat yoki operatsiyalar jadvalini shaxsiy ma’lumotlarni yashirgan holda yuboring. Tahlilni quyidagicha tuzaman:\n1. Aniqlangan holat\n2. Dalil va hujjat\n3. Ehtimoliy soliq/buxgalteriya xavfi\n4. Yetishmayotgan ma’lumot\n5. Tavsiya etilgan tuzatish va qayta tekshirish.\n\nXulosa birlamchi hujjatlar va amaldagi me’yorlar bilan tasdiqlanishi kerak.")
    return ("**SOLIQ PRO AI boshlang‘ich rejimda ishlayapti.** OpenAI API kaliti sozlanmagani uchun to‘liq AI javoblari hozircha mavjud emas.\n\nSavolingizga aniqroq javob berishim uchun soliq turi, davr, korxona maqomi va operatsiya ma’lumotlarini yozing. Amaldagi qonunchilikni [LexUZ](https://lex.uz/) va [Soliq qo‘mitasi](https://soliq.uz/) orqali tekshiring.")

def ask_openai(messages, mode):
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT + "\n\nTanlangan ish bo‘limi: " + mode + "\n" + MODE_PROMPTS.get(mode, "")}]
    for item in messages:
        api_messages.append({"role": item["role"], "content": item["content"]})
    response = client.responses.create(model=OPENAI_MODEL, input=api_messages)
    return response.output_text

# Sidebar: navigation and official resources
with st.sidebar:
    st.markdown('<div class="side-brand">🧾 SOLIQ PRO <span>AI</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="side-sub">Soliq va buxgalteriya yordamchisi</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🧭 Ish bo‘limlari")
    section = st.radio("Bo‘limni tanlang", ["Bosh sahifa", "Yangi maslahat", "QQS hisob-kitobi", "Foyda solig‘i", "Buxgalteriya provodkasi", "Soliq auditi", "Moliyaviy tahlil", "Hujjatni tahlil qilish"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### 🌐 Rasmiy manbalar")
    st.markdown("- [LexUZ — qonunchilik](https://lex.uz/)\n- [Soliq qo‘mitasi](https://soliq.uz/)\n- [AI SOLIQ](https://ai.soliq.uz/)")
    st.info("Muhim: amaldagi qonunchilik va stavkalarni rasmiy manbadan tekshiring.")
    st.caption("Prototip soliq hisobotini avtomatik yubormaydi va soliq tizimlariga ulanmagan.")

mode_map = {
    "Bosh sahifa": "Umumiy maslahat", "Yangi maslahat": "Umumiy maslahat",
    "QQS hisob-kitobi": "QQS hisob-kitobi", "Foyda solig‘i": "Foyda solig‘i",
    "Buxgalteriya provodkasi": "Buxgalteriya provodkasi", "Soliq auditi": "Soliq auditi",
    "Moliyaviy tahlil": "Moliyaviy tahlil", "Hujjatni tahlil qilish": "Hujjatni tahlil qilish"
}
mode = mode_map[section]

st.markdown("""
<div class="hero">
  <div class="kicker">O‘ZBEKISTON UCHUN · SOLIQ VA BUXGALTERIYA</div>
  <div class="hero-title">SOLIQ PRO <span>AI</span></div>
  <div class="hero-sub">Soliq, buxgalteriya, moliya va audit bo‘yicha kundalik ishlaringiz uchun aqlli yordamchi.</div>
  <div class="feature-row"><span>Tartibli tushuntirishlar</span><span>Amaliy hisob-kitoblar</span><span>Rasmiy manbalarni eslatish</span></div>
</div>
""", unsafe_allow_html=True)

api_key_present = bool(OPENAI_API_KEY)
c1, c2, c3 = st.columns(3)
with c1: st.metric("Ishlash rejimi", "AI ulangan" if api_key_present else "Boshlang‘ich rejim")
with c2: st.metric("Til", "O‘zbek")
with c3: st.metric("Bugungi sana", datetime.now().strftime("%d.%m.%Y"))

st.markdown('<div class="section-title">⚡ Tezkor bo‘limlar</div>', unsafe_allow_html=True)
card_cols = st.columns(4)
cards = [
    ("🧮", "QQS", "QQS operatsiyalari va hisob-kitob", "QQS hisob-kitobi"),
    ("📊", "Foyda solig‘i", "Soliq bazasi va xarajatlar tahlili", "Foyda solig‘i"),
    ("📘", "Provodkalar", "Debet, kredit va operatsiya izohi", "Buxgalteriya provodkasi"),
    ("🛡️", "Audit", "Xavflar va tekshiruv bosqichlari", "Soliq auditi"),
]
for col, (icon, title, desc, target) in zip(card_cols, cards):
    with col:
        st.markdown(f'<div class="quick-card"><div class="icon">{icon}</div><strong>{title}</strong><small>{desc}</small></div>', unsafe_allow_html=True)
        if st.button("Bo‘limni ochish →", key="go_" + target, use_container_width=True):
            st.session_state["active_mode"] = mode_map[target]
            st.rerun()

# Shortcut kartochkasi tanlansa, tanlangan ish rejimini saqlash
if "active_mode" not in st.session_state:
    st.session_state["active_mode"] = mode
elif section != "Bosh sahifa" and mode != st.session_state["active_mode"]:
    st.session_state["active_mode"] = mode
mode = st.session_state["active_mode"]

st.markdown('<div class="section-title">💬 AI bilan maslahat</div>', unsafe_allow_html=True)
st.markdown(f'<div class="chat-panel"><b>🧾 SOLIQ PRO AI</b> &nbsp; <span class="status-dot"></span><span style="color:#72E5B0">{"AI ulangan" if api_key_present else "Boshlang‘ich rejim"}</span><br><span style="color:#B8CBE0;font-size:13px">Joriy bo‘lim: {mode}</span></div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.markdown("""
    <div style="padding:18px 20px;border:1px solid #2B5682;border-radius:18px;background:linear-gradient(120deg,rgba(20,61,102,.92),rgba(8,31,55,.96));margin:8px 0 14px;">
      <div style="font-size:20px;font-weight:800;color:#FFFFFF;margin-bottom:6px;">Assalomu alaykum! 👋</div>
      <div style="color:#D5E4F4;line-height:1.65;">Men SOLIQ PRO AI yordamchisiman. Quyidagi tezkor savollardan birini tanlang yoki o‘z savolingizni yozing.</div>
      <div style="color:#8AF0BE;font-size:12px;margin-top:10px;">Maslahat: soliq davri va operatsiya tafsilotlarini yozsangiz, javob aniqroq bo‘ladi. Maxfiy ma’lumotlarni yubormang.</div>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

suggestions = st.columns(4)
suggestion_texts = ["QQS bo‘yicha nimalar kerak?", "Foyda solig‘i bazasini tushuntir", "Provodka tuzish uchun ma’lumotlar", "Audit xavflarini qanday ko‘raman?"]
for col, suggestion in zip(suggestions, suggestion_texts):
    with col:
        if st.button(suggestion, key="suggest_" + str(suggestion), use_container_width=True):
            st.session_state["pending_prompt"] = suggestion
            st.rerun()

prompt = st.chat_input("Soliq, buxgalteriya yoki audit bo‘yicha savolingizni yozing...")
if st.session_state.get("pending_prompt"):
    prompt = st.session_state.pop("pending_prompt")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Javob tayyorlanmoqda..."):
            try:
                if api_key_present:
                    answer = ask_openai(st.session_state.messages, mode)
                else:
                    answer = local_reply(prompt, mode)
                st.markdown(answer)
            except Exception:
                answer = ("AI xizmatiga ulanishda muammo yuz berdi. Streamlit Cloud → Settings → Secrets bo‘limida `OPENAI_API_KEY` sozlamasini tekshiring. API kalitini chatga yoki GitHub kodiga yozmang.")
                st.error(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

b1, b2 = st.columns([1, 4])
with b1:
    if st.button("🗑️ Suhbatni tozalash", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
with b2:
    st.markdown('<div class="footer-note">SOLIQ PRO AI — prototip. Natijalarni rasmiy manbalar va birlamchi hujjatlar bilan tekshiring. Rasmiy soliq API integratsiyasi mavjud emas.</div>', unsafe_allow_html=True)
