import os
import random
import uuid
from datetime import datetime

import discord
from PIL import Image
from io import BytesIO

from models.database.memeData import Meme
from models.database.userData import User
from utils.constants import Constants


def bannerize_meme_image(image_data: bytes) -> bytes:
    """
    Converts a meme image to a Discord banner format.
    """
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

    return png_image_stream.read()


async def save_meme_image(image: discord.Attachment, author: User, message: str, date: datetime) -> None:
    """
    Saves the original meme image to the meme_images directory.
    """
    image_data = await image.read()
    image_stream = BytesIO(image_data)
    img = Image.open(image_stream)

    meme_uuid = str(uuid.uuid4())

    # Save the original image
    original_image_path = f"{Constants.FILE_PATHS.MEME_FOLDER}/{meme_uuid}.png"
    img.save(original_image_path)

    # Save metadata about the meme image
    await save_meme_metadata(meme_uuid, author, message, date)


async def save_meme_metadata(meme_uuid: str, author: User, message: str, date: datetime) -> None:
    """
    Saves metadata about the meme image to a CSV file.
    """
    await Meme.create(meme_uuid=meme_uuid, author=author, message=message, date=date)


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


def get_random_bannerized_meme() -> bytes:
    """
    Returns a random meme image from the meme_images directory, converted to Discord banner format.
    """
    # Get a random meme image
    random_meme_image = get_random_meme_image()

    # Convert the random meme image to banner format
    bannerized_image = bannerize_meme_image(random_meme_image)

    return bannerized_image
