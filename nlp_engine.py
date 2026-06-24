import spacy
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load the model (ensure you have run: python -m spacy download en_core_web_sm)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Model not found. Please run: python -m spacy download en_core_web_sm")
    nlp = None

def analyze_log_entry(text):
    if not nlp: return False
    doc = nlp(text)
    for token in doc:
        if token.text.lower() in ["alert", "intruder", "hijack"]:
            logging.warning(f"CRITICAL NLP ALERT: Semantic anomaly detected: {token.text}")
            return True
    return False

if __name__ == "__main__":
    # Test the function
    sample_text = "System reports a possible hijack detected at the gate."
    print(f"Analyzing: {sample_text}")
    result = analyze_log_entry(sample_text)
    print(f"Anomaly detected: {result}")
