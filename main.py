import os
import telebot
import yfinance as yf
from telebot import types
import time

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")

bot = telebot.TeleBot(TOKEN)

def get_short_data(ticker):
    try:
        stock = yf.Ticker(ticker, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        # Force fetching info with a delay-friendly approach
        info = stock.info
        if not info or 'currentPrice' not in info:
            return 0, 0, 0, "⚠️ رمز غير صحيح أو بيانات محجوبة"
            
        price = info.get('currentPrice') or info.get('regularMarketPreviousClose') or 0
        s_qty = info.get('shortInterest', 0)
        s_pct = (info.get('shortPercentOfFloat', 0) or 0) * 100
        status = "✅ طبيعي" if s_pct < 15 else "⚠️ ضغط عالي"
        return s_qty, s_pct, price, status
    except Exception as e:
        return 0, 0, 0, f"❌ خطأ: {str(e)}"

@bot.message_handler(func=lambda message: True)
def phantom_radar(message):
    # تحويل النص لحروف كبيرة وإزالة أي مسافات أو رموز
    ticker = message.text.upper().strip().replace('#', '')
    
    if not ticker:
        bot.reply_to(message, "📝 الرجاء إدخال رمز السهم (مثال: AAPL)")
        return
    
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