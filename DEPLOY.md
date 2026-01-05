# HXT Edge-TTS 🎤

Text-to-Speech tool với Edge-TTS API, hỗ trợ 100+ giọng nói đa ngôn ngữ.

## 🌟 Tính năng

- 🎙️ **100+ giọng nói**: Tiếng Việt, English, 中文, 日本語, 한국어, Français, Deutsch, Español...
- 🎚️ **Tùy chỉnh chi tiết**: Tốc độ, âm lượng, cao độ (điều chỉnh từng bước 5%)
- 🔐 **Hệ thống đăng nhập**: Admin panel, quản lý user
- ⏰ **Quản lý thời gian**: User có thời hạn (theo ngày) hoặc vĩnh viễn
- 💾 **Lưu phiên**: Tự động đăng nhập, không cần nhập lại (7 ngày)
- 🎨 **Giao diện đẹp**: Gradient tím, responsive design

## 🚀 Deploy lên Streamlit Cloud (MIỄN PHÍ)

### Bước 1: Đẩy code lên GitHub

```bash
cd "D:\TOOOL DONGJ DDOC\edge-tts"
git init
git add .
git commit -m "Initial commit - HXT Edge-TTS"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/hxt-edge-tts.git
git push -u origin main
```

### Bước 2: Deploy trên Streamlit Cloud

1. Truy cập: https://share.streamlit.io
2. Đăng nhập bằng GitHub
3. Click **"New app"**
4. Chọn repository: `YOUR_USERNAME/hxt-edge-tts`
5. Main file path: `app_with_login.py`
6. Click **"Deploy"**

✅ Xong! App sẽ chạy tại: `https://your-app-name.streamlit.app`

## 🔧 Chạy local

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy app
streamlit run app_with_login.py --server.port=8510
```

## 👤 Tài khoản mặc định

- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Quan trọng**: Đổi mật khẩu admin sau khi deploy!

## 📁 Cấu trúc

```
edge-tts/
├── app_with_login.py      # Main application
├── requirements.txt       # Dependencies
├── users.json             # User database
├── session.json           # Session storage (auto-generated)
├── outputs/               # Generated MP3 files
└── .streamlit/
    └── config.toml        # Streamlit config
```

## 🌐 Deploy các nền tảng khác

### Railway.app
1. Tạo tài khoản tại: https://railway.app
2. New Project → Deploy from GitHub
3. Chọn repo và deploy

### Render.com
1. Tạo tài khoản tại: https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `streamlit run app_with_login.py --server.port=$PORT --server.address=0.0.0.0`

## 📝 License

MIT License - Free to use

---

Made with ❤️ by HXT
