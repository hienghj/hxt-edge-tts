#!/usr/bin/env python3
"""Demo tự động của Edge-TTS tool"""

import asyncio
import edge_tts
import os

# Tạo thư mục output
OUTPUT_DIR = "demo_outputs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


async def demo():
    """Chạy demo các tính năng"""
    
    print("\n" + "="*70)
    print("🎤 EDGE-TTS TOOL - DEMO TỰ ĐỘNG".center(70))
    print("="*70 + "\n")
    
    # Demo 1: Tạo audio tiếng Việt
    print("📌 Demo 1: Tạo audio tiếng Việt với giọng nữ")
    print("-" * 70)
    text1 = "Xin chào! Đây là công nghệ chuyển văn bản thành giọng nói của Microsoft Edge."
    voice1 = "vi-VN-HoaiMyNeural"
    output1 = os.path.join(OUTPUT_DIR, "demo1_vietnam_female.mp3")
    
    print(f"📝 Văn bản: {text1}")
    print(f"🎤 Giọng: {voice1}")
    
    communicate = edge_tts.Communicate(text1, voice1)
    await communicate.save(output1)
    
    print(f"✅ Đã lưu: {output1}\n")
    await asyncio.sleep(1)
    
    # Demo 2: Tạo audio tiếng Việt giọng nam
    print("📌 Demo 2: Tạo audio tiếng Việt với giọng nam")
    print("-" * 70)
    text2 = "Chào mừng bạn đến với Edge TTS. Tôi là giọng nam tiếng Việt."
    voice2 = "vi-VN-NamMinhNeural"
    output2 = os.path.join(OUTPUT_DIR, "demo2_vietnam_male.mp3")
    
    print(f"📝 Văn bản: {text2}")
    print(f"🎤 Giọng: {voice2}")
    
    communicate = edge_tts.Communicate(text2, voice2)
    await communicate.save(output2)
    
    print(f"✅ Đã lưu: {output2}\n")
    await asyncio.sleep(1)
    
    # Demo 3: Tạo audio tiếng Anh
    print("📌 Demo 3: Tạo audio tiếng Anh")
    print("-" * 70)
    text3 = "Hello! This is Microsoft Edge Text-to-Speech technology."
    voice3 = "en-US-JennyNeural"
    output3 = os.path.join(OUTPUT_DIR, "demo3_english.mp3")
    
    print(f"📝 Văn bản: {text3}")
    print(f"🎤 Giọng: {voice3}")
    
    communicate = edge_tts.Communicate(text3, voice3)
    await communicate.save(output3)
    
    print(f"✅ Đã lưu: {output3}\n")
    await asyncio.sleep(1)
    
    # Demo 4: Thay đổi tốc độ
    print("📌 Demo 4: Thay đổi tốc độ nói (chậm hơn)")
    print("-" * 70)
    text4 = "Tôi đang nói chậm hơn bình thường."
    voice4 = "vi-VN-HoaiMyNeural"
    output4 = os.path.join(OUTPUT_DIR, "demo4_slow_rate.mp3")
    
    print(f"📝 Văn bản: {text4}")
    print(f"🎤 Giọng: {voice4}")
    print(f"⚙️  Tốc độ: -50%")
    
    communicate = edge_tts.Communicate(text4, voice4, rate="-50%")
    await communicate.save(output4)
    
    print(f"✅ Đã lưu: {output4}\n")
    await asyncio.sleep(1)
    
    # Demo 5: Thay đổi cao độ
    print("📌 Demo 5: Thay đổi cao độ giọng nói")
    print("-" * 70)
    text5 = "Giọng nói của tôi có cao độ khác thường."
    voice5 = "vi-VN-NamMinhNeural"
    output5 = os.path.join(OUTPUT_DIR, "demo5_low_pitch.mp3")
    
    print(f"📝 Văn bản: {text5}")
    print(f"🎤 Giọng: {voice5}")
    print(f"⚙️  Cao độ: -50Hz")
    
    communicate = edge_tts.Communicate(text5, voice5, pitch="-50Hz")
    await communicate.save(output5)
    
    print(f"✅ Đã lưu: {output5}\n")
    await asyncio.sleep(1)
    
    # Hiển thị danh sách giọng tiếng Việt
    print("📌 Danh sách giọng nói tiếng Việt có sẵn:")
    print("-" * 70)
    
    voices = await edge_tts.list_voices()
    vi_voices = [v for v in voices if v["Locale"].startswith("vi-VN")]
    
    for voice in vi_voices:
        name = voice["ShortName"]
        gender = voice["Gender"]
        print(f"   🎤 {name} ({gender})")
    
    print("\n" + "="*70)
    print("✅ HOÀN THÀNH DEMO!".center(70))
    print("="*70)
    print(f"\n📁 Tất cả file đã được lưu trong thư mục: {OUTPUT_DIR}/\n")


if __name__ == "__main__":
    try:
        asyncio.run(demo())
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
