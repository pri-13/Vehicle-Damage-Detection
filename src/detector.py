# loads the trained YOLO model and performs damage detection.

from ultralytics import YOLO
import cv2

class DamageDetector:
    # Vehicle Damage Detector using YOLOv8.
    def __init__(self, model_path):
        # load the trained model
        self.model = YOLO(model_path)

    def detect(self, image_path, conf=0.25):
        # Run YOLO inference
        results = self.model.predict(
            source=image_path,
            conf=conf,
            verbose=False
        )
        result = results[0]

        # Image with bounding boxes
        annotated_image = result.plot()
        detections = []

        # Read original image to get dimensions
        image = cv2.imread(image_path)
        image_height, image_width = image.shape[:2]

        # Extract detections
        for box in result.boxes:
            class_id = int(box.cls.item())
            class_name = self.model.names[class_id]
            confidence = round(float(box.conf.item()), 3)
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            detection = {
                "damage_type": class_name,
                "confidence": confidence,
                "bbox": [
                    int(x1),
                    int(y1),
                    int(x2),
                    int(y2)
                ],
                "image_width": image_width,
                "image_height": image_height
            }
            detections.append(detection)
        return annotated_image, detections
    def save_prediction(self, annotated_image, output_path):
        cv2.imwrite(output_path, annotated_image)