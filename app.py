# app.py - Indian Language Summarizer - Modern AI SaaS UI
import sys, os, re, io
import streamlit as st
import torch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

st.set_page_config(
    page_title="Summarize AI · Indian Languages",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Sora:wght@400;600;700&display=swap');

:root {
  --bg:        #0F1117;
  --bg2:       #161B27;
  --bg3:       #1E2535;
  --border:    #2A3245;
  --accent:    #6366F1;
  --accent2:   #818CF8;
  --accent3:   #A5B4FC;
  --success:   #10B981;
  --warn:      #F59E0B;
  --danger:    #EF4444;
  --text:      #F1F5F9;
  --text2:     #94A3B8;
  --text3:     #64748B;
  --card-glow: 0 0 0 1px rgba(99,102,241,0.15), 0 4px 24px rgba(0,0,0,0.4);
  --card-glow-hover: 0 0 0 1px rgba(99,102,241,0.35), 0 8px 32px rgba(99,102,241,0.12);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
  font-family: 'Inter', sans-serif;
  background: var(--bg) !important;
  color: var(--text) !important;
}

#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 1.2rem 1.5rem !important; max-width: 1400px !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── TOP NAV ── */
.nav {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0.7rem 1.2rem; margin-bottom: 1.2rem;
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.3);
}
.nav-brand {
  display: flex; align-items: center; gap: 0.6rem;
}
.nav-logo {
  width: 30px; height: 30px; border-radius: 8px;
  background: linear-gradient(135deg, #6366F1, #A855F7);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.9rem; color: white; font-weight: 700;
}
.nav-title {
  font-family: 'Sora', sans-serif; font-size: 1rem; font-weight: 600; color: var(--text);
}
.nav-subtitle { font-size: 0.72rem; color: var(--text3); }
.nav-chips { display: flex; gap: 0.4rem; flex-wrap: wrap; }
.nav-chip {
  background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.25);
  color: var(--accent3); font-size: 0.67rem; padding: 0.2rem 0.55rem;
  border-radius: 20px; font-weight: 500; letter-spacing: 0.02em;
}
.nav-status {
  display: flex; align-items: center; gap: 0.4rem;
  font-size: 0.72rem; color: var(--success);
}
.status-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--success); box-shadow: 0 0 6px var(--success);
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%,100% { opacity:1; transform:scale(1); }
  50% { opacity:0.6; transform:scale(1.3); }
}

/* ── PANEL CARDS ── */
.panel {
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 16px; padding: 1.2rem;
  box-shadow: var(--card-glow);
  height: 100%;
}
.panel-label {
  font-size: 0.7rem; font-weight: 600; letter-spacing: 0.1em;
  text-transform: uppercase; color: var(--text3);
  margin-bottom: 0.8rem;
  display: flex; align-items: center; gap: 0.4rem;
}
.panel-label-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--accent); display: inline-block;
}

/* ── STATS ROW ── */
.stats-row { display: flex; gap: 0.6rem; margin-bottom: 0.9rem; }
.stat {
  flex: 1; background: var(--bg3); border: 1px solid var(--border);
  border-radius: 10px; padding: 0.6rem 0.8rem; text-align: center;
}
.stat-val { font-size: 1.3rem; font-weight: 700; color: var(--accent2); line-height: 1; }
.stat-lbl { font-size: 0.65rem; color: var(--text3); margin-top: 0.2rem;
            text-transform: uppercase; letter-spacing: 0.05em; }

/* ── OUTPUT CARD ── */
.output-card {
  background: var(--bg3); border: 1px solid rgba(99,102,241,0.2);
  border-radius: 12px; padding: 1rem 1.1rem;
  min-height: 130px; font-size: 0.9rem; line-height: 1.75;
  color: var(--text); margin-bottom: 0.8rem;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
}
.output-placeholder {
  color: var(--text3); font-style: italic; font-size: 0.85rem;
  display: flex; align-items: center; justify-content: center;
  height: 100%; min-height: 120px; flex-direction: column; gap: 0.5rem;
}
.output-icon { font-size: 1.8rem; opacity: 0.3; }

