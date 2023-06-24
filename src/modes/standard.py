from PIL import Image
from tqdm import tqdm
import os
from PyQt5.QtWidgets import QApplication
import subprocess
from src.constants import *

def get_info():
    return {
        "name": "Standard",
        "description": "Stamps the logo on the bottom-right corner of the image and decides whether it should stamp black or white."
    }

class Standard():
    def __init__(self, window_text, window_progress_bar):
        self.window_text = window_text
        self.window_progress_bar = window_progress_bar

    def stamp(self, photos_directory):
        print("running standard stamping mode...")
        logo_size_ratio = 1.5
        logo_displacement_x = 400
        logo_displacement_y = 250

        if not os.path.exists(BRANDED_PHOTOS_DIRECTORY):
            os.makedirs(BRANDED_PHOTOS_DIRECTORY)

        if os.path.exists(BRANDED_PHOTOS_DIRECTORY):
            files = os.listdir(BRANDED_PHOTOS_DIRECTORY)
            if files:
                for file in files:
                    file_path = os.path.join(BRANDED_PHOTOS_DIRECTORY, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
        
        # getting the files
        total_files = len(os.listdir(photos_directory))
        completed_files = 0
        filename_array = list(filter(lambda filename: filename.endswith(".jpg") 
                                    or filename.endswith(".png") 
                                    or filename.endswith(".JPG"), 
                                os.listdir(photos_directory)))
        total_i = len(filename_array)
        print(filename_array)

        for i, filename in enumerate(tqdm(filename_array, desc="Processing photos")):
            logo_path_blue = LOGO_PATH + "/" + "NuIEEE_logo_blue.png"
            logo_template = Image.open(logo_path_blue)
            logo_template = logo_template.convert("RGBA")
            logo_width = int(logo_size_ratio * logo_template.size[0])
            logo_height = int((logo_width / logo_template.size[0]) * logo_template.size[1])
            logo_template = logo_template.resize((logo_width, logo_height), Image.LANCZOS)

            photo_path = photos_directory + filename
            photo = Image.open(photo_path)
            region = photo.crop((photo.width - logo_displacement_x - logo_width, 
                                photo.height - logo_displacement_y - logo_height, 
                                photo.width, 
                                photo.height))
            
            # analysing region's brightness
            region = region.convert("RGB")
            region_data = region.getdata()
            brightness_threshold = 170 
            brightness_sum = 0
            pixel_count = 0

            for pixel in region_data:
                r, g, b = pixel[:3]
                brightness = (r + g + b) // 3
                brightness_sum += brightness
                pixel_count += 1
            average_brightness = brightness_sum // pixel_count

            if average_brightness < brightness_threshold:
                logo_color = "white"
            else:
                logo_color = "black"

            # resizes the logo to the size of the region
            logo = Image.open(LOGO_PATH + "/" + f'NuIEEE_logo_{logo_color}.png')
            logo = logo.convert("RGBA")
            logo = logo.resize((logo_width, logo_height), Image.LANCZOS)
            photo_path = os.path.join(photos_directory, filename)
            photo = Image.open(photo_path)
            photo = photo.convert("RGBA")

            position = (
                photo.width - logo.width - logo_displacement_x, 
                photo.height - logo.height - logo_displacement_y
            )

            # Progress
            ## progress text
            tqdm.write("Making photo: " + filename)
            self.window_text.append("Making photo: " + filename + " (" + str(i+1) + " of " + str(total_i) + ")")
            self.window_text.ensureCursorVisible()
            ## progress bar
            completed_files += 1
            progress = int((completed_files / total_files) * 100)
            self.window_progress_bar.setValue(progress)
            QApplication.processEvents()  # Update the GUI

            image_with_logo = Image.new("RGBA", photo.size)
            image_with_logo.paste(photo, (0, 0))
            image_with_logo.paste(logo, position, mask=logo.split()[3])

            new_filename = "logo_" + filename
            new_photo_path = os.path.join(BRANDED_PHOTOS_DIRECTORY, new_filename)
            image_with_logo.save(new_photo_path, format="PNG")
        
        # progress bar finished
        self.window_progress_bar.setValue(100)
        self.window_text.append("Finished processing photos.")
        self.window_text.ensureCursorVisible()
        QApplication.processEvents()  # Update the GUI

        #open brandified_photos directory
        try:
            subprocess.Popen(['xdg-open', BRANDED_PHOTOS_DIRECTORY])
        except:
            try:
                subprocess.Popen(['open', BRANDED_PHOTOS_DIRECTORY])
            except:
                subprocess.Popen(['explorer', BRANDED_PHOTOS_DIRECTORY])

def run(photos_directory, window_text, window_progress_bar):
    stamper = Standard(window_text, window_progress_bar)
    stamper.stamp(photos_directory)