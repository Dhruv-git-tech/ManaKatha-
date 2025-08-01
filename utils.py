import random

def get_emoji(sentiment):
    return {
        'positive': '😊',
        'negative': '😔',
        'neutral': '😐'
    }.get(sentiment, '🙂')

def generate_ai_rating(story_text):
    length_score = min(len(story_text) // 100, 10)
    emotion_score = random.randint(6, 10)
    clarity_score = random.randint(5, 10)
    avg_rating = round((length_score + emotion_score + clarity_score) / 3, 1)
    return avg_rating, emotion_score, clarity_score

def generate_appreciation(sentiment):
    compliments = {
        "positive": ["అద్భుతమైన కథ!", "చాలా బాగుంది నీ కథ!", "నీ భావోద్వేగం అద్భుతం!"],
        "neutral": ["వినోదంగా ఉంది!", "భాగంగా చెప్పావ్!", "అనుభవం బాగుంది."],
        "negative": ["గొప్ప నిబద్ధత చూపించావ్.", "కష్టం అయినా, బాగా వివరించావ్."],
    }
    return random.choice(compliments.get(sentiment, ["బాగుంది!"]))
