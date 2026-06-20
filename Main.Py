import os
import sys

# هذا الجزء يقوم بتثبيت المكتبات تلقائياً عند الضغط على Run
os.system('pip3 install --user pyTelegramBotAPI pypdf google-generativeai')

import telebot
import pypdf
import google.generativeai as genai

genai.configure(api_key="AIzaSyAA8I06lC9JbBuMg8fPoUTRQOhKn9OwLjY")
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot("8797538798:AAEjGEZbp9nXLXg9pEVYFnabKCJ5_TDxLqY")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = message.document.file_name
        with open(file_name, 'wb') as f: f.write(downloaded_file)
        
        reader = pypdf.PdfReader(file_name)
        text = "\n".join([page.extract_text() for page in reader.pages[:2]])
        
        response = model.generate_content(f"Extract details: {text[:2000]}")
        bot.reply_to(message, response.text)
        os.remove(file_name)
    except Exception as e:
        bot.reply_to(message, str(e))

bot.infinity_polling()
