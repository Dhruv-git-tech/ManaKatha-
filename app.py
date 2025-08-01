import streamlit as st
from transformers import pipeline
import time
from utils import get_emoji, generate_ai_rating, generate_appreciation

@st.cache_resource
def load_sentiment_model():
    try:
        sentiment_pipeline = pipeline("sentiment-analysis", model="ai4bharat/indic-bert-sentiment")
    except:
        sentiment_pipeline = pipeline("sentiment-analysis")
    return sentiment_pipeline

sentiment_model = load_sentiment_model()

st.set_page_config(page_title="ManaKatha - Telugu Stories", layout="centered")
st.title("📖 మన కథ - Telugu Story Sharing with AI")
st.markdown("**తెలుగు లో మీ కథను పంచుకోండి** – AI మీ కథను చదివి అభినందనలు, స్పందన, రేటింగ్ ఇస్తుంది.")

with st.form("story_form"):
    title = st.text_input("కథ శీర్షిక (Title)")
    tags = st.text_input("ట్యాగులు (Tags like ప్రేమ, బాళ్యం, బాధ, etc.)")
    story = st.text_area("మీ కథను ఇక్కడ వ్రాయండి...", height=300)
    is_public = st.checkbox("ఇది పబ్లిక్ కథగా ప్రచురించాలా?", value=True)
    submitted = st.form_submit_button("కథ పంపించు")

if submitted:
    with st.spinner("AI మీ కథ చదువుతోంది..."):
        time.sleep(1)
        sentiment_result = sentiment_model(story[:512])[0]
        sentiment = sentiment_result['label'].lower()
        emoji = get_emoji(sentiment)
        compliment = generate_appreciation(sentiment)
        rating, emo_score, clarity_score = generate_ai_rating(story)

    st.success("✅ మీ కథకి స్పందన వచ్చింది!")
    st.markdown(f"### 🗣️ అభినందన: **{compliment}** {emoji}")
    st.markdown(f"### 🌟 రేటింగ్: **{rating}/10**")
    st.markdown(f"- భావోద్వేగం: {emo_score}/10\n- స్పష్టత: {clarity_score}/10")

    if is_public:
        st.markdown("📚 **మీ కథను పబ్లిక్ గాలరీలో జోడించాం.** (ఇది డేటాబేస్ కి వదిలిన తర్వాత వర్తిస్తుంది)")

import streamlit as st
from transformers import pipeline
import time
from utils import get_emoji, generate_ai_rating, generate_appreciation

@st.cache_resource
def load_sentiment_model():
    try:
        sentiment_pipeline = pipeline("sentiment-analysis", model="ai4bharat/indic-bert-sentiment")
    except:
        sentiment_pipeline = pipeline("sentiment-analysis")
    return sentiment_pipeline

sentiment_model = load_sentiment_model()

st.set_page_config(page_title="ManaKatha - Telugu Stories", layout="centered")
st.title("📖 మన కథ - Telugu Story Sharing with AI")
st.markdown("**తెలుగు లో మీ కథను పంచుకోండి** – AI మీ కథను చదివి అభినందనలు, స్పందన, రేటింగ్ ఇస్తుంది.")

with st.form("story_form"):
    title = st.text_input("కథ శీర్షిక (Title)")
    tags = st.text_input("ట్యాగులు (Tags like ప్రేమ, బాళ్యం, బాధ, etc.)")
    story = st.text_area("మీ కథను ఇక్కడ వ్రాయండి...", height=300)
    is_public = st.checkbox("ఇది పబ్లిక్ కథగా ప్రచురించాలా?", value=True)
    submitted = st.form_submit_button("కథ పంపించు")

if submitted:
    with st.spinner("AI మీ కథ చదువుతోంది..."):
        time.sleep(1)
        sentiment_result = sentiment_model(story[:512])[0]
        sentiment = sentiment_result['label'].lower()
        emoji = get_emoji(sentiment)
        compliment = generate_appreciation(sentiment)
        rating, emo_score, clarity_score = generate_ai_rating(story)

    st.success("✅ మీ కథకి స్పందన వచ్చింది!")
    st.markdown(f"### 🗣️ అభినందన: **{compliment}** {emoji}")
    st.markdown(f"### 🌟 రేటింగ్: **{rating}/10**")
    st.markdown(f"- భావోద్వేగం: {emo_score}/10\n- స్పష్టత: {clarity_score}/10")

    if is_public:
        st.markdown("📚 **మీ కథను పబ్లిక్ గాలరీలో జోడించాం.** (ఇది డేటాబేస్ కి వదిలిన తర్వాత వర్తిస్తుంది)")



