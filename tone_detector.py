from transformers import pipeline

classifier = pipeline("sentiment-analysis")  # default model works well

def detect_tone(text: str) -> str:
    """
    Returns one of: 'empathetic', 'polite', 'formal'
    Mapping:
      - NEGATIVE -> empathetic
      - POSITIVE -> polite
      - NEUTRAL -> formal
    """
    # If text is empty or only spaces, default to 'formal'
    if not text or text.strip() == "":
        return "formal"
    res = classifier(text[:512])[0]   # Run sentiment analysis on the first 512 characters

    # Get the label and convert to uppercase for consistent comparison
    label = res.get("label", "").upper()
    if label.startswith("NEG"):
        return "empathetic"
    if label.startswith("POS"):
        return "polite"
    return "formal"

if __name__ == "__main__":
    # Sample texts to test the tone detection
    samples = [
        "I am extremely disappointed. My order is late and no one replied.",
        "Thank you so much for the fast delivery!",
        "Can you confirm the meeting time?"
    ]
    for s in samples:
        print(s, "->", detect_tone(s))