/* ── TRANSLATION SECTION ── */
.trans-section {
  background: var(--bg); border: 1px solid var(--border);
  border-radius: 10px; padding: 0.8rem 1rem; margin-top: 0.8rem;
}
.trans-header {
  font-size: 0.7rem; font-weight: 600; color: var(--text3);
  text-transform: uppercase; letter-spacing: 0.08em;
  margin-bottom: 0.6rem;
}
.trans-result {
  background: var(--bg3); border: 1px solid var(--border);
  border-radius: 8px; padding: 0.7rem 0.9rem;
  font-size: 0.88rem; line-height: 1.7; color: var(--text);
  margin-top: 0.6rem;
}

/* ── ACTION BAR ── */
.action-bar {
  display: flex; gap: 0.5rem; align-items: center;
  background: var(--bg3); border: 1px solid var(--border);
  border-radius: 10px; padding: 0.5rem 0.7rem;
  margin-top: 0.7rem;
}
.action-label { font-size: 0.7rem; color: var(--text3); white-space: nowrap; }

/* ── WORD COUNT BAR ── */
.wc-bar {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.35rem 0; margin-bottom: 0.5rem;
}
.wc-text { font-size: 0.72rem; color: var(--text3); }
.wc-badge {
  font-size: 0.7rem; color: var(--accent3);
  background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.2);
  padding: 0.15rem 0.5rem; border-radius: 6px;
}

/* ── TOAST ── */
.toast {
  position: fixed; bottom: 1.5rem; right: 1.5rem; z-index: 9999;
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 12px; padding: 0.7rem 1rem;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  display: flex; align-items: center; gap: 0.6rem;
  font-size: 0.82rem; color: var(--text);
  animation: slideUp 0.3s ease;
}
.toast-success { border-left: 3px solid var(--success); }
.toast-error   { border-left: 3px solid var(--danger); }
@keyframes slideUp {
  from { opacity:0; transform:translateY(20px); }
  to   { opacity:1; transform:translateY(0); }
}

/* ── STREAMLIT OVERRIDES ── */
.stTextArea textarea {
  background: var(--bg3) !important; color: var(--text) !important;
  border: 1px solid var(--border) !important; border-radius: 10px !important;
  font-family: 'Inter', sans-serif !important; font-size: 0.88rem !important;
  resize: vertical !important; caret-color: var(--accent) !important;
  transition: border 0.2s !important;
}
.stTextArea textarea:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
  outline: none !important;
}
.stTextArea label { display: none !important; }

.stButton > button {
  font-family: 'Inter', sans-serif !important; font-weight: 600 !important;
  font-size: 0.82rem !important; border-radius: 8px !important;
  transition: all 0.2s !important; border: none !important;
  cursor: pointer !important;
}
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
  color: white !important; padding: 0.55rem 1.2rem !important;
  box-shadow: 0 2px 12px rgba(99,102,241,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 20px rgba(99,102,241,0.45) !important;
}
.stButton > button[kind="secondary"] {
  background: var(--bg3) !important; color: var(--text2) !important;
  border: 1px solid var(--border) !important;
}
.stButton > button[kind="secondary"]:hover {
  border-color: var(--accent) !important; color: var(--accent3) !important;
}

.stSelectbox > div > div,
.stSelectbox [data-baseweb="select"] > div {
  background: var(--bg3) !important; border: 1px solid var(--border) !important;
  border-radius: 8px !important; color: var(--text) !important;
  font-family: 'Inter', sans-serif !important; font-size: 0.82rem !important;
}
.stSelectbox label { color: var(--text3) !important; font-size: 0.72rem !important; }

