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

-------------------------------------------------------------------------------------------------

📹 ✅ O que o código atual faz bem:
O script detector_veiculos_velocidade_youtube.py funciona perfeitamente para vídeos do YouTube com link fixo e conteúdo previamente gravado, como exemplo o que foi testado (DUJY5Z0TfeI), pois o pacote yt-dlp consegue baixar o arquivo em .mp4 completo para depois o OpenCV processar frame a frame.

📡 🚫 Mas transmissões ao vivo (ao vivo/lives) são diferentes:
Links como este:

🔴 https://www.youtube.com/watch?v=Mht3ibtExC4
são live streams — ou seja, transmissão contínua, sem final definido.

E aí surgem dois problemas:
yt-dlp não baixa a live como um arquivo .mp4 pronto, porque ela ainda não foi encerrada (sem “fim” delimitado).

O OpenCV cv2.VideoCapture() espera um arquivo estático ou um feed contínuo, e não lida bem com URLs dinâmicas do YouTube Live (precisaria de um intermediador).

🔁 ✅ Alternativas possíveis
✅ 1. Capturar da webcam pública (RTSP / IP)
Se a câmera ao vivo fornecer um link de stream direto (como RTSP, HTTP ou MJPEG), aí sim Exemplo (funciona com algumas câmeras urbanas públicas e câmeras IP de rodovias):

cap = cv2.VideoCapture("http://<ip_da_câmera>:8080/video")

✅ 2. Usar ferramentas como streamlink para abrir a live
Você pode usar o streamlink para redirecionar a live para um stream local, que o OpenCV possa capturar (Mas é mais complexo e envolve usar ffmpeg + OpenCV em tempo real, com threads para leitura de pipe):

streamlink https://www.youtube.com/watch?v=Mht3ibtExC4 best -O | ffmpeg -i pipe:0 -f rawvideo ...
