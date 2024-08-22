import bs4
from enum import Enum
import time
import requests
from requests_ntlm import HttpNtlmAuth
from config import Config

BUE_E_LEARNING_URL = "https://learn1.bue.edu.eg/login/index.php"

REDIRECTS_CALENDAR_URL = (
    f"https://learn1.bue.edu.eg/calendar/view.php?view=month&time={int(time.time())}"
)

CALENDAR_TABLE_ID = "#month-detailed-66c77365d26d266c77365adeb625"

COURSE_DATA_FILE = "courses.json"


class ItemType(Enum, str):
    ASSIGNMENT = "Assignment Submission"
    PROJECT = "Phase Submission"
    OTHERS = "Others"


class CourseItem:
    def __init__(self, item_title: str, item_link: str, item_type: ItemType) -> None:
        self.title = item_title
        self.link = item_link
        self.type = item_type


class Course:
    material: dict[str, CourseItem]

    def __init__(
        self, code, title, id, semester, material={}, announcements=""
    ) -> None:
        self.code = code
        self.title = title
        self.id = id
        self.semester = semester
        self.material = material
        self.announcements = announcements


class SubmissionScrapper:
    cached_courses: dict[str, Course]
    cached_pages: dict[str, bs4.BeautifulSoup] = {}

    def __init__(self, config: Config) -> None:
        self.config = config

    def scrape_bue_page(self, uri):
        if uri not in SubmissionScrapper.cached_pages:
            req = requests.get(
                BUE_E_LEARNING_URL + uri,
                auth=HttpNtlmAuth(self.config.bue_username, self.config.bue_password),
            )
            # TODO: complete the logic of the Scrapper
