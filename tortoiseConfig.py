from utils.constants import Constants

TORTOISE_ORM = {
    "connections": {
        "default": f"sqlite://{Constants.FILE_PATHS.DB_FILE}"
    },
    "apps": {
        "models": {
            "models": [
                "models.database.userData",
                "models.database.memeData",
                "models.database.aiData",
                "aerich.models",
            ],
            "default_connection":
            "default",
        },
    },
}
