# 1. Usa uma imagem leve do Python oficial
FROM python:3.9-slim

# 2. Define a pasta de trabalho dentro do container
WORKDIR /app

# 3. Copia o arquivo de dependências para dentro
COPY requirements.txt .

# 4. Instala as bibliotecas necessárias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia todo o resto do seu código para dentro do container
COPY . .

# 6. Comando padrão para rodar seu script (ajuste o nome do arquivo se precisar)
# Exemplo: se seu script principal estiver em src/main.py ou src/app.py
CMD ["python", "src/etl_loggi.py"]