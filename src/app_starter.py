from PyQt5.QtWidgets import QApplication
import importlib
import os
from src.brandify_ui import InputWindow

def run():
    print("starting script...")
    app = QApplication([])
    input_values = {
        'logo_path': "resources/NuIEEE_logos",
        'photos_directory': "resources/photos_to_brandify",
        'branded_photos_directory': "brandified_photos"
    }

    # gets info from all mode scripts inside the modes directory
    modes_scripts = list(filter(lambda mode: mode.endswith(".py"), os.listdir("src/modes/")))
    modes = []
    for mode in modes_scripts:
        curr_mode = os.path.splitext(mode)[0]  # Remove the .py extension
        try:
            # Import the module
            module = importlib.import_module(f'src.modes.{curr_mode}')
            print(f"Module '{curr_mode}' imported successfully.")
            modes.append({
                "name": module.get_info()["name"],
                "module": module,
                "description": module.get_info()["description"]
            })

        except ImportError as e:
            print(f"Error importing module '{curr_mode}': {str(e)}") 

    window = InputWindow(input_values, modes)
    window.show()
    app.exec_()