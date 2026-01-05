"""
Hướng dẫn cài đặt Voice Cloning đơn giản hơn
Sử dụng OpenVoice thay vì GPT-SoVITS (dễ hơn, không cần GPU mạnh)
"""

import os
import subprocess
import sys

print("""
╔══════════════════════════════════════════════════════════════╗
║     HƯỚNG DẪN CÀI ĐẶT VOICE CLONING                         ║
╚══════════════════════════════════════════════════════════════╝

⚠️  GPT-SoVITS yêu cầu GPU NVIDIA + CUDA → Phức tạp!

💡 Giải pháp đơn giản hơn:

1. OpenVoice (Khuyến nghị - Dễ nhất)
   - Không cần GPU mạnh
   - Cài đặt nhanh
   - Chất lượng tốt
   
2. F5-TTS (Mới, Tốt)
   - Zero-shot TTS
   - Chất lượng cao
   - Dễ sử dụng

3. Sử dụng API Cloud (Không cần cài gì)
   - ElevenLabs API
   - PlayHT API
   - Azure Speech API

════════════════════════════════════════════════════════════════

Bạn muốn:
1. Cài OpenVoice (Đề xuất)
2. Cài F5-TTS
3. Hướng dẫn dùng API Cloud
4. Tiếp tục với GPT-SoVITS (Cần GPU + CUDA)

""")

choice = input("Nhập lựa chọn (1-4): ").strip()

if choice == "1":
    print("\n🔧 Đang cài đặt OpenVoice...\n")
    
    # Install OpenVoice
    commands = [
        "pip install openai-whisper",
        "pip install git+https://github.com/myshell-ai/OpenVoice.git",
    ]
    
    for cmd in commands:
        print(f"Chạy: {cmd}")
        subprocess.run(cmd, shell=True)
    
    print("\n✅ Cài đặt OpenVoice thành công!")
    print("Bạn có thể dùng trong web app ngay bây giờ!")

elif choice == "2":
    print("\n🔧 Đang cài đặt F5-TTS...\n")
    
    commands = [
        "pip install f5-tts",
    ]
    
    for cmd in commands:
        print(f"Chạy: {cmd}")
        subprocess.run(cmd, shell=True)
    
    print("\n✅ Cài đặt F5-TTS thành công!")

elif choice == "3":
    print("""
╔══════════════════════════════════════════════════════════════╗
║           HƯỚNG DẪN SỬ DỤNG API CLOUD                        ║
╚══════════════════════════════════════════════════════════════╝

1. ElevenLabs (Tốt nhất - Clone giống 99%)
   - Trang web: https://elevenlabs.io
   - Giá: $1 cho 10,000 ký tự
   - API đơn giản, dễ dùng

2. PlayHT (Tốt)
   - Trang web: https://play.ht
   - Giá: $0.5 cho 10,000 ký tự
   - Nhiều giọng

3. Azure Speech (Microsoft)
   - Trang web: https://azure.microsoft.com/en-us/services/cognitive-services/speech-services/
   - Miễn phí 500k ký tự/tháng
   - Chất lượng tốt

════════════════════════════════════════════════════════════════

Tích hợp vào web app: Chỉ cần API key!

""")

elif choice == "4":
    print("""
╔══════════════════════════════════════════════════════════════╗
║      CÀI ĐẶT GPT-SoVITS (Yêu cầu GPU NVIDIA)                ║
╚══════════════════════════════════════════════════════════════╝

Bước 1: Cài CUDA
   - Download: https://developer.nvidia.com/cuda-downloads
   - Chọn CUDA 12.1 hoặc 11.8
   
Bước 2: Cài cuDNN
   - Download: https://developer.nvidia.com/cudnn
   - Giải nén vào thư mục CUDA

Bước 3: Cài PyTorch với CUDA
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

Bước 4: Chạy lại setup

════════════════════════════════════════════════════════════════

⚠️  Rất phức tạp! Đề xuất dùng OpenVoice hoặc API Cloud!

""")

else:
    print("❌ Lựa chọn không hợp lệ!")
