import streamlit as st
from google import genai
from web3 import Web3
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()


DEFAULT_API_KEY = os.getenv("GEMINI_API_KEY")
DEFAULT_RPC_URL = "http://127.0.0.1:7545" # Ganache RPC
DEFAULT_CONTRACT_ADDR = "YOUR CONTRACT ADDR"
DEFAULT_PRIVATE_KEY = "YOUR PRIVATE KEY"
DEFAULT_WALLET_ADDR = "YOUR WALLET ADDR"


st.set_page_config(page_title="AI Code Auditor DAO", layout="wide", page_icon="🛡️")


def get_gemini_client(api_key):
    return genai.Client(api_key=api_key)

def run_multi_agent_analysis(client, code):
    # Agent 1: Security
    sec_prompt = f"Sen Security Agent'sın. Sadece GÜVENLİK açıklarını bul: {code}"
    try:
        sec_res = client.models.generate_content(model="gemini-2.5-flash", contents=sec_prompt).text
    except: sec_res = "Hata"
    
    # Agent 2: Style
    style_prompt = f"Sen Style Guru'sun. Kod kalitesini ve PEP8'i incele: {code}"
    try:
        style_res = client.models.generate_content(model="gemini-2.5-flash", contents=style_prompt).text
    except: style_res = "Hata"

    # Agent 3: Judge
    judge_prompt = f"""
    Sen Oracle Judge'sın. Şu iki raporu analiz et ve JSON skor üret:
    Security: {sec_res}
    Style: {style_res}
    Format: {{"score": 0-100, "summary": "Tek cümlelik özet"}}
    Sadece JSON ver.
    """
    try:
        judge_res = client.models.generate_content(model="gemini-2.5-flash", contents=judge_prompt)
        clean_json = judge_res.text.replace("```json", "").replace("```", "").strip()
        verdict = json.loads(clean_json)
    except Exception as e:
        verdict = {"score": 0, "summary": f"Hata: {e}"}

    return sec_res, style_res, verdict

# --- BLOCKCHAIN FONKSİYONU ---
def write_to_chain(rpc, contract_addr, private_key, wallet, repo_name, score, summary):
    try:
        w3 = Web3(Web3.HTTPProvider(rpc))
        if not w3.is_connected(): return False, "Ağ bağlantısı yok"

        with open('abi.json', 'r') as f: abi = json.load(f)
        contract = w3.eth.contract(address=contract_addr, abi=abi)
        
        tx = contract.functions.recordAudit(repo_name, score, summary).build_transaction({
            'chainId': 1337,
            'gas': 3000000,
            'gasPrice': w3.to_wei('50', 'gwei'),
            'nonce': w3.eth.get_transaction_count(wallet)
        })
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        w3.eth.wait_for_transaction_receipt(tx_hash)
        return True, w3.to_hex(tx_hash)
    except Exception as e:
        return False, str(e)

# --- ARAYÜZ ---
def main():
    # Session State (Hafıza) Başlatma
    if 'audit_result' not in st.session_state:
        st.session_state['audit_result'] = None

    # Sidebar Ayarları
    with st.sidebar:
        st.header("⚙️ Sistem Ayarları")
        api_key = st.text_input("Gemini API Key", value=DEFAULT_API_KEY, type="password")
        st.divider()
        st.subheader("Blockchain Bağlantısı")
        repo_name = st.text_input("Proje Adı (ID)", value="Project_Omega_v2")
        rpc = st.text_input("RPC URL", value=DEFAULT_RPC_URL)
        contract = st.text_input("Contract Address", value=DEFAULT_CONTRACT_ADDR)
        p_key = st.text_input("Private Key", value=DEFAULT_PRIVATE_KEY, type="password")
        wallet = st.text_input("Wallet Address", value=DEFAULT_WALLET_ADDR)

    # Ana Başlık
    st.title("🛡️ Decentralized AI Code Auditor")
    st.markdown("**Multi-Agent System** for Automated Code Quality & Security Assurance")
    
    code_input = st.text_area("Analiz edilecek kodu buraya yapıştırın:", height=200, placeholder="def example(): pass...")

    # --- 1. BUTON: ANALİZ ET ---
    if st.button("🚀 Kodu Denetle (Start Multi-Agent Audit)", type="primary"):
        if not code_input or not api_key:
            st.warning("Lütfen kod ve API Key giriniz.")
        else:
            # Görsel Şov: Status Animasyonu
            with st.status("🕵️‍♂️ AI Ajanları Görev Başında...", expanded=True) as status:
                client = get_gemini_client(api_key)
                
                st.write("🔍 Security Agent: Güvenlik açıkları taranıyor...")
                time.sleep(0.5) # Yapay bekleme (görsellik için)
                
                st.write("🎨 Style Guru: Kod kalitesi ve syntax inceleniyor...")
                time.sleep(0.5)
                
                sec, style, verdict = run_multi_agent_analysis(client, code_input)
                
                st.write("⚖️ Oracle Judge: Skor hesaplanıyor ve karar veriliyor...")
                time.sleep(0.5)
                
                status.update(label="Analiz Başarıyla Tamamlandı!", state="complete", expanded=False)
                
                # Sonucu hafızaya kaydet
                st.session_state['audit_result'] = {
                    "sec": sec, "style": style, "verdict": verdict
                }

    # --- SONUÇLARI GÖSTER (Hafızadan) ---
    if st.session_state['audit_result']:
        res = st.session_state['audit_result']
        verdict = res['verdict']
        
        # Görsel Skor Kartları
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric(label="🛡️ Güven Skoru", value=f"{verdict['score']}/100")
            # Renkli Uyarılar
            if verdict['score'] < 50:
                st.error("🚨 KRİTİK: RİSKLİ KOD!")
            elif verdict['score'] < 80:
                st.warning("⚠️ UYARI: GELİŞTİRİLMELİ")
            else:
                st.success("✅ ONAYLANDI: GÜVENLİ")

        with col2:
            st.info(f"**Yargıç Özeti:** {verdict['summary']}")

        # Detaylı Rapor Sekmeleri
        tab1, tab2 = st.tabs(["🔴 Güvenlik Raporu", "🔵 Kod Kalitesi Raporu"])
        with tab1:
            st.markdown(res['sec'])
        with tab2:
            st.markdown(res['style'])

        # --- 2. BUTON: BLOCKCHAIN KAYIT ---
        st.divider()
        st.subheader("🔗 Blockchain Kaydı")
        st.caption(f"Bu sonuç '{repo_name}' kimliği ile Smart Contract'a mühürlenecek.")
        
        if st.button("💾 Sonucu Blockchain'e Mühürle"):
            with st.spinner("Ethereum ağına bağlanılıyor ve işlem imzalanıyor..."):
                success, msg = write_to_chain(
                    rpc, contract, p_key, wallet,
                    repo_name, verdict['score'], verdict['summary']
                )
                
                if success:
                    st.balloons() 
                    st.success(f"✅ İŞLEM BAŞARILI! Blokzincire Kazındı.")
                    st.code(f"Transaction Hash: {msg}", language="text")
                    st.markdown(f"**Not:** Artık bu kodun kalitesi değiştirilemez bir kanıt olarak saklanmaktadır.")
                else:
                    st.error(f"Hata oluştu: {msg}")

if __name__ == "__main__":
    main()