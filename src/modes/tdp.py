import subprocess
from PIL import Image
import os
from PyQt5.QtWidgets import QApplication

def get_info():
    return {
        "name": "Tomada de Posse",
        "description": "TDP stamping mode is coming soon."
    }

def run():
    print("running tdp stamping mode...")