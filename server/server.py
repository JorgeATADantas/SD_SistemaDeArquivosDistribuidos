# server/server.py

import socket
import threading
import json

#Endereço e porta do servidor
HOST = '0.0.0.0'
PORT = 5000

#Estrutura de armazenamento: {'nome.txt': ['peer1:9001', 'peer2:9002']}
file_registry = {}

#Função que lida com cada conexão de um peer
def handle_client(conn, addr):
    print(f"[SERVER] Conexão de {addr}")
    try:
        data = conn.recv(4096).decode()
        message = json.loads(data)
        command = message['command']

        if command == 'REGISTER':
            filename = message['filename']
            peer_addr = message['peer_addr']
            file_registry.setdefault(filename, []).append(peer_addr)
            conn.send(b'OK')

        elif command == 'LOOKUP':
            filename = message['filename']
            peers = file_registry.get(filename)
            if peers:
                conn.send(json.dumps({'status': 'FOUND', 'peers': peers}).encode())
            else:
                conn.send(json.dumps({'status': 'NOT_FOUND'}).encode())
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
        
# Função principal do servidor
def start_server():
    print(f"[SERVER] Iniciando em {HOST}:{PORT}")
    s = socket.socket()         # Cria um socket TCP/IP
    s.bind((HOST, PORT))        # Associa ao endereço e porta
    s.listen()                  # Habilita o modo servidor

    while True:
        conn, addr = s.accept() # Aceita conexões
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
