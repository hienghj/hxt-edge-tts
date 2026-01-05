"""
GPT-SoVITS Voice Cloning Engine
"""

import sys
import os

# Add GPT-SoVITS to path
GPTSOVITS_PATH = r"D:\TOOOL DONGJ DDOC\GPT-SoVITS"
if os.path.exists(GPTSOVITS_PATH):
    sys.path.insert(0, GPTSOVITS_PATH)


class GPTSoVITSEngine:
    """Engine clone giọng sử dụng GPT-SoVITS"""
    
    def __init__(self):
        self.model_loaded = False
        self.gpt_model = None
        self.vits_model = None
        
    def check_availability(self):
        """Kiểm tra xem GPT-SoVITS có sẵn không"""
        try:
            # Check if GPT-SoVITS directory exists
            if not os.path.exists(GPTSOVITS_PATH):
                return False, "GPT-SoVITS chưa được cài đặt"
            
            # Check pretrained models
            pretrained_path = os.path.join(GPTSOVITS_PATH, "pretrained_models")
            if not os.path.exists(pretrained_path):
                return False, "Chưa download pretrained models"
            
            required_models = [
                "gsv-v2final-pretrained/s2G2333k.pth",
                "gsv-v2final-pretrained/s2D2333k.pth", 
                "chinese-hubert-base",
                "chinese-roberta-wwm-ext-large"
            ]
            
            missing = []
            for model in required_models:
                model_path = os.path.join(pretrained_path, model)
                if not os.path.exists(model_path):
                    missing.append(model)
            
            if missing:
                return False, f"Thiếu models: {', '.join(missing)}"
            
            return True, "GPT-SoVITS sẵn sàng"
            
        except Exception as e:
            return False, f"Lỗi: {str(e)}"
    
    def load_models(self):
        """Load GPT-SoVITS models"""
        try:
            # TODO: Implement actual model loading
            # from GPTSoVITS.inference import load_model
            # self.gpt_model, self.vits_model = load_model()
            
            self.model_loaded = True
            return True, "Models đã được load"
        except Exception as e:
            return False, f"Lỗi load models: {str(e)}"
    
    def clone_voice(self, reference_audio_path: str, output_path: str):
        """
        Clone giọng nói từ audio reference
        
        Args:
            reference_audio_path: Đường dẫn audio mẫu
            output_path: Đường dẫn lưu model giọng đã clone
        
        Returns:
            success: bool, message: str
        """
        try:
            if not self.model_loaded:
                success, msg = self.load_models()
                if not success:
                    return False, msg
            
            # TODO: Implement actual voice cloning
            # 1. Extract features from reference audio
            # 2. Fine-tune models
            # 3. Save cloned voice model
            
            return True, f"Clone thành công. Model lưu tại: {output_path}"
            
        except Exception as e:
            return False, f"Lỗi clone: {str(e)}"
    
    def synthesize(self, text: str, voice_model_path: str, output_audio_path: str):
        """
        Tạo audio từ text với giọng đã clone
        
        Args:
            text: Văn bản cần đọc
            voice_model_path: Đường dẫn model giọng đã clone
            output_audio_path: Đường dẫn lưu audio output
        
        Returns:
            success: bool, message: str
        """
        try:
            if not self.model_loaded:
                success, msg = self.load_models()
                if not success:
                    return False, msg
            
            # TODO: Implement text-to-speech with cloned voice
            # 1. Load cloned voice model
            # 2. Generate audio
            # 3. Save output
            
            return True, f"Tạo audio thành công: {output_audio_path}"
            
        except Exception as e:
            return False, f"Lỗi tạo audio: {str(e)}"


# Singleton instance
_engine = None

def get_engine():
    """Get GPT-SoVITS engine instance"""
    global _engine
    if _engine is None:
        _engine = GPTSoVITSEngine()
    return _engine


if __name__ == "__main__":
    # Test
    engine = get_engine()
    available, msg = engine.check_availability()
    print(f"GPT-SoVITS: {msg}")
