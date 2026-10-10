# SOLIQ PRO AI — 0.1 prototip

Mahalliy Windows kompyuterida ishlaydigan O‘zbekiston soliq, buxgalteriya va audit yordamchisining boshlang‘ich versiyasi.

## 1. Kerakli dasturlar

- Windows 10/11
- Python 3.11–3.13 tavsiya etiladi: https://www.python.org/downloads/windows/
- AI rejimi uchun internet va OpenAI API kaliti. API ishlatish alohida haq to‘lanishi mumkin.
- API kalitisiz ham dastur ochiladi, lekin faqat cheklangan boshlang‘ich yo‘riqnoma beradi.

Python o‘rnatayotganda installer ichidagi **Add Python to PATH** belgisini yoqing.

## 2. Ishga tushirish (eng oson usul)

1. ZIP faylni o‘zingiz tanlagan papkaga chiqaring.
2. Shu papkada manzil satriga `cmd` yozib Enter bosing.
3. Quyidagi buyruqlarni birma-bir bajaring:

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Brauzerda odatda `http://localhost:8501` ochiladi. Terminal oynasini dastur ishlayotgan paytda yopmang. To‘xtatish uchun terminalda `Ctrl+C` bosing.

## 3. AI rejimini ulash

OpenAI API kaliti ChatGPT obunasidan alohida hisoblanadi va API xarajatlari yuzaga kelishi mumkin. Kalitni hech qachon chatga, kodga yoki ommaviy faylga joylamang.

Windows CMD oynasida (faqat shu terminal sessiyasi uchun):

```bat
set OPENAI_API_KEY=BU_YERGA_OZINGIZNING_API_KALITINGIZ
set OPENAI_MODEL=gpt-4.1-mini
streamlit run app.py
```

Kalitni buyruq tarixida saqlab qo‘ymaslik uchun imkon qadar Windows’ning xavfsiz muhit o‘zgaruvchisi sozlamalaridan foydalaning. Kalitni boshqa odamga bermang. Model hisobingizda mavjud bo‘lishi kerak.

API kaliti bo‘lmasa, dastur AI modeliga so‘rov yubormaydi. OpenAI API’dan foydalanish uchun hisobingiz va billing sozlamalaringiz talab qilinishi mumkin.

## 4. Muhim cheklovlar

- Bu versiya AI SOLIQ yoki Soliq qo‘mitasi API’iga ulanmagan.
- Hozircha rasmiy qonunchilik bazasini avtomatik yuklamaydi va internetdagi qonunlarni avtomatik tekshirmaydi.
- Soliq stavkalari, muddatlar, imtiyozlar va modda raqamlari yakuniy qaror oldidan LexUZ hamda Soliq qo‘mitasi manbalaridan tekshirilishi kerak.
- Maxfiy soliq hujjatlari, ERI kaliti, parol, token va mijozning shaxsiy ma’lumotlarini yubormang.
- Bu prototip soliq hisobotlarini yubormaydi va soliq organlari tizimlarida amal bajarmaydi.

## 5. Keyingi bosqichlar

1. Foydalaniladigan soliq turlari va ish jarayonlarini aniqlash.
2. Rasmiy hujjatlar kutubxonasini va manba ko‘rsatish funksiyasini qo‘shish.
3. Excel/CSV fayllarini tekshirish.
4. Soliq hisob-kitoblari uchun testlangan formulalar va audit chek-listlari.
5. Ruxsat berilgan API mavjud bo‘lsa, hujjatlashtirilgan usulda integratsiya.
