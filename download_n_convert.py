from PIL import Image
import requests
import os


def create_spritesheet(image_folder, output_path, images_per_row=16, padding=1):
    """Creates a spritesheet with padding between images."""
    image_files = sorted([f for f in os.listdir(image_folder) if f.lower(
    ).endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))])
    if not image_files:
        print(f"No images found in {image_folder}")
        return

    images = []
    for image_file in image_files:
        try:
            image_path = os.path.join(image_folder, image_file)
            img = Image.open(image_path)
            images.append(img)
        except Exception as e:
            print(f"Error opening image {image_file}: {e}")
            return

    sprite_width = images[0].width
    sprite_height = images[0].height
    num_images = len(images)
    num_rows = (num_images + images_per_row - 1) // images_per_row

    # Calculate spritesheet dimensions with padding
    spritesheet_width = (sprite_width + padding) * images_per_row - padding
    spritesheet_height = (sprite_height + padding) * num_rows - padding

    spritesheet = Image.new(
        "RGBA", (spritesheet_width, spritesheet_height), (0, 0, 0, 0))

    for i, img in enumerate(images):
        x = (i % images_per_row) * (sprite_width + padding)
        y = (i // images_per_row) * (sprite_height + padding)
        spritesheet.paste(img, (x, y))

    spritesheet.save(output_path)
    print(f"Spritesheet created at {output_path}")


def resize_and_dither(url_template, start_number, end_number, output_folder, transparent_color):
    """
    Iterates through links based on the provided template, resizes images to 32x32,
    applies Floyd-Steinberg dithering, and saves them in the output folder.

    Args:
        url_template (str): The template for constructing individual image URLs.
            Must contain a placeholder for the number (e.g., "{number}.png").
        start_number (int): The starting number for the sequence.
        end_number (int): The ending number for the sequence (inclusive).
        output_folder (str): The folder to save the resized and dithered images.
    """

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(os.path.join(output_folder, "RAW"), exist_ok=True)
    os.makedirs(os.path.join(output_folder, "FORMATTED"), exist_ok=True)

    errors = 0
    file_number = 1

    for number in range(start_number, end_number + 1):
        print(f"Processing image {number}...")
        url = url_template.format(number=number)

        try:
            response = requests.get(url, stream=True)  # Download the image
            response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.exceptions.RequestException as e:
            print(f"file_number: {file_number}")
            print(f"Error downloading {url}: {e}")
            errors += 1
            continue

        with open(os.path.join(output_folder,  "RAW", f"{file_number}.png"), 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        try:
            image = Image.open(os.path.join(
                output_folder,  "RAW", f"{file_number}.png"))
            resized_image = image.resize((32, 32), Image.LANCZOS)

# Replace alpha channel with a background color (e.g., white)
            if resized_image.mode in ("RGBA", "LA"):  # Directly has alpha
                background = Image.new(
                    "RGB", resized_image.size, transparent_color)
                try:
                    background.paste(
                        resized_image, mask=resized_image.split()[3])
                except IndexError:  # Handle images without alpha channel
                    # Paste without mask (full opacity)
                    background.paste(resized_image)
                resized_image = background
            elif resized_image.mode == "P" and "transparency" in resized_image.info:  # Indexed with transparency info
                resized_image = resized_image.convert(
                    "RGBA")  # Convert to RGBA to get alpha
                background = Image.new(
                    "RGB", resized_image.size, transparent_color)
                background.paste(resized_image, mask=resized_image.split()[3])
                resized_image = background
            elif resized_image.mode != "RGB":  # Other color modes, convert to RGB
                resized_image = resized_image.convert(
                    "RGBA")  # Convert to RGBA to get alpha
                background = Image.new(
                    "RGB", resized_image.size, transparent_color)
                background.paste(resized_image, mask=resized_image.split()[3])
                resized_image = background
                resized_image = resized_image.convert("RGB")

            resized_image = resized_image.convert(
                "RGB", palette=Image.ADAPTIVE, colors=8)
            resized_image.save(os.path.join(
                output_folder, "FORMATTED", f"{file_number}.png"))
            print(f"Image {number} processed successfully.")
        except FileNotFoundError:
            print(f"Failed to open image: {number}.png")
        except OSError as e:
            print(f"Error resizing and dithering {number}.png: {e}")

        file_number += 1

    print(f"Processing complete with {errors} errors.")


if __name__ == "__main__":

    url_template = "https://littlealchemy.com/hints/icons-png/{number}.png"
    start_number = 1
    end_number = 617
    transparent_color = (255, 0, 128)
    output_folder = "ELEMENTS"

    print("This script will download and process elements from Little Alchemy.")

    response = input("Do you want to download elements? (y/n): ")

    if response == "y" or response == "Y":

        print("Downloading elements...")
        resize_and_dither(url_template, start_number,
                          end_number, output_folder, transparent_color)
        print("Elements downloaded.")

    create_spritesheet(os.path.join(output_folder, "FORMATTED"), os.path.join(
        output_folder, "elements_spritesheet.png"), padding=2)
