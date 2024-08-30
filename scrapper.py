import bs4
import requests
import time
import calendar
from datetime import date, datetime
from config import Config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

LOGIN_URL = "https://learn1.bue.edu.eg/login/index.php"
CALENDAR_URL = "https://learn1.bue.edu.eg/calendar/view.php"


def automate_getting_calendar(config: Config) -> requests.Response:
    """
    This function automates logging in to the BUE E-Learning using Selenium
    to get the user specific Calendar page

    Args:
        config (Config): User Specific Configration file

    Returns:
        requests.Response: User's Calendar page to be web scraped later
    """

    # Set up Selenium WebDriver (make sure the WebDriver executable is in your PATH)
    driver = webdriver.Chrome()  # or use webdriver.Firefox() for Firefox

    # Open the login page
    driver.get(LOGIN_URL)

    # Perform login
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "loginbtn")

    username.send_keys(config.bue_username)
    password.send_keys(config.bue_password)
    login_button.send_keys(Keys.RETURN)

    # Wait for the login to complete
    time.sleep(1)  # Adjust if needed based on the site

    # Retrieve cookies from Selenium
    cookies = driver.get_cookies()

    # Convert cookies to a format that `requests` can use
    cookies_dict = {cookie["name"]: cookie["value"] for cookie in cookies}

    # Close the WebDriver
    driver.quit()

    # Use cookies with requests
    session = requests.Session()
    session.cookies.update(cookies_dict)

    # Make the request to the calendar page with the following query params
    params = {
        "view": "month",
        "time": int(time.time()),
    }
    response = session.get(CALENDAR_URL, params=params)

    return response


def get_submission_date(day) -> str:
    current_month_name = calendar.month_name[date.today().month]
    year = datetime.now().year
    return f"{day}/{current_month_name}/{year}"


def scrape_bue_calendar(config: Config):
    res = automate_getting_calendar(config)
    soup = bs4.BeautifulSoup(res.content, "html.parser")

    print("Scrapping BUE Calendar for Submissions...")
    # Find all days with submissions
    days_with_submissions = soup.find_all("td", class_="clickable")
    if not days_with_submissions:
        print("No days with submissions found.")
        return

    submissions = []
    for day in days_with_submissions:
        date_element = day.find("a", class_="day")
        if not date_element:
            continue
        date = date_element.text.strip()

        # Find the div containing day-content
        day_content = day.find("div", {"data-region": "day-content"})
        if not day_content:
            continue

        # Find all submission items within this day-content
        submission_items = day_content.find_all("li", {"data-region": "event-item"})
        for submission in submission_items:
            title_element = submission.find("span", class_="eventname")
            link_element = submission.find("a", {"data-action": "view-event"})
            if title_element and link_element:
                submission_details = {
                    "date": get_submission_date(date),
                    "title": title_element.text.strip(),
                    "link": link_element["href"],
                }
                submissions.append(submission_details)

    # if not submissions:
    #     print("No submissions found.")
    # else:
    #     for submission in submissions:
    #         print(f"Date: {submission['date']}")
    #         print(f"Title: {submission['title']}")
    #         print(f"Link: {submission['link']}")
    #         print("----------")
    return submissions
