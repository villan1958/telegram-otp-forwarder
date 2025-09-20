from flask import Flask, request
import requests, os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route("/ivasms-webhook", methods=["POST"])
def ivasms_webhook():
    data = request.json or {}
    sender = data.get("msisdn") or data.get("from") or data.get("sender")
    text = data.get("text") or data.get("message") or str(data)

    forward_text = f"Incoming SMS from {sender}:\n\n{text}"

    requests.post(TELEGRAM_API, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": forward_text
    })
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
