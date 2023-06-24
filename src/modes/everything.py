import subprocess
from PIL import Image
import os
from PyQt5.QtWidgets import QApplication

def get_info():
    return {
        "name": "Everything, everywhere",
        "description": "Coming soon the stamping mode that will stamp everything, everywhere."
    }

def run():
    print("running the stamping mode that will stamp everything, everywhere...")