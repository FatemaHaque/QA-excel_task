import datetime as dt
from pages.hr_page import HRPage

def _from_to_plus_one_day():

    f = dt.date.today()
    t = f + dt.timedelta(days=1)
    return f.isoformat(), t.isoformat()

def test_attendance_report_search(driver, snapshot):
    hr = HRPage(driver)


    hr.go_to_my_attendance()

    from_date, to_date = _from_to_plus_one_day()
    hr.set_attendance_filters(from_date, to_date, status_text="On Leave")

    # 5. Validate that results screen appears (table or explicit “No data”)
    hr.tap_search()
    assert hr.results_present(), "Attendance screen did not render results/table header/empty state"

    # 6. Screenshot of results
    snapshot(driver, f"attendance_onleave_{from_date}_to_{to_date}")


