import subprocess
from PIL import Image
from tqdm import tqdm
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QProgressBar, QVBoxLayout, QHBoxLayout, QTextEdit, QComboBox

class InputWindow(QWidget):
    def __init__(self, input_values):
        super().__init__()
        self.setWindowTitle("PhotoBrandify")
        self.setGeometry(100, 100, 400, 200)
        self.input_values = input_values

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # stamping_mode
        stamping_mode_layout = QHBoxLayout()
        self.stamping_mode_label = QLabel("Stamping Mode:")
        self.stamping_mode_combo = QComboBox()
        self.stamping_mode_combo.addItem("Option 1")
        self.stamping_mode_combo.addItem("Option 2")
        self.stamping_mode_combo.addItem("Option 3")
        stamping_mode_layout.addWidget(self.stamping_mode_label)
        stamping_mode_layout.addWidget(self.stamping_mode_combo)
        main_layout.addLayout(stamping_mode_layout)

        # photos_directory
        photos_layout = QHBoxLayout()
        self.photos_directory_label = QLabel("Photos Directory:")
        self.photos_directory_edit = QLineEdit()
        self.photos_directory_button = QPushButton("Browse")
        photos_layout.addWidget(self.photos_directory_label)
        photos_layout.addWidget(self.photos_directory_edit)
        photos_layout.addWidget(self.photos_directory_button)
        main_layout.addLayout(photos_layout)

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
        self.photos_directory_edit.setText(input_values['photos_directory'])

        # Connect button signals to slots
        self.photos_directory_button.clicked.connect(self.select_photos_directory)
        self.start_button.clicked.connect(self.start)

    def select_photos_directory(self):
        photos_directory = QFileDialog.getExistingDirectory(self, 'Select Photos Directory')
        self.photos_directory_edit.setText(photos_directory)

    def start(self):
        self.input_values['photos_directory'] = self.photos_directory_edit.text()
        self.progress_bar.setValue(0)
        add_logo_to_photos(self.input_values, self)
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
    filename_array = list(filter(lambda filename: filename.endswith(".jpg") 
                                or filename.endswith(".png") 
                                or filename.endswith(".JPG"), 
                            os.listdir(photos_directory)))
    total_i = len(filename_array)
    print(filename_array)

    for i, filename in enumerate(tqdm(filename_array, desc="Processing photos")):
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
        window.progress_text.append("Making photo: " + filename + " (" + str(i+1) + " of " + str(total_i) + ")")
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
    window.progress_text.append("Finished processing photos.")
    window.progress_text.ensureCursorVisible()
    QApplication.processEvents()  # Update the GUI

    #open brandified_photos directory
    try:
        subprocess.Popen(['xdg-open', input_values['branded_photos_directory']])
    except:
        try:
            subprocess.Popen(['open', input_values['branded_photos_directory']])
        except:
            subprocess.Popen(['explorer', input_values['branded_photos_directory']])

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
    window = InputWindow(input_values)
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
