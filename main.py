import telebot
import yfinance as yf
from telebot import types

TOKEN = 'TOKEN_BOT_HERE' # ضع توكن بوتك هنا
bot = telebot.TeleBot(TOKEN)

def get_short_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        # سحب بيانات الشورت الفعلية
        short_shares = stock.info.get('shortInterest', 0)
        short_pct = stock.info.get('shortPercentOfFloat', 0) * 100
        return short_shares, short_pct
    except:
        return 0, 0

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    ticker = message.text.upper().replace('#', '')
    short_qty, short_pct = get_short_data(ticker)
    
    # مسح الأزرار القديمة (التي في صورتك) واستبدالها بالجديدة
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("🛡️ الدعم", url="https://t.me/basm068_")
    markup.add(btn)

    response = f"📊 **إحصائيات الشورت (#{ticker}):**\n"
    response += f"• إجمالي أسهم الشورت: {short_qty:,}\n"
    response += f"• نسبة الشورت: {short_pct:.2f}%\n"
    response += "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
    response += "⚠️ ملاحظة: إذا كان العدد ضخماً، فالسهم ثقيل في الصعود."
    
    # إرسال التقرير مع مسح الكيبورد القديم قسرياً
    bot.reply_to(message, response, reply_markup=markup)

bot.polling()