.stTabs [data-baseweb="tab-list"] {
  background: var(--bg3) !important; border-radius: 8px !important;
  padding: 0.2rem !important; gap: 0.1rem !important;
  border-bottom: none !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important; border-radius: 6px !important;
  color: var(--text3) !important; font-size: 0.8rem !important;
  font-weight: 500 !important; padding: 0.35rem 0.9rem !important;
  transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
  background: var(--accent) !important; color: white !important;
}
.stTabs [data-baseweb="tab-panel"] {
  padding: 0.6rem 0 0 0 !important;
}

.stSlider > div > div > div { background: var(--accent) !important; }
.stSlider > div > div { background: var(--bg3) !important; }
.stSlider label { color: var(--text3) !important; font-size: 0.75rem !important; }
.stSlider > div > div > div > div {
  background: white !important; border: 2px solid var(--accent) !important;
}

.stFileUploader > div {
  background: var(--bg3) !important; border: 2px dashed var(--border) !important;
  border-radius: 10px !important; color: var(--text2) !important;
}
.stFileUploader label { color: var(--text3) !important; font-size: 0.75rem !important; }

.stAlert { border-radius: 10px !important; font-size: 0.82rem !important; }
.stSuccess { background: rgba(16,185,129,0.1) !important; color: var(--success) !important; border-color: rgba(16,185,129,0.3) !important; }
.stError, .stWarning { background: rgba(239,68,68,0.1) !important; }

div[data-testid="stAudio"] {
  background: var(--bg3) !important; border-radius: 10px !important;
  padding: 0.5rem !important; border: 1px solid var(--border) !important;
}

.stExpander {
  background: var(--bg3) !important; border: 1px solid var(--border) !important;
  border-radius: 10px !important;
}
.stExpander summary { color: var(--text2) !important; font-size: 0.8rem !important; }

/* ── DIVIDER ── */
.v-div {
  width: 1px; background: var(--border);
  margin: 0 0.5rem; align-self: stretch;
}

/* ── SECTION TITLE ── */
.sec-title {
  font-size: 0.68rem; font-weight: 600; letter-spacing: 0.1em;
  text-transform: uppercase; color: var(--text3);
  margin: 0.7rem 0 0.4rem 0;
  display: flex; align-items: center; gap: 0.4rem;
}
.sec-title::after {
  content: ''; flex: 1; height: 1px; background: var(--border);
}

