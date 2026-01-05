"""
Edge-TTS Web App - Phiên bản Final 
Tích hợp Edge-TTS + Tùy chọn future Voice Cloning
"""

import streamlit as st
import edge_tts
import asyncio
import os
from datetime import datetime
import base64
import json

# Cấu hình
st.set_page_config(
    page_title="Edge-TTS Pro",
    page_icon="🎤",
    layout="wide"
)

OUTPUT_DIR = "web_outputs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


async def get_voices():
    """Lấy danh sách giọng"""
    return await edge_tts.list_voices()


async def generate_audio(text, voice, rate=None, volume=None, pitch=None):
    """Tạo audio"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = os.path.join(OUTPUT_DIR, f"audio_{timestamp}.mp3")
    
    kwargs = {'text': text, 'voice': voice}
    if rate:
        kwargs['rate'] = rate
    if volume:
        kwargs['volume'] = volume
    if pitch:
        kwargs['pitch'] = pitch
    
    communicate = edge_tts.Communicate(**kwargs)
    await communicate.save(output)
    return output


def get_audio_player(audio_file):
    """Audio player"""
    with open(audio_file, "rb") as f:
        audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()
    return f'<audio controls autoplay style="width:100%;"><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>'


# CSS
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {gap: 24px;}
    .stTabs [data-baseweb="tab"] {height: 50px; padding: 0 20px;}
    .big-font {font-size:20px !important; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# Header
st.title("🎤 Edge-TTS Pro")
st.markdown("**Công cụ chuyển văn bản thành giọng nói chuyên nghiệp**")
st.markdown("---")

# Main Interface
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### 📝 Nhập văn bản")
    text_input = st.text_area(
        "Văn bản cần chuyển:",
        height=250,
        placeholder="Nhập văn bản của bạn tại đây..."
    )
    
    # Samples
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📌 Mẫu tiếng Việt", use_container_width=True):
            st.session_state.text_input = "Xin chào! Tôi là trợ lý ảo sử dụng công nghệ chuyển văn bản thành giọng nói."
            st.rerun()
    with col2:
        if st.button("📌 Mẫu tiếng Anh", use_container_width=True):
            st.session_state.text_input = "Hello! This is a professional text-to-speech system powered by Microsoft Edge."
            st.rerun()
    with col3:
        if st.button("🗑️ Xóa", use_container_width=True):
            st.session_state.text_input = ""
            st.rerun()

with col_right:
    st.markdown("### ⚙️ Cấu hình")
    
    # Load voices
    if 'voices' not in st.session_state:
        with st.spinner("Đang tải giọng..."):
            st.session_state.voices = asyncio.run(get_voices())
    
    voices = st.session_state.voices
    
    # Language filter
    lang_options = {
        "🇻🇳 Tiếng Việt": "vi-VN",
        "🇺🇸 Tiếng Anh Mỹ": "en-US",
        "🇬🇧 Tiếng Anh Anh": "en-GB",
        "🇨🇳 Tiếng Trung": "zh-CN",
        "🇯🇵 Tiếng Nhật": "ja-JP",
        "🇰🇷 Tiếng Hàn": "ko-KR",
        "🇫🇷 Tiếng Pháp": "fr-FR",
        "🇩🇪 Tiếng Đức": "de-DE",
        "🇪🇸 Tiếng Tây Ban Nha": "es-ES"
    }
    
    selected_lang_display = st.selectbox("Ngôn ngữ", list(lang_options.keys()))
    selected_lang = lang_options[selected_lang_display]
    
    # Filter voices
    filtered = [v for v in voices if v["Locale"].startswith(selected_lang)]
    voice_map = {f"{v['ShortName'].split('-')[-1]} ({v['Gender']})": v['ShortName'] for v in filtered}
    
    selected_display = st.selectbox("Giọng nói", list(voice_map.keys()))
    selected_voice = voice_map[selected_display]
    
    # Advanced settings
    with st.expander("🎚️ Tùy chỉnh nâng cao"):
        enable_rate = st.checkbox("Thay đổi tốc độ")
        rate_value = None
        if enable_rate:
            rate = st.slider("Tốc độ (%)", -50, 50, 0, 5)
            rate_value = f"{rate:+d}%" if rate != 0 else None
        
        enable_volume = st.checkbox("Thay đổi âm lượng")
        volume_value = None
        if enable_volume:
            volume = st.slider("Âm lượng (%)", -50, 50, 0, 5)
            volume_value = f"{volume:+d}%" if volume != 0 else None
        
        enable_pitch = st.checkbox("Thay đổi cao độ")
        pitch_value = None
        if enable_pitch:
            pitch = st.slider("Cao độ (Hz)", -50, 50, 0, 5)
            pitch_value = f"{pitch:+d}Hz" if pitch != 0 else None

# Generate button
st.markdown("---")

if st.button("🎙️ TẠO GIỌNG NÓI", type="primary", use_container_width=True):
    if not text_input:
        st.error("⚠️ Vui lòng nhập văn bản!")
    else:
        with st.spinner("🔄 Đang tạo audio..."):
            try:
                output = asyncio.run(generate_audio(
                    text_input, selected_voice, rate_value, volume_value, pitch_value
                ))
                
                st.success("✅ Tạo thành công!")
                
                # Audio player
                st.markdown("### 🔊 Kết quả")
                st.markdown(get_audio_player(output), unsafe_allow_html=True)
                
                # Download
                with open(output, "rb") as f:
                    st.download_button(
                        "⬇️ Tải xuống MP3",
                        f,
                        file_name=os.path.basename(output),
                        mime="audio/mp3",
                        use_container_width=True
                    )
                
                # Info
                st.info(f"""
                **📊 Thông tin:**
                - 🎤 Giọng: {selected_voice}
                - 📝 Ký tự: {len(text_input)}
                - 📁 File: {os.path.basename(output)}
                {f"- ⚡ Tốc độ: {rate_value}" if rate_value else ""}
                {f"- 🔊 Âm lượng: {volume_value}" if volume_value else ""}
                {f"- 🎵 Cao độ: {pitch_value}" if pitch_value else ""}
                """)
                
            except Exception as e:
                st.error(f"❌ Lỗi: {e}")

# Sidebar
with st.sidebar:
    st.markdown("## 📖 Hướng dẫn")
    
    st.markdown("""
    **Cách sử dụng:**
    1. Chọn ngôn ngữ và giọng nói
    2. Nhập văn bản
    3. Tùy chỉnh (nếu muốn)
    4. Nhấn "Tạo giọng nói"
    5. Nghe và tải xuống
    
    **Mẹo:**
    - Văn bản càng ngắn, xử lý càng nhanh
    - Dùng mẫu để test nhanh
    - Tùy chỉnh tốc độ/âm lượng để phù hợp
    """)
    
    st.markdown("---")
    
    st.markdown("## 🎭 Voice Cloning")
    st.info("""
    **Tính năng Voice Cloning:**
    
    Để clone giọng nói của bạn (giống 99%), sử dụng một trong các dịch vụ sau:
    
    **1. ElevenLabs** ⭐
    - Chất lượng tốt nhất
    - Clone từ 1 phút audio
    - elevenlabs.io
    
    **2. PlayHT**
    - Giá rẻ hơn
    - Nhiều tùy chọn
    - play.ht
    
    **3. Microsoft Azure**
    - Miễn phí thử
    - Ổn định
    - azure.microsoft.com
    """)
    
    # Stats
    if os.path.exists(OUTPUT_DIR):
        files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.mp3')]
        st.metric("📊 File đã tạo", len(files))

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🎤 Edge-TTS Pro | Powered by Microsoft Edge Text-to-Speech</p>
    <p><small>Version 1.0 | © 2026</small></p>
</div>
""", unsafe_allow_html=True)
