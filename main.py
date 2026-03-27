import telebot
import yfinance as yf
from telebot import types

# توكن البوت الخاص بك (تم وضعه بنجاح)
TOKEN = '8471388372:AAEZGJ4yBL3D22HLK88ZBSKWzgXs3O2z_zQ'
bot = telebot.TeleBot(TOKEN)

def get_short_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        # سحب الأرقام الفعلية للشورت
        short_shares = info.get('shortInterest', 0)
        short_ratio = info.get('shortPercentOfFloat', 0) * 100
        
        status = "✅ ضغط طبيعي"
        if short_ratio > 15: status = "⚠️ سهم ثقيل (شورت عالي)"
        if short_ratio > 25: status = "🚨 خطر: سيطرة شورت كاملة"
        
        return short_shares, short_ratio, status
    except:
        return 0, 0, "بيانات غير متوفرة حالياً"

@bot.message_handler(func=lambda message: True)
def analyze(message):
    ticker = message.text.upper().replace('#', '')
    short_qty, short_pct, status = get_short_data(ticker)
    
    # مسح الأزرار الأربعة القديمة (التي في صورتك) نهائياً من شاشتك
    markup_remove = types.ReplyKeyboardRemove()
    
    # لوحة التحكم الشفافة الجديدة (Inline)
    inline_markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("🛡️ الدعم والمشاركة: @basm068_", url="https://t.me/basm068_")
    inline_markup.add(btn)

    report = f"""
🛸 **رادار فانتوم — تحديث الشورت والسيولة**
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
🏷 الرمز: #{ticker}

📊 **إحصائيات الشورت (الضغط البيعي):**
• إجمالي أسهم الشورت: {short_qty:,} سهم
• نسبة الشورت من الفلوت: {short_pct:.2f}%
• حالة الضغط: {status}

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
⚠️ **ملاحظة الاستراتيجية:**
إذا كان عدد أسهم الشورت ضخماً، فهذا يعني أن المضارب يضغط السهم بيعياً ليمنع الارتفاع. كلما نقص هذا العدد مع دخول سيولة، كانت فرصة الانفجار أقوى.
    """
    
    # إرسال التقرير ومسح الأزرار القديمة
    bot.reply_to(message, report, reply_markup=markup_remove)
    # إرسال لوحة التحكم الجديدة أسفل الرسالة
    bot.send_message(message.chat.id, "خيارات التحكم:", reply_markup=inline_markup)

bot.polling()
