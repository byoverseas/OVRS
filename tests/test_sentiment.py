from app.nlp.sentiment import analyze_sentiment


def test_positive_sentiment():
    assert analyze_sentiment("I love this brand") > 0


def test_negative_sentiment():
    assert analyze_sentiment("This product is terrible") < 0
