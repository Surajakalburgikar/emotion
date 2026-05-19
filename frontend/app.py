import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8000/api/analyze"
HEALTH_URL = "http://127.0.0.1:8000/api/health"

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Emotion Detector AI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS (Monochromatic Black, Silver, and White Palette) ────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Custom scrollbar for sidebar */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.08);
    border-radius: 999px;
}

/* Dark background - Pure Matte Black and charcoal gradient */
.stApp {
    background: linear-gradient(135deg, #09090b, #121214, #18181b);
    min-height: 100vh;
}

/* Sidebar styling - Darkest Jet Black */
[data-testid="stSidebar"] {
    background-color: rgba(9, 9, 11, 0.98) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}

/* Hero header - Premium White-Silver Gradient */
.hero-title {
    text-align: center;
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(90deg, #ffffff, #e4e4e7, #a1a1aa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 0rem; 
    margin-bottom: 2rem;
}

/* Card container for results */
.glass-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.5rem;
    backdrop-filter: blur(12px);
    margin-top: 1rem;
    margin-bottom: 1rem;
}

/* Metric row */
.metric-row {
    display: flex;
    gap: 0.75rem;
    justify-content: center;
    margin-top: 1rem;
}
.metric-box {
    flex: 1;
    background: rgba(255,255,255,0.03);
    border-radius: 10px;
    padding: 0.8rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.05);
}
.metric-label {
    font-size: 0.7rem;
    color: #71717a;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.2rem;
}
.metric-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: #f4f4f5;
}

/* Sidebar History item - Silver left border */
.history-item {
    background: rgba(255,255,255,0.02);
    border-left: 3px solid #d4d4d8;
    border-radius: 0 8px 8px 0;
    padding: 0.5rem 0.7rem;
    margin-bottom: 0.5rem;
    font-size: 0.8rem;
    color: #e4e4e7;
    border-top: 1px solid rgba(255,255,255,0.03);
    border-right: 1px solid rgba(255,255,255,0.03);
    border-bottom: 1px solid rgba(255,255,255,0.03);
}

/* Override Streamlit text area to be extremely sleek */
.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #f4f4f5 !important;
    font-size: 0.95rem !important;
}

/* Sleek Monochromatic Button - Pure White with black text */
.stButton > button {
    width: 100%;
    border-radius: 10px !important;
    padding: 0.65rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    background: linear-gradient(90deg, #ffffff, #e4e4e7) !important;
    border: 1px solid #ffffff !important;
    color: #09090b !important;
    transition: transform 0.1s ease, background 0.2s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #e4e4e7, #d4d4d8) !important;
    border-color: #e4e4e7 !important;
}
.stButton > button:active { 
    transform: scale(0.99); 
}

/* Selectbox dropdown overrides */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #f4f4f5 !important;
}

