# SD_SistemaDeArquivosDistribuidos

## Sistema de Arquivos Distribuídos (Cliente-Servidor + P2P)
Trabalho de Sistema de Arquivos Distribuídos da matéria de Sistemas Digitais. Este projeto implementa um sistema de arquivos distribuído com arquitetura híbrida: servidor central para metadados e peers com transferência P2P.


### ✨ Alunos:
- Jorge Aliomar Trocolo Abdon Dantas
- Samuel Pedro Fernandes Amorim 


### 📁 Estrutura do Projeto / Diretórios

Projeto/<br>
├── peer/ ← Peer (cliente + servidor P2P). Peer que registra, envia e baixa arquivos<br>
│ └── config.py<br>
│ └── peer.py<br>
│ └── Dockerfile<br>
├── server/ ← Servidor central (metadados) com Flask<br>
│ └── server.py<br>
│ └── Dockerfile<br>
├── shared/ ← Código compartilhado<br>
│ └── protocol.py<br>
├── README.md ← Instruções de uso<br>
├── docker-compose.yml ← Para subir tudo com 1 comando

### 📦 Componentes

- peer: cliente que registra, envia e baixa arquivos e se comunica diretamente com outros peers.
- server: servidor que utiliza socket que armazena metadados dos arquivos.
- shared: configurações comuns.
- docker: imagens para servidor e peers.

### ▶️ Execução

1. Execute em um terminal:

    ```bash
    docker-compose up --build
    ```

2. Aguarde o carregamento.

3. Em outro terminal, abra um shell para os peers:
    
    ```bash
    docker exec -it peer1 bash
    docker exec -it peer2 bash
    ```
4. Upload de arquivo

    No terminal do peer1:

    ```bash
    echo "Teste Peer 1 para Peer 2" > storage/testeP1-P2.txt
    python peer.py
    upload testeP1-P2.txt
    ```

5. Download de arquivo

    No terminal do peer2:

    ```bash
    python peer.py
    download testeP1-P2.txt
    ```
O arquivo será salvo em peer2/storage/.

## 🔧 Personalização/Expansão

Para adicionar mais peers:

1. Copie o serviço peer1 em docker-compose.yml
2. Altere a porta (ex: 9002) e o nome do serviço
3. Recompile:

```bash
docker-compose up --build
```

### 📌 Requisitos Técnicos

- Python 3.12
- Socket (servidor)
- Socket (peer)
