from django.template.response import TemplateResponse
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings
import os
from PIL import ImageDraw, Image, ImageOps
from ultralytics import YOLO
from django.http import JsonResponse
from django.http import StreamingHttpResponse
from django.shortcuts import render
import cv2
import numpy as np

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

        # Resize image while maintaining aspect ratio
        img = Image.open(path)
        img.thumbnail((480, 640))

        # Save the resized image
        resized_path = os.path.join(settings.MEDIA_ROOT, "resized_image.jpg")
        img.save(resized_path)

        # Print the dimensions of the resized image
        print("Resized image dimensions:", img.size)

        # Load YOLO model
        model = YOLO("best.pt")  # Load pre-trained model
        model.conf = 0.3  # Adjust confidence threshold as needed

        # Perform inference
        img = Image.open(resized_path).convert("RGB")
        results = model(img)

        # Draw bounding boxes on image
        for detection in results:
            for box in detection.boxes.xyxy:
                x1, y1, x2, y2 = box.tolist()[:4]  # Extract bounding box coordinates
                img_draw = ImageDraw.Draw(img)
                img_draw.rectangle([x1, y1, x2, y2], outline="yellow", width=5)

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


def resize_image(image, target_size):
    width_height_tuple = (target_size[1], target_size[0])  # PIL uses (width, height)
    resized_image = ImageOps.fit(image, width_height_tuple)
    return resized_image


def live_video_feed(request):
    # Load YOLO model
    model = YOLO("best.pt")
    model.conf = 0.3  # Adjust confidence threshold as needed

    # Function to generate frames from the live video feed
    def generate_frames():
        # Initialize webcam
        cap = cv2.VideoCapture(0)

        # Check if the webcam is opened successfully
        if not cap.isOpened():
            raise Exception("Failed to open webcam")

        # Loop to continuously capture frames from the webcam
        while True:
            success, frame = cap.read()
            if not success:
                break

            # Perform inference
            img = Image.fromarray(frame)  # Convert frame to PIL Image
            results = model(img)

            # Draw bounding boxes on the frame
            # Draw bounding boxes on the frame
            for detection in results:
                for box in detection.boxes.xyxy:
                    x1, y1, x2, y2 = box  # Access box coordinates directly
                    x1, y1, x2, y2 = (
                        int(x1),
                        int(y1),
                        int(x2),
                        int(y2),
                    )  # Convert to integers
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Convert frame to JPEG format and yield it
            _, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
            )

        # Release the video capture object
        cap.release()

    return StreamingHttpResponse(
        generate_frames(), content_type="multipart/x-mixed-replace; boundary=frame"
    )