/* ── SAMPLE BUTTONS ROW ── */
.sample-row { display: flex; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 0.6rem; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* fix columns gap */
[data-testid="column"] { padding: 0 0.4rem !important; }
[data-testid="column"]:first-child { padding-left: 0 !important; }
[data-testid="column"]:last-child  { padding-right: 0 !important; }

/* hide streamlit default separators */
hr { display: none !important; }

</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────
SAMPLES = {
    "Hindi":   "प्रधानमंत्री नरेंद्र मोदी ने आज नई दिल्ली में किसानों के लिए एक नई योजना की घोषणा की। इस योजना के तहत किसानों को सस्ते कर्ज और आधुनिक उपकरण दिए जाएंगे। सरकार का लक्ष्य अगले पांच वर्षों में किसानों की आय दोगुनी करना है। वित्त मंत्री ने बताया कि इस योजना पर पचास हजार करोड़ रुपये खर्च होंगे।",
    "Tamil":   "தமிழ்நாட்டில் இன்று பெரும் மழை பெய்தது. சென்னை உட்பட பல மாவட்டங்களில் வெள்ளம் ஏற்பட்டது. அரசு நிவாரண பணிகளை தீவிரமாக மேற்கொண்டது. பொதுமக்கள் பாதுகாப்பான இடங்களுக்கு மாற்றப்பட்டனர்.",
    "Bengali": "আজ কলকাতায় একটি বড় সাংস্কৃতিক অনুষ্ঠান আয়োজিত হয়েছে। এই অনুষ্ঠানে বিভিন্ন রাজ্যের শিল্পীরা অংশগ্রহণ করেছেন। দর্শকদের মধ্যে ব্যাপক উৎসাহ দেখা গেছে।",
}

TRANSLATE_LANGS = {
    "— Select language —": None,
    "English":          "en",
    "Hindi (हिंदी)":    "hi",
    "Tamil (தமிழ்)":    "ta",
    "Telugu (తెలుగు)":  "te",
    "Bengali (বাংলা)":  "bn",
    "Marathi (मराठी)":  "mr",
    "Gujarati":         "gu",
    "Kannada":          "kn",
    "Malayalam":        "ml",
    "Urdu (اردو)":      "ur",
    "French":           "fr",
    "German":           "de",
    "Spanish":          "es",
}

TTS_LANGS = {
    "Auto": None, "Hindi": "hi", "Tamil": "ta", "Telugu": "te",
    "Bengali": "bn", "Marathi": "mr", "Gujarati": "gu",
    "Kannada": "kn", "Malayalam": "ml", "Urdu": "ur", "English": "en",
}

# ── Helpers ───────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    from inference import Summarizer
    return Summarizer()

def extract_file(f):
    name = f.name.lower()
    if name.endswith(".txt"):
        return f.read().decode("utf-8", errors="ignore")
    elif name.endswith(".pdf"):
        try:
            import pdfplumber
            with pdfplumber.open(io.BytesIO(f.read())) as pdf:
                return "\n".join(p.extract_text() or "" for p in pdf.pages).strip()
        except: return ""
    elif name.endswith(".docx"):
        try:
            import docx
            doc = docx.Document(io.BytesIO(f.read()))
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        except: return ""
    return ""

def tts(text, lang):
    try:
        from gtts import gTTS
        tts_obj = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO(); tts_obj.write_to_fp(fp); fp.seek(0)
        return fp.read()
    except Exception as e:
        st.error(f"Audio error: {e}"); return None

def translate(text, lang):
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source='auto', target=lang).translate(text)
    except:
        try:
            from googletrans import Translator
            return Translator().translate(text, dest=lang).text
        except Exception as e:
            st.error(f"Translation error: {e}"); return text

def auto_lang(text):
    try:
        from langdetect import detect
        d = detect(text)
        return {"hi":"hi","ta":"ta","te":"te","bn":"bn","mr":"mr",
                "gu":"gu","kn":"kn","ml":"ml","ur":"ur","en":"en"}.get(d,"hi")
    except: return "hi"

# ── Load model ────────────────────────────────────────────────
with st.spinner(""):
    summarizer = load_model()

# ── NAV ───────────────────────────────────────────────────────
st.markdown("""
<div class="nav">
  <div class="nav-brand">
    <div class="nav-logo">✦</div>
    <div>
      <div class="nav-title">Summarize AI</div>
      <div class="nav-subtitle">Indian Language Summarizer · mT5 XLSum</div>
    </div>
  </div>
  <div class="nav-chips">
    <span class="nav-chip">Hindi</span><span class="nav-chip">Tamil</span>
    <span class="nav-chip">Telugu</span><span class="nav-chip">Bengali</span>
    <span class="nav-chip">+5 more</span>
  </div>
  <div class="nav-status">
    <div class="status-dot"></div> Model Ready
  </div>
</div>
""", unsafe_allow_html=True)

# ── TWO COLUMN LAYOUT ─────────────────────────────────────────
left, right = st.columns([1.05, 1], gap="medium")

