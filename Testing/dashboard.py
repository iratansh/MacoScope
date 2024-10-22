from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time

class MacroScopeDashboardTests(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.driver.get("http://localhost:5173/")
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_user_registration(self):
        """Test user registration flow."""
        driver = self.driver

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Register']"))
        ).click()
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        email_input.send_keys(f"testuser{int(time.time())}@gmail.com")
        password_input.send_keys("testing")

        driver.find_element(By.CLASS_NAME, ".auth-button").click()

        update_message = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "update-toast"))
        )

        self.assertIn(
            "Please check your email to verify your account", update_message.text
        )

    def test_user_login(self):
        """Test successful user login flow."""
        driver = self.driver

        # Input existing user credentials
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        email_input.send_keys("ishaanratanshi1@gmail.com")
        password_input.send_keys("abcd")

        driver.find_element(By.CSS_SELECTOR, ".auth-button").click()

        self.wait.until(EC.url_contains("/dashboard"))
        self.assertIn("dashboard", driver.current_url)

    def test_login_with_unverified_account(self):
        """Test login attempt with an unverified account."""
        driver = self.driver

        # Input unverified user credentials
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        email_input.send_keys("carl.pong4@gmail.com")
        password_input.send_keys("1234")

        driver.find_element(By.CSS_SELECTOR, ".auth-button").click()
        error_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "error-toast"))
        )
        self.assertIn("Your account is not activated", error_message.text)

    def test_forgot_password(self):
        """Test the forgot password navigation."""
        driver = self.driver
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Forgot Password?']"))
        ).click()
        self.wait.until(EC.url_contains("/forgot-password"))
        self.assertIn("forgot-password", driver.current_url)


if __name__ == "__main__":
    unittest.main()
