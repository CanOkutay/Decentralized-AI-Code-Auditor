from google import genai
import json


API_KEY = "AIzaSyBev6ZAcSRpOeGwBhvaR6ylzVFT32gEZBI"

client = genai.Client(api_key=API_KEY)


MODEL_ID = "gemini-2.5-flash"

def analyze_code_with_gemini(code_content):
    print(f"🤖 AI Ajanı ({MODEL_ID}) kodu inceliyor...")
    
    prompt = f"""
    Sen uzman bir Smart Contract ve Python denetçisisin.
    Görevin: Aşağıdaki kodu analiz etmek ve JSON formatında rapor vermek.
    
    Lütfen yanıtını SADECE saf JSON formatında ver. Markdown (```json ... ```) kullanma.
    Format şu olmalı:
    {{
        "guvenlik_aciklari": ["Kısa ve net açıklama 1", "Kısa ve net açıklama 2"],
        "kod_kalitesi_notu": "Kısa bir yorum",
        "skor": 0 ile 100 arası bir tamsayı
    }}
    
    Analiz edilecek kod:
    ---------------------------------------------------
    {code_content}
    ---------------------------------------------------
    """
    
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Hata: {e}"

# --- TEST SENARYOSU ---
if __name__ == "__main__":
    # Test için yine hatalı bir kod veriyoruz
    sample_code = """
    def login(user, pwd):
        # HARDCODED PASSWORD!
        if user == "admin" and pwd == "12345": 
            return True
        return False
    """

    raw_result = analyze_code_with_gemini(sample_code)
    
    print("\n" + "="*30)
    print("📝 GEMINI 3 - DENETİM RAPORU")
    print("="*30)
    
    # Gelen sonucu ekrana bas
    print(raw_result)
    
    # JSON olup olmadığını test edelim (İleride Blockchain'e bunu göndereceğiz)
    try:
        # Bazen AI, ```json ile sarar, onu temizleyelim
        clean_json = raw_result.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        print(f"\n✅ Başarılı! Skor algılandı: {data['skor']}/100")
    except:
        print("\n⚠️ Not: Çıktı tam JSON formatında gelmedi ama sorun değil, içeriği okuyabiliyoruz.")