import google.generativeai as genai

# ANAHTARINI BURAYA YAPIŞTIR
api_key = "AIzaSyCmvbgZdttkckso73lwUsGfHZpz-vC0bkE"

try:
    genai.configure(api_key=api_key)
    print("Mevcut Modeller Listeleniyor...\n")
    
    # Kullanılabilir tüm modelleri listele
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            
except Exception as e:
    print(f"Hata: {e}")