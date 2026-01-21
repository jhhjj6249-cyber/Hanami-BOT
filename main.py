import os
import telebot
import requests
import time
from telebot import types

# Lấy Token từ Environment Variables (Render Settings)
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GROQ_KEY = os.getenv('GROQ_API_KEY')

bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=50)
session = requests.Session()

def ask_ai(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama3-8b-8192", 
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "stream": False
    }
    try:
        res = session.post(url, headers=headers, json=payload, timeout=10)
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"⚠️ Hệ thống bận: {str(e)}"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🌐 RENDER CLOUD", callback_data="none"))
    
    welcome = (
        "🚀 **NEXUS AI v6.0 ONLINE**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📡 **Host:** `Render.com` (24/7)\n"
        "⚡ **Speed:** `Extreme High Speed`\n"
        "🤖 **Model:** `Llama 3 (8B)`\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💬 *Hãy gửi tin nhắn để trải nghiệm!*"
    )
    bot.send_message(message.chat.id, welcome, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def chat(message):
    response = ask_ai(message.text)
    bot.reply_to(message, response, parse_mode='Markdown')

if __name__ == "__main__":
    print("🤖 Bot is starting on Render...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)

