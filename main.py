import telebot
import yfinance as yf
from telebot import types

# توكن البوت الخاص بك
TOKEN = '8471388372:AAEZGJ4yBL3D22HLK88ZBSKWzgXs3O2z_zQ'
bot = telebot.TeleBot(TOKEN)

def get_full_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        short_shares = info.get('shortInterest', 0)
        short_pct = info.get('shortPercentOfFloat', 0) * 100
        price = info.get('currentPrice', 0)
        vol = info.get('volume', 0)
        avg_vol = info.get('averageVolume', 1)
        return short_shares, short_pct, price, vol, avg_vol
    except: return 0, 0, 0, 0, 1

@bot.message_handler(func=lambda message: True)
def phantom_radar(message):
    ticker = message.text.upper().replace('#', '')
    s_qty, s_pct, price, vol, avg_vol = get_full_data(ticker)
    
    # إعادة الأزرار (بشكل شفاف وأنيق لا يعلق)
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🚀 صيد السيولة", callback_data="liq")
    btn2 = types.InlineKeyboardButton("🕋 الأسهم النقية", callback_data="halal")
    btn3 = types.InlineKeyboardButton("🛡️ الدعم: @basm068_", url="https://t.me/basm068_")
    markup.add(btn1, btn2, btn3)

    # تنسيق "رادار فانتوم" الفخم
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
💧 **قوة السيولة:** {round(vol/avg_vol, 1)}x
   📊 حجم اليوم: {vol:,}
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
📡 **حالة الرادار:**
{"⚠️ سهم ثقيل جداً (اختراق وهمي محتمل)" if s_pct > 15 else "✅ السهم خفيف وجاهز للانفجار"}
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
🛡 للدعم والعضوية: @basm068_
    """
    bot.reply_to(message, report, reply_markup=markup)

bot.polling()
