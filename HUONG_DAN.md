# EDGE-TTS - Hướng dẫn sử dụng nhanh

## 📁 Các file batch có sẵn:

### 1. **run_tool.bat** - Tool tương tác (Menu)
Chạy tool với giao diện menu để chọn chức năng:
```
Nhấp đúp vào run_tool.bat
```

### 2. **tts.bat** - Tạo audio nhanh (Command Line)

**Cách dùng:**
```cmd
tts.bat "Văn bản của bạn" [tên_file.mp3] [tên_giọng]
```

**Ví dụ:**
```cmd
tts.bat "Xin chào"
tts.bat "Xin chào" hello.mp3
tts.bat "Xin chào" hello.mp3 vi-VN-NamMinhNeural
```

### 3. **list_voices.bat** - Xem danh sách giọng
```
Nhấp đúp vào list_voices.bat
```

## 🎤 Giọng nói tiếng Việt:
- `vi-VN-HoaiMyNeural` - Giọng nữ (mặc định)
- `vi-VN-NamMinhNeural` - Giọng nam

## 🚀 Cách dùng Python trực tiếp:

**Tool tương tác:**
```bash
python tts_tool.py
```

**Command line:**
```bash
python tts_cli.py -t "Văn bản" -o output.mp3
python tts_cli.py -t "Văn bản" -o output.mp3 -v vi-VN-NamMinhNeural
python tts_cli.py -t "Văn bản" -o output.mp3 -s
python tts_cli.py -t "Văn bản" -o output.mp3 --rate=+50%
python tts_cli.py --list-voices vi-VN
```

## 📌 Tùy chọn nâng cao:
- `-s` hoặc `--subtitles` : Tạo file phụ đề .srt
- `--rate=+50%` : Tăng tốc độ 50%
- `--rate=-50%` : Giảm tốc độ 50%
- `--volume=+20%` : Tăng âm lượng 20%
- `--pitch=-10Hz` : Giảm cao độ 10Hz

## 📂 Thư mục output:
- File batch: Lưu trong thư mục hiện tại
- Tool tương tác: Lưu trong thư mục `audio_outputs/`
- Demo: Lưu trong thư mục `demo_outputs/`
