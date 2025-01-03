import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time

class MacroScopeAuthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(10)
        cls.base_url = os.getenv("BASE_URL", "https://mmacroscope.com")
        cls.driver.get(cls.base_url)
        cls.wait = WebDriverWait(cls.driver, 10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_user_registration(self):
        """Test user registration flow."""
        driver = self.driver
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Register']"))
        ).click() 
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        email_input.send_keys(f"testuser{int(time.time())}@gmail.com")
        password_input.send_keys("testing1234")

        driver.find_element(By.CLASS_NAME, "auth-button").click()

        update_message = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "update-toast"))
        )
        self.assertIn(
            "Please check your email to verify your account", update_message.text
        )

    def test_user_login(self):
        """Test successful user login flow."""
        driver = self.driver
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
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        email_input.send_keys("ishaanratanshi2@gmail.com")
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

    def test_registration_with_invalid_email(self):
        """Test registration with an invalid email."""
        driver = self.driver
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Register']"))
        ).click()
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        email_input.send_keys("invalidemail")
        password_input.send_keys("testing1234")
        driver.find_element(By.CLASS_NAME, "auth-button").click()

        error_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "error-toast"))
        )
        self.assertIn("Invalid email address", error_message.text)

    def test_password_reset_flow(self):
        """Test the password reset functionality."""
        driver = self.driver
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Forgot Password?']"))
        ).click()
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys("testuser@gmail.com")
        driver.find_element(By.CLASS_NAME, "auth-button").click()

        success_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "update-toast"))
        )
        self.assertIn("Password reset email sent", success_message.text)

    def test_login_with_invalid_credentials(self):
        """Test login with incorrect credentials."""
        driver = self.driver
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        email_input.send_keys("testuser@gmail.com")
        password_input.send_keys("thisisnotapassword")
        driver.find_element(By.CSS_SELECTOR, ".auth-button").click()

        error_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "error-toast"))
        )
        self.assertIn("Invalid credentials", error_message.text)


    def test_dashboard_loading(self):
        """Test dashboard content loads correctly."""
        driver = self.driver
        self.wait.until(EC.url_contains("/dashboard"))

        dashboard_heading = driver.find_element(By.CLASS_NAME, "dashboard-title")
        self.assertEqual(dashboard_heading.text, "Welcome to MacroScope")

    def test_switch_between_graphs(self):
        """Test switching between different economic indicators."""
        driver = self.driver
        self.wait.until(EC.url_contains("/dashboard"))

        driver.find_element(By.ID, "gdp-button").click()
        gdp_graph = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "gdp-graph"))
        )
        self.assertTrue(gdp_graph.is_displayed())

        driver.find_element(By.ID, "inflation-button").click()
        inflation_graph = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "inflation-graph"))
        )
        self.assertTrue(inflation_graph.is_displayed())

    def test_data_tooltips(self):
        """Test tooltips on dashboard graphs."""
        driver = self.driver
        self.wait.until(EC.url_contains("/dashboard"))

        graph = driver.find_element(By.CLASS_NAME, "chartjs-render-monitor")
        webdriver.ActionChains(driver).move_to_element(graph).perform()

        tooltip = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "chart-tooltip"))
        )
        self.assertTrue(tooltip.is_displayed())

    def test_forecast_component_loading(self):
        """Test loading the forecast component."""
        driver = self.driver
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Forecast']"))
        ).click()
        self.wait.until(EC.url_contains("/forecast"))
        forecast_heading = driver.find_element(By.CLASS_NAME, "forecast-title")
        self.assertEqual(forecast_heading.text, "Forecast Analysis")

    def test_interactive_tip_stars(self):
        """Test clicking on tip stars to display tips."""
        driver = self.driver
        tip_star = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "tip-star"))
        )
        tip_star.click()

        tip_popup = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "tip-popup"))
        )
        self.assertTrue(tip_popup.is_displayed())

    def test_page_not_found(self):
        """Test 404 error handling."""
        driver = self.driver
        driver.get(self.base_url + "/non-existent-page")
        error_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "error-404"))
        )
        self.assertIn("Page Not Found", error_message.text)

    def test_server_error_handling(self):
        """Test 500 error handling."""
        driver = self.driver
        driver.get(self.base_url + "/trigger-server-error")
        error_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "error-500"))
        )
        self.assertIn("Server Error", error_message.text)

    def test_navigation_to_profile(self):
        """Test navigation to the Profile page."""
        driver = self.driver
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Profile']"))
        ).click()
        self.wait.until(EC.url_contains("/profile"))
        self.assertIn("profile", driver.current_url)

    def test_dark_mode_toggle(self):
        """Test toggling dark mode."""
        driver = self.driver
        toggle_button = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "dark-mode-toggle"))
        )
        toggle_button.click()

        body = driver.find_element(By.TAG_NAME, "body")
        self.assertIn("dark-mode", body.get_attribute("class"))

    def test_dashboard_loading(self):
        """Test dashboard content loads correctly."""
        driver = self.driver
        self.wait.until(EC.url_contains("/dashboard"))

        dashboard_heading = driver.find_element(By.CLASS_NAME, "dashboard-title")
        self.assertEqual(dashboard_heading.text, "Welcome to MacroScope")

    def test_switch_between_graphs(self):
        """Test switching between different economic indicators."""
        driver = self.driver
        self.wait.until(EC.url_contains("/dashboard"))

        driver.find_element(By.ID, "gdp-button").click()
        gdp_graph = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "gdp-graph"))
        )
        self.assertTrue(gdp_graph.is_displayed())

        driver.find_element(By.ID, "inflation-button").click()
        inflation_graph = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "inflation-graph"))
        )
        self.assertTrue(inflation_graph.is_displayed())

    def test_data_tooltips(self):
        """Test tooltips on dashboard graphs."""
        driver = self.driver
        self.wait.until(EC.url_contains("/dashboard"))

        graph = driver.find_element(By.CLASS_NAME, "chartjs-render-monitor")
        webdriver.ActionChains(driver).move_to_element(graph).perform()

        tooltip = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "chart-tooltip"))
        )
        self.assertTrue(tooltip.is_displayed())

if __name__ == "__main__":
    unittest.main()
