from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from features.datapool import DATA_ACCESS
from features.object import Singleton
from features.pages.basepage import BasePage
from features.pages.loginpage import LoginPage
from features.pages.homepage import HomePage


@given(u'I navigate to the Login page')
def navigate_to_login_page(context):
    context.browser.get(context.location)


@when(u'I fill the credentials from {user}')
def fill_credentials(context, user):
    login_page = Singleton.getInstance(context, LoginPage)
    email = BasePage.datapool_read(DATA_ACCESS, user, 'email')
    password = BasePage.datapool_read(DATA_ACCESS, user, 'password')
    WebDriverWait(context.browser, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, login_page.card_box_layout))
    )
    context.browser.find_element(By.ID, login_page.email_field).send_keys(email)
    context.browser.find_element(By.ID, login_page.password_field).send_keys(password)
    context.browser.find_element(By.ID, login_page.sign_in_button).click()


@then(u'I should see the my home page')
def verify_home_page(context):
    home_page = Singleton.getInstance(context, HomePage)
    result = WebDriverWait(context.browser, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, home_page.first_result))
    )
    assert result.is_displayed(), \
        f"Expected home page content to be visible after login on '{context.browser.current_url}'"


@then(u'I should see an authentication error message')
def verify_auth_error(context):
    login_page = Singleton.getInstance(context, LoginPage)
    error = WebDriverWait(context.browser, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, login_page.error_message))
    )
    assert error.is_displayed(), \
        f"Expected authentication error message after invalid login on '{context.browser.current_url}'"
