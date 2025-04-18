from flask import Flask, render_template, request, session
import requests
from g4f.client import Client

app = Flask(__name__)
app.secret_key = 'sk-ococjdicjdwicjweidjweiji'

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", history=session.get('history', []))

@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.form["prompt"]
    model = request.form.get("model", "flux")
    size = request.form.get("size")
    client = Client()
    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        response_format="url"
    )
    image_url = response.data[0].url
    history = session.get("history", [])
    history.insert(0, {"prompt": prompt, "model": model, "url": image_url})
    session["history"] = history[:5]

    return render_template("index.html", image_url=image_url, history=session["history"])

if __name__ == "__main__":
    app.run(debug=True)