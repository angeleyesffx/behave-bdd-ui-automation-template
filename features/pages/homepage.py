from selenium.webdriver.common.by import By

from features.pages.basepage import BasePage


class HomePage(BasePage):

    project_url = "https://automationexercise.com/products"
    search_bar = "search_product"   # id
    search_button = "submit_search"  # id
    first_result = ".productinfo p"
    search_heading = "h2.title"

    local_directories = {
        "slogan": "hero__title",
        "filter_on_search_page": "js_filterlist",
    }
