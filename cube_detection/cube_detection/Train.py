from ultralytics import YOLO

model = YOLO("yolo11n.pt")

results = model.train(
    data="data.yaml",
    epochs=25,
    imgsz=640,
    batch=16,
    name="rubik_cube_yolo11"
)
metrics = model.val()