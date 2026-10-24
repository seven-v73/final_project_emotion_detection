"""Flask web application for the Watson emotion detector."""

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """Render the form and, when submitted, display the prediction."""
    text = ""
    result = None
    error = None
    if request.method == "POST":
        text = request.form.get("text", "")
        if not text.strip():
            error = "Please enter a statement to analyze."
        else:
            result = emotion_detector(text)
            if result["dominant_emotion"] is None:
                error = "The emotion service could not analyze this statement."
    return render_template("index.html", text=text, result=result, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
