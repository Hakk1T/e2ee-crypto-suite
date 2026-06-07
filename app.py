from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import random
import sys
import math

sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cok-gizli-siber-anahtar'
socketio = SocketIO(app, cors_allowed_origins="*")

# --- 1. MERKLE-HELLMAN MOTORU ---
def egcd(a, b):
    if a == 0: return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def mod_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1: raise Exception('Modüler ters bulunamadı.')
    return x % m

def generate_keypair(n=8):
    w, total = [], 0
    for i in range(n):
        val = random.randint(total + 1, total + 10)
        w.append(val)
        total += val
    q = random.randint(total + 1, total + 50)
    r = random.randint(2, q - 1)
    while egcd(r, q)[0] != 1:
        r = random.randint(2, q - 1)
    public_key = [(val * r) % q for val in w]
    return public_key, (w, q, r)

def encrypt_message(message, public_key):
    cipher_list = []
    for char in message:
        binary_str = format(ord(char), '08b')
        ciphertext = sum(int(bit) * pk_val for bit, pk_val in zip(binary_str, public_key))
        cipher_list.append(ciphertext)
    return cipher_list

def decrypt_message(cipher_list, private_key):
    w, q, r = private_key
    r_inv = mod_inverse(r, q)
    decrypted_str = ""
    for ciphertext in cipher_list:
        c_prime = (ciphertext * r_inv) % q
        binary_bits = []
        for val in reversed(w):
            if c_prime >= val:
                binary_bits.append('1')
                c_prime -= val
            else:
                binary_bits.append('0')
        binary_bits.reverse()
        decrypted_str += chr(int("".join(binary_bits), 2))
    return decrypted_str

# --- 2. API YOLLARI ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate_keys', methods=['GET'])
def api_generate_keys():
    pub_key, priv_key = generate_keypair()
    max_pk = max(pub_key)
    density = 8 / math.log2(max_pk) if max_pk > 1 else 0
    return jsonify({
        'public_key': pub_key, 'private_key': priv_key,
        'density': round(density, 4), 'is_vulnerable': density < 0.94
    })

@app.route('/api/encrypt', methods=['POST'])
def api_encrypt():
    data = request.json
    message = data.get('message')
    pub_key = data.get('public_key')
    
    if not message or not pub_key:
        return jsonify({'error': 'Eksik metin veya anahtar!'}), 400
        
    cipher = encrypt_message(message, pub_key)
    return jsonify({'ciphertext': cipher})

@app.route('/api/decrypt', methods=['POST'])
def api_decrypt():
    data = request.json
    ciphertext = data.get('ciphertext')
    priv_key = data.get('private_key')

    if not ciphertext or not priv_key:
        return jsonify({'error': 'Eksik şifreli metin veya anahtar!'}), 400
        
    plaintext = decrypt_message(ciphertext, priv_key)
    return jsonify({'plaintext': plaintext})

# --- 3. SOCKET.IO AĞ YÖNLENDİRİCİSİ ---
@socketio.on('connect')
def handle_connect():
    print("[AĞ] Yeni cihaz E2EE tüneline katıldı.")

@socketio.on('broadcast_public_key')
def handle_pubkey(data):
    emit('receive_public_key', data, broadcast=True, include_self=False)

@socketio.on('send_encrypted_message')
def handle_message(data):
    emit('receive_encrypted_message', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    print("="*50)
    print(" SİBER GÜVENLİK SÜİTİ BAŞLATILDI ")
    print("="*50)
    socketio.run(app, debug=True, port=5000)
