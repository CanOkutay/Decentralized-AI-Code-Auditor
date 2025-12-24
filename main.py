import json
import os
from google import genai
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 2. Ganache RPC Adresi (Genelde böyledir, Ganache üstünde yazar)
BLOCKCHAIN_RPC_URL = "http://127.0.0.1:7545"

# 3. Remix'ten kopyaladığın Kontrat Adresi
CONTRACT_ADDRESS = "YOUR CONTRACT ADDR"

# 4. Ganache'dan aldığın Private Key (Cüzdanın Anahtarı)
PRIVATE_KEY = "YOUR PRIVATE KEY"

# 5. Cüzdan Adresi (Public Key - Ganache'daki 'Address' sütunu)
WALLET_ADDRESS = "YOUR WALLET ADDR" 

# ==========================================

# --- İŞLEMCİLER ---

def analyze_code_with_ai(code_content):
    """Gemini AI kullanarak kodu analiz eder."""
    print(f"\n🤖 AI Ajanı kodu inceliyor...")
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""
    Sen bir Smart Contract ve Python güvenlik denetçisisin.
    Görevin: Kodu analiz edip JSON formatında raporlamak.
    Format: {{"summary": "Tek cümlelik özet", "score": 0-100 arası tamsayı}}
    
    Kod:
    {code_content}
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        # JSON temizliği
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except Exception as e:
        print(f"❌ AI Hatası: {e}")
        return None

def write_to_blockchain(repo_name, score, summary):
    """Sonucu Blockchain'e yazar."""
    print(f"\n🔗 Blockchain'e bağlanılıyor ({BLOCKCHAIN_RPC_URL})...")
    
    w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_RPC_URL))
    
    if not w3.is_connected():
        print("❌ Hata: Blockchain'e bağlanılamadı! Ganache açık mı?")
        return

    # ABI Dosyasını Oku
    try:
        with open('abi.json', 'r') as f:
            contract_abi = json.load(f)
    except FileNotFoundError:
        print("❌ Hata: abi.json dosyası bulunamadı! Remix'ten alıp kaydettin mi?")
        return

    # Kontrat Bağlantısı
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)
    
    print("📝 İşlem hazırlanıyor (Transaction)...")
    
    # İşlemi Oluştur
    tx = contract.functions.recordAudit(
        repo_name,
        score,
        summary
    ).build_transaction({
        'chainId': 1337,  # Ganache Chain ID'si genelde 1337'dir
        'gas': 3000000,
        'gasPrice': w3.to_wei('370', 'gwei'),
        'nonce': w3.eth.get_transaction_count(WALLET_ADDRESS),
    })

    # İşlemi İmzala
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    
    # İşlemi Gönder
    print("🚀 İşlem ağa gönderiliyor...")
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    # Onay Bekle
    print(f"⏳ Onay bekleniyor... TX Hash: {w3.to_hex(tx_hash)}")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    print(f"\n✅ BAŞARILI! Blokzincire Yazıldı.")
    print(f"📦 Blok Numarası: {receipt['blockNumber']}")
    print(f"⛽ Harcanan Gas: {receipt['gasUsed']}")

# --- MAIN ---
if __name__ == "__main__":
    # Test edilecek örnek proje kodu
    sample_project_code = """
    def secure_money_transfer(user_role, amount, balance):
        \"\"\"
        Güvenli para transferi işlemi.
        Kontroller: Yetki kontrolü, bakiye kontrolü ve negatif sayı kontrolü.
        \"\"\"
        # 1. Yetki Kontrolü (Authorization)
        if user_role != "admin":
            raise PermissionError("Yetkisiz işlem! Sadece admin transfer yapabilir.")
        
        # 2. Girdi Doğrulama (Input Validation)
        if amount <= 0:
            raise ValueError("Transfer miktarı pozitif olmalıdır.")
            
        # 3. Mantıksal Kontrol (Business Logic)
        if balance < amount:
            raise ValueError("Yetersiz bakiye.")

        # İşlem gerçekleştiriliyor
        new_balance = balance - amount
        return new_balance
    """
   
    
    project_name = "Project_Beta_v1"

    # 1. AI Analizi Yap
    report = analyze_code_with_ai(sample_project_code)
    
    if report:
        print(f"\n📊 AI Raporu: Skor {report['score']} - {report['summary']}")
        
        # 2. Blockchain'e Yaz
        choice = input("\nBu sonucu Blockchain'e kaydetmek ister misin? (e/h): ")
        if choice.lower() == 'e':
            write_to_blockchain(project_name, report['score'], report['summary'])
        else:
            print("İşlem iptal edildi.")