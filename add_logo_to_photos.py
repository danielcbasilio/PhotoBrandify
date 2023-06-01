from PIL import Image
import os

logo_path = "NuIEEE_logo_blue.png"
photos_directory = "test_datattack_photos/"
braded_photos_directory = "branded_photos_test/"
logo_size_ratio = 1.5

def add_logo_to_photos(logo_path, photos_directory):
    logo = Image.open(logo_path)
    logo = logo.convert("RGBA")
    logo_width = int(logo_size_ratio * logo.size[0])
    logo_height = int((logo_width / logo.size[0]) * logo.size[1])
    logo = logo.resize((logo_width, logo_height), Image.ANTIALIAS)

    for filename in os.listdir(photos_directory):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".JPG"):

            photo_path = os.path.join(photos_directory, filename)
            photo = Image.open(photo_path)
            photo = photo.convert("RGBA")

            # Calculate the position for the logo (bottom right corner)
            position = (photo.width - logo.width - 400, photo.height - logo.height - 250)

            # Create a new image with the logo on top of the photo
            image_with_logo = Image.new("RGBA", photo.size)
            image_with_logo.paste(photo, (0, 0))
            image_with_logo.paste(logo, position, mask=logo.split()[3])
            print("Making photo: " + filename)
            # Save the new image with the logo
            new_filename = "logo_" + filename
            new_photo_path = os.path.join(braded_photos_directory, new_filename)
            image_with_logo.save(new_photo_path, format="PNG")

add_logo_to_photos(logo_path, photos_directory)