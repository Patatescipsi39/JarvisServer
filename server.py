from flask import Flask, request, jsonify
from google import genai
import os

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY ortam değişkeni bulunamadı.")

client = genai.Client(
    api_key=api_key
)


@app.route("/", methods=["GET"])
def home():
    return "Jarvis server online."


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "error": "Mesaj boş"
        }), 400

    try:

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=user_message,
            system_instruction=(
                "Sen Jarvis adında Türkçe konuşan Android asistanısın. "
                "Kısa, doğal ve yardımcı cevaplar ver. "
                "Kullanıcı Türkçe konuşuyorsa Türkçe cevap ver."
            )
        )

        return jsonify({
            "reply": interaction.output_text
        })

    except Exception as e:

        print(
            "GEMINI HATASI:",
            repr(e),
            flush=True
        )

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )