# peer/config.py

import os

SERVER_HOST = 'server'
SERVER_PORT = 5000

PEER_PORT = int(os.environ.get('PEER_PORT', 9001))
STORAGE_DIR = './storage'
