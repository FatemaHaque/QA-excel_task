import os, pytest, datetime as dt
from appium import webdriver
from appium.options.android import UiAutomator2Options

@pytest.fixture(scope="session")
def driver(request):
    caps = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": os.getenv("DEVICE_NAME", "emulator-5554"),
        "appPackage": "com.arcone.arcone",
        "appActivity": "com.arcone.arcone.MainActivity",
        "noReset": True,          # keep logged-in session
        "newCommandTimeout": 180
    }
    # only set "app" if you want install/upgrade each run
    apk = os.getenv("APP_APK")
    if apk:
        caps["app"] = apk

    drv = webdriver.Remote("http://127.0.0.1:4723", options=UiAutomator2Options().load_capabilities(caps))

    def fin():
        try: drv.quit()
        except Exception: pass
    request.addfinalizer(fin)
    return drv

@pytest.fixture
def snapshot(tmp_path):
    """Save a screenshot to ./artifacts/ for every call."""
    outdir = os.path.abspath(os.path.join(os.getcwd(), "artifacts"))
    os.makedirs(outdir, exist_ok=True)
    def _snap(driver, name):
        path = os.path.join(outdir, f"{name}.png")
        driver.save_screenshot(path)
        return path
    return _snap
