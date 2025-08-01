from transformers import pipeline

def get_summarizer():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def generate_summary(text, max_tokens=130):
    summarizer = get_summarizer()
    result = summarizer(text, max_length=max_tokens, min_length=30, do_sample=False)
    return result[0]['summary_text']
