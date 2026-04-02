import streamlit as st
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder
from utils import ask_ai
from gtts import gTTS
import base64, io, hashlib, uuid, time, os

st.set_page_config(page_title="FinChat AI", page_icon="💹", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

body, .stApp {
    background: #f0f2f6;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid #334155;
}
section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

.sidebar-logo {
    text-align: center;
    padding: 24px 0 16px;
    border-bottom: 1px solid #334155;
    margin-bottom: 20px;
}
.sidebar-logo h1 {
    font-size: 26px;
    font-weight: 700;
    color: #38bdf8 !important;
    margin: 8px 0 4px;
}
.sidebar-logo p {
    font-size: 13px;
    color: #94a3b8 !important;
}

.sidebar-section {
    background: rgba(255,255,255,0.05);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
}
.sidebar-section h4 {
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #38bdf8 !important;
    margin: 0 0 12px;
}
.sidebar-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    border-radius: 8px;
    margin-bottom: 6px;
    background: rgba(255,255,255,0.04);
    font-size: 13px;
    color: #cbd5e1 !important;
}
.sidebar-step {
    background: #38bdf8;
    color: #0f172a !important;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 700;
    flex-shrink: 0;
}
.status-dot {
    width: 8px; height: 8px;
    background: #22c55e;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── Main header ── */
.main-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border: 1px solid #1e40af;
}
.main-header-left h1 {
    font-size: 28px;
    font-weight: 700;
    color: #f8fafc;
    margin: 0 0 4px;
}
.main-header-left p {
    font-size: 14px;
    color: #94a3b8;
    margin: 0;
}
.header-badge {
    background: rgba(56,189,248,0.15);
    border: 1px solid #38bdf8;
    color: #38bdf8;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}

/* ── Chat area ── */
.chat-wrapper {
    background: white;
    border-radius: 16px;
    padding: 24px;
    min-height: 400px;
    border: 1px solid #e2e8f0;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.chat-user {
    display: flex;
    justify-content: flex-end;
    margin: 12px 0;
}
.chat-user-bubble {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    padding: 14px 20px;
    border-radius: 18px 18px 4px 18px;
    max-width: 75%;
    font-size: 17px;
    line-height: 1.6;
    box-shadow: 0 2px 8px rgba(37,99,235,0.3);
}
.chat-bot {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin: 12px 0;
}
.bot-avatar {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #0ea5e9, #2563eb);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}
.chat-bot-bubble {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    color: #1e293b;
    padding: 16px 20px;
    border-radius: 4px 18px 18px 18px;
    max-width: 75%;
    font-size: 17px;
    line-height: 1.7;
}
.signature-tag {
    display: inline-block;
    margin-top: 10px;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    color: #1d4ed8;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.3px;
}

/* ── Audio player ── */
.audio-wrapper {
    margin: 8px 0 4px 46px;
}
.audio-wrapper audio {
    height: 32px;
    width: 260px;
    border-radius: 20px;
}

/* ── Input bar ── */
.input-bar {
    background: white;
    border-radius: 16px;
    padding: 16px 20px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.input-label {
    font-size: 12px;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 10px;
}

/* ── Welcome card ── */
.welcome-card {
    text-align: center;
    padding: 48px 24px;
    color: #94a3b8;
}
.welcome-card h3 {
    font-size: 20px;
    color: #475569;
    margin-bottom: 8px;
}
.welcome-card p { font-size: 14px; }
.topic-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 20px;
}
.chip {
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    color: #475569;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
}

/* Hide streamlit defaults */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──
for key, val in [
    ("chat_history", []),
    ("messages", []),
    ("last_audio_hash", None)
]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size:42px">💹</div>
        <h1>FinChat AI</h1>
        <p>Powered by LLaMA 3 + Groq</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-section">
        <h4>🟢 System Status</h4>
        <div class="sidebar-item">
            <span class="status-dot"></span> AI Model — Online
        </div>
        <div class="sidebar-item">
            <span class="status-dot"></span> Voice Engine — Ready
        </div>
        <div class="sidebar-item">
            <span class="status-dot"></span> Speech Recognition — Active
        </div>
    </div>

    <div class="sidebar-section">
        <h4>📖 How to use</h4>
        <div class="sidebar-item">
            <span class="sidebar-step">1</span> Type your finance question below
        </div>
        <div class="sidebar-item">
            <span class="sidebar-step">2</span> Or click the mic and speak
        </div>
        <div class="sidebar-item">
            <span class="sidebar-step">3</span> Wait for AI response + audio
        </div>
        <div class="sidebar-item">
            <span class="sidebar-step">4</span> Play audio or read the reply
        </div>
    </div>

    <div class="sidebar-section">
        <h4>💡 What I can help with</h4>
        <div class="sidebar-item">📊 Stock market & P/E ratio</div>
        <div class="sidebar-item">💰 SIP, Mutual funds, FD, PPF</div>
        <div class="sidebar-item">🇮🇳 NSE, BSE, SEBI, RBI, GST</div>
        <div class="sidebar-item">📒 Balance sheet, P&L, Cash flow</div>
        <div class="sidebar-item">📈 Equity, Debt, Risk & Return</div>
        <div class="sidebar-item">🧮 Financial calculations</div>
    </div>

    <div class="sidebar-section">
        <h4>⚡ Try asking</h4>
        <div class="sidebar-item">"What is P/E ratio?"</div>
        <div class="sidebar-item">"How does SIP work?"</div>
        <div class="sidebar-item">"Explain bull vs bear market"</div>
        <div class="sidebar-item">"What is SEBI?"</div>
    </div>
    """, unsafe_allow_html=True)

# ── Main area ──


# ── Audio helper ──
def generate_audio_b64(text):
    clean = text.replace("— Made by Mohd Jameel | FinChat AI 💹", "").strip()
    tts = gTTS(text=clean, lang='en')
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

# ── Process input ──
def process_input(user_input):
    with st.spinner("FinBot is thinking..."):
        reply, st.session_state.chat_history = ask_ai(user_input, st.session_state.chat_history)
        audio_b64 = generate_audio_b64(reply)
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": reply, "audio": audio_b64})
    st.rerun()

# ── Chat display ──

if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <div style="font-size:52px; margin-bottom:16px">💹</div>
        <h3>Welcome to FinChat AI</h3>
        <p>Ask me anything about finance, investing, or the stock market.</p>
        <div class="topic-chips">
            <span class="chip">📊 Stock Market</span>
            <span class="chip">💰 Mutual Funds</span>
            <span class="chip">🇮🇳 Indian Finance</span>
            <span class="chip">📈 Investing</span>
            <span class="chip">🧮 Calculations</span>
            <span class="chip">📒 Accounting</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-user">
                <div class="chat-user-bubble">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-bot">
                <div class="bot-avatar">🤖</div>
                <div>
                    <div class="chat-bot-bubble">{msg["content"]}</div>
                    <div class="signature-tag">💹 FinChat AI · Mohd Jameel</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="audio-wrapper">
                <audio controls autoplay>
                    <source src="data:audio/mp3;base64,{msg['audio']}" type="audio/mp3">
                </audio>
            </div>
            """, unsafe_allow_html=True)


# ── Input bar ──
# ── Input bar ──
col1, col2 = st.columns([5, 1])
with col1:
    text_input = st.chat_input("e.g. What is P/E ratio? How does SIP work?")
with col2:
    st.markdown("<div style='padding-top:4px; text-align:center; color:#64748b; font-size:12px'>🎙️ Voice</div>", unsafe_allow_html=True)
    audio_bytes = audio_recorder(
        text="",
        recording_color="#e74c3c",
        neutral_color="#2563eb",
        icon_size="2x",
        pause_threshold=2.5
    )

# ── Handle text ──
if text_input:
    process_input(text_input)

# ── Handle voice ──
if audio_bytes and len(audio_bytes) > 5000:
    audio_hash = hashlib.md5(audio_bytes).hexdigest()
    if audio_hash != st.session_state.last_audio_hash:
        st.session_state.last_audio_hash = audio_hash
        with st.spinner("Transcribing voice..."):
            time.sleep(0.5)
            recognizer = sr.Recognizer()
            audio_file = io.BytesIO(audio_bytes)
            try:
                with sr.AudioFile(audio_file) as source:
                    audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                if text.strip():
                    process_input(text)
            except sr.UnknownValueError:
                st.warning("Could not understand audio. Try again.")
            except sr.RequestError:
                st.error("Speech recognition service error.")

# ── Clear button ──
if st.session_state.messages:
    st.markdown("<div style='text-align:right; margin-top:8px'>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.last_audio_hash = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
