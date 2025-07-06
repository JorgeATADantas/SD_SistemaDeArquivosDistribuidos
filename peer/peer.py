# peer/peer.py
#Objetivo: cada peer:
#        - Registra arquivos no servidor
#        - "Escuta" pedidos de outros peers
#        - Solicita arquivos de outros peers

import socket
import threading
import os
import json
import time
from config import SERVER_HOST, SERVER_PORT, PEER_PORT, STORAGE_DIR

#Registra todos os arquivos locais no servidor central
def register_with_server(filename):
    msg = {
        'command': 'REGISTER',
        'filename': filename,
        'peer_addr': f'{socket.gethostbyname(socket.gethostname())}:{PEER_PORT}'
    }
    with socket.socket() as s:
        s.connect((SERVER_HOST, SERVER_PORT))
        s.send(json.dumps(msg).encode())
        print(f"[REGISTER] {filename} registrado no servidor")

#Servidor local de arquivos (aceita pedidos de outros peers)
def peer_server():
    s = socket.socket()
    s.bind(('0.0.0.0', PEER_PORT))
    s.listen()
    print(f"[PEER] Servindo arquivos em porta {PEER_PORT}")
    while True:
        conn, addr = s.accept()
        filename = conn.recv(1024).decode()
        file_path = os.path.join(STORAGE_DIR, filename)
        if os.path.exists(file_path):               # Verifica se um arquivo existe localmente
            with open(file_path, 'rb') as f:
                conn.sendall(f.read())
        else:
            conn.send(b'FILE_NOT_FOUND')
        conn.close()
        
#Baixa arquivo de outro peer
def download_file(filename):
    msg = {
        'command': 'LOOKUP',
        'filename': filename
    }
    with socket.socket() as s:
        s.connect((SERVER_HOST, SERVER_PORT))   # Conecta ao servidor
        s.send(json.dumps(msg).encode())
        data = s.recv(4096)                     # Recebe resposta
        result = json.loads(data.decode())

        if result['status'] == 'FOUND':
            peer = result['peers'][0]
            host, port = peer.split(':')
            with socket.socket() as ps:
                ps.connect((host, int(port)))
                ps.send(filename.encode())
                content = ps.recv(1024 * 1024)
                with open(os.path.join(STORAGE_DIR, filename), 'wb') as f:
                    f.write(content)
                print(f"[DOWNLOAD] Arquivo {filename} baixado de {peer}")
                register_with_server(filename)
        else:
            print(f"[DOWNLOAD] Arquivo {filename} não encontrado no servidor")

if __name__ == "__main__":

    # Cria o diretório de storage se não existir
    os.makedirs(STORAGE_DIR, exist_ok=True) 

    threading.Thread(target=peer_server).start()    # Inicia o servidor P2P em background
    time.sleep(2)                                   # Espera o servidor P2P inicializar

    while True:
        cmd = input("Comando (upload <arquivo> | download <arquivo>): ")
        if cmd.startswith("upload "):
            _, filename = cmd.split(" ", 1)
            filepath = os.path.join(STORAGE_DIR, filename)
            if os.path.exists(filepath):
                register_with_server(filename)
            else:
                print("[ERRO] Arquivo não encontrado no diretório local.")
        elif cmd.startswith("download "):
            _, filename = cmd.split(" ", 1)
            download_file(filename)
