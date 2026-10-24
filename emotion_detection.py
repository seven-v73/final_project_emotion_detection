"""Emotion detection client for the Watson NLP service."""

import requests


WATSON_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {"grpc-metadata-mm-model-id": "emotion_single_watson_predict"}


def emotion_detector(text_to_analyze):
    """Return the five emotion scores and the dominant emotion.

    The public contract is a dictionary with anger, disgust, fear, joy,
    sadness and dominant_emotion keys.  A failed/invalid request returns
    zero values and ``None`` for the dominant emotion, as required by the
    web application error handling.
    """
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return _empty_result()

    try:
        response = requests.post(
            WATSON_URL,
            json={"raw_document": {"text": text_to_analyze}},
            headers=HEADERS,
            timeout=30,
        )
    except requests.RequestException:
        return _empty_result()

    if response.status_code == 400:
        return _empty_result()
    if response.status_code != 200:
        return _empty_result()

    try:
        scores = response.json()["emotionPredictions"][0]["emotion"]
    except (ValueError, KeyError, IndexError, TypeError):
        return _empty_result()

    result = {emotion: float(scores.get(emotion, 0.0)) for emotion in EMOTIONS}
    result["dominant_emotion"] = max(EMOTIONS, key=result.get)
    return result


EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def _empty_result():
    """Return the documented response for invalid input or HTTP 400."""
    return {
        **{emotion: None for emotion in EMOTIONS},
        "dominant_emotion": None,
    }
