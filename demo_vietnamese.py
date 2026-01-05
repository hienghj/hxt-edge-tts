#!/usr/bin/env python3
"""Demo edge-tts với tiếng Việt"""

import asyncio
import edge_tts

TEXT = "Xin chào! Tôi là trợ lý ảo sử dụng công nghệ chuyển văn bản thành giọng nói của Microsoft Edge."
VOICE = "vi-VN-HoaiMyNeural"
OUTPUT_FILE = "demo_vietnamese.mp3"


async def main() -> None:
    """Hàm chính - tạo file audio tiếng Việt"""
    print(f"Đang tạo file audio: {OUTPUT_FILE}")
    print(f"Văn bản: {TEXT}")
    print(f"Giọng nói: {VOICE}")
    
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)
    
    print(f"✓ Hoàn thành! File đã được lưu tại: {OUTPUT_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
