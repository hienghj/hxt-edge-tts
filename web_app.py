"""
Edge-TTS Web Interface - Giao diện web chuyển văn bản thành giọng nói
"""

import streamlit as st
import edge_tts
import asyncio
import os
from datetime import datetime
import base64

# Cấu hình trang
st.set_page_config(
    page_title="Edge-TTS Web",
    page_icon="🎤",
    layout="wide"
)

# Tạo thư mục output
OUTPUT_DIR = "web_outputs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


async def get_voices_list():
    """Lấy danh sách giọng nói"""
    voices = await edge_tts.list_voices()
    return voices


async def generate_audio(text, voice, rate=None, volume=None, pitch=None):
    """Tạo file audio"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(OUTPUT_DIR, f"audio_{timestamp}.mp3")
    
    kwargs = {'text': text, 'voice': voice}
    if rate:
        kwargs['rate'] = rate
    if volume:
        kwargs['volume'] = volume
    if pitch:
        kwargs['pitch'] = pitch
    
    communicate = edge_tts.Communicate(**kwargs)
    await communicate.save(output_file)
    
    return output_file


def get_audio_player(audio_file):
    """Tạo audio player HTML"""
    with open(audio_file, "rb") as f:
        audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
        <audio controls autoplay style="width: 100%;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
    """
    return audio_html


# Header
st.title("🎤 Edge-TTS - Chuyển văn bản thành giọng nói")
st.markdown("---")

# Sidebar - Cấu hình
with st.sidebar:
    st.header("⚙️ Cấu hình")
    
    # Load danh sách giọng nói
    if 'voices' not in st.session_state:
        with st.spinner("Đang tải danh sách giọng nói..."):
            st.session_state.voices = asyncio.run(get_voices_list())
    
    voices = st.session_state.voices
    
    # Lọc theo ngôn ngữ
    language_filter = st.selectbox(
        "🌍 Chọn ngôn ngữ",
        ["Tiếng Việt (vi-VN)", "Tiếng Anh Mỹ (en-US)", "Tiếng Anh Anh (en-GB)", 
         "Tiếng Trung (zh-CN)", "Tiếng Nhật (ja-JP)", "Tiếng Hàn (ko-KR)", "Tất cả"]
    )
    
    # Map language filter
    lang_map = {
        "Tiếng Việt (vi-VN)": "vi-VN",
        "Tiếng Anh Mỹ (en-US)": "en-US",
        "Tiếng Anh Anh (en-GB)": "en-GB",
        "Tiếng Trung (zh-CN)": "zh-CN",
        "Tiếng Nhật (ja-JP)": "ja-JP",
        "Tiếng Hàn (ko-KR)": "ko-KR",
        "Tất cả": None
    }
    
    selected_lang = lang_map[language_filter]
    
    # Lọc giọng nói
    if selected_lang:
        filtered_voices = [v for v in voices if v["Locale"].startswith(selected_lang)]
    else:
        filtered_voices = voices
    
    # Tạo danh sách hiển thị giọng
    voice_options = {}
    for v in filtered_voices:
        display_name = f"{v['ShortName']} ({v['Gender']})"
        voice_options[display_name] = v['ShortName']
    
    selected_voice_display = st.selectbox(
        "🎤 Chọn giọng nói",
        list(voice_options.keys())
    )
    selected_voice = voice_options[selected_voice_display]
    
    st.markdown("---")
    st.subheader("🎚️ Tùy chỉnh giọng nói")
    
    # Tốc độ
    enable_rate = st.checkbox("Thay đổi tốc độ")
    rate_value = None
    if enable_rate:
        rate_slider = st.slider("Tốc độ (%)", -100, 100, 0, 10)
        rate_value = f"{rate_slider:+d}%" if rate_slider != 0 else None
    
    # Âm lượng
    enable_volume = st.checkbox("Thay đổi âm lượng")
    volume_value = None
    if enable_volume:
        volume_slider = st.slider("Âm lượng (%)", -100, 100, 0, 10)
        volume_value = f"{volume_slider:+d}%" if volume_slider != 0 else None
    
    # Cao độ
    enable_pitch = st.checkbox("Thay đổi cao độ")
    pitch_value = None
    if enable_pitch:
        pitch_slider = st.slider("Cao độ (Hz)", -100, 100, 0, 10)
        pitch_value = f"{pitch_slider:+d}Hz" if pitch_slider != 0 else None

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Nhập văn bản")
    
    # Text input
    text_input = st.text_area(
        "Nhập văn bản cần chuyển thành giọng nói:",
        height=200,
        placeholder="Nhập văn bản của bạn tại đây...",
        help="Văn bản sẽ được chuyển thành giọng nói với giọng đã chọn"
    )
    
    # Các nút mẫu
    st.markdown("**Văn bản mẫu:**")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("📌 Mẫu 1"):
            text_input = "Xin chào! Đây là công nghệ chuyển văn bản thành giọng nói của Microsoft Edge."
            st.rerun()
    
    with col_sample2:
        if st.button("📌 Mẫu 2"):
            text_input = "Chào mừng bạn đến với Edge TTS. Đây là một công cụ rất hữu ích và dễ sử dụng."
            st.rerun()
    
    with col_sample3:
        if st.button("📌 Mẫu 3"):
            text_input = "Hello! This is Microsoft Edge Text-to-Speech technology. It's very easy to use!"
            st.rerun()
    
    st.markdown("---")
    
    # Nút tạo audio
    generate_button = st.button("🎙️ Tạo giọng nói", type="primary", use_container_width=True)
    
    if generate_button:
        if not text_input:
            st.error("⚠️ Vui lòng nhập văn bản!")
        else:
            with st.spinner("🔄 Đang tạo audio..."):
                try:
                    output_file = asyncio.run(
                        generate_audio(text_input, selected_voice, rate_value, volume_value, pitch_value)
                    )
                    
                    st.success("✅ Tạo audio thành công!")
                    
                    # Hiển thị audio player
                    st.markdown("### 🔊 Phát audio")
                    audio_html = get_audio_player(output_file)
                    st.markdown(audio_html, unsafe_allow_html=True)
                    
                    # Download button
                    with open(output_file, "rb") as f:
                        st.download_button(
                            label="⬇️ Tải xuống file MP3",
                            data=f,
                            file_name=os.path.basename(output_file),
                            mime="audio/mp3",
                            use_container_width=True
                        )
                    
                    # Thông tin
                    st.info(f"""
                    📊 **Thông tin:**
                    - 🎤 Giọng: {selected_voice}
                    - 📝 Độ dài văn bản: {len(text_input)} ký tự
                    - 📁 File: {os.path.basename(output_file)}
                    """)
                    
                except Exception as e:
                    st.error(f"❌ Lỗi: {str(e)}")

