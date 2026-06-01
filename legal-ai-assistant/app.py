from PyPDF2 import PdfReader
from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ===== FUNCTION CALL AI =====
def ask_ai(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    return result["choices"][0]["message"]["content"]

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# ===== WEB PAGE =====
@app.route("/")
def home():
    return render_template("index.html")

# ===== SUMMARIZE =====
@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.json["text"]
    prompt = f"Summarize this legal document into bullet points:\n{text}"
    result = ask_ai(prompt)
    return jsonify({"result": result})

# ===== SIMPLIFY =====
@app.route("/simplify", methods=["POST"])
def simplify():
    text = request.json["text"]
    prompt = f"Explain this legal text in simple everyday language:\n{text}"
    result = ask_ai(prompt)
    return jsonify({"result": result})

@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    try:
        file = request.files["pdf"]

        text = extract_text_from_pdf(file)

        prompt = f"Summarize this legal document into bullet points:\n{text}"
        result = ask_ai(prompt)

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"result": "PDF Error: " + str(e)})
    
@app.route("/ask", methods=["POST"])
def ask():
    try:
        question = request.json["question"]

        prompt = f"You are a helpful legal assistant. Answer clearly:\n{question}"
        result = ask_ai(prompt)

        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"result": "Error: " + str(e)})    

if __name__ == "__main__":
    app.run(debug=True)