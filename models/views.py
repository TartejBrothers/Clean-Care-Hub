from django.shortcuts import render
from django.template.response import TemplateResponse
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings
import os
from PIL import Image, ImageDraw
from ultralytics import YOLO
from django.http import JsonResponse

classes = ["mixed", "restaurant-fastfood", "retail-groceries"]


class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        return name


def index(request):
    message = ""
    fss = CustomFileSystemStorage()

    try:
        media_root = settings.MEDIA_ROOT
        for filename in os.listdir(media_root):
            file_path = os.path.join(media_root, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                return JsonResponse(
                    {"error": f"Failed to delete {filename}: {str(e)}"}, status=500
                )

        # Read input image
        image = request.FILES["image"]
        _image = fss.save(image.name, image)
        path = os.path.join(settings.MEDIA_ROOT, _image)

        # Load YOLO model
        model = YOLO("best.pt")  # Load pre-trained model
        model.conf = 0.3  # Adjust confidence threshold as needed

        # Perform inference
        img = Image.open(path).convert("RGB")
        results = model(img)

        # Draw bounding boxes on image
        for detection in results:
            for box in detection.boxes.xyxy:
                x1, y1, x2, y2 = box.tolist()[:4]  # Extract bounding box coordinates
                img_draw = ImageDraw.Draw(img)
                img_draw.rectangle([x1, y1, x2, y2], outline="red")

        # Save result image
        result_image_path = os.path.join(settings.MEDIA_ROOT, "result_image.jpg")
        img.save(result_image_path)

        return TemplateResponse(
            request,
            "litterdetection.html",
            {
                "message": message,
                "image_url": fss.url(_image),
                "result_image_url": fss.url("result_image.jpg"),
            },
        )
    except MultiValueDictKeyError:
        return TemplateResponse(
            request,
            "litterdetection.html",
            {"message": "No Image Selected"},
        )
    except Exception as e:
        return TemplateResponse(
            request,
            "litterdetection.html",
            {"message": str(e)},
        )
