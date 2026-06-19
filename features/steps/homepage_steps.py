from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from features.datapool import DATA_ACCESS
from features.object import Singleton
from features.pages.homepage import HomePage


@given(u'I navigate to the Products page')
def navigate_to_products_page(context):
    home = Singleton.getInstance(context, HomePage)
    context.browser.get(home.project_url)


@when(u'I search for {search_data}')
def search_for(context, search_data):
    home = Singleton.getInstance(context, HomePage)
    search_bar = WebDriverWait(context.browser, 15).until(
        EC.presence_of_element_located((By.ID, home.search_bar))
    )
    search_bar.clear()
    keyword = home.datapool_read(DATA_ACCESS, search_data, 'keyword')
    search_bar.send_keys(keyword)
    context.browser.find_element(By.ID, home.search_button).click()


@when(u'I submit an empty search')
def submit_empty_search(context):
    home = Singleton.getInstance(context, HomePage)
    search_bar = WebDriverWait(context.browser, 15).until(
        EC.presence_of_element_located((By.ID, home.search_bar))
    )
    search_bar.clear()
    context.browser.find_element(By.ID, home.search_button).click()


@then(u'I should see the results')
def get_results(context):
    home = Singleton.getInstance(context, HomePage)
    result = WebDriverWait(context.browser, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, home.first_result))
    )
    assert result.is_displayed(), \
        f"Expected search results to be visible but none found on '{context.browser.current_url}'"


@then(u'the search results page is shown')
def verify_search_results_page(context):
    home = Singleton.getInstance(context, HomePage)
    heading = WebDriverWait(context.browser, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, home.search_heading))
    )
    assert "searched" in heading.text.lower(), \
        f"Expected 'Searched Products' heading but got: '{heading.text}' on '{context.browser.current_url}'"


@then(u'I should see no products found')
def verify_no_results(context):
    home = Singleton.getInstance(context, HomePage)
    WebDriverWait(context.browser, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, home.search_heading))
    )
    results = context.browser.find_elements(By.CSS_SELECTOR, home.first_result)
    assert len(results) == 0, \
        f"Expected 0 products for non-existent search but found {len(results)} on '{context.browser.current_url}'"
