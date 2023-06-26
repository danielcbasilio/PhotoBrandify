from PIL import Image
import os
from PyQt5.QtWidgets import QApplication
from src.constants import *
import math
from tqdm import tqdm

def get_info():
    return {
        "name": "Everything, everywhere",
        "description": "White, black, blue or dark blue logo. Bottom-center, upper-left, upper-right, bottom-left, bottom-right and a powerful algorithm to determine the optimal combination. You'll just have to wait though."
    }

# define logo dimensions
logo_path_blue = LOGO_PATH + "/" + "NuIEEE_logo_blue.png"
logo_template = Image.open(logo_path_blue)
logo_template = logo_template.convert("RGBA")
logo_width = int(1.5 * logo_template.size[0])
logo_height = int((logo_width / logo_template.size[0]) * logo_template.size[1])
logo_displacement_x = int(logo_width/2)
logo_displacement_y = int(logo_height*3/4)
logo_template = logo_template.resize((logo_width, logo_height), Image.LANCZOS)

# tests if the region is suitable to place logo and assigns scores to all colors
def test_position(photo, x, y):
    region = photo.crop((x, y, x + logo_width, y + logo_height))
    region = region.convert("RGB")
    region_data = region.getdata()
    #plt.imshow(region)
    #plt.axis('off')
    #plt.show()

    pixel_count = 0

    brightness_sum = 0
    for pixel in region_data:
        r, g, b = pixel[:3]
        brightness = (r + g + b) / 3
        brightness_sum += brightness
        pixel_count += 1
        average_brightness = brightness_sum / pixel_count

    pixel_count = 0
    brightness_sum = 0
    red_sum = 0
    green_sum = 0
    blue_sum = 0

    for pixel in region_data:
        r, g, b = pixel[:3]
        brightness = (r + g + b) / 3
        brightness_sum += brightness
        red_sum += r
        green_sum += g
        blue_sum += b
        pixel_count += 1

    average_brightness = brightness_sum / pixel_count
    average_red = red_sum / pixel_count
    average_green = green_sum / pixel_count
    average_blue = blue_sum / pixel_count

    brightness_variance = 0
    red_variance = 0
    green_variance = 0
    blue_variance = 0

    for pixel in region_data:
        r, g, b = pixel[:3]
        brightness_variance += (brightness - average_brightness) ** 2
        red_variance += (r - average_red) ** 2
        green_variance += (g - average_green) ** 2
        blue_variance += (b - average_blue) ** 2

    brightness_stddev = math.sqrt(brightness_variance / pixel_count)
    #red_stddev = math.sqrt(red_variance / pixel_count)
    #green_stddev = math.sqrt(green_variance / pixel_count)
    blue_stddev = math.sqrt(blue_variance / pixel_count)

    # resizing photo for analysis
    photo = photo.resize((int(photo.width/6), int(photo.height/6)), Image.LANCZOS)
    photo = photo.convert("RGB")

    blue_sum = 0
    photo_data = photo.getdata()
    for pixel in photo_data:
        r, g, b = pixel[:3]
        blue = (r/2 + g/2 + b*2) / 3
        blue_sum += blue
        pixel_count += 1
        average_blue = blue_sum / pixel_count
        
    darkblue_sum = 0
    photo_data = photo.getdata()
    for pixel in photo_data:
        r, g, b = pixel[:3]
        darkblue = b
        darkblue_sum += darkblue
        pixel_count += 1
        average_darkblue = darkblue_sum / pixel_count

    white_score = int((255*100)/(1 + average_brightness) - brightness_stddev*5)
    black_score = int((average_brightness*7/255) * 100 - brightness_stddev*5)
    blue_score = int((average_blue*15/255) * 100 + (average_brightness*2/255) * 100 - brightness_stddev*4 - blue_stddev*2)
    darkblue_score = int((average_darkblue*13/255) * 100 + (average_brightness*5/255) * 100 - brightness_stddev*4 - blue_stddev*2)

    return {
        "white": white_score,
        "black": black_score,
        "blue": blue_score,
        "darkblue": darkblue_score
    } 

