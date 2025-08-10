import datetime as dt
from pages.hr_page import HRPage

def _leave_dates():
    start = dt.date.today() + dt.timedelta(days=2)
    end   = start + dt.timedelta(days=1)    
    return start.isoformat(), end.isoformat()

def test_checkin_and_leave_application(driver, snapshot):
    hr = HRPage(driver)


    ok = hr.perform_check_in()
    assert ok and hr.is_checked_in(), "Expected to be checked-in (Check-OUT visible)"
    snapshot(driver, "after_check_in")


    from_date, to_date = _leave_dates()
    hr.create_leave_application(
        leave_type="Casual Leave",
        from_date=from_date,
        to_date=to_date,
        reason="Automation test"
    )


    assert hr.leave_submission_listed(), "Leave application not visible after submission"
    snapshot(driver, f"leave_listing_{from_date}_to_{to_date}")


