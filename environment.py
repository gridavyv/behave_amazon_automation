from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import re

def before_feature(context, feature):
    context.WAIT_TIME = 10
    context.PAGE_URL = "https://www.ebay.com/"  # store the constant on feature layer


def before_scenario(context, scenario):
    # set options to remain window open
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option(name="detach", value=True)
    chrome_options.add_argument("--start-maximized")
    context.driver = webdriver.Chrome(options=chrome_options)
    context.cur_banner_text = ""
    context.result_links = {}


def after_step(context, step):
    if step.status == 'failed':
        # step_name = re.sub(pattern="[^a-zA-Z0-9 \n\.]", repl="_", string=step.name).lower()
        clean_step_name = "_".join(re.findall(pattern='\w+', string=step.name.lower()))
        context.driver.save_screenshot(f"failed_steps_screenshots/{clean_step_name}.png")

def after_scenario(context, scenario):
    context.driver.close()
    print("Browser is closed.")
    context.driver.quit()
    print("Driver is quited.")
