"""Unit tests for the detector and its HTTP error handling."""

from unittest.mock import Mock, patch

from emotion_detection import emotion_detector


def _response(payload, status=200):
    response = Mock(status_code=status)
    response.json.return_value = payload
    return response


def test_detector_returns_formatted_scores():
    emotions = {
        "anger": 0.1, "disgust": 0.2, "fear": 0.3,
        "joy": 0.8, "sadness": 0.4,
    }
    payload = {"emotionPredictions": [{"emotion": emotions}]}
    with patch(
        "emotion_detection.requests.post", return_value=_response(payload)
    ):
        result = emotion_detector("I am happy")
    assert result["joy"] == 0.8
    assert result["dominant_emotion"] == "joy"


def test_http_400_returns_empty_result():
    with patch(
        "emotion_detection.requests.post", return_value=_response({}, 400)
    ):
        result = emotion_detector("invalid")
    assert result["dominant_emotion"] is None


def test_blank_input_returns_empty_result():
    assert emotion_detector("   ")["dominant_emotion"] is None
