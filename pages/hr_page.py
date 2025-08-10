from appium.webdriver.common.appiumby import AppiumBy
from utils.android_helpers import (
    wait_visible, wait_clickable, exists, set_date_via_textbox,
    datepicker_is_open, datepicker_select_exact_date
)
from selenium.common.exceptions import TimeoutException
import os, time, datetime as dt


class HRPage:
    def __init__(self, driver, app_package="com.arcone.arcone"):
        self.driver = driver
        self.app_package = app_package

        self.TILE_MY_ATTENDANCE     = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("My Attendance")')
        self.TILE_LEAVE_APPLICATION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Leave Application")')

        self.CHECK_IN_BTN  = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Check-IN")')
        self.CHECK_OUT_BTN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Check-OUT")')

        self.NO_DATA_LABELS = [
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("No data")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("No record")'),
            (AppiumBy.XPATH, '//*[contains(@text,"No data") or contains(@text,"No record")]'),
        ]

        self.FROM_INPUTS = [
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("From")'),
            (AppiumBy.XPATH, '//*[@text="From" or contains(@resource-id,"from")]'),
        ]
        self.TO_INPUTS = [
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("To")'),
            (AppiumBy.XPATH, '//*[@text="To" or contains(@resource-id,"to")]'),
        ]
        self.STATUS_OPENERS = [
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Status")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("All")'),
            (AppiumBy.XPATH, '//*[@text="Status" or @text="All" or contains(@resource-id,"status")]'),
        ]
        self.SEARCH_BUTTONS = [
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Search")'),
            (AppiumBy.ACCESSIBILITY_ID, "Search"),
            (AppiumBy.XPATH, '//*[@text="Search" or @content-desc="Search"]'),
        ]
        self.RESULTS_LIST = (AppiumBy.XPATH, '//*[@class="androidx.recyclerview.widget.RecyclerView" or contains(@resource-id, "recycler")]')

        self.ADD_LEAVE_BTN       = (AppiumBy.ACCESSIBILITY_ID, "Add")
        self.LEAVE_TYPE_DROPDOWN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Leave Type")')
        self.LEAVE_REASON_INPUT  = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")')
        self.SUBMIT_BTN          = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Submit")')

        self.EMAIL_FIELDS = [
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").textContains("Email")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").textContains("email")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").textContains("Username")'),
        ]
        self.PASSWORD_FIELDS = [
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").textContains("Password")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").password(true)'),
        ]
        self.LOGIN_BUTTON_CANDIDATES = [
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Login")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Login")'),
            (AppiumBy.ACCESSIBILITY_ID, "Login"),
            (AppiumBy.XPATH, '//*[@text="Login" or @content-desc="Login"]'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").textContains("Login")'),
        ]

    def _first_visible(self, locators, timeout=2):
        for loc in locators:
            if exists(self.driver, loc, timeout=timeout):
                return wait_visible(self.driver, loc)
        return None

    def _hide_keyboard(self):
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass

    def _scroll_into_view_by_text(self, text):
        try:
            self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{text}"))'
            )
        except Exception:
            pass

    def _tap_login_button(self):
        for loc in self.LOGIN_BUTTON_CANDIDATES:
            if exists(self.driver, loc, timeout=1):
                try:
                    wait_clickable(self.driver, loc).click()
                    return True
                except Exception:
                    pass
        self._scroll_into_view_by_text("Login")
        for loc in self.LOGIN_BUTTON_CANDIDATES:
            if exists(self.driver, loc, timeout=1):
                try:
                    wait_clickable(self.driver, loc).click()
                    return True
                except Exception:
                    pass
        try:
            self.driver.press_keycode(66)
            return True
        except Exception:
            return False

    def _login_if_needed(self):
        email_el = self._first_visible(self.EMAIL_FIELDS, timeout=2)
        pwd_el   = self._first_visible(self.PASSWORD_FIELDS, timeout=1)
        if not (email_el and pwd_el):
            return
        username = os.getenv("APP_USERNAME", "azmin@excelbd.com")
        password = os.getenv("APP_PASSWORD", "D!m77(2SJ,5j")
        email_el.click(); email_el.clear(); email_el.send_keys(username)
        pwd_el.click();   pwd_el.clear();   pwd_el.send_keys(password)
        self._hide_keyboard()
        clicked = self._tap_login_button()
        start = time.time()
        while time.time() - start < 15:
            if exists(self.driver, self.TILE_MY_ATTENDANCE, timeout=1) or \
               exists(self.driver, self.TILE_LEAVE_APPLICATION, timeout=1):
                return
            time.sleep(0.4)
        if not clicked:
            raise TimeoutException("Login did not submit.")

    def ensure_home(self):
        self._login_if_needed()
        wait_visible(self.driver, self.TILE_MY_ATTENDANCE)

    def back_to_home(self):
        for _ in range(3):
            if exists(self.driver, self.TILE_MY_ATTENDANCE, timeout=1):
                return
            self.driver.back()
            time.sleep(0.6)

    def go_to_my_attendance(self):
        self.ensure_home()
        wait_clickable(self.driver, self.TILE_MY_ATTENDANCE).click()

    def go_to_leave_application(self):
        self.ensure_home()
        wait_clickable(self.driver, self.TILE_LEAVE_APPLICATION).click()

    def go_to_check_in_card(self):
        self.back_to_home()
        self.ensure_home()
        self._scroll_into_view_by_text("Check-IN")
        self._scroll_into_view_by_text("Check-OUT")

    def _open_and_pick_date(self, field_locators, target_date: dt.date):
        field = None
        for loc in field_locators:
            if exists(self.driver, loc, timeout=1):
                field = wait_clickable(self.driver, loc)
                break
        if not field:
            for label in ("From", "To"):
                try:
                    self.driver.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{label}"))'
                    )
                except Exception:
                    pass
            for loc in field_locators:
                if exists(self.driver, loc, timeout=1):
                    field = wait_clickable(self.driver, loc)
                    break
        if field:
            field.click()
            if datepicker_is_open(self.driver):
                datepicker_select_exact_date(self.driver, target_date)

    def set_attendance_filters(self, from_date: str, to_date: str, status_text: str = "On Leave"):
        d_from = dt.date.fromisoformat(from_date)
        d_to   = dt.date.fromisoformat(to_date)

        self._open_and_pick_date(self.FROM_INPUTS, d_from)
        self._open_and_pick_date(self.TO_INPUTS, d_to)

        opened = False
        for loc in self.STATUS_OPENERS:
            if exists(self.driver, loc, timeout=1):
                wait_clickable(self.driver, loc).click()
                opened = True
                break
        if opened:
            target = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{status_text}")')
            try:
                wait_clickable(self.driver, target).click()
            except Exception:
                try:
                    self.driver.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{status_text}"))'
                    )
                    wait_clickable(self.driver, target).click()
                except Exception:
                    pass

    def tap_search(self):
        for loc in self.SEARCH_BUTTONS:
            if exists(self.driver, loc, timeout=1):
                wait_clickable(self.driver, loc).click()
                return
        return

    def results_present(self):
        if exists(self.driver, self.RESULTS_LIST, timeout=3):
            return True
        return any(exists(self.driver, loc, timeout=1) for loc in self.NO_DATA_LABELS)

    def perform_check_in(self):
        if self.is_checked_in():
            return True

        self.go_to_check_in_card()
        if exists(self.driver, self.CHECK_IN_BTN, timeout=4):
            wait_clickable(self.driver, self.CHECK_IN_BTN).click()
            start = time.time()
            while time.time() - start < 12:
                if exists(self.driver, self.CHECK_OUT_BTN, timeout=1):
                    return True
                time.sleep(0.4)

        self._scroll_into_view_by_text("Check-IN")
        self._scroll_into_view_by_text("Check-OUT")
        return exists(self.driver, self.CHECK_OUT_BTN, timeout=2)

    def is_checked_in(self):
        self.go_to_check_in_card()
        return exists(self.driver, self.CHECK_OUT_BTN, timeout=2)

    def create_leave_application(self, leave_type="Casual Leave", from_date="2025-08-01", to_date="2025-08-02", reason="Personal work"):
        self.go_to_leave_application()
        if exists(self.driver, self.ADD_LEAVE_BTN, timeout=3):
            wait_clickable(self.driver, self.ADD_LEAVE_BTN).click()
        else:
            plus = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("+")')
            wait_clickable(self.driver, plus).click()
        wait_clickable(self.driver, self.LEAVE_TYPE_DROPDOWN).click()
        wait_clickable(self.driver, (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{leave_type}")')).click()
        from_el = wait_clickable(self.driver, (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("From Date")'))
        from_el.click(); from_el.clear(); from_el.send_keys(from_date)
        to_el = wait_clickable(self.driver, (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("To Date")'))
        to_el.click(); to_el.clear(); to_el.send_keys(to_date)
        reason_el = wait_clickable(self.driver, self.LEAVE_REASON_INPUT)
        reason_el.click(); reason_el.clear(); reason_el.send_keys(reason)
        wait_clickable(self.driver, self.SUBMIT_BTN).click()

    def leave_submission_listed(self):
        return exists(self.driver, (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Leave")'), timeout=8)
