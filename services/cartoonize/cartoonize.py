import os
import sys
import io

from .white_box_cartoonizer.cartoonize import WB_Cartoonize
from PIL import Image
import numpy as np
import tensorflow as tf
import cv2

gpu_available = tf.test.is_gpu_available()
weigth_path = os.path.join(os.path.dirname(__file__), "white_box_cartoonizer/saved_models/")
wb_cartoonizer = WB_Cartoonize(weigth_path, gpu_available)


def convert_bytes_to_image(img_bytes):
    """Convert bytes to numpy array

    Args:
        img_bytes (bytes): Image bytes read from flask.

    Returns:
        [numpy array]: Image numpy array
    """
    
    pil_image = Image.open(io.BytesIO(img_bytes))
    if pil_image.mode=="RGBA":
        image = Image.new("RGB", pil_image.size, (255,255,255))
        image.paste(pil_image, mask=pil_image.split()[3])
    else:
        image = pil_image.convert('RGB')
    
    image = np.array(image)
    
    return image

def cartoonize(img):
    
    image = convert_bytes_to_image(img)
    cartoon_image = wb_cartoonizer.infer(image)
    # cartoon_image = cv2.cvtColor(cartoon_image, cv2.COLOR_RGB2BGR)
    cartoon_image = Image.fromarray(cartoon_image)
    bio = io.BytesIO()
    cartoon_image.save(bio, "PNG")
    return bio.getbuffer()
