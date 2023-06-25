import subprocess
from PIL import Image
import os
from PyQt5.QtWidgets import QApplication

def get_info():
    return {
        "name": "Tomada de Posse",
        "description": "TDP stamping mode is coming soon."
    }

def run(photos_directory, window_text, window_progress_bar):
    print("running tdp stamping mode...")