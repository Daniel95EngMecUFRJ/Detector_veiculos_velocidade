import cv2
from ultralytics import YOLO
import subprocess
import time
import os

# Caminho do executável do streamlink
streamlink_path = r"C:\Program Files\Streamlink\bin\streamlink.exe"

# URL da live no YouTube
youtube_url = "https://www.youtube.com/watch?v=Mht3ibtExC4"

# Nome do arquivo temporário para salvar o stream
output_file = "live_stream_temp.ts"

# Comando para capturar a live com streamlink
streamlink_cmd = [
    streamlink_path,
    "--stdout",
    youtube_url,
    "best"
]

# Inicia o streamlink e grava em arquivo
print("📡 Iniciando captura da live...")
with open(output_file, "wb") as f:
    proc = subprocess.Popen(streamlink_cmd, stdout=f)
    time.sleep(5)  # Aguarda início da gravação

# Inicia detecção com YOLO
print("🚗 Iniciando detecção com YOLO...")
video = cv2.VideoCapture(output_file)
model = YOLO("yolov8n.pt")

while True:
    ret, frame = video.read()
    if not ret:
        print("🔄 Aguardando mais frames da live...")
        time.sleep(1)
        continue

    results = model(frame)[0]
    annotated = results.plot()
    cv2.imshow("Detecção - Live YouTube", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
proc.terminate()
os.remove(output_file)
print("🧹 Live encerrada e arquivo temporário removido.")
