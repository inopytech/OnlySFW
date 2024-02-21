import torch
from PIL import Image
from transformers import AutoModelForImageClassification, ViTImageProcessor
import os


class NSFWDetector:
    def __init__(self):
        self.logits = None
        self.outputs = None
        self.inputs = None
        self.model = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")
        self.processor = ViTImageProcessor.from_pretrained('Falconsai/nsfw_image_detection')

    def detect(self, path: str, os_: str):
        img = Image.open(path)

        with torch.no_grad():
            self.inputs = self.processor(images=img, return_tensors="pt")
            self.outputs = self.model(**self.inputs)
            self.logits = self.outputs.logits

        predicted_label = self.logits.argmax(-1).item()
        if os_ == "windows":
            os.system(f"rm {path}")
        elif os_ == "unix":
            os.system(f"rm -rf {path}")
        return self.model.config.id2label[predicted_label]
