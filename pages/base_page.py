from appium.webdriver.common.appiumby import AppiumBy
from utils.android_helpers import wait_clickable, wait_visible

class BasePage:
    def __init__(self, driver, app_package="com.arcone.arcone"):
        self.driver = driver
        self.app_package = app_package

    def by_id(self, rid: str):
        """
        Resolves a resource-id either fully-qualified or short.
        Usage: self.by_id("id/submit") or self.by_id("com.arcone.arcone:id/submit")
        """
        rid = rid if ":" in rid else f"{self.app_package}:{rid if rid.startswith('id/') else 'id/' + rid}"
        return (AppiumBy.ID, rid)

    def by_text(self, text: str):
        return (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')

    def click_text(self, text: str):
        el = wait_clickable(self.driver, self.by_text(text))
        el.click()
        return el

    def wait_visible(self, locator):
        return wait_visible(self.driver, locator)

    def wait_clickable(self, locator):
        return wait_clickable(self.driver, locator)
