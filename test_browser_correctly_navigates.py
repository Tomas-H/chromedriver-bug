import random
import time
import unittest
import os
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(level=logging.INFO, format="%(message)s")

class TestNavigation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Driver setup:
        - By default: system Chrome with chromedriver downloaded by Selenium Manager
        - If USE_CHROMIUM=1 in environment: use /usr/bin/chromium + /usr/bin/chromedriver  # chromedriver 128
        """
        options = Options()

        if os.getenv("USE_CHROMIUM128", "0") == "1":
            options.binary_location = "/usr/bin/chromium"
            service = Service("/usr/bin/chromedriver")
            cls.driver = webdriver.Chrome(service=service, options=options)
        else:
            # Remove any folder that contains the old chromedriver, so new one is downloaded
            old_paths = [p for p in os.environ["PATH"].split(os.pathsep) if "bin" not in p]
            os.environ["PATH"] = os.pathsep.join(old_paths)
            os.environ["SELENIUM_MANAGER_CACHE"] = "/tmp/selenium_drivers"

            cls.driver = webdriver.Chrome(options=options)

        version = cls.driver.capabilities.get("browserVersion") or cls.driver.capabilities.get("version")
        print(f"⚡ Using Chrome version: {version}")

        cls.wait = WebDriverWait(cls.driver, 20)

    def tearDown(self):
        if hasattr(self, "driver") and self.driver:
            self.driver.quit()

    def find_visible(self, by, locator, timeout=10):
        """Wait until element is visible, then return it."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, locator))
        )

    def test_browser_navigation_race(self):
        expected_url = "https://consumer.regtest.nic.cz/consumer/saml/"
        timeout = 5  # seconds
        for attempt in range(1, 50):
            with self.subTest(step="consumer_register_delete_and_navigate_to_other_url", iteration=attempt):
                consumer_name = f"{random.randint(1000000, 9999999)}"

                # Register consumer
                self.driver.get("https://consumer.regtest.nic.cz/consumer/oic/register/")
                self.find_visible(By.ID, "id_name").send_keys(consumer_name)
                self.find_visible(By.ID, "id_issuer").send_keys("https://mojeid.cz/oidc/")
                self.find_visible(By.CSS_SELECTOR, 'input[type="submit"]').click()
                self.find_visible(By.XPATH, f"//table//td[text()='{consumer_name}']")

                # Delete consumer
                self.driver.get("https://consumer.regtest.nic.cz/consumer/oic/list-clients/")
                self.find_visible(
                    By.XPATH,
                    f"//tr[contains(.,'{consumer_name}')]/td[contains(.,'Delete')]"
                ).click()
                self.find_visible(By.XPATH, "//input[@value='Confirm']").click()
                # Normally in the real test I would wait for some confirmation, that it's deleted,
                # but not for bug demonstration

                # Access another page (the bug sometimes happens here, it looks like the get request is lost)
                self.driver.get("https://consumer.regtest.nic.cz/consumer/saml/")

                start_time = time.time()
                current_url = ""
                while time.time() - start_time < timeout:
                    current_url = self.driver.current_url
                    if current_url == expected_url:
                        logging.info(f"Test NO {attempt} OK.")
                        break
                    time.sleep(0.2)

                self.assertEqual(current_url, expected_url)
