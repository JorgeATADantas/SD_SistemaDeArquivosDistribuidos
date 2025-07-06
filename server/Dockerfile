# server/Dockerfile

# imagem base da qual sua imagem Docker será construída
FROM python:3.12-slim

# diretório de trabalho dentro do container
WORKDIR /app

#copia arquivos da máquina host para dentro do container (server.py -->todos)
COPY server.py .

#comando padrão que será executado quando o container iniciar
CMD ["python", "server.py"]
