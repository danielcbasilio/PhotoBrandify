# detect the necessary logos given the photo
# balance the amount of logos in a photo album

from PIL import Image
from tqdm import tqdm
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QProgressBar, QVBoxLayout, QHBoxLayout, QTextEdit

class InputWindow(QWidget):
    def __init__(self, app, input_values):
        super().__init__()
        self.setWindowTitle("Input Values")
        self.setGeometry(100, 100, 400, 200)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # logo_path
        logo_layout = QHBoxLayout()
        self.logo_path_label = QLabel("Logo Path:")
        self.logo_path_edit = QLineEdit()
        self.logo_path_button = QPushButton("Browse")
        logo_layout.addWidget(self.logo_path_label)
        logo_layout.addWidget(self.logo_path_edit)
        logo_layout.addWidget(self.logo_path_button)
        main_layout.addLayout(logo_layout)

        # photos_directory
        photos_layout = QHBoxLayout()
        self.photos_directory_label = QLabel("Photos Directory:")
        self.photos_directory_edit = QLineEdit()
        self.photos_directory_button = QPushButton("Browse")
        photos_layout.addWidget(self.photos_directory_label)
        photos_layout.addWidget(self.photos_directory_edit)
        photos_layout.addWidget(self.photos_directory_button)
        main_layout.addLayout(photos_layout)

        # branded_photos_directory
        branded_photos_layout = QHBoxLayout()
        self.branded_photos_directory_label = QLabel("Branded Photos Directory:")
        self.branded_photos_directory_edit = QLineEdit()
        self.branded_photos_directory_button = QPushButton("Browse")
        branded_photos_layout.addWidget(self.branded_photos_directory_label)
        branded_photos_layout.addWidget(self.branded_photos_directory_edit)
        branded_photos_layout.addWidget(self.branded_photos_directory_button)
        main_layout.addLayout(branded_photos_layout)

        # logo_size_ratio
        logo_size_ratio_layout = QHBoxLayout()
        self.logo_size_ratio_label = QLabel("Logo Size Ratio:")
        self.logo_size_ratio_edit = QLineEdit()
        logo_size_ratio_layout.addWidget(self.logo_size_ratio_label)
        logo_size_ratio_layout.addWidget(self.logo_size_ratio_edit)
        main_layout.addLayout(logo_size_ratio_layout)

        # logo_displacement_x
        logo_displacement_x_layout = QHBoxLayout()
        self.logo_displacement_x_label = QLabel("Logo Displacement X:")
        self.logo_displacement_x_edit = QLineEdit()
        logo_displacement_x_layout.addWidget(self.logo_displacement_x_label)
        logo_displacement_x_layout.addWidget(self.logo_displacement_x_edit)
        main_layout.addLayout(logo_displacement_x_layout)

        # logo_displacement_y
        logo_displacement_y_layout = QHBoxLayout()
        self.logo_displacement_y_label = QLabel("Logo Displacement Y:")
        self.logo_displacement_y_edit = QLineEdit()
        logo_displacement_y_layout.addWidget(self.logo_displacement_y_label)
        logo_displacement_y_layout.addWidget(self.logo_displacement_y_edit)
        main_layout.addLayout(logo_displacement_y_layout)

        # start button    
        start_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        start_layout.addStretch()
        start_layout.addWidget(self.start_button)
        main_layout.addLayout(start_layout)

        # progress bar
        self.progress_bar = QProgressBar()
        main_layout.addWidget(self.progress_bar)

        # progress text
        self.progress_text = QTextEdit(self)
        self.progress_text.setReadOnly(True)
        main_layout.addWidget(self.progress_text)

        # Set default values
        self.logo_path_edit.setText(input_values['logo_path'])
        self.photos_directory_edit.setText(input_values['photos_directory'])
        self.branded_photos_directory_edit.setText(input_values['branded_photos_directory'])
        self.logo_size_ratio_edit.setText(str(input_values['logo_size_ratio']))
        self.logo_displacement_x_edit.setText(str(input_values['logo_displacement_x']))
        self.logo_displacement_y_edit.setText(str(input_values['logo_displacement_y']))

        # Connect button signals to slots
        self.logo_path_button.clicked.connect(self.select_logo_path)
        self.photos_directory_button.clicked.connect(self.select_photos_directory)
        self.branded_photos_directory_button.clicked.connect(self.select_branded_photos_directory)
        self.start_button.clicked.connect(self.start)

    def select_logo_path(self):
        logo_path = QFileDialog.getExistingDirectory(self, 'Select Logo Path')
        self.logo_path_edit.setText(logo_path[0])

    def select_photos_directory(self):
        photos_directory = QFileDialog.getExistingDirectory(self, 'Select Photos Directory')
        self.photos_directory_edit.setText(photos_directory)

    def select_branded_photos_directory(self):
        branded_photos_directory = QFileDialog.getExistingDirectory(self, 'Select Branded Photos Directory')
        self.branded_photos_directory_edit.setText(branded_photos_directory)

    def start(self):
        input_values = {
            'logo_path': self.logo_path_edit.text(),
            'photos_directory': self.photos_directory_edit.text(),
            'branded_photos_directory': self.branded_photos_directory_edit.text(),
            'logo_size_ratio': float(self.logo_size_ratio_edit.text()),
            'logo_displacement_x': int(self.logo_displacement_x_edit.text()),
            'logo_displacement_y': int(self.logo_displacement_y_edit.text())
        }
        self.progress_bar.setValue(0)
        add_logo_to_photos(input_values, self)
        self.progress_bar.setValue(100)