with col2:
    st.subheader("ℹ️ Thông tin")
    
    # Thông tin giọng đã chọn
    selected_voice_info = next((v for v in filtered_voices if v['ShortName'] == selected_voice), None)
    if selected_voice_info:
        st.info(f"""
        **Giọng đã chọn:**
        - 🎤 Tên: {selected_voice_info['ShortName']}
        - 👤 Giới tính: {selected_voice_info['Gender']}
        - 🌍 Ngôn ngữ: {selected_voice_info['Locale']}
        """)
    
    # Cài đặt hiện tại
    if rate_value or volume_value or pitch_value:
        st.markdown("**Cài đặt hiện tại:**")
        settings = []
        if rate_value:
            settings.append(f"⚡ Tốc độ: {rate_value}")
        if volume_value:
            settings.append(f"🔊 Âm lượng: {volume_value}")
        if pitch_value:
            settings.append(f"🎵 Cao độ: {pitch_value}")
        
        for setting in settings:
            st.write(setting)
    
    st.markdown("---")
    
    # Hướng dẫn
    with st.expander("📖 Hướng dẫn sử dụng"):
        st.markdown("""
        **Các bước sử dụng:**
        1. Chọn ngôn ngữ và giọng nói ở thanh bên trái
        2. Nhập văn bản cần chuyển đổi
        3. Tùy chỉnh tốc độ, âm lượng, cao độ (nếu cần)
        4. Nhấn "Tạo giọng nói"
        5. Nghe và tải xuống file audio
        
        **Mẹo:**
        - Văn bản càng ngắn, tốc độ xử lý càng nhanh
        - Có thể dùng văn bản mẫu để test
        - File audio sẽ được lưu trong thư mục `web_outputs`
        """)
    
    # Thống kê
    if os.path.exists(OUTPUT_DIR):
        files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.mp3')]
        st.metric("📊 Số file đã tạo", len(files))

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🎤 Edge-TTS Web Interface | Powered by Microsoft Edge TTS</p>
</div>
""", unsafe_allow_html=True)
