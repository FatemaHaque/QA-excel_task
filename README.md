# ABC Company Mobile App – QA Assignment

## 📌 Project Overview
This repository contains deliverables for the **ABC Company** mobile app QA assignment, covering:
1. **Exploratory Manual Testing**
2. **Bug Reporting & Test Case Writing**
3. **Automation Testing using Appium (Python)**

The mobile app under test supports property search, property listing, attendance management, and leave applications.  
The goal is to ensure flawless functionality across devices.


---

## 🧪 Manual Testing Deliverables
- **Bug Reports:** Documented in `docs/bug_reports_and_test_cases.pdf`
- **Test Cases:** Written for the **Property Listing** feature
- **Evidence:** Screenshots stored in `docs/screenshots/`

---

## ⚙️ Automation Scripts
Automation is implemented using **Appium (Python)** for two workflows:

### **Automation Task 1: Attendance Report Search**
1. Launch the ABC Company mobile app
2. Navigate to `HR → My Attendance`
3. Input `From Date` and `To Date` (max 1 month gap)
4. Filter by Status: `On Leave`
5. Validate that search results appear
6. Capture a screenshot
7. Close the app

**Script:** `tests/test_attendance_search.py`

---

### **Automation Task 2: Check-IN & Leave Application Creation**
1. Launch the ABC Company mobile app
2. Navigate to `HR → Check-IN`
3. Perform check-in process
4. Navigate to `HR → Leave Application`
5. Create new leave application (all required fields)
6. Capture confirmation screenshot
7. Close the app

**Script:** `tests/test_checkin_and_leave.py`

---

## 🔧 Setup Instructions

### **Prerequisites**
- Python 3.8+
- Node.js & Appium
- Android SDK & Emulator
- Appium Inspector (optional for locator debugging)

### **Installation**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Appium globally
npm install -g appium
npm install -g appium-uiautomator2-driver


v[🎥 Watch Demo](https://drive.google.com/file/d/1vE7rXU-hdcURUDywOGdkJz_haSOJwtbX/view?usp=sharing)
