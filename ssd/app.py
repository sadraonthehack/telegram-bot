from flask import Flask
import threading
import asyncio
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_bot():
    subprocess.run(["python3", "bot.py"])

if __name__ == "__main__":
    thread = threading.Thread(target=run_bot)
    thread.start()
    app.run(host='0.0.0.0', port=8080)