div[data-testid="stAlert"] {
    border-radius: 10px !important;
    background-color: rgba(255, 255, 255, 0.05) !important;
    color: #f4f4f5 !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

/* Monochromatic Progress Bar - Clean silver/white */
.stProgress > div > div > div > div {
    background-color: #ffffff !important;
}

/* Hide streamlit default top spacing */
.block-container {
    padding-top: 3.5rem !important;
    padding-bottom: 2rem !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Emotion Emoji Map (Polished Monochromatic Accents) ────────────────────────
# Tailored variations of platinum, silver, and bright white to fit the theme
EMOTION_CONFIG = {
    "happy":    {"emoji": "😄", "color": "#ffffff"}, # Glowing white
    "joy":      {"emoji": "😄", "color": "#ffffff"},
    "sad":      {"emoji": "😢", "color": "#a1a1aa"}, # Zinc / Dark Silver
    "sadness":  {"emoji": "😢", "color": "#a1a1aa"},
    "angry":    {"emoji": "😠", "color": "#d4d4d8"}, # Medium Silver
    "anger":    {"emoji": "😠", "color": "#d4d4d8"},
    "fear":     {"emoji": "😨", "color": "#e4e4e7"}, # Platinum
    "surprise": {"emoji": "😲", "color": "#f4f4f5"}, # White-Silver
    "disgust":  {"emoji": "🤢", "color": "#a1a1aa"},
    "neutral":  {"emoji": "😐", "color": "#d4d4d8"},
}

def get_emotion_info(emotion: str):
    key = emotion.lower()
    return EMOTION_CONFIG.get(key, {"emoji": "🤔", "color": "#e4e4e7"})

# ─── Session State ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "prev_input" not in st.session_state:
    st.session_state.prev_input = ""

# ─── Backend Health Check ──────────────────────────────────────────────────────
def check_backend():
    try:
        r = requests.get(HEALTH_URL, timeout=2)
        return r.status_code == 200
    except Exception:
        return False

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title"><span style="filter: grayscale(100%); margin-right: 12px; display: inline-block;">🧠</span>Emotion Detector AI</div>', unsafe_allow_html=True)

# Silent health check
backend_ok = check_backend()
if not backend_ok:
    st.error("🔌 **Backend Offline** — Start the FastAPI server to run analyses.")
    st.code("cd backend\nuvicorn app.main:app --reload", language="bash")
    st.stop()

# ─── Sidebar Configuration ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Inference Model")
    model_option = st.selectbox(
        "Select model:",
        options=["auto", "gemini", "local"],
        format_func=lambda x: {
            "auto":   "🤖 Auto (Gemini + Fallback)",
            "gemini": "✨ Gemini AI Only",
            "local":  "💻 Local Model Only"
        }[x],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📋 Analysis History")
    
    if st.session_state.history:
        for item in st.session_state.history:
            st.markdown(f"""
            <div class="history-item">
                <b><span style="filter: grayscale(100%); margin-right: 4px; display: inline-block;">{item['emoji']}</span> {item['emotion'].capitalize()}</b>
                &nbsp;·&nbsp; <span style="color:#71717a;">{item['source']}</span>
                <br><span style="color:#a1a1aa; font-size:0.75rem;">"{item['text']}"</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.session_state.last_result = None
            st.rerun()
    else:
        st.markdown("<p style='color:#71717a; font-size:0.85rem; font-style:italic;'>No recent runs yet.</p>", unsafe_allow_html=True)

# ─── Main Workspace (Monochromatic and Clean) ─────────────────────────────────

# Place a single, custom empty placeholder above text box for the header info
header_placeholder = st.empty()

user_input = st.text_area(
    "Input text box",
    height=130,
    placeholder="Type or paste any text to detect its emotion…",
    label_visibility="collapsed"
)

# Render character count and active model in a sleek, non-intrusive HTML row above
char_count = len(user_input)
header_placeholder.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; padding: 0 2px;">
    <span style="color:#71717a; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.05em;">Model: <b style="color:#ffffff;">{model_option.upper()}</b></span>
    <span style="color:#71717a; font-size:0.78rem; font-weight:500;">{char_count} / 1000 chars</span>
</div>
""", unsafe_allow_html=True)

# Discard old result on input change
if user_input != st.session_state.prev_input:
    st.session_state.last_result = None
    st.session_state.prev_input = user_input

# Sleek and centered Analyze Button
analyze_btn = st.button("🔍 Analyze Emotion", disabled=not backend_ok)

# ─── Analysis Trigger ──────────────────────────────────────────────────────────
if analyze_btn:
    if not user_input.strip():
        st.warning("⚠️ Please enter some text first.")
    elif char_count > 1000:
        st.error("❌ Text exceeds the 1000 character limit.")
    else:
        try:
            with st.spinner("Analyzing…"):
                start = time.time()
                response = requests.post(
                    API_URL,
                    json={"text": user_input.strip(), "model": model_option},
                    timeout=30
                )
                elapsed = round(time.time() - start, 2)

            if response.status_code == 200:
                data = response.json()["data"]
                emotion   = data["emotion"]
                confidence = data["confidence"]
                source     = data["source"]
                info       = get_emotion_info(emotion)

                # Save current result into state
                st.session_state.last_result = {
                    "emotion": emotion,
                    "confidence": confidence,
                    "source": source,
                    "elapsed": elapsed,
                    "info": info
                }

                # Save to history
                st.session_state.history.insert(0, {
                    "text": user_input.strip()[:35] + ("…" if len(user_input) > 35 else ""),
                    "emotion": emotion,
                    "emoji": info["emoji"],
                    "source": source.split(" ")[0],
                    "time": elapsed
                })
                # Keep history clean
                st.session_state.history = st.session_state.history[:8]
                st.rerun()

            else:
                error_msg = response.json().get("error", "Unknown error from backend.")
                if "quota" in error_msg.lower() or "429" in error_msg:
                    st.error("🚫 **Gemini API quota exceeded.** Switch to **Local Model Only** or **Auto** mode in the sidebar — the local model works offline and has no limits.")
                elif "both" in error_msg.lower():
                    st.error("❌ Both Gemini and local model failed. Please check the backend logs.")
                else:
                    st.error(f"❌ Error: {error_msg}")

        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to the backend. Make sure FastAPI is running on port 8000.")
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out after 30s. The model may be loading — try again.")
        except Exception as error:
            st.error(f"❌ Unexpected error: {error}")

# ─── Persistent Result Rendering ───────────────────────────────────────────────
if st.session_state.last_result:
    res = st.session_state.last_result
    info = res["info"]
    
    st.markdown(f"""
    <div class="glass-card" style="border-color: {info['color']}44; margin-top:1.5rem; animation: fadeIn 0.5s;">
        <div style="text-align:center;">
            <div style="font-size:3.5rem; margin-bottom:0.25rem; filter: grayscale(100%); display: inline-block;">{info['emoji']}</div>
            <div style="font-size:1.8rem; font-weight:700; color:{info['color']};
                        text-transform:capitalize; margin-bottom:0.25rem;">
                {res['emotion']}
            </div>
        </div>
        <div class="metric-row">
            <div class="metric-box">
                <div class="metric-label">Confidence</div>
                <div class="metric-value" style="color:{info['color']};">
                    {int(res['confidence']*100)}%
                </div>
            </div>
            <div class="metric-box" style="max-width: 45%;">
                <div class="metric-label">Source</div>
                <div class="metric-value" style="font-size:0.8rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{res['source']}">
                    {res['source']}
                </div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Time</div>
                <div class="metric-value">{res['elapsed']}s</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sleek progress bar (Monochromatic)
    st.markdown(f"<div style='font-size:0.85rem; font-weight:500; color:#e4e4e7; margin-bottom:0.2rem; margin-top:0.5rem;'>Confidence Score: {int(res['confidence']*100)}%</div>", unsafe_allow_html=True)
    st.progress(res['confidence'])
