#!/bin/bash

# Configurar ambiente
echo "🔧 Configurando ambiente Python..."
python -m venv venv
source venv/bin/activate

# Instalar dependências
echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

# Executar bot
echo "🤖 Iniciando Wave Song Bot..."
python app.py

# Se falhar, tentar novamente
echo "🔄 Reiniciando bot..."
sleep 5
python app.py
