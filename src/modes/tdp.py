import subprocess
from src.constants import *
from PIL import Image
import os
from PyQt5.QtWidgets import QApplication

def get_info():
    return {
        "name": "Tomada de Posse",
        "description": "Chooses between upper-left, upper-right and bottom-center position to stamp the logo and whether it should be black or white."
    }

def run(photos_directory, window_text, window_progress_bar):
    print("running tdp stamping mode...")