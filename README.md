# Detector_veiculos_velocidade
# YOLOv8 - Detecção de Veículos com Estimativa de Velocidade (YouTube)

Este projeto implementa uma aplicação de visão computacional com **YOLOv8** (You Only Look Once, versão 8) para **detecção de veículos** e **estimativa de velocidade** a partir de vídeos do **YouTube**, sem necessidade de download manual.

A proposta foi desenvolvida como experimento educacional voltado à demonstração prática de Inteligência Artificial e suas aplicações em mobilidade urbana, meio ambiente e cidades inteligentes.

## 🔍 Funcionalidades
- Detecção de veículos em tempo real com YOLOv8 pré-treinado.
- Estimativa da velocidade dos veículos com base no deslocamento por frame.
- Processamento direto do link do vídeo no YouTube.
- Exibição simultânea dos resultados com bounding boxes e valores estimados.

## 📦 Requisitos
- Python 3.10+
- torch
- ultralytics
- opencv-python
- pytube
- numpy
- (opcional para live streaming) [streamlink](https://streamlink.github.io/)

## ▶️ Como usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/SEU_USUARIO/detector-veiculos-youtube.git
   cd detector-veiculos-youtube

2.Crie e ative um ambiente virtual:

bash

python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac


3.Instale os requisitos:

bash

pip install -r requirements.txt

4. Execute o código:

bash

python detector_veiculos_velocidade_youtube.py

6. Insira o link do vídeo do YouTube quando solicitado.