# gets all possible positions
def possible_positions(photo):
    # upper-left corner
    x_ul = int(logo_displacement_x - logo_width/8)
    y_ul = int(logo_displacement_y)
    ul = (x_ul, y_ul)

    # upper-right corner
    x_ur = int(photo.width - logo_width - logo_displacement_x)
    y_ur = int(logo_displacement_y)
    ur = (x_ur, y_ur)

    # bottom-left corner
    x_bl = int(logo_displacement_x - logo_width/8)
    y_bl = int(photo.height - logo_height - logo_displacement_y)
    bl = (x_bl, y_bl)

    # bottom-right corner
    x_br = int(photo.width - logo_width - logo_displacement_x)
    y_br = int(photo.height - logo_height - logo_displacement_y)
    br = (x_br, y_br)

    # bottom-center alignment
    x_bc = int(photo.width/2 - logo_width/2 - logo_displacement_x/4)
    y_bc = int(photo.height - logo_height - logo_displacement_y)
    bc = (x_bc, y_bc)

    return [bc, ul, ur, bl, br]

# finds the best color and position for the logo
def best_position_logo(photo, window_text):
    position_array = []
    possible_positions_array = possible_positions(photo)

    for i, position in enumerate(possible_positions_array):
        window_text.append("Checking position " + str(i+5) + ".")
        window_text.ensureCursorVisible()
        QApplication.processEvents()
        position_array.append(test_position(
            photo, 
            possible_positions_array[i][0],
            possible_positions_array[i][1]
        ))
    
    print(position_array)
    best = 0
    for index, position in enumerate(position_array):
        for color, value in position.items():
            if value > best:
                best = value
                best_index = index
                best_color = color

    return {
        'position': possible_positions_array[best_index],
        'color': best_color
    }

# get resized logo with given the color
def get_logo(logo_color):
    logo = Image.open(LOGO_PATH + "/" + f'NuIEEE_logo_{logo_color}.png')
    logo = logo.convert("RGBA")
    logo = logo.resize((logo_width, logo_height), Image.LANCZOS)
    return logo

def run(photos_directory, window_text, window_progress_bar):
    print("running the stamping mode that will stamp everything, everywhere...")
    # getting the files
    total_files = len(os.listdir(photos_directory))
    completed_files = 0
    filename_array = list(filter(lambda filename: filename.endswith(".jpg") 
                                or filename.endswith(".png") 
                                or filename.endswith(".JPG"), 
                            os.listdir(photos_directory)))
    total_i = len(filename_array)
    print(filename_array)

    for i, filename in enumerate(filename_array):
        # getting the photo
        photo_path = photos_directory + "/" + filename
        photo = Image.open(photo_path)
        photo = photo.convert("RGBA")

        # Progress
        ## progress text
        tqdm.write("Making photo: " + filename)
        window_text.append("Making photo: " + filename + " (" + str(i+1) + " of " + str(total_i) + ")")
        window_text.ensureCursorVisible()
        ## progress bar
        completed_files += 1
        progress = int((completed_files / total_files) * 100)
        window_progress_bar.setValue(progress)
        QApplication.processEvents()  # Update the GUI

        # paste the logo in the right position in the photo
        window_text.append("Finding the best position and color for " + filename + "...")
        window_text.ensureCursorVisible()
        QApplication.processEvents()
        best_position = best_position_logo(photo, window_text)
        position = best_position['position']
        logo_color = best_position['color']
        logo = get_logo(logo_color)
        image_with_logo = Image.new("RGBA", photo.size)
        image_with_logo.paste(photo, (0, 0))
        image_with_logo.paste(logo, position, mask=logo.split()[3])

        # save the created photo in memory
        new_filename = "logo_" + filename
        new_photo_path = os.path.join(BRANDED_PHOTOS_DIRECTORY, new_filename)
        image_with_logo.save(new_photo_path, format="PNG")

    # progress bar finished
    window_progress_bar.setValue(100)
    window_text.append("Finished processing photos.")
    window_text.ensureCursorVisible()
    QApplication.processEvents()  # Update the GUI