from PIL import Image
import os

def get_logo_test(input_values):
    return {
        'color': "blue"
    }

def get_logo(filename, input_values):
    logo_path = input_values['logo_path'] + "NuIEEE_logo_blue.png"
    logo_size_ratio = input_values['logo_size_ratio']
    logo_displacement_x = input_values['logo_displacement_x']
    logo_displacement_y = input_values['logo_displacement_y']
    photo_path = input_values['photos_directory'] + filename

    logo = Image.open(logo_path) #still to be decided after when color has been detected
    logo = logo.convert("RGBA")
    logo_width = int(logo_size_ratio * logo.size[0])
    logo_height = int((logo_width / logo.size[0]) * logo.size[1])
    logo = logo.resize((logo_width, logo_height), Image.ANTIALIAS)

    photo = Image.open(photo_path)
    region = photo.crop((logo_displacement_x, logo_displacement_y, logo_displacement_x + logo_width, logo_displacement_y + logo_height))
    region = region.convert("RGB")
    region_data = region.getdata()

    brightness_threshold = 150  # Adjust as needed

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
    
    return {
        'path': input_values['logo_path'] + f'NuIEEE_logo_{logo_color}.png', #still to finish
        'color': logo_color
    }

def add_logo_to_photos(logo_path, photos_directory, branded_photos_directory, logo_size_ratio, logo_displacement_x, logo_displacement_y):
    logo = Image.open(logo_path + "NuIEEE_logo_blue.png")
    logo = logo.convert("RGBA")
    logo_width = int(logo_size_ratio * logo.size[0])
    logo_height = int((logo_width / logo.size[0]) * logo.size[1])
    logo = logo.resize((logo_width, logo_height), Image.ANTIALIAS)

    if not os.path.exists(branded_photos_directory):
        os.makedirs(branded_photos_directory)

    for filename in os.listdir(photos_directory):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".JPG"):
            photo_path = os.path.join(photos_directory, filename)
            photo = Image.open(photo_path)
            photo = photo.convert("RGBA")

            # Calculate the position for the logo (bottom right corner)
            position = (photo.width - logo.width - logo_displacement_x, photo.height - logo.height - logo_displacement_y)

            # Create a new image with the logo on top of the photo
            image_with_logo = Image.new("RGBA", photo.size)
            image_with_logo.paste(photo, (0, 0))
            image_with_logo.paste(logo, position, mask=logo.split()[3])
            print("Making photo: " + filename)

            # Save the new image with the logo
            new_filename = "logo_" + filename
            new_photo_path = os.path.join(branded_photos_directory, new_filename)
            image_with_logo.save(new_photo_path, format="PNG")

# INSERT VALUES HERE:
input_values = {
    'logo_path' : "NuIEEE_logos/",
    'photos_directory' : "test_datattack_photos/",
    'branded_photos_directory' : "new_photos_test/",
    'logo_size_ratio' : 1.5,
    'logo_displacement_x' : 400,
    'logo_displacement_y' : 250
}

def main():
    print("starting script...")
    for filename in os.listdir(input_values['photos_directory']):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".JPG"):
            logo_object = get_logo(filename, input_values)
            print(logo_object)
    #add_logo_to_photos(logo_path, photos_directory, branded_photos_directory, logo_size_ratio, logo_displacement_x, logo_displacement_y)

if __name__ == "__main__":
    main()
