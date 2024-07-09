import os.path
import jsonpickle

CONFIG_FILE = "config.json"


class Config:
    def __init__(self, bue_username, bue_password, ms_todo_token, ms_todo_list):
        self.bue_username = bue_username
        self.bue_password = bue_password
        self.ms_todo_token = ms_todo_token
        self.ms_todo_list = ms_todo_list
        self.course_aliases = {}
        self.ms_todo_courses_sections = {}


def save_config(config: Config):
    with open(CONFIG_FILE, "w+") as f:
        f.write(jsonpickle.encode(config))


def load_config() -> Config:
    if not os.path.isfile(CONFIG_FILE):
        return Config()

    with open(CONFIG_FILE, "r") as f:
        return jsonpickle.decode(f.read())


def is_configured() -> bool:
    return os.path.isfile(CONFIG_FILE)
