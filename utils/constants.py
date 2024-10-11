from datetime import datetime


class ChannelIds:
    MENSA_CHANNEL = 846297031407435796
    
class ServerIds:
    CUR_SERVER = 844928169253142528
    
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
