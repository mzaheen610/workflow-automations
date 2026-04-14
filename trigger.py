"""To schedule the trigger of the automation scripts through the telegram bot,
using custom messages or commands."
"""
import telebot
import subprocess
import os
import dotenv
dotenv.load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_BOT_API")
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['spy'])
def trigger_script(message):
    bot.reply_to(message, "Executing your script...")
    # This runs your specific monitoring script
    subprocess.Popen(["python", "screenspy.py"]) 
    bot.reply_to(message, "Script is now running!")

@bot.message_handler(commands=['stop'])
def stop_script(message):
    bot.reply_to(message, "Stopping the script...")
    # This is a simple way to stop the script
    subprocess.Popen(["pkill", "-f", "screenspy.py"]) 
    bot.reply_to(message, "Script has been stopped.")

print("Telegram bot is running...")
bot.polling()