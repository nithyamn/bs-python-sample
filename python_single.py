from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time
username = os.getenv("BROWSERSTACK_USERNAME")
access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
build_name = os.getenv("BROWSERSTACK_BUILD_NAME")
browserstack_local = "true"
browserstack_local_identifier = os.getenv("BROWSERSTACK_LOCAL_IDENTIFIER")

desired_cap = {
 'browser': 'Chrome',
 'browser_version': 'latest',
 'os': 'Windows',
 'os_version' : '10',
 'name': 'BStack-[Python] Sample Test', # test name
 'build': build_name, # CI/CD job or build name
 'browserstack.user': username,
 'browserstack.key': access_key,
 'browserstack.local': browserstack_local,
 'browserstack.localIdentifier': browserstack_local_identifier
}
driver = webdriver.Remote(
    command_executor='https://hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=desired_cap)
driver.get("http://localhost:8888")
time.sleep(10)
driver.get("https://www.google.com")
if not "Google" in driver.title:
    raise Exception("Unable to load google page!")
elem = driver.find_element_by_name("q")
elem.send_keys("BrowserStack")
elem.submit()
try:
    WebDriverWait(driver, 5).until(EC.title_contains("BrowserStack"))
    # Setting the status of test as 'passed' or 'failed' based on the condition; if title of the web page starts with 'BrowserStack'
    driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Title matched!"}}')
except TimeoutException:
    driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Title not matched"}}')
print(driver.title)
driver.quit() 