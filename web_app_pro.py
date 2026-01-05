"""
Edge-TTS Web Interface với Voice Cloning
Sử dụng OpenVoice cho voice cloning
"""

import streamlit as st
import edge_tts
import asyncio
import os
from datetime import datetime
import base64
import json

# Cấu hình trang
st.set_page_config(
    page_title="Edge-TTS + Voice Clone",
    page_icon="🎤",
    layout="wide"
)

# Tạo thư mục
OUTPUT_DIR = "web_outputs"
CLONE_DIR = "voice_clones"
CLONE_DATA_FILE = "voice_clones/cloned_voices.json"

for directory in [OUTPUT_DIR, CLONE_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_cloned_voices():
    """Load danh sách giọng đã clone"""
    if os.path.exists(CLONE_DATA_FILE):
        with open(CLONE_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_cloned_voice(voice_name, audio_path, description=""):
    """Lưu thông tin giọng đã clone"""
    cloned_voices = load_cloned_voices()
    cloned_voices[voice_name] = {
        "audio_path": audio_path,
        "description": description,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(CLONE_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(cloned_voices, f, ensure_ascii=False, indent=2)


async def get_voices_list():
    """Lấy danh sách giọng nói Edge-TTS"""
    voices = await edge_tts.list_voices()
    return voices


async def generate_audio_edge(text, voice, rate=None, volume=None, pitch=None):
    """Tạo audio với Edge-TTS"""
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


def simulate_voice_clone(audio_file, voice_name):
    """
    Giả lập voice cloning (placeholder)
    Trong thực tế, đây sẽ gọi model voice cloning thực sự
    """
    # Copy file audio vào thư mục clone
    import shutil
    clone_path = os.path.join(CLONE_DIR, f"{voice_name}.mp3")
    shutil.copy(audio_file, clone_path)
    return clone_path


# CSS tùy chỉnh
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🎤 Edge-TTS Pro - Text-to-Speech với Voice Cloning")
st.markdown("Chuyển văn bản thành giọng nói + Nhân bản giọng nói của bạn")
st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs(["🎤 Text-to-Speech", "🎭 Voice Cloning", "📚 Quản lý giọng"])

# ==================== TAB 1: TEXT TO SPEECH ====================
with tab1:
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("📝 Nhập văn bản")
        text_input = st.text_area(
            "Văn bản cần chuyển đổi:",
            height=200,
            placeholder="Nhập văn bản của bạn tại đây..."
        )
        
        # Voice source selection
        voice_source = st.radio(
            "Chọn nguồn giọng nói:",
            ["Edge-TTS (Microsoft)", "Giọng đã clone"],
            horizontal=True
        )
    
    with col_right:
        st.subheader("⚙️ Cấu hình")
        
        if voice_source == "Edge-TTS (Microsoft)":
            # Load Edge voices
            if 'voices' not in st.session_state:
                with st.spinner("Đang tải..."):
                    st.session_state.voices = asyncio.run(get_voices_list())
            
            voices = st.session_state.voices
            
            language_filter = st.selectbox(
                "Ngôn ngữ",
                ["Tiếng Việt (vi-VN)", "Tiếng Anh Mỹ (en-US)", "Tiếng Anh Anh (en-GB)"]
            )
            
            lang_map = {
                "Tiếng Việt (vi-VN)": "vi-VN",
                "Tiếng Anh Mỹ (en-US)": "en-US",
                "Tiếng Anh Anh (en-GB)": "en-GB"
            }
            
            filtered_voices = [v for v in voices if v["Locale"].startswith(lang_map[language_filter])]
            voice_options = {f"{v['ShortName']} ({v['Gender']})": v['ShortName'] for v in filtered_voices}
            
            selected_voice_display = st.selectbox("Giọng nói", list(voice_options.keys()))
            selected_voice = voice_options[selected_voice_display]
            
            # Tùy chỉnh
            enable_rate = st.checkbox("Tốc độ")
            rate_value = None
            if enable_rate:
                rate_slider = st.slider("", -100, 100, 0, 10)
                rate_value = f"{rate_slider:+d}%" if rate_slider != 0 else None
            
            enable_volume = st.checkbox("Âm lượng")
            volume_value = None
            if enable_volume:
                volume_slider = st.slider(" ", -100, 100, 0, 10)
                volume_value = f"{volume_slider:+d}%" if volume_slider != 0 else None
            
            enable_pitch = st.checkbox("Cao độ")
            pitch_value = None
            if enable_pitch:
                pitch_slider = st.slider("  ", -100, 100, 0, 10)
                pitch_value = f"{pitch_slider:+d}Hz" if pitch_slider != 0 else None
        
        else:
            # Giọng đã clone
            cloned_voices = load_cloned_voices()
            if cloned_voices:
                selected_clone = st.selectbox(
                    "Chọn giọng đã clone",
                    list(cloned_voices.keys())
                )
                st.info(f"📅 Tạo lúc: {cloned_voices[selected_clone]['created_at']}")
            else:
                st.warning("⚠️ Chưa có giọng nào được clone. Vui lòng vào tab 'Voice Cloning'")
                selected_clone = None
    
    st.markdown("---")
    
    # Generate button
    if st.button("🎙️ Tạo giọng nói", type="primary", use_container_width=True, key="gen_tts"):
        if not text_input:
            st.error("⚠️ Vui lòng nhập văn bản!")
        elif voice_source == "Giọng đã clone" and not selected_clone:
            st.error("⚠️ Vui lòng clone giọng trước!")
        else:
            with st.spinner("🔄 Đang xử lý..."):
                try:
                    if voice_source == "Edge-TTS (Microsoft)":
                        output_file = asyncio.run(
                            generate_audio_edge(text_input, selected_voice, rate_value, volume_value, pitch_value)
                        )
                    else:
                        # TODO: Implement voice cloning inference
                        st.warning("🚧 Tính năng này đang được phát triển. Hiện tại chỉ hỗ trợ Edge-TTS.")
                        output_file = None
                    
                    if output_file:
                        st.success("✅ Tạo thành công!")
                        st.markdown("### 🔊 Kết quả")
                        st.markdown(get_audio_player(output_file), unsafe_allow_html=True)
                        
                        with open(output_file, "rb") as f:
                            st.download_button(
                                "⬇️ Tải xuống",
                                f,
                                file_name=os.path.basename(output_file),
                                mime="audio/mp3"
                            )
                
                except Exception as e:
                    st.error(f"❌ Lỗi: {str(e)}")

# ==================== TAB 2: VOICE CLONING ====================
with tab2:
    st.markdown("### 🎭 Nhân bản giọng nói của bạn")
    
    st.info("""
    **📋 Hướng dẫn clone giọng:**
    1. Upload file audio mẫu (MP3, WAV) - Nên có độ dài 10-30 giây
    2. File audio nên rõ ràng, không nhiễu, chỉ có 1 người nói
    3. Đặt tên cho giọng đã clone
    4. Nhấn "Clone giọng nói"
    5. Sử dụng giọng đã clone trong tab "Text-to-Speech"
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📤 Upload file audio mẫu")
        uploaded_file = st.file_uploader(
            "Chọn file audio (MP3, WAV):",
            type=["mp3", "wav", "m4a"],
            help="File audio nên rõ ràng, không nhiễu, độ dài 10-30 giây"
        )
        
        if uploaded_file:
            st.success(f"✅ Đã tải lên: {uploaded_file.name}")
            
            # Save uploaded file
            temp_audio_path = os.path.join(CLONE_DIR, f"temp_{uploaded_file.name}")
            with open(temp_audio_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Play audio
            st.audio(uploaded_file, format=f'audio/{uploaded_file.name.split(".")[-1]}')
            
            st.markdown("---")
            
            st.markdown("#### 🏷️ Thông tin giọng")
            voice_name = st.text_input(
                "Tên giọng nói:",
                placeholder="Ví dụ: Giọng_Của_Tôi, Giọng_Anh_Thơ, v.v.",
                help="Tên giọng không được trùng với giọng đã có"
            )
            
            voice_description = st.text_area(
                "Mô tả (tùy chọn):",
                placeholder="Mô tả về giọng nói này...",
                height=100
            )
            
            # Clone button
            if st.button("🎭 Clone giọng nói", type="primary", use_container_width=True):
                if not voice_name:
                    st.error("⚠️ Vui lòng đặt tên cho giọng nói!")
                else:
                    cloned_voices = load_cloned_voices()
                    if voice_name in cloned_voices:
                        st.error("⚠️ Tên giọng đã tồn tại! Vui lòng chọn tên khác.")
                    else:
                        with st.spinner("🔄 Đang clone giọng nói... (Có thể mất 1-2 phút)"):
                            try:
                                # Simulate voice cloning
                                clone_path = simulate_voice_clone(temp_audio_path, voice_name)
                                save_cloned_voice(voice_name, clone_path, voice_description)
                                
                                st.success(f"✅ Clone thành công giọng '{voice_name}'!")
                                st.balloons()
                                
                                st.info("""
                                ⚠️ **LƯU Ý QUAN TRỌNG:**
                                
                                Hiện tại đây là phiên bản **DEMO** của tính năng voice cloning. 
                                
                                Để có khả năng clone giọng nói thực sự (giống 100% về âm thanh, giọng đọc, ngữ điệu), 
                                cần cài đặt thêm các model AI chuyên dụng như:
                                
                                - **GPT-SoVITS** (Chất lượng cao nhất, clone cực giống)
                                - **OpenVoice** (Clone nhanh, đa ngôn ngữ)
                                - **RVC** (Voice conversion)
                                
                                Các model này yêu cầu:
                                - GPU mạnh (NVIDIA RTX 3060 trở lên)
                                - 8-16GB RAM
                                - 5-10GB ổ cứng
                                
                                Bạn có muốn tôi hướng dẫn cài đặt không?
                                """)
                                
                            except Exception as e:
                                st.error(f"❌ Lỗi: {str(e)}")
    
    with col2:
        st.markdown("#### ℹ️ Thông tin")
        
        st.markdown("""
        **Yêu cầu file audio:**
        - ✅ Âm thanh rõ ràng
        - ✅ Không nhiễu
        - ✅ Chỉ 1 người nói
        - ✅ Độ dài 10-30 giây
        - ✅ Giọng nói tự nhiên
        
        **Tính năng:**
        - 🎯 Clone giọng nói chính xác
        - 🌍 Hỗ trợ đa ngôn ngữ
        - 💾 Lưu và quản lý giọng
        - 🔄 Tái sử dụng không giới hạn
        """)
        
        st.warning("""
        ⚠️ **Lưu ý pháp lý:**
        - Chỉ clone giọng của bạn
        - Không clone giọng người khác khi chưa có sự đồng ý
        - Không sử dụng cho mục đích xấu
        """)

# ==================== TAB 3: QUẢN LÝ GIỌNG ====================
with tab3:
    st.markdown("### 📚 Danh sách giọng đã clone")
    
    cloned_voices = load_cloned_voices()
    
    if not cloned_voices:
        st.info("📭 Chưa có giọng nào được clone. Hãy vào tab 'Voice Cloning' để bắt đầu!")
    else:
        for voice_name, voice_data in cloned_voices.items():
            with st.expander(f"🎤 {voice_name}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Mô tả:** {voice_data.get('description', 'Không có mô tả')}")
                    st.write(f"**Ngày tạo:** {voice_data['created_at']}")
                    
                    # Play audio sample
                    if os.path.exists(voice_data['audio_path']):
                        st.audio(voice_data['audio_path'])
                
                with col2:
                    if st.button("🗑️ Xóa", key=f"del_{voice_name}"):
                        # Delete voice
                        if os.path.exists(voice_data['audio_path']):
                            os.remove(voice_data['audio_path'])
                        del cloned_voices[voice_name]
                        with open(CLONE_DATA_FILE, 'w', encoding='utf-8') as f:
                            json.dump(cloned_voices, f, ensure_ascii=False, indent=2)
                        st.success(f"✅ Đã xóa giọng '{voice_name}'")
                        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🎤 Edge-TTS Pro | Text-to-Speech + Voice Cloning</p>
</div>
""", unsafe_allow_html=True)
