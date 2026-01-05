#!/usr/bin/env python3
"""Tool chuyển văn bản thành giọng nói tương tác"""

import asyncio
import edge_tts
import os
from datetime import datetime

# Cấu hình mặc định
DEFAULT_VOICE = "vi-VN-HoaiMyNeural"
OUTPUT_DIR = "audio_outputs"

# Tạo thư mục output nếu chưa có
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


async def generate_audio(text: str, voice: str, filename: str) -> None:
    """Tạo file audio từ văn bản"""
    output_path = os.path.join(OUTPUT_DIR, filename)
    
    print(f"\n🎙️  Đang tạo audio...")
    print(f"   Văn bản: {text}")
    print(f"   Giọng nói: {voice}")
    print(f"   File: {output_path}")
    
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    
    print(f"✅ Hoàn thành! File đã lưu tại: {output_path}\n")


async def list_voices(language_code: str = None) -> None:
    """Liệt kê các giọng nói có sẵn"""
    voices = await edge_tts.list_voices()
    
    print("\n📋 Danh sách giọng nói có sẵn:\n")
    print(f"{'Tên':<35} {'Giới tính':<10} {'Ngôn ngữ':<10}")
    print("-" * 60)
    
    for voice in voices:
        if language_code is None or voice["Locale"].startswith(language_code):
            name = voice["ShortName"]
            gender = voice["Gender"]
            locale = voice["Locale"]
            print(f"{name:<35} {gender:<10} {locale:<10}")


async def main_menu():
    """Menu chính của tool"""
    print("\n" + "="*60)
    print("🎤 EDGE-TTS - Chuyển văn bản thành giọng nói".center(60))
    print("="*60)
    
    while True:
        print("\n📌 Chọn chức năng:")
        print("1. Tạo audio tiếng Việt")
        print("2. Tạo audio tiếng Anh")
        print("3. Tạo audio với giọng tùy chỉnh")
        print("4. Liệt kê giọng tiếng Việt")
        print("5. Liệt kê giọng tiếng Anh")
        print("6. Liệt kê tất cả giọng nói")
        print("0. Thoát")
        
        choice = input("\n👉 Nhập lựa chọn (0-6): ").strip()
        
        if choice == "0":
            print("\n👋 Cảm ơn bạn đã sử dụng! Tạm biệt!")
            break
            
        elif choice == "1":
            text = input("📝 Nhập văn bản tiếng Việt: ").strip()
            if text:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"vietnamese_{timestamp}.mp3"
                await generate_audio(text, "vi-VN-HoaiMyNeural", filename)
                
        elif choice == "2":
            text = input("📝 Nhập văn bản tiếng Anh: ").strip()
            if text:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"english_{timestamp}.mp3"
                await generate_audio(text, "en-US-JennyNeural", filename)
                
        elif choice == "3":
            text = input("📝 Nhập văn bản: ").strip()
            voice = input("🎤 Nhập tên giọng nói (vd: vi-VN-NamMinhNeural): ").strip()
            if text and voice:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"custom_{timestamp}.mp3"
                await generate_audio(text, voice, filename)
                
        elif choice == "4":
            await list_voices("vi-VN")
            
        elif choice == "5":
            await list_voices("en-US")
            
        elif choice == "6":
            await list_voices()
            
        else:
            print("❌ Lựa chọn không hợp lệ!")
        
        input("\n⏎ Nhấn Enter để tiếp tục...")


if __name__ == "__main__":
    try:
        asyncio.run(main_menu())
    except KeyboardInterrupt:
        print("\n\n👋 Đã dừng chương trình!")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
