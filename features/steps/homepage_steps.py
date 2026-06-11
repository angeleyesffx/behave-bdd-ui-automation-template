from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from features.datapool import DATA_ACCESS
from features.object import Singleton
from features.pages.homepage import HomePage


@given(u'I navigate to the Google Home page')
def navigate_to_home_page(context):
    home = Singleton.getInstance(context, HomePage)
    context.browser.get(home.project_url)


@when(u'I search for {search_data}')
def search_for(context, search_data):
    home = Singleton.getInstance(context, HomePage)
    search_bar = WebDriverWait(context.browser, 15).until(
        EC.presence_of_element_located((By.NAME, home.search_bar))
    )
    search_bar.clear()
    info = home.datapool_read(DATA_ACCESS, search_data, 'language')
    search_bar.send_keys(info + Keys.RETURN)


@then(u'I should see the results')
def get_results(context):
    home = Singleton.getInstance(context, HomePage)
    result = WebDriverWait(context.browser, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, home.first_result))
    )
    assert result.is_displayed(), \
        f"Expected search results to be visible but none found on '{context.browser.current_url}'"


@then(u'the URL should contain the search query')
def verify_url_contains_query(context):
    current_url = context.browser.current_url
    assert "q=" in current_url, \
        f"Expected URL to contain search query parameter 'q=' but got: '{current_url}'"
