import webview
import sys
import subprocess
import time
import os


STREAMLIT_PORT = 8501
APP_FILE = "app.py"

def start_app():
    
    process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", APP_FILE, "--server.headless=true", f"--server.port={STREAMLIT_PORT}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    
    time.sleep(3) 

    
    webview.create_window(
        title="Decentralized AI Auditor", 
        url=f"http://localhost:{STREAMLIT_PORT}",
        width=1200,
        height=800,
        resizable=True
    )

    
    webview.start()

    
    process.kill()

if __name__ == '__main__':
    start_app()