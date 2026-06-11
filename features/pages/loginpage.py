from selenium.webdriver.common.by import By

from features.pages.basepage import BasePage


class LoginPage(BasePage):

    project_url = "https://www.google.com/?gws_rd=ssl"
    card_box_layout = "#card_layout"
    email_field = "signInName"
    password_field = "password"
    sign_in_button = "next"
    error_message = "#errorMessage"

    local_directories = {
        "slogan": "hero__title",
        "filter_on_search_page": "js_filterlist",
    }
