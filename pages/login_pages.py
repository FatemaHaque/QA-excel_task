# pages/login_page.py
from appium.webdriver.common.appiumby import AppiumBy
from utils.android_helpers import wait_visible, wait_clickable, exists

class LoginPage:
    # Try multiple reasonable selectors (adjust later after Appium Inspector)
    EMAIL_INPUTS = [
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").textContains("Email")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").textContains("email")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").textContains("Username")'),
    ]
    PASSWORD_INPUTS = [
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").textContains("Password")'),
    ]
    LOGIN_BTNS = [
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Login")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Sign In")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Login")'),
    ]

    def __init__(self, driver):
        self.driver = driver

    def is_displayed(self, timeout=4):
        # Heuristic: any email or password field visible?
        return any(exists(self.driver, loc, timeout=timeout) for loc in (self.EMAIL_INPUTS + self.PASSWORD_INPUTS))

    def _first_visible(self, locators):
        for loc in locators:
            if exists(self.driver, loc, timeout=1):
                return wait_visible(self.driver, loc)
        return None

    def login(self, username: str, password: str):
        email_el = self._first_visible(self.EMAIL_INPUTS)
        pwd_el   = self._first_visible(self.PASSWORD_INPUTS)
        btn_el   = self._first_visible(self.LOGIN_BTNS)

        if not (email_el and pwd_el and btn_el):
            raise RuntimeError("Login screen not fully detected (email/password/button).")

        email_el.click(); email_el.clear(); email_el.send_keys(username)
        pwd_el.click();   pwd_el.clear();   pwd_el.send_keys(password)
        btn_el.click()
