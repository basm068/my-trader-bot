import os
import telebot
import yfinance as yf
from telebot import types

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")

bot = telebot.TeleBot(TOKEN)

def get_short_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        # جلب البيانات مع التأكد من وجودها
        s_qty = info.get('shortInterest', 0)
        s_pct = info.get('shortPercentOfFloat', 0) * 100
        price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        
        status = "✅ ضغط طبيعي"
        if s_pct > 15: status = "⚠️ سهم ثقيل (شورت عالي)"
        if s_pct > 25: status = "🚨 خطر: سيطرة شورت كاملة"
        
        return s_qty, s_pct, price, status
    except:
        return 0, 0, 0, "بيانات غير متوفرة"

@bot.message_handler(func=lambda message: True)
def phantom_radar(message):
    # تحويل النص لحروف كبيرة وإزالة أي مسافات أو رموز
    ticker = message.text.upper().strip().replace('#', '')
    s_qty, s_pct, price, status = get_short_data(ticker)
    
    markup_remove = types.ReplyKeyboardRemove()
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🚀 صيد السيولة", callback_data="liq")
    btn2 = types.InlineKeyboardButton("🕋 الأسهم النقية", callback_data="halal")
    btn3 = types.InlineKeyboardButton("🛡️ الدعم: @basm068", url="https://t.me/basm068")
    markup.add(btn1, btn2, btn3)

    report = f"""
🛸 **رادار فانتوم — الكشف اللحظي**
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
🏷 الرمز: #{ticker}
💰 السعر الحي: ${price}
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
📊 **إحصائيات الشورت (ثقل السهم):**
• إجمالي أسهم الشورت: {s_qty:,} سهم
• نسبة الضغط: {s_pct:.2f}%
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
📡 **حالة الرادار:**
{status}
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
🛡 للدعم: @basm068
    """
    bot.reply_to(message, report, reply_markup=markup_remove)
    bot.send_message(message.chat.id, "خيارات التحكم:", reply_markup=markup)

if __name__ == "__main__":
    bot.polling(none_stop=True)