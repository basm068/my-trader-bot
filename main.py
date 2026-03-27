import os
import time
import threading
import yfinance as yf
import telebot
import pandas as pd
import pytz
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

# ══════════════════════════════════════════════
# 1. إعداد خادم وهمي لإرضاء منصة ريندر المجانية
# ══════════════════════════════════════════════
app = Flask('')

@app.route('/')
def home():
    return "Phantom Bot is Active and Running!"

def run_web():
    # ريندر يستخدم المنفذ 10000 افتراضياً في الخدمة المجانية
    app.run(host='0.0.0.0', port=10000)

# ══════════════════════════════════════════════
# 2. الإعدادات الأساسية للبوت
# ══════════════════════════════════════════════
API_TOKEN = '8471388372:AAEZGJ4yBL3D22HLK88ZBSKWzgXs3O2z_zQ'
CHAT_ID   = '2271910'
SUPPORT   = '@basm068'

bot = telebot.TeleBot(API_TOKEN)
DIVIDER = "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"

# ══════════════════════════════════════════════
# 3. الدوال الفنية (الأهداف والسيولة)
# ══════════════════════════════════════════════
def get_technical_levels(symbol):
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period="7d", interval="1h")
        if df.empty: return None, None, None
        day_high = df.tail(24)['High'].max()
        two_day_high = df.tail(48)['High'].max()
        weekly_high = df['High'].max()
        return day_high, two_day_high, weekly_high
    except: return None, None, None

def analyze_volume(info):
    cur_vol = info.get('regularMarketVolume', 0)
    avg_vol = info.get('averageVolume', 1)
    if avg_vol == 0: avg_vol = 1
    ratio = cur_vol / avg_vol
    if ratio >= 3.0: return "⚡ سيولة انفجارية"
    elif ratio >= 1.2: return "🔸 سيولة مستقرة"
    else: return "⚠️ ضعف سيولة"

def build_smart_report(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        df1m = stock.history(period='1d', interval='1m')
        if df1m.empty: return "❌ تعذر جلب بيانات السهم حالياً."
        
        price = df1m['Close'].iloc[-1]
        d_high, td_high, w_high = get_technical_levels(symbol)
        
        # حساب النسب
        p1 = ((d_high - price) / price * 100) if d_high else 0
        p2 = ((td_high - price) / price * 100) if td_high else 0
        p3 = ((w_high - price) / price * 100) if w_high else 0
        
        volume_status = analyze_volume(info)
        stop_loss = price * 0.90 

        report = (
            f"🛸 *رادار فانتوم — كشف فرصة ذكية*\n"
            f"{DIVIDER}\n"
            f"🏷 *الرمز:* `#{symbol}`\n"
            f"💰 *السعر الحالي:* `${price:.2f}`\n"
            f"{DIVIDER}\n"
            f"🎯 *الأهداف الفنية (مقاومات السعر):*\n"
            f"1️⃣ **الهدف القريب:** `${d_high:.2f}` (+{p1:.1f}%)\n"
            f"   ⮕ (قمة اليوم اللحظية)\n\n"
            f"2️⃣ **الهدف المتوسط:** `${td_high:.2f}` (+{p2:.1f}%)\n"
            f"   ⮕ (أعلى قمة في آخر 48 ساعة)\n\n"
            f"3️⃣ **هدف الانفجار:** `${w_high:.2f}` (+{p3:.1f}%)\n"
            f"   ⮕ (القمة الأسبوعية الفاصلة)\n"
            f"{DIVIDER}\n"
            f"🌊 *تدفق السيولة:* {volume_status}\n"
            f"🛑 *وقف الخسارة النهائي:* `${stop_loss:.2f}` (-10%)\n"
            f"{DIVIDER}\n"
            f"🔍 *رؤية فانتوم الفنية:*\n"
            f"تم تحديد الأهداف بناءً على قمم حقيقية. اختراق الهدف الأول بسيولة يؤكد التوجه للثاني.\n\n"
            f"🛡️ *بروتوكول حماية المحفظة:*\n"
            f"• الدخول 50% الآن، و50% بعد اختراق الهدف الأول.\n"
            f"{DIVIDER}\n"
            f"🛡 *للدعم:* {SUPPORT}"
        )
        return report
    except Exception as e:
        return f"❌ خطأ في تحليل {symbol}: {str(e)}"

# ══════════════════════════════════════════════
# 4. معالج الرسائل وتشغيل النظام
# ══════════════════════════════════════════════
@bot.message_handler(func=lambda m: True)
def handle_all(message):
    symbol = message.text.strip().upper()
    if len(symbol) <= 5:
        bot.reply_to(message, f"🔍 جاري تحليل `#{symbol}`...")
        report = build_smart_report(symbol)
        bot.send_message(message.chat.id, report, parse_mode='Markdown')

if __name__ == "__main__":
    # تشغيل الخادم الوهمي في مسار منفصل (Thread)
    t = Thread(target=run_web)
    t.daemon = True
    t.start()
    
    print("🛸 فانتوم يعمل الآن على ريندر...")
    bot.infinity_polling()
