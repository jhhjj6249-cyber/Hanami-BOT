import os
import telebot
import requests
from flask import Flask
from threading import Thread

# --- CẤU HÌNH BIẾN MÔI TRƯỜNG ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GROQ_KEY = os.getenv('GROQ_API_KEY')

bot = telebot.TeleBot(TOKEN, threaded=True)
app = Flask(__name__)

# Tạo Web Server mini để Render không bao giờ báo lỗi Deploy Failed
@app.route('/')
def health_check():
    return "NEXUS AI IS ONLINE 2026", 200

def run_web():
    # Render yêu cầu chạy trên port do họ cung cấp
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- HÀM XỬ LÝ AI SIÊU TỐC ---
def ask_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }
    # Sử dụng Llama-3-8b để không bao giờ bị dính giới hạn (Rate Limit) của bản Free
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "Bạn là AI siêu cấp chạy trên Render 2026. Trả lời cực nhanh, thông minh."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ Hệ thống đang bảo trì hoặc Key hết hạn. Lỗi: {str(e)}"

# --- GIAO DIỆN LỆNH ---
@bot.message_handler(commands=['start'])
def welcome(message):
    text = (
        "💎 **NEXUS AI SYSTEM 2026** 💎\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📡 **Server:** `Render Cloud Active`\n"
        "⚡ **Inference:** `Groq Hyper-Speed`\n"
        "🟢 **Status:** `No Error / Always Online`\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💬 *Gửi tin nhắn ngay để trải nghiệm tốc độ vài mili giây!*"
    )
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Tạo hiệu ứng giả lập đang gõ cho hiện đại
    bot.send_chat_action(message.chat.id, 'typing')
    answer = ask_groq(message.text)
    bot.reply_to(message, answer)

# --- KHỞI CHẠY SONG SONG ---
if __name__ == "__main__":
    # Chạy Web Server ở một luồng riêng để giữ Render Live
    server_thread = Thread(target=run_web)
    server_thread.start()
    
    # Chạy Bot Telegram chính
    print("🚀 Bot is starting on Render...")
    bot.infinity_polling()