# ════════════════════════════════════════════════════════
#  LEFT PANEL
# ════════════════════════════════════════════════════════
with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-label"><span class="panel-label-dot"></span> INPUT</div>', unsafe_allow_html=True)

    # Tabs
    tab_paste, tab_upload = st.tabs(["✏️  Paste Text", "📂  Upload File"])

    input_text = ""

    with tab_paste:
        # Sample buttons
        s1, s2, s3 = st.columns(3)
        with s1:
            if st.button("Hindi", key="sh", use_container_width=True):
                st.session_state['itext'] = SAMPLES["Hindi"]
        with s2:
            if st.button("Tamil", key="st", use_container_width=True):
                st.session_state['itext'] = SAMPLES["Tamil"]
        with s3:
            if st.button("Bengali", key="sb", use_container_width=True):
                st.session_state['itext'] = SAMPLES["Bengali"]

        input_text = st.text_area(
            "input",
            value=st.session_state.get('itext', ''),
            height=220,
            placeholder="Paste your Hindi, Tamil, Telugu, Bengali or any Indian language article here…",
            key="ta_main"
        )
        if input_text:
            wc = len(input_text.split())
            st.markdown(f'<div class="wc-bar"><span class="wc-text">Ready to summarize</span><span class="wc-badge">📊 {wc} words · {len(input_text)} chars</span></div>', unsafe_allow_html=True)

    with tab_upload:
        uf = st.file_uploader("file", type=["txt","pdf","docx"], label_visibility="collapsed")
        if uf:
            with st.spinner("Reading file…"):
                extracted = extract_file(uf)
            if extracted:
                input_text = extracted
                st.session_state['itext'] = extracted
                wc = len(extracted.split())
                st.success(f"✅ {uf.name} · {wc} words loaded")
                st.text_area("preview", value=extracted[:300]+"…" if len(extracted)>300 else extracted,
                             height=100, disabled=True, label_visibility="collapsed")

    # Settings
    with st.expander("⚙️  Advanced Settings", expanded=False):
        max_len   = st.slider("Max summary length", 40, 200, 128, 8)
        num_beams = st.slider("Beam width (quality)", 1, 8, 4, 1)
    if 'max_len'   not in st.session_state: max_len   = 128
    if 'num_beams' not in st.session_state: num_beams = 4

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # Action bar
    a1, a2, a3 = st.columns([2.2, 1, 1])
    with a1:
        gen = st.button("✦  Generate Summary", type="primary", use_container_width=True)
    with a2:
        clr = st.button("🗑  Clear", use_container_width=True)
    with a3:
        if st.session_state.get('summary'):
            st.download_button("⬇ Save", st.session_state['summary'],
                               "summary.txt", "text/plain", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── Handle actions ────────────────────────────────────────────
active_text = input_text or st.session_state.get('itext', '')

if clr:
    for k in ['itext','summary','translated','audio_bytes','trans_audio','summary_input']:
        st.session_state.pop(k, None)
    st.rerun()

if gen:
    if not active_text or len(active_text.strip()) < 20:
        st.warning("⚠️ Please enter at least 20 characters.")
    else:
        with st.spinner("Generating summary…"):
            try:
                result = summarizer.summarize(active_text, max_summary=max_len, num_beams=num_beams)
                st.session_state['summary']       = result
                st.session_state['summary_input'] = active_text
                for k in ['translated','audio_bytes','trans_audio']:
                    st.session_state.pop(k, None)
            except Exception as e:
                st.error(f"Error: {e}")

# ════════════════════════════════════════════════════════
#  RIGHT PANEL
# ════════════════════════════════════════════════════════
with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-label"><span class="panel-label-dot"></span> OUTPUT</div>', unsafe_allow_html=True)

    summary = st.session_state.get('summary', '')
    inp_snap = st.session_state.get('summary_input', active_text or '')

    # ── Stats ──────────────────────────────────────────────────
    in_w  = len(inp_snap.split())  if inp_snap else 0
    out_w = len(summary.split())   if summary  else 0
    comp  = round((1 - out_w / max(in_w,1)) * 100) if in_w else 0

    st.markdown(f"""
    <div class="stats-row">
      <div class="stat"><div class="stat-val">{in_w}</div><div class="stat-lbl">Input Words</div></div>
      <div class="stat"><div class="stat-val">{out_w}</div><div class="stat-lbl">Summary Words</div></div>
      <div class="stat"><div class="stat-val">{comp}%</div><div class="stat-lbl">Compression</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Summary output ─────────────────────────────────────────
    if summary:
        st.markdown(f'<div class="output-card">{summary}</div>', unsafe_allow_html=True)

        # Copy / Audio inline row
        oc1, oc2, oc3 = st.columns([1.5, 1, 1])
        with oc1:
            st.download_button("⬇ Download .txt", summary, "summary.txt",
                               "text/plain", use_container_width=True)
        with oc2:
            tts_lang_sel = st.selectbox("lang", list(TTS_LANGS.keys()),
                                        index=0, label_visibility="collapsed",
                                        key="tts_sel")
        with oc3:
            if st.button("🔊 Audio", use_container_width=True, key="gen_audio"):
                lc = TTS_LANGS.get(tts_lang_sel) or auto_lang(summary)
                with st.spinner("Generating audio…"):
                    ab = tts(summary, lc)
                    if ab:
                        st.session_state['audio_bytes'] = ab
                        st.session_state['audio_lang']  = lc

        if st.session_state.get('audio_bytes'):
            st.audio(st.session_state['audio_bytes'], format="audio/mp3")
            st.download_button("⬇ Download audio (.mp3)",
                               st.session_state['audio_bytes'],
                               "summary_audio.mp3", "audio/mpeg",
                               use_container_width=True)

        # ── Translation ────────────────────────────────────────
        st.markdown('<div class="trans-section">', unsafe_allow_html=True)
        st.markdown('<div class="trans-header">🌐 Translate Summary</div>', unsafe_allow_html=True)

        tc1, tc2 = st.columns([2, 1])
        with tc1:
            tr_lang = st.selectbox("to", list(TRANSLATE_LANGS.keys()),
                                   index=0, label_visibility="collapsed",
                                   key="tr_sel")
        with tc2:
            tr_btn = st.button("Translate →", use_container_width=True,
                               disabled=(TRANSLATE_LANGS.get(tr_lang) is None),
                               key="tr_btn")

        if tr_btn and TRANSLATE_LANGS.get(tr_lang):
            with st.spinner(f"Translating to {tr_lang}…"):
                t = translate(summary, TRANSLATE_LANGS[tr_lang])
                if t:
                    st.session_state['translated']      = t
                    st.session_state['translated_lang'] = tr_lang
                    st.session_state['translated_code'] = TRANSLATE_LANGS[tr_lang]

        if st.session_state.get('translated'):
            tlang = st.session_state.get('translated_lang', '')
            ttext = st.session_state['translated']
            tcode = st.session_state.get('translated_code', 'tr')
            st.markdown(f'<div class="trans-result">{ttext}</div>', unsafe_allow_html=True)

            td1, td2 = st.columns(2)
            with td1:
                st.download_button(f"⬇ Download ({tlang[:6]})", ttext,
                                   f"summary_{tcode}.txt", "text/plain",
                                   use_container_width=True, key="dl_tr")
            with td2:
                if st.button("🔊 Listen", use_container_width=True, key="tts_tr"):
                    lc2 = TTS_LANGS.get(tlang, None) or auto_lang(ttext)
                    with st.spinner(""):
                        ab2 = tts(ttext, lc2)
                        if ab2:
                            st.session_state['trans_audio'] = ab2

            if st.session_state.get('trans_audio'):
                st.audio(st.session_state['trans_audio'], format="audio/mp3")

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="output-card">
          <div class="output-placeholder">
            <div class="output-icon">✦</div>
            <div>Your summary will appear here</div>
            <div style="font-size:0.75rem;opacity:0.5">Paste text → Generate Summary</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:1rem 0 0.5rem;color:#334155;font-size:0.72rem;">
  BTech Data Science · mT5 Multilingual XLSum · Streamlit
</div>
""", unsafe_allow_html=True)