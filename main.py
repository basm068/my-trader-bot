import telebot
import yfinance as yf
from telebot import types

# توكن البوت في سطر واحد
TOKEN = '8471388372:AAEZGJ4yBL3D22HLK88ZBSKWzgXs3O2z_zQ'
bot = telebot.TeleBot(TOKEN)

def get_short_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        short_shares = info.get('shortInterest', 0)
        short_pct = info.get('shortPercentOfFloat', 0) * 100
        price = info.get('currentPrice', 0)
        
        status = "✅ ضغط طبيعي"
        if short_pct > 15: status = "⚠️ سهم ثقيل (شورت عالي)"
        if short_pct > 25: status = "🚨 خطر: سيطرة شورت كاملة"
        
        return short_shares, short_pct, price, status
    except:
        return 0, 0, 0, "بيانات غير متوفرة"

@bot.message_handler(func=lambda message: True)
def phantom_radar(message):
    ticker = message.text.upper().replace('#', '')
    s_qty, s_pct, price, status = get_short_data(ticker)
    
    # مسح الأزرار القديمة قسرياً
    markup_remove = types.ReplyKeyboardRemove()
    
    # الأزرار الجديدة الأنيقة
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
