
import cv2
from ultralytics import YOLO
import subprocess
import time
import numpy as np
import csv

# Caminho do streamlink.exe
streamlink_path = r"C:\Program Files\Streamlink\bin\streamlink.exe"

# URL da live do YouTube
youtube_url = "https://www.youtube.com/watch?v=Mht3ibtExC4"

# Extrai a URL do stream m3u8 usando streamlink
print("🔗 Obtendo URL do stream...")
result = subprocess.run([streamlink_path, "--stream-url", youtube_url, "best"], capture_output=True, text=True)

if result.returncode != 0:
    print("❌ Erro ao obter URL do stream:", result.stderr)
    exit()

stream_url = result.stdout.strip()
print("✅ Stream URL obtido:", stream_url)

# Inicializa o vídeo com OpenCV a partir da URL do stream
video = cv2.VideoCapture(stream_url)
if not video.isOpened():
    print("❌ Não foi possível abrir o vídeo da live")
    exit()

# Carrega o modelo YOLOv8
model = YOLO("yolov8n.pt")

# Variáveis para rastrear veículos e velocidades
tracked_vehicles = {}
frame_rate = video.get(cv2.CAP_PROP_FPS) or 30
distancia_metros = 3  # estimativa de distância entre dois frames para velocidade

# Arquivo CSV para salvar dados
csv_file = open("registro_veiculos.csv", mode="w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["ID", "Velocidade (km/h)"])

print("🚗 Iniciando detecção - pressione 'q' para sair")
while True:
    success, frame = video.read()
    if not success:
        print("⚠️ Frame não capturado")
        break

    # Detecção com YOLOv8 + rastreamento
    results = model.track(frame, persist=True, conf=0.4, tracker="botsort.yaml")[0]

    for box in results.boxes:
        if not box.id:
            continue
        track_id = int(box.id.item())
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if track_id in tracked_vehicles:
            prev_pos, prev_time = tracked_vehicles[track_id]
            dist_px = np.linalg.norm(np.array([cx, cy]) - np.array(prev_pos))
            tempo_seg = time.time() - prev_time
            px_por_seg = dist_px / tempo_seg if tempo_seg > 0 else 0

            escala = 0.05  # ajustar conforme o vídeo
            velocidade_kmh = px_por_seg * escala * 3.6

            cv2.putText(frame, f"ID {track_id} - {velocidade_kmh:.1f} km/h", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            if velocidade_kmh > 0:
                csv_writer.writerow([track_id, round(velocidade_kmh, 1)])

        tracked_vehicles[track_id] = ((cx, cy), time.time())
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    cv2.imshow("YOLOv8 - Live YouTube com Velocidade e Contagem", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
csv_file.close()
cv2.destroyAllWindows()
