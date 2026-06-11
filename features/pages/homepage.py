from selenium.webdriver.common.by import By

from features.pages.basepage import BasePage


class HomePage(BasePage):

    project_url = "https://www.google.com/?gws_rd=ssl"
    search_bar = "q"
    first_result = "#rso h3"

    local_directories = {
        "slogan": "hero__title",
        "filter_on_search_page": "js_filterlist",
    }
