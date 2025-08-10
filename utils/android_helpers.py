from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
import datetime as dt

DEFAULT_WAIT = 12

def wait_visible(driver, locator, timeout=DEFAULT_WAIT):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))

def wait_clickable(driver, locator, timeout=DEFAULT_WAIT):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))

def exists(driver, locator, timeout=2):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
        return True
    except Exception:
        return False

def set_date_via_textbox(driver, el, yyyy_mm_dd: str):
    el.click()
    try:
        el.clear()
    except Exception:
        pass
    el.send_keys(yyyy_mm_dd)

OK_BUTTONS = [
    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("OK")'),
    (AppiumBy.ID, "android:id/button1"),
]
CANCEL_BUTTONS = [
    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("CANCEL")'),
    (AppiumBy.ID, "android:id/button2"),
]
MONTH_NEXT = [
    (AppiumBy.ACCESSIBILITY_ID, "Next month"),
    (AppiumBy.ID, "com.google.android.material:id/month_navigation_next"),
    (AppiumBy.ID, "android:id/next"),
]
MONTH_PREV = [
    (AppiumBy.ACCESSIBILITY_ID, "Previous month"),
    (AppiumBy.ID, "com.google.android.material:id/month_navigation_previous"),
    (AppiumBy.ID, "android:id/prev"),
]

def datepicker_is_open(driver):
    return any(exists(driver, loc, timeout=1) for loc in OK_BUTTONS + CANCEL_BUTTONS)

def datepicker_confirm_ok(driver):
    for loc in OK_BUTTONS:
        if exists(driver, loc, timeout=2):
            wait_clickable(driver, loc).click()
            return True
    return False

def _try_tap_day_by_formats(driver, d: dt.date) -> bool:
    candidates = [
        f"{d.day} {d.strftime('%B')} {d.year}",
        f"{d.strftime('%a')}, {d.strftime('%b')} {d.day}, {d.year}",
        f"{d.strftime('%a')}, {d.strftime('%B')} {d.day}",
        str(d.day),
    ]
    for s in candidates:
        locs = [
            (AppiumBy.ACCESSIBILITY_ID, s),
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().description("{s}")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{s}")'),
        ]
        for loc in locs:
            if exists(driver, loc, timeout=1):
                wait_clickable(driver, loc).click()
                return True
    return False

def _tap_button_any(driver, locators) -> bool:
    for loc in locators:
        if exists(driver, loc, timeout=1):
            wait_clickable(driver, loc).click()
            return True
    return False

def datepicker_select_exact_date(driver, target: dt.date, max_month_jumps: int = 12) -> bool:
    if not datepicker_is_open(driver):
        return False
    today = dt.date.today()
    direction_first = MONTH_NEXT if target >= today else MONTH_PREV
    direction_second = MONTH_PREV if direction_first is MONTH_NEXT else MONTH_NEXT
    for dirs in (direction_first, direction_second):
        for _ in range(max_month_jumps):
            if _try_tap_day_by_formats(driver, target):
                return datepicker_confirm_ok(driver)
            if not _tap_button_any(driver, dirs):
                break
    return datepicker_confirm_ok(driver)
