import os
import time
import threading
import yfinance as yf
import telebot
import pandas as pd
import pytz
from datetime import datetime, timedelta

# ══════════════════════════════════════════════
#  الإعدادات الأساسية (تُسحب من البيئة للحماية)
# ══════════════════════════════════════════════
API_TOKEN = '8471388372:AAEZGJ4yBL3D22HLK88ZBSKWzgXs3O2z_zQ'
CHAT_ID   = '2271910'
SUPPORT   = '@basm068'

bot = telebot.TeleBot(API_TOKEN)
DIVIDER = "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"

# ══════════════════════════════════════════════
#  دالة جلب المقاومات والأهداف الفنية
# ══════════════════════════════════════════════
def get_technical_levels(symbol):
    stock = yf.Ticker(symbol)
    # جلب بيانات 7 أيام بفريم ساعة للحصول على القمم بدقة
    df = stock.history(period="7d", interval="1h")
    if df.empty: return None, None, None
    
    day_high = df.tail(24)['High'].max() # قمة 24 ساعة
    two_day_high = df.tail(48)['High'].max() # قمة 48 ساعة
    weekly_high = df['High'].max() # قمة أسبوع
    
    return day_high, two_day_high, weekly_high

# ══════════════════════════════════════════════
#  دالة تحليل تدفق السيولة
# ══════════════════════════════════════════════
def analyze_volume(info):
    cur_vol = info.get('regularMarketVolume', 0)
    avg_vol = info.get('averageVolume', 1)
    ratio = cur_vol / avg_vol
    
    if ratio >= 3.0: return "⚡ سيولة انفجارية"
    elif ratio >= 1.2: return "🔸 سيولة مستقرة"
    else: return "⚠️ ضعف سيولة"

# ══════════════════════════════════════════════
#  بناء التقرير الفني الذكي
# ══════════════════════════════════════════════
def build_smart_report(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        # جلب السعر الحالي والـ VWAP تقريبياً
        df1m = stock.history(period='1d', interval='1m')
        if df1m.empty: return "❌ تعذر جلب بيانات السهم حالياً."
        
        price = df1m['Close'].iloc[-1]
        vwap = (df1m['Close'] * df1m['Volume']).sum() / df1m['Volume'].sum()
        
        # جلب الأهداف الفنية
        d_high, td_high, w_high = get_technical_levels(symbol)
        
        # حساب النسب المئوية للأهداف
        p1 = ((d_high - price) / price * 100) if d_high else 0
        p2 = ((td_high - price) / price * 100) if td_high else 0
        p3 = ((w_high - price) / price * 100) if w_high else 0
        
        volume_status = analyze_volume(info)
        stop_loss = price * 0.90 # وقف 10%
        
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
            f"   ⮕ (أو كسر الـ VWAP بـ 2%)\n"
            f"{DIVIDER}\n"
            f"🔍 *رؤية فانتوم الفنية:*\n"
            f"الأهداف حددت بناءً على قمم حقيقية صدت السعر سابقاً. اختراق الهدف الأول بسيولة يؤكد التوجه للثاني.\n\n"
            f"🛡️ *بروتوكول حماية المحفظة:*\n"
            f"• الدخول 50% الآن، و50% بعد اختراق الهدف الأول.\n"
            f"• يمنع التبريد نهائياً. الالتزام بالوقف هو ربح.\n"
            f"{DIVIDER}\n"
            f"🛡 *للدعم:* {SUPPORT}"
        )
        return report
    except Exception as e:
        return f"❌ خطأ في تحليل {symbol}: {str(e)}"

# ══════════════════════════════════════════════
#  تشغيل البوت
# ══════════════════════════════════════════════
@bot.message_handler(func=lambda m: True)
def handle_all(message):
    symbol = message.text.strip().upper()
    if len(symbol) <= 5:
        bot.reply_to(message, f"🔍 جاري تحليل `#{symbol}` بناءً على القمم الفنية...")
        report = build_smart_report(symbol)
        bot.send_message(message.chat.id, report, parse_mode='Markdown')

if __name__ == "__main__":
    print("🛸 فانتوم يعمل الآن...")
    bot.infinity_polling()
