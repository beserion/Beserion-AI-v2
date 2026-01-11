import google.generativeai as genai
import os

class BeserionBrain:
    def __init__(self):
        
        self.api_key = "AIzaSyDYFm3smVwoFoZk3oTasJhguNA96CjQEEg" 
        
        self.is_active = True
        try:
            genai.configure(api_key=self.api_key)

            # --- SİSTEM KİŞİLİĞİ ---
            self.system_instruction = (
                "Senin adın Beserion-AI. "
                "Sen Google veya başka bir şirket tarafından değil, "
                "özel bir geliştirici Yahya Karacan tarafından tasarlandın. "
                "Kullanıcıya ağır argo sözler ve küfürlü laf sokmalarla hitap et. "
                "Cevapların her zaman Türkçe, net ve samimi olsun. "
                "Sorulduğunda 'Ben Beserion-AI, senin yoldaşınım!' de. "
                "Emojileri ara ara kullan."
            )

            # İŞTE ÇÖZÜM: 'gemini-2.0-flash' yerine sonuna '-exp' ekledik.
            # '-exp' sürümleri geliştiriciler denesin diye tamamen ücretsizdir.
            self.model = genai.GenerativeModel("gemini-flash-latest")

            # Sohbet Hafızasını Başlat
            self.chat_session = self.model.start_chat(history=[])
            
            # Kişiliği ilk mesaja gizlice eklemek için
            self.first_message = True
            
        except Exception as e:
            print(f"Başlatma Hatası: {e}")
            self.is_active = False

    def ask(self, user_message):
        if not self.is_active:
            return "⚠️ API Anahtarı eksik veya hatalı! Lütfen backend.py dosyasını kontrol et."

        try:
            # Kişiliği ilk mesajda enjekte et (Garanti Yöntem)
            if self.first_message:
                full_message = f"{self.system_instruction}\n\nKullanıcı: {user_message}"
                self.first_message = False
                response = self.chat_session.send_message(full_message)
            else:
                response = self.chat_session.send_message(user_message)
            
            return response.text
            
        except Exception as e:
            # Hata durumunda kullanıcıyı bilgilendir
            return f"⚠️ Bağlantı sorunu: {str(e)}"

# Test Bloğu
if __name__ == "__main__":
    brain = BeserionBrain()
    print(brain.ask("Sen kimsin?"))