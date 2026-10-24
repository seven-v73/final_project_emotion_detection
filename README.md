# Emotion Detector

A Flask web application that uses the Watson NLP EmotionPredict service to
identify anger, disgust, fear, joy and sadness from a text statement.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server.py
```

Open <http://localhost:5000>. The API client returns a normalized dictionary
with five scores and `dominant_emotion`; invalid input and HTTP 400 responses
are handled safely.

## Verification

```bash
pytest -q
flake8 . --exclude=venv
```
