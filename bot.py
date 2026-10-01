import os
import requests
import random
import time
from openai import OpenAI

# ===== اطلاعات از Secrets خونده می‌شه =====
TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHANNEL_ID = os.environ["TELEGRAM_CHANNEL_ID"]
EITAA_TOKEN = os.environ["EITAA_TOKEN"]
EITAA_CHANNEL_ID = os.environ["EITAA_CHANNEL_ID"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

TOPICS = [
    "یه جمله انگلیسی درباره زندگی روزمره بنویس",
    "یه جمله انگلیسی درباره کار و شغل بنویس",
    "یه جمله انگلیسی درباره سفر بنویس",
    "یه جمله انگلیسی درباره غذا و رستوران بنویس",
    "یه جمله انگلیسی درباره خرید کردن بنویس",
    "یه جمله انگلیسی درباره خانواده بنویس",
    "یه جمله انگلیسی درباره دوستی بنویس",
    "یه جمله انگلیسی درباره آب و هوا بنویس",
    "یه جمله انگلیسی درباره سلامتی بنویس",
    "یه جمله انگلیسی درباره تحصیل و دانشگاه بنویس",
    "یه جمله انگلیسی درباره تکنولوژی بنویس",
    "یه جمله انگلیسی درباره ورزش بنویس",
]

def generate_lesson():
    topic = random.choice(TOPICS)
    
    prompt = f"""
    {topic}
    
    دقیقاً ۳ جمله کوتاه انگلیسی (حداکثر ۱۰ کلمه) بنویس.
    برای هر جمله، این اطلاعات رو به این فرمت بده:
    
    جمله انگلیسی
    معنی: (ترجمه فارسی)
    
    بعد از ۳ جمله، این بخش رو اضافه کن:
    
    📚 لغات مهم:
    - کلمه انگلیسی: معنی فارسی
    - کلمه انگلیسی: معنی فارسی
    - کلمه انگلیسی: معنی فارسی
    - کلمه انگلیسی: معنی فارسی
    - کلمه انگلیسی: معنی فارسی
    - کلمه انگلیسی: معنی فارسی
    - کلمه انگلیسی: معنی فارسی
    - کلمه انگلیسی: معنی فارسی
    - کلمه انگلیسی: معنی فارسی
    - کلمه انگلیسی: معنی فارسی
    
    فقط این فرمت رو رعایت کن. تلفظ ننویس. توضیح اضافه نده.
    """
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "تو یه معلم زبان انگلیسی هستی که جملات کوتاه روزمره با معنی فارسی آموزش می‌دی. تلفظ ننویس."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content.strip()

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHANNEL_ID, "text": text, "parse_mode": "HTML"}
    r = requests.post(url, json=payload)
    return r.status_code == 200

def send_to_eitaa(text):
    url = f"https://eitaayar.ir/api/{EITAA_TOKEN}/sendMessage"
    params = {"chat_id": EITAA_CHANNEL_ID, "text": text}
    try:
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ خطا در ارسال به ایتا: {e}")
        return False

print("ربات شروع شد...")

while True:
    try:
        lesson = generate_lesson()
        
        if send_to_telegram(lesson):
            print(f"✅ تلگرام: ارسال شد")
        else:
            print(f"❌ تلگرام: خطا")
        
        if send_to_eitaa(lesson):
            print(f"✅ ایتا: ارسال شد")
        else:
            print(f"❌ ایتا: خطا")
        
        time.sleep(900)  # هر 15 دقیقه
        
    except Exception as e:
        print(f"❌ خطا: {e}")
        time.sleep(60)
