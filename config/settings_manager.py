import json
import os


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

SETTINGS_FILE = os.path.join(
    BASE_DIR,
    "settings.json"
)


DEFAULT_SETTINGS = {
    "player": {
        "default_username": "Player1"
    },

    "controls": {
        "mobile": True
    },

    "sound": {
        "volume": 0.7
    }
}


def load_settings():

    if not os.path.exists(SETTINGS_FILE):

        save_settings(DEFAULT_SETTINGS)

        return DEFAULT_SETTINGS.copy()

    try:

        with open(
            SETTINGS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            settings = json.load(file)

        if not isinstance(settings, dict):

            raise ValueError(
                "Settings must be a JSON object"
            )

        # PLAYER
        if (
            "player" not in settings
            or not isinstance(
                settings["player"],
                dict
            )
        ):

            settings["player"] = {}

        # CONTROLS
        if (
            "controls" not in settings
            or not isinstance(
                settings["controls"],
                dict
            )
        ):

            settings["controls"] = {}

        # SOUND
        if (
            "sound" not in settings
            or not isinstance(
                settings["sound"],
                dict
            )
        ):

            settings["sound"] = {}

        settings["player"].setdefault(
            "default_username",
            DEFAULT_SETTINGS["player"][
                "default_username"
            ]
        )

        settings["controls"].setdefault(
            "mobile",
            DEFAULT_SETTINGS["controls"]["mobile"]
        )

        settings["sound"].setdefault(
            "volume",
            DEFAULT_SETTINGS["sound"]["volume"]
        )

        # Volume validation
        try:

            settings["sound"]["volume"] = max(
                0.0,
                min(
                    1.0,
                    float(
                        settings["sound"]["volume"]
                    )
                )
            )

        except (
            TypeError,
            ValueError
        ):

            settings["sound"]["volume"] = (
                DEFAULT_SETTINGS["sound"]["volume"]
            )

        # Mobile validation
        settings["controls"]["mobile"] = bool(
            settings["controls"]["mobile"]
        )

        save_settings(settings)

        return settings

    except (
        json.JSONDecodeError,
        OSError,
        ValueError
    ):

        save_settings(
            DEFAULT_SETTINGS
        )

        return DEFAULT_SETTINGS.copy()


def save_settings(settings):

    os.makedirs(
        BASE_DIR,
        exist_ok=True
    )

    with open(
        SETTINGS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            settings,
            file,
            indent=4
        )