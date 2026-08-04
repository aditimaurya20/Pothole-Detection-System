from ultralytics import YOLO

# load your trained model (use latest folder)
model = YOLO("runs/detect/train-6/weights/best.pt")

# use your image name here
results = model("image.jpeg", show=True)