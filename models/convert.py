import os
import tensorflow as tf
import cv2

# Define the path to the YOLO model in HDF5 format
yolo_model_h5_path = "./yolo.h5"

# Ensure the HDF5 file exists before attempting to load it
if not os.path.exists(yolo_model_h5_path):
    raise FileNotFoundError(f"YOLO model HDF5 file not found at: {yolo_model_h5_path}")

# Define the path where the converted model will be saved
saved_model_path = "../saved_model"

# Load the YOLO model in HDF5 format
try:
    yolo_model = tf.keras.models.load_model(yolo_model_h5_path)
except Exception as e:
    raise ValueError(f"Failed to load YOLO model from HDF5 file: {e}")

# Convert the YOLO model to TensorFlow's SavedModel format
tf.saved_model.save(yolo_model, saved_model_path)
