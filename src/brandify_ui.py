from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QProgressBar, QVBoxLayout, QHBoxLayout, QTextEdit, QComboBox
from PyQt5.QtCore import QThread
from src.modes import standard

class InputWindow(QWidget):
    def __init__(self, input_values, modes):
        super().__init__()
        self.setWindowTitle("PhotoBrandify")
        self.setGeometry(100, 100, 400, 200)
        self.input_values = input_values
        self.modes = modes

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # stamping_mode
        stamping_mode_layout = QHBoxLayout()
        self.stamping_mode_label = QLabel("Stamping Mode:")
        self.stamping_mode_combo = QComboBox()
        self.stamping_mode_combo.addItem("Standard")
        self.stamping_mode_combo.addItem("Tomada de Posse")
        self.stamping_mode_combo.addItem("Everywhere, Everything")
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

        # stamping mode
        self.stamping_mode_combo.currentIndexChanged.connect(self.update_text)
        self.update_text()

        # stamping process thread
        self.worker_thread = QThread()

    def update_text(self):
        selected_item = self.stamping_mode_combo.currentText()
        if selected_item in self.modes:
            description = selected_item.description
            text = f"<b>{selected_item.name}</b>: {description}"
            self.update_text_label(text)

    def update_text_label(self, text):
        self.progress_text.setText(text)

    def select_photos_directory(self):
        photos_directory = QFileDialog.getExistingDirectory(self, 'Select Photos Directory')
        self.photos_directory_edit.setText(photos_directory)

    def start(self):
        try:
            self.input_values['logo_path'] = self.input_values['logo_path'] + "/"
            self.input_values['photos_directory'] = self.photos_directory_edit.text() + "/"
            self.input_values['branded_photos_directory'] = self.input_values['branded_photos_directory'] + "/"
        except:
            print("problem to be solved...")
            #self.input_values['photos_directory'] = self.photos_directory_edit.text() + "\\"
        
        # Disable UI elements
        self.update_text_label("") # delete text in text label
        self.stamping_mode_combo.setEnabled(False)
        self.photos_directory_edit.setEnabled(False)
        self.photos_directory_button.setEnabled(False)
        self.start_button.setEnabled(False)

        # Start the worker thread
        self.progress_bar.setValue(0)
        self.worker_thread.started.connect(standard.run(self.input_values, self))
        self.worker_thread.finished.connect(self.enable_ui_elements)
        self.worker_thread.start()
        self.progress_bar.setValue(100)

    def enable_ui_elements(self):
            self.stamping_mode_combo.setEnabled(True)
            self.photos_directory_edit.setEnabled(True)
            self.photos_directory_button.setEnabled(True)
            self.start_button.setEnabled(True)

def run():
    print("starting script...")
    app = QApplication([])

    input_values = {
        'logo_path': "resources/NuIEEE_logos",
        'photos_directory': "resources/photos_to_brandify",
        'branded_photos_directory': "brandified_photos",
    }
    modes = [
        {
            'name': "Standard",
            'script': "standard.py",
            'description': "Stamps the logo on the bottom-right corner of the image and decides whether it should stamp black or white."
        },
        {
            'name': "Tomada de Posse",
            'script': "tdp.py",
            'description': "Description for Tomada de Posse mode."
        },
        {
            'name': "Everywhere, Everything",
            'script': "everything.py",
            'description': "Description for 'Everywhere, Everything' mode."
        }
    ]

    window = InputWindow(input_values, modes)
    window.show()
    app.exec_()
