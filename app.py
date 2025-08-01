import streamlit as st
from transformers import pipeline
from utils import get_emoji, generate_ai_rating, generate_appreciation
from summary import generate_summary
from voice_input import transcribe_audio
from download import generate_pdf
import time, uuid

# -------------------- SESSION SETUP --------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None
if "stories" not in st.session_state:
    st.session_state.stories = []

# -------------------- LOGIN SECTION --------------------
def login_section():
    st.sidebar.title("🔐 Login Panel")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state.user = "admin"
            st.session_state.role = "admin"
            st.success("Logged in as Admin!")
        elif username:
            st.session_state.user = username
            st.session_state.role = "guest"
            st.success(f"Logged in as {username}")
        else:
            st.error("Invalid credentials")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.role = None
        st.experimental_rerun()

# -------------------- SENTIMENT MODEL --------------------
@st.cache_resource
def load_sentiment_model():
    try:
        return pipeline("sentiment-analysis", model="ai4bharat/indic-bert-sentiment")
    except:
        return pipeline("sentiment-analysis")

sentiment_model = load_sentiment_model()

# -------------------- STORY SUBMISSION --------------------
def story_submission():
    st.title("📖 మన కథ - Share Your Telugu Story")

    st.markdown("🎙️ **Optional: Upload Telugu voice (MP3)**")
    audio_file = st.file_uploader("Upload MP3", type=["mp3"])
    voice_story = ""
    if audio_file:
        st.info("Transcribing audio...")
        voice_story = transcribe_audio(audio_file)
        st.success("Audio transcribed!")

    with st.form(key="story_form_submit"):
        title = st.text_input("కథ శీర్షిక")
        tags = st.text_input("ట్యాగులు (comma separated)")
        story = st.text_area("మీ కథను వ్రాయండి", value=voice_story, height=250)
        is_public = st.checkbox("ఇది పబ్లిక్ కథగా ప్రచురించాలా?", value=True)
        submit = st.form_submit_button("కథ పంపించు")

    if submit and title and story:
        with st.spinner("AI మీ కథను విశ్లేషిస్తోంది..."):
            sentiment_result = sentiment_model(story[:512])[0]
            sentiment = sentiment_result["label"].lower()
            emoji = get_emoji(sentiment)
            compliment = generate_appreciation(sentiment)
            rating, e_score, c_score = generate_ai_rating(story)
            summary = generate_summary(story)

        story_obj = {
            "id": str(uuid.uuid4())[:8],
            "title": title,
            "tags": tags,
            "story": story,
            "summary": summary,
            "rating": rating,
            "emotion": e_score,
            "clarity": c_score,
            "sentiment": sentiment,
            "emoji": emoji,
            "likes": 0,
            "views": 0,
            "public": is_public,
            "author": st.session_state.user or "guest"
        }
        st.session_state.stories.append(story_obj)

        st.success("✅ కథ సబ్మిట్ అయింది!")
        st.markdown(f"### 🗣️ {compliment} {emoji}")
        st.markdown(f"### 🌟 రేటింగ్: {rating}/10")
        st.markdown(f"- భావోద్వేగం: {e_score}/10\n- స్పష్టత: {c_score}/10")
        st.markdown(f"### 🧾 సంక్షిప్తంగా: {summary}")

# -------------------- GALLERY --------------------
def public_gallery():
    st.title("📚 పబ్లిక్ కథల గ్యాలరీ")
    tags = list({t.strip() for s in st.session_state.stories if s["public"] for t in s["tags"].split(",")})
    selected = st.selectbox("ట్యాగ్ ద్వారా కథలు చూడండి", ["All"] + tags)

    for s in st.session_state.stories:
        if not s["public"]:
            continue
        if selected != "All" and selected not in s["tags"]:
            continue

        s["views"] += 1
        st.subheader(f"{s['title']} {s['emoji']}")
        st.caption(f"👤 {s['author']} | 💬 {s['tags']} | ⭐ {s['rating']}/10 | 👀 {s['views']} | ❤️ {s['likes']}")
        st.markdown(f"**సంక్షిప్తంగా**: {s['summary']}")

        col1, col2 = st.columns(2)
        if col1.button(f"❤️ Like", key=f"like_{s['id']}"):
            s["likes"] += 1
            st.experimental_rerun()
        if col2.button("📄 Download PDF", key=f"pdf_{s['id']}"):
            path = generate_pdf(s, f"{s['title']}.pdf")
            with open(path, "rb") as f:
                st.download_button("⬇️ Click to Download", f, file_name=f"{s['title']}.pdf")

# -------------------- ADMIN PANEL --------------------
def admin_panel():
    st.title("🛠️ Admin Panel")
    for i, s in enumerate(st.session_state.stories):
        st.markdown(f"**{s['title']}** by {s['author']} - [ID: {s['id']}]")
        col1, col2 = st.columns(2)
        if col1.button("❌ Delete", key=f"del_{s['id']}"):
            st.session_state.stories.pop(i)
            st.success("Story deleted.")
            st.experimental_rerun()
        if col2.button("🚫 Toggle Public", key=f"pub_{s['id']}"):
            s["public"] = not s["public"]
            st.experimental_rerun()

# -------------------- MAIN --------------------
login_section()
nav = st.sidebar.radio("Navigate", ["📤 Submit Story", "📚 View Gallery", "🛠️ Admin Panel" if st.session_state.role == "admin" else ""])

if nav == "📤 Submit Story":
    story_submission()
elif nav == "📚 View Gallery":
    public_gallery()
elif nav == "🛠️ Admin Panel":
    admin_panel()
