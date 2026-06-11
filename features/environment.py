import os
import datetime
import yaml
from dotenv import load_dotenv
from selenium import webdriver

load_dotenv()

_file_path = os.path.dirname(__file__)


def _browser_config(browser_name):
    if browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-geolocation")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-translate")
        return webdriver.Firefox(options=options)

    if browser_name == "headless-chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    if browser_name == "edge":
        return webdriver.Edge()

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-geolocation")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


def _take_screenshot(context, scenario):
    path_screenshots = os.path.join(_file_path, "screenshots")
    os.makedirs(path_screenshots, exist_ok=True)
    date_hour = datetime.datetime.now().strftime("%d-%m-%y-%H-%M-%S")
    scenario_name = scenario.feature.name.replace(' ', '_')
    filename = f"BUG-{scenario_name}-{date_hour}.png"
    context.browser.save_screenshot(os.path.join(path_screenshots, filename))


def before_all(context):
    os.makedirs(os.path.join("build", "behave.reports"), exist_ok=True)


def before_scenario(context, scenario):
    browser_name = context.config.userdata.get('browser', 'chrome')
    context.browser = _browser_config(browser_name)
    context.browser.implicitly_wait(30)
    context.browser.set_page_load_timeout(30)

    env_key = context.config.userdata.get('environment', 'homolog')
    environment_config = yaml.safe_load(
        open(os.path.join(_file_path, "config.yml"))
    ).get(env_key, {})

    context.location = environment_config.get('url')
    context.base_url = os.environ.get('BASE_URL', environment_config.get('base_url', ''))
    context.user = os.environ.get('APP_USER')
    context.password = os.environ.get('APP_PASSWORD')
    context.some_api_url = environment_config.get('some_api_url')
    context.whatever_api = environment_config.get('whatever_api_url')
    context.username_some_api = os.environ.get('SOME_API_USER', environment_config.get('username_some_api'))
    context.password_some_api = os.environ.get('SOME_API_PASSWORD', environment_config.get('password_some_api'))
    context.username_whatever_api = os.environ.get('WHATEVER_API_USER', environment_config.get('username_whatever_api'))
    context.password_whatever_api = os.environ.get('WHATEVER_API_PASSWORD', environment_config.get('password_whatever_api'))


def after_scenario(context, scenario):
    if scenario.status == 'failed':
        _take_screenshot(context, scenario)
    context.browser.quit()
