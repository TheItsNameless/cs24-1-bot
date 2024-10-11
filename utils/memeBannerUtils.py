import os
import random

import discord
from PIL import Image
from io import BytesIO
from utils.constants import Constants

async def save_meme_image(image: discord.Attachment) -> None:
    """
    Saves a meme image to the meme_images directory as a PNG, cropped to fit Discord banner size.
    """
    image_data = await image.read()
    image_stream = BytesIO(image_data)
    img = Image.open(image_stream)

    # Define the target size for the Discord banner
    target_width, target_height = 960, 339

    # Calculate the aspect ratio and resize the image to fit within the target dimensions
    img.thumbnail((target_width, target_height))

    # Create a new image with a black background
    new_img = Image.new(
        "RGB",
        (target_width, target_height),
        (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    # Calculate the position to paste the resized image onto the black background
    paste_x = (target_width - img.width) // 2
    paste_y = (target_height - img.height) // 2

    # Paste the resized image onto the black background
    new_img.paste(img, (paste_x, paste_y))

    # Convert image to PNG
    png_image_stream = BytesIO()
    new_img.save(png_image_stream, format='PNG')
    png_image_stream.seek(0)

    # Save the PNG image
    with open(f"{Constants.FILE_PATHS.MEME_FOLDER}/{image.filename.split('.jpg')[0]}.png", "wb") as f:
        f.write(png_image_stream.read())

def get_random_meme_image() -> bytes:
    """
    Returns a random meme image from the meme_images directory
    """
    meme_files = [f for f in os.listdir(Constants.FILE_PATHS.MEME_FOLDER) if f.endswith('.png')]

    if not meme_files:
        raise FileNotFoundError("No meme images found in the meme_images directory.")

    random_meme_file = random.choice(meme_files)
    meme_path = os.path.join(Constants.FILE_PATHS.MEME_FOLDER, random_meme_file)

    with open(meme_path, 'rb') as f:
        meme_image = f.read()

    return meme_image
