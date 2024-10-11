import os
from datetime import datetime


class ChannelIds:
    MENSA_CHANNEL = os.getenv("MENSA_CHANNEL")
    
class ServerIds:
    CUR_SERVER = os.getenv("CUR_SERVER")
    
class Reactions:
    CHECK = "✅"
    CROSS = "❌"
    
class Urls:
    MENSAPLAN = "https://www.studentenwerk-leipzig.de/mensen-cafeterien/speiseplan/?location=140&date="
    
class Constants:
    CHANNEL_IDS = ChannelIds
    SERVER_IDS = ServerIds
    REACTIONS = Reactions
    URLS = Urls
    # --- ADDITIONAL CONSTANTS ---
    SYSTIMEZONE = datetime.now().astimezone(
    ).tzinfo 
