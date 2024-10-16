import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()


class ChannelIds:
    MENSA_CHANNEL = int(os.getenv("MENSA_CHANNEL"))
    MEME_CHANNEL = int(os.getenv("MEME_CHANNEL"))


class ServerIds:
    CUR_SERVER = int(os.getenv("CUR_SERVER"))


class Reactions:
    CHECK = "✅"
    CROSS = "❌"


class FilePaths:
    RAW_MEME_FOLDER = "data/memes/raw"
    BANNERIZED_MEME_FOLDER = "data/memes/bannerized"
    OCR_DATA_FOLDER = "data/ocr"
    DB_FILE = os.getenv("DB_FILE_PATH")


class Urls:
    MENSAPLAN = "https://www.studentenwerk-leipzig.de/mensen-cafeterien/speiseplan/?location=140&date="


class Constants:
    CHANNEL_IDS = ChannelIds
    SERVER_IDS = ServerIds
    REACTIONS = Reactions
    URLS = Urls
    FILE_PATHS = FilePaths
    # --- ADDITIONAL CONSTANTS ---
    SYSTIMEZONE = datetime.now().astimezone(
    ).tzinfo
