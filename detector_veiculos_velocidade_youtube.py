
# detector_veiculos_velocidade_youtube.py
# Requisitos: pip install ultralytics opencv-python numpy yt-dlp imageio[ffmpeg]

from ultralytics import YOLO
import cv2
import numpy as np

# === Função para estimar velocidade ===
def calcular_velocidade(prev_center, new_center, fps, ppm=10):
    dx = new_center[0] - prev_center[0]
    dy = new_center[1] - prev_center[1]
    distancia_pixel = np.sqrt(dx**2 + dy**2)
    metros = distancia_pixel / ppm
    velocidade_ms = metros * fps
    return round(velocidade_ms * 3.6, 2)  # km/h

# === Inicializar ===
print("🚀 Carregando modelo YOLOv8...")
model = YOLO("yolov8n.pt")  # Você pode usar yolov8m.pt ou yolov8l.pt para mais precisão

# === Parâmetros ===
ppm = 10  # pixels por metro - estimado (pode ajustar conforme distância/cena)
fps = 30  # valor padrão (se for conhecido, substitua pelo real)
rastreamento = {}  # {id: (x,y)}

# === Rodar rastreamento direto de link do YouTube ===
print("🎥 Iniciando detecção e estimativa de velocidade...")
results = model.track(
    source="https://www.youtube.com/watch?v=3TyodLAvXRo",
    show=True,
    stream=True,
    persist=True,
    conf=0.4,
    tracker="botsort.yaml"
)

# === Loop por frame ===
for r in results:
    frame = r.orig_img.copy()
    if r.boxes.id is not None:
        ids = r.boxes.id.cpu().numpy().astype(int)
        boxes = r.boxes.xyxy.cpu().numpy()

        for i, box in enumerate(boxes):
            obj_id = ids[i]
            x1, y1, x2, y2 = box
            cx, cy = int((x1 + x2)/2), int((y1 + y2)/2)

            if obj_id in rastreamento:
                prev = rastreamento[obj_id]
                vel = calcular_velocidade(prev, (cx, cy), fps, ppm)
                cv2.putText(frame, f"{vel} km/h", (cx, cy - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            rastreamento[obj_id] = (cx, cy)

    # Mostrar com anotações
    cv2.imshow("YOLOv8 - Detecção de Veículos + Velocidade", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
print("✅ Finalizado.")
