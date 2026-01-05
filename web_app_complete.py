"""
Edge-TTS Tool - Beautiful & Clean Interface
"""

import streamlit as st
import edge_tts
import asyncio
import os
from datetime import datetime
import base64

st.set_page_config(
    page_title="Edge-TTS Tool",
    page_icon="🎤",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* Hide sidebar completely */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Main container */
    .main {
        padding: 2rem;
    }
    
    /* Title styling */
    .big-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 3rem;
    }
    
    /* Input area */
    .stTextArea textarea {
        font-size: 1.1rem;
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        padding: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        transition: transform 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        border-radius: 10px;
        background-color: #f8f9fa;
        font-weight: 600;
    }
    
    /* Audio player */
    audio {
        width: 100%;
        margin: 1rem 0;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stInfo {
        border-radius: 10px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def cleanup_old_files(max_files=50):
    """Tự động xóa file cũ khi quá 50 file"""
    try:
        files = [os.path.join(OUTPUT_DIR, f) for f in os.listdir(OUTPUT_DIR) if f.endswith('.mp3')]
        if len(files) > max_files:
            # Sắp xếp theo thời gian tạo
            files.sort(key=os.path.getctime)
            # Xóa file cũ nhất
            for f in files[:len(files) - max_files]:
                os.remove(f)
    except:
        pass

async def get_voices():
    return await edge_tts.list_voices()

async def generate_tts(text, voice, rate, volume, pitch):
    # Cleanup trước khi tạo file mới
    cleanup_old_files()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(OUTPUT_DIR, f"tts_{timestamp}.mp3")
    
    # Fix format: Edge-TTS requires "+0%" not "0%"
    if rate == "0%":
        rate = "+0%"
    if volume == "0%":
        volume = "+0%"
    if pitch == "0Hz":
        pitch = "+0Hz"
    
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        volume=volume,
        pitch=pitch
    )
    
    await communicate.save(output_file)
    return output_file

def get_audio_download_link(file_path):
    with open(file_path, "rb") as f:
        audio_bytes = f.read()
    b64 = base64.b64encode(audio_bytes).decode()
    filename = os.path.basename(file_path)
    return f"""
    <div style="text-align: center; margin: 1rem 0;">
        <a href="data:audio/mp3;base64,{b64}" download="{filename}" 
           style="display: inline-block; padding: 0.8rem 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                  color: white; text-decoration: none; border-radius: 10px; font-weight: 600; transition: transform 0.2s;">
            📥 Download MP3
        </a>
    </div>
    """

# Header
st.markdown('<div class="big-title">HXT Edge-TTS</div>', unsafe_allow_html=True)

# Main content
st.markdown("### 📝 Văn bản của bạn")
text_input = st.text_area(
    "",
    height=180,
    placeholder="Nhập văn bản cần chuyển thành giọng nói...\n\nHỗ trợ: Tiếng Việt, English, 中文, 日本語, và nhiều ngôn ngữ khác",
    label_visibility="collapsed"
)

if text_input:
    char_count = len(text_input)
    st.caption(f"✍️ {char_count} ký tự")

st.markdown("---")

# Voice selection in 2 columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎙️ Chọn giọng")
    
    if 'voices' not in st.session_state:
        with st.spinner("Đang tải..."):
            st.session_state.voices = asyncio.run(get_voices())
    
    voices = st.session_state.voices
    
    # Language filter
    languages = {
        "vi": "🇻🇳 Tiếng Việt",
        "en": "🇬🇧 English",
        "zh": "🇨🇳 中文",
        "ja": "🇯🇵 日本語",
        "ko": "🇰🇷 한국어",
        "fr": "🇫🇷 Français",
        "de": "🇩🇪 Deutsch",
        "es": "🇪🇸 Español"
    }
    
    selected_lang = st.selectbox(
        "Ngôn ngữ",
        ["All"] + list(languages.keys()),
        format_func=lambda x: "🌍 Tất cả" if x == "All" else languages.get(x, x)
    )
    
    if selected_lang != "All":
        filtered_voices = [v for v in voices if v['Locale'].startswith(selected_lang)]
    else:
        filtered_voices = voices
    
    voice_options = {
        f"{v['ShortName'].split('-')[-1]} ({v['Gender']})": v['ShortName'] 
        for v in filtered_voices
    }
    
    selected_voice_display = st.selectbox(
        "Giọng nói",
        list(voice_options.keys())
    )
    selected_voice = voice_options[selected_voice_display]

with col2:
    st.markdown("### ⚙️ Tùy chỉnh")
    
    rate = st.select_slider(
        "🎚️ Tốc độ",
        options=["-50%", "-25%", "+0%", "+25%", "+50%"],
        value="+0%"
    )
    
    volume = st.select_slider(
        "🔊 Âm lượng",
        options=["-50%", "-25%", "+0%", "+25%", "+50%"],
        value="+0%"
    )
    
    pitch = st.select_slider(
        "🎵 Cao độ",
        options=["-50Hz", "-25Hz", "+0Hz", "+25Hz", "+50Hz"],
        value="+0Hz"
    )

st.markdown("---")

# Generate button
st.markdown("<br>", unsafe_allow_html=True)
generate_btn = st.button("🎵 TẠO AUDIO", type="primary")

if generate_btn:
    if not text_input.strip():
        st.error("❌ Vui lòng nhập văn bản!")
    else:
        with st.spinner("🎨 Đang tạo audio..."):
            try:
                output_file = asyncio.run(generate_tts(
                    text=text_input,
                    voice=selected_voice,
                    rate=rate,
                    volume=volume,
                    pitch=pitch
                ))
                
                st.success("✅ Hoàn thành!")
                
                # Audio player
                st.audio(output_file, format='audio/mp3')
                
                # Download button
                st.markdown(get_audio_download_link(output_file), unsafe_allow_html=True)
                
                # File info
                file_size = os.path.getsize(output_file) / 1024
                st.caption(f"📁 {os.path.basename(output_file)} • 💾 {file_size:.1f} KB")
                
            except Exception as e:
                st.error(f"❌ Lỗi: {str(e)}")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #999; padding: 2rem 0;">
        <p>🎤 <strong>Edge-TTS Tool</strong></p>
        <p>Powered by Microsoft Edge • 100+ AI Voices</p>
    </div>
    """,
    unsafe_allow_html=True
)
