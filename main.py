import telebot
import yfinance as yf
from telebot import types

# التوكن الخاص بك
TOKEN = '8471388372:AAEZGJ4yBL3D22HLK88ZBSKWzgXs3O2z_zQ'
bot = telebot.TeleBot(TOKEN)

def get_short_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        # جلب أرقام الشورت الفعلية
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
    
    # مسح الأزرار القديمة (التي في صورتك الأولى) نهائياً
    markup_remove = types.ReplyKeyboardRemove()
    
    # أزرار التحكم الجديدة (شفافة وأنيقة)
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
    # إرسال التقرير مع مسح الأزرار القديمة
    bot.reply_to(message, report, reply_markup=markup_remove)
    # إرسال الأزرار الجديدة
    bot.send_message(message.chat.id, "خيارات الرادار:", reply_markup=markup)

bot.polling()
