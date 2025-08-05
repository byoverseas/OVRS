from textblob import TextBlob


def analyze_sentiment(text: str) -> float:
    return TextBlob(text).sentiment.polarity
