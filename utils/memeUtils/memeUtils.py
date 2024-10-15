import os
import random
import uuid
from datetime import datetime

import discord
from PIL import Image, ImageSequence, ImageFile
from io import BytesIO

from models.database.memeData import Meme, MemeFormat
from models.database.userData import User
from utils.constants import Constants
from utils.memeUtils.memeBannerUtils import bannerize_meme_image


async def save_meme_image(image: discord.Attachment, author: User, message: str, date: datetime) -> None:
    """
    Saves the original meme image to the meme_images directory.
    """
    image_data = await image.read()
    image_stream = BytesIO(image_data)
    img = Image.open(image_stream)

    meme_uuid = str(uuid.uuid4())
    extension = 'gif' if img.format == 'GIF' else 'png'

    # Save the original image
    original_image_path = f"{Constants.FILE_PATHS.RAW_MEME_FOLDER}/{meme_uuid}.{extension}"
    save_meme_image_file(img, original_image_path)

    # Create a bannerized version of the image and save it
    bannerized_image = bannerize_meme_image(image_data, extension == "gif")
    bannerized_image_path = f"{Constants.FILE_PATHS.BANNERIZED_MEME_FOLDER}/{meme_uuid}.{extension}"
    save_meme_image_file(Image.open(BytesIO(bannerized_image)), bannerized_image_path)

    # Save metadata about the meme image
    await save_meme_metadata(meme_uuid, MemeFormat(extension), author, message, date)


def save_meme_image_file(img: ImageFile, path: str) -> None:
    if img.format == "GIF":
        frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
        frames[0].save(path, save_all=True, append_images=frames[1:], loop=0, format='GIF')
    else:
        img.save(path)


async def save_meme_metadata(
    meme_uuid: str, meme_format: MemeFormat, author: User, message: str, date: datetime) -> None:
    """
    Saves metadata about the meme image to a CSV file.
    """
    await Meme.create(uuid=meme_uuid, format=meme_format, author=author, message=message, date=date)


async def get_random_meme(bannerized: bool) -> bytes:
    """
    Returns a random meme image from the database.
    :param bannerized: Whether to return a bannerized version of the meme.
    :return:
    """
    memes = await Meme.all()

    if len(memes) == 0:
        raise ValueError("No meme images found in the database.")

    random_meme: Meme = random.choice(memes)
    meme_path = os.path.join(
        Constants.FILE_PATHS.BANNERIZED_MEME_FOLDER if bannerized else Constants.FILE_PATHS.RAW_MEME_FOLDER,
        f"{random_meme.uuid}.{random_meme.format.value}")

    with open(meme_path, 'rb') as f:
        meme_image = f.read()

    return meme_image