def get_logo(filename, input_values):
    logo_path = input_values['logo_path'] + "NuIEEE_logo_blue.png"
    logo_size_ratio = input_values['logo_size_ratio']
    logo_displacement_x = input_values['logo_displacement_x']
    logo_displacement_y = input_values['logo_displacement_y']
    # branded_photos_directory = input_values['branded_photos_directory']
    photo_path = input_values['photos_directory'] + filename

    logo_template = Image.open(logo_path)
    logo_template = logo_template.convert("RGBA")
    logo_width = int(logo_size_ratio * logo_template.size[0])
    logo_height = int((logo_width / logo_template.size[0]) * logo_template.size[1])
    logo_template = logo_template.resize((logo_width, logo_height), Image.LANCZOS)

    photo = Image.open(photo_path)
    region = photo.crop((photo.width - logo_displacement_x - logo_width, 
                         photo.height - logo_displacement_y - logo_height, 
                         photo.width, 
                         photo.height))
    region = region.convert("RGB")
    region_data = region.getdata()

    """
    # for testing
    new_filename = "region_" + filename
    region_path = os.path.join(branded_photos_directory, new_filename)
    region.save(region_path, format="PNG")
    """

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

    logo = Image.open(input_values['logo_path'] + f'NuIEEE_logo_{logo_color}.png')
    logo = logo.convert("RGBA")
    logo = logo.resize((logo_width, logo_height), Image.LANCZOS)    
    
    return {
        'logo_object': logo,
        'color': logo_color
    }

def add_logo_to_photos(input_values, window):
    photos_directory = input_values['photos_directory']
    branded_photos_directory = input_values['branded_photos_directory']
    logo_displacement_x = input_values['logo_displacement_x']
    logo_displacement_y = input_values['logo_displacement_y']

    print('branded_photos_directory: ' + str(branded_photos_directory))

    if not os.path.exists(branded_photos_directory):
        os.makedirs(branded_photos_directory)

    if os.path.exists(branded_photos_directory):
        files = os.listdir(branded_photos_directory)
        if files:
            for file in files:
                file_path = os.path.join(branded_photos_directory, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
    
    # for progress bar
    total_files = len(os.listdir(input_values['photos_directory']))
    completed_files = 0

    for filename in tqdm(os.listdir(photos_directory), desc="Processing photos"):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".JPG"):
            logo_object = get_logo(filename, input_values)
            logo = logo_object['logo_object']
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
            window.progress_text.append("Making photo: " + filename)
            window.progress_text.ensureCursorVisible()
            ## progress bar
            completed_files += 1
            progress = int((completed_files / total_files) * 100)
            window.progress_bar.setValue(progress)
            QApplication.processEvents()  # Update the GUI

            image_with_logo = Image.new("RGBA", photo.size)
            image_with_logo.paste(photo, (0, 0))
            image_with_logo.paste(logo, position, mask=logo.split()[3])

            new_filename = "logo_" + filename
            new_photo_path = os.path.join(branded_photos_directory, new_filename)
            image_with_logo.save(new_photo_path, format="PNG")
    
    # progress bar finished
    window.progress_bar.setValue(100)

def main():
    print("starting script...")
    app = QApplication([])
    input_values = {
        'logo_path': "NuIEEE_logos/",
        'photos_directory': "photos_to_brandify/",
        'branded_photos_directory': "brandified_photos/",
        'logo_size_ratio': 1.5,
        'logo_displacement_x': 400,
        'logo_displacement_y': 250
    }
    window = InputWindow(app, input_values)
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
