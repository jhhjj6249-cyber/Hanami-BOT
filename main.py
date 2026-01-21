import os
import telebot
import requests
from flask import Flask
from threading import Thread

# --- CẤU HÌNH HỆ THỐNG ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GROQ_KEY = os.getenv('GROQ_API_KEY')

bot = telebot.TeleBot(TOKEN, threaded=True)
app = Flask(__name__)

# Web server mini để Render không báo lỗi
@app.route('/')
def home():
    return "Bot is Running!"

def run_web():
    app.run(host='0.0.manual', port=int(os.environ.get('PORT', 8080)))

# --- LOGIC AI ---
def ask_ai(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}"}
    payload = {
        "model": "llama-3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        return res.json()['choices'][0]['message']['content']
    except:
        return "⚠️ Lỗi kết nối AI."

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 **NEXUS RENDER CLOUD ONLINE v7.0**\nĐã sẵn sàng phản hồi siêu tốc!", parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def chat(message):
    bot.send_chat_action(message.chat.id, 'typing')
    response = ask_ai(message.text)
    bot.reply_to(message, response)

# --- CHẠY SONG SONG ---
if __name__ == "__main__":
    # Chạy Web Server ở luồng riêng
    t = Thread(target=run_web)
    t.start()
    
    # Chạy Bot Telegram
    print("🤖 Bot is starting...")
    bot.infinity_polling()
