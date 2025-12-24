# 🛡️ Decentralized AI Code Auditor

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Solidity](https://img.shields.io/badge/solidity-0.8.19-lightgrey)
![Status](https://img.shields.io/badge/status-Prototype-orange)

**Decentralized AI Code Auditor** is a next-generation code review platform that combines the analytical power of **Multi-Agent AI** (Google Gemini 1.5) with the immutability of **Blockchain Technology** (Ethereum).

This system solves the "Trust" problem in AI code audits by cryptographically signing and recording every audit result on the blockchain, creating a permanent and tamper-proof "Proof of Audit."

---

## 🚀 Features

* **🕵️‍♂️ Multi-Agent Architecture:**
    * **Security Expert:** Hunts for vulnerabilities (OWASP Top 10, SQLi, XSS).
    * **Style Guru:** Checks for PEP8 compliance, modularity, and clean code principles.
    * **Oracle Judge:** Synthesizes reports and assigns a final trust score (0-100).
* **🔗 Blockchain Immutability:** Audit results are stored on an Ethereum Smart Contract (Ganache/Sepolia), ensuring they cannot be altered later.
* **📊 Interactive GUI:** Built with **Streamlit** for a seamless user experience.
* **⚡ Fast & Cost-Effective:** Uses Gemini 1.5 Flash for rapid analysis and optimized Solidity structs for low gas consumption.
* **🖥️ Desktop Mode:** Can be run as a standalone desktop application using `pywebview`.

---

## 🏗️ System Architecture

1.  **User Input:** Developer submits code via the Streamlit Interface.
2.  **AI Analysis:** The Python backend orchestrates 3 distinct AI Agents to analyze the code.
3.  **Adjudication:** The Oracle Judge calculates a score and generates a summary.
4.  **On-Chain Commit:** The system signs a transaction using `Web3.py` and writes the result to the Smart Contract.
5.  **Verification:** Users can verify the audit history using the Transaction Hash or Remix IDE.

---

## 🛠️ Installation & Setup

### Prerequisites
* Python 3.8+
* [Ganache](https://trufflesuite.com/ganache/) (Local Blockchain)
* Google Gemini API Key

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Decentralized-AI-Auditor.git
cd Decentralized-AI-Auditor
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Blockchain (Ganache)
1.  Open **Ganache** and start a "Quickstart" workspace.
2.  Copy the **RPC Server URL** (usually `http://127.0.0.1:7545`).
3.  Copy a **Private Key** from one of the accounts.

### 4. Deploy Smart Contract
1.  Open [Remix IDE](https://remix.ethereum.org/).
2.  Create a file named `AICodeAudit.sol` and paste the contract code (found in `contracts/` folder).
3.  Compile with Solidity **0.8.19**.
4.  In the "Deploy" tab, select **Dev - Ganache Provider** (connect to your local Ganache).
5.  Deploy and copy the **Contract Address**.

### 5. Configure the App
Open `app.py` and update the configuration section with your keys:
*(Note: For production, consider using environment variables)*

```python
DEFAULT_API_KEY = "YOUR_GEMINI_API_KEY"
DEFAULT_RPC_URL = "http://127.0.0.1:7545"
DEFAULT_CONTRACT_ADDR = "YOUR_DEPLOYED_CONTRACT_ADDRESS"
DEFAULT_PRIVATE_KEY = "YOUR_GANACHE_PRIVATE_KEY"
DEFAULT_WALLET_ADDR = "YOUR_WALLET_ADDRESS"
```

---

## ▶️ Usage

Run the application using Streamlit (Web Mode):

```bash
python -m streamlit run app.py
```

Or run as a desktop application (Standalone Mode):

```bash
python run_desktop.py
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

