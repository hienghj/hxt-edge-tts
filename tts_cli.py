#!/usr/bin/env python3
"""Edge-TTS CLI Tool - Công cụ chuyển văn bản thành giọng nói đơn giản"""

import asyncio
import edge_tts
import argparse
import os
from datetime import datetime


async def generate_speech(text: str, voice: str, output: str, rate: str = None, 
                         volume: str = None, pitch: str = None, 
                         with_subtitles: bool = False):
    """Tạo file audio từ văn bản"""
    
    print(f"\n🎙️  Đang xử lý...")
    print(f"   📝 Văn bản: {text}")
    print(f"   🎤 Giọng: {voice}")
    
    # Tạo communicate object với các tham số
    kwargs = {'text': text, 'voice': voice}
    if rate:
        kwargs['rate'] = rate
    if volume:
        kwargs['volume'] = volume
    if pitch:
        kwargs['pitch'] = pitch
    
    # Lưu audio và subtitles
    if with_subtitles:
        subtitle_file = output.rsplit('.', 1)[0] + '.srt'
        submaker = edge_tts.SubMaker()
        
        communicate = edge_tts.Communicate(**kwargs)
        
        with open(output, 'wb') as audio_file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_file.write(chunk["data"])
                elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                    submaker.feed(chunk)
        
        with open(subtitle_file, 'w', encoding='utf-8') as f:
            f.write(submaker.get_srt())
        
        print(f"   ✅ Audio: {output}")
        print(f"   ✅ Phụ đề: {subtitle_file}")
    else:
        communicate = edge_tts.Communicate(**kwargs)
        await communicate.save(output)
        print(f"   ✅ Audio: {output}")
    
    print(f"\n✅ Hoàn thành!\n")


async def list_voices_func(language: str = None):
    """Liệt kê các giọng nói"""
    voices = await edge_tts.list_voices()
    
    print(f"\n{'Tên giọng':<40} {'Giới tính':<10} {'Ngôn ngữ':<10}")
    print("-" * 65)
    
    count = 0
    for voice in voices:
        locale = voice["Locale"]
        if language is None or locale.startswith(language):
            name = voice["ShortName"]
            gender = voice["Gender"]
            print(f"{name:<40} {gender:<10} {locale:<10}")
            count += 1
    
    print(f"\n📊 Tổng cộng: {count} giọng nói\n")


def main():
    parser = argparse.ArgumentParser(
        description='🎤 Edge-TTS - Chuyển văn bản thành giọng nói',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  
  Tạo audio tiếng Việt:
    python tts_cli.py -t "Xin chào" -o hello.mp3
  
  Tạo audio với giọng nam:
    python tts_cli.py -t "Xin chào" -o hello.mp3 -v vi-VN-NamMinhNeural
  
  Tạo audio với phụ đề:
    python tts_cli.py -t "Xin chào" -o hello.mp3 -s
  
  Thay đổi tốc độ, âm lượng, cao độ:
    python tts_cli.py -t "Xin chào" -o hello.mp3 --rate=-50% --volume=+20% --pitch=-10Hz
  
  Liệt kê giọng tiếng Việt:
    python tts_cli.py --list-voices vi-VN
  
  Liệt kê giọng tiếng Anh:
    python tts_cli.py --list-voices en-US
  
  Liệt kê tất cả giọng:
    python tts_cli.py --list-voices all
        """
    )
    
    parser.add_argument('-t', '--text', type=str, help='Văn bản cần chuyển thành giọng nói')
    parser.add_argument('-o', '--output', type=str, help='Tên file output (vd: output.mp3)')
    parser.add_argument('-v', '--voice', type=str, default='vi-VN-HoaiMyNeural',
                       help='Tên giọng nói (mặc định: vi-VN-HoaiMyNeural)')
    parser.add_argument('-s', '--subtitles', action='store_true',
                       help='Tạo file phụ đề .srt')
    parser.add_argument('--rate', type=str, help='Tốc độ nói (vd: +50%%, -50%%)')
    parser.add_argument('--volume', type=str, help='Âm lượng (vd: +50%%, -50%%)')
    parser.add_argument('--pitch', type=str, help='Cao độ (vd: +50Hz, -50Hz)')
    parser.add_argument('--list-voices', type=str, nargs='?', const='all',
                       help='Liệt kê giọng nói (vi-VN, en-US, all)')
    
    args = parser.parse_args()
    
    # Xử lý list voices
    if args.list_voices:
        language = None if args.list_voices == 'all' else args.list_voices
        asyncio.run(list_voices_func(language))
        return
    
    # Kiểm tra text và output
    if not args.text:
        parser.print_help()
        print("\n❌ Lỗi: Vui lòng nhập văn bản với -t hoặc --text\n")
        return
    
    if not args.output:
        # Tự động tạo tên file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"output_{timestamp}.mp3"
        print(f"ℹ️  Tên file output tự động: {args.output}")
    
    # Tạo audio
    asyncio.run(generate_speech(
        text=args.text,
        voice=args.voice,
        output=args.output,
        rate=args.rate,
        volume=args.volume,
        pitch=args.pitch,
        with_subtitles=args.subtitles
    ))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Đã hủy!")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}\n")
