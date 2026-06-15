import os
import telebot
import yfinance as yf

# سحب رمز البوت بشكل آمن من إعدادات ريندر
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

def load_data():
    print("Loading data from yfinance...")
    # هنا يمكنك إضافة منطق سحب البيانات الخاص بك مستقبلاً
    try:
        ticker = yf.Ticker("SPY")
        info = ticker.info
        print("Data loaded successfully!")
        return "تم الاتصال بـ yfinance وسحب البيانات بنجاح!"
    except Exception as e:
        print(f"Error loading data: {e}")
        return "فشل في سحب البيانات من yfinance."

# استقبال أمر /start من المستخدمين في تليجرام
@bot.message_handler(commands=['start'])
def send_welcome(message):
    print("/start command received. Preparing to execute...")
    status_msg = load_data()
    bot.reply_to(message, f"أهلاً بك! البوت يعمل الآن بنجاح.\n{status_msg}")

if __name__ == "__main__":
    print("البوت بدأ الاستماع المستمر للرسائل...")
    # هذا السطر السحري يجبر السيرفر على البقاء مستيقظاً 24 ساعة
    bot.infinity_polling()
