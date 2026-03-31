#! python3
# -*- coding: utf-8 -*-
"""NaukriFlow Daily update - Using Chrome"""

import io
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from random import choice, randint
from string import ascii_uppercase, digits
from typing import Optional, Tuple, Union

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth

import constants

# --- Configuration paths using pathlib ---
originalResumePath = Path(constants.ORIGINAL_RESUME_PATH)
modifiedResumePath = Path(constants.MODIFIED_RESUME_PATH)

# Update your naukri username and password here before running
username = constants.USERNAME
password = constants.PASSWORD
mob = constants.MOBILE

# False if you dont want to add Random HIDDEN chars to your resume
updatePDF = False

# If Headless = True, script runs Chrome in headless mode without visible GUI
headless = False

# ----- No other changes required -----

# Set login URL
NaukriURL = constants.NAUKRI_LOGIN_URL

logging.basicConfig(
    level=logging.INFO, filename="naukri.log", format="%(asctime)s    : %(message)s"
)
# logging.disable(logging.CRITICAL)
os.environ["WDM_LOCAL"] = "1"
os.environ["WDM_LOG_LEVEL"] = "0"


def log_msg(message: str, level: int = logging.INFO) -> None:
    """Print to console and store to Log"""
    print(message)
    logging.log(level, message)


def catch(error: Exception) -> None:
    """Method to catch errors and log error details"""
    _, _, exc_tb = sys.exc_info()
    lineNo = str(exc_tb.tb_lineno) if exc_tb else "Unknown"
    msg = f"{type(error).__name__} : {error} at Line {lineNo}."
    log_msg(msg, level=logging.ERROR)


def get_locator_type(locator_type: str) -> By:
    """Maps string locator type to Selenium By object"""
    mapping = {
        "ID": By.ID,
        "NAME": By.NAME,
        "XPATH": By.XPATH,
        "TAG": By.TAG_NAME,
        "CLASS": By.CLASS_NAME,
        "CSS": By.CSS_SELECTOR,
        "LINKTEXT": By.LINK_TEXT,
    }
    return mapping.get(locator_type.upper(), By.ID)


def get_element(
    driver: webdriver.Chrome, 
    element_tag: str, 
    locator: str = "ID", 
    timeout: int = 15,
    silent: bool = False
) -> Optional[WebElement]:
    """Wait for element and then select when it is available"""
    try:
        by = get_locator_type(locator)
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, element_tag))
        )
        return element
    except (TimeoutException, NoSuchElementException):
        if not silent:
            log_msg(f"Element not found within {timeout}s: [{locator}] {element_tag}", level=logging.DEBUG)
        return None
    except Exception as e:
        catch(e)
        return None


def is_element_present(driver: webdriver.Chrome, how: By, what: str) -> bool:
    """Returns True if element is present"""
    try:
        driver.find_element(by=how, value=what)
        return True
    except NoSuchElementException:
        return False


def wait_till_present(
    driver: webdriver.Chrome, 
    element_tag: str, 
    locator: str = "ID", 
    timeout: int = 30
) -> bool:
    """Wait till element is present on the page"""
    try:
        by = get_locator_type(locator)
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, element_tag))
        )
        return True
    except TimeoutException:
        log_msg(f"Timeout waiting for [{locator}] {element_tag}", level=logging.DEBUG)
        return False


def try_click(
    driver: webdriver.Chrome, 
    element_tag: str, 
    locator: str = "XPATH", 
    timeout: int = 5
) -> bool:
    """Try to click an element, handling it silently if missing (ideal for popups)"""
    try:
        el = get_element(driver, element_tag, locator=locator, timeout=timeout, silent=True)
        if el and el.is_displayed():
            el.click()
            return True
    except Exception:
        pass
    return False

def Logout(driver: webdriver.Chrome) -> bool:
    """Logout from Naukri session with modernized selectors"""

    try:
        # -------- Drawer/User Menu XPaths --------
        drawer_xpaths = [
            f"//*[contains({ci('@class')}, 'nI-gNb-drawer')]",
            f"//*[contains({ci('@class')}, 'header__user-name')]",
            f"//*[contains({ci('@class')}, 'drawer__icon')]",
        ]

        for xpath in drawer_xpaths:
            if try_click(driver, xpath, timeout=5):
                log_msg("User menu/drawer opened.")
                time.sleep(1)
                break

        # -------- Logout XPaths --------
        logout_xpaths = [
            "//a[contains(@href, 'logout')]",
            "//a[@title='Logout']",
            "//a[@data-type='logoutLink']",
            f"//*[contains({ci('text()')}, 'logout')]",
        ]

        for xpath in logout_xpaths:
            el = get_element(driver, xpath, locator="XPATH", timeout=5, silent=True)
            if el and el.is_displayed():
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", el)
                    time.sleep(0.5)
                    el.click()
                    log_msg("Logout: SUCCESS")
                    time.sleep(2)
                    return True
                except Exception:
                    continue

        log_msg("Logout button not found.", level=logging.DEBUG)
        return False

    except Exception as e:
        catch(e)
        return False
    
def ci(xpath_part: str) -> str:
    """
    Wraps an XPath string in lowercase translate() for case-insensitive matching.
    Usage:
        ci("@class") → "translate(@class,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"
        ci("text()") → "translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"
    """
    return f"translate({xpath_part},'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"


def tearDown(driver):
    try:
        driver.close()
        log_msg("Driver Closed Successfully")
    except Exception as e:
        catch(e)
        pass

    try:
        driver.quit()
        log_msg("Driver Quit Successfully")
    except Exception as e:
        catch(e)
        pass


def randomText():
    return "".join(choice(ascii_uppercase + digits) for _ in range(randint(1, 5)))


def LoadNaukri(headless: bool) -> webdriver.Chrome:
    """Open Chrome with stealth mode enabled to load Naukri.com"""

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-popups")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")

    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

    # Chrome Driver initialization
    service = ChromeService()
    try:
        driver = webdriver.Chrome(options=options, service=service)
    except Exception as e:
        log_msg(f"Chrome initialization failed: {e}", level=logging.WARNING)
        driver = webdriver.Chrome(options=options)

    # Initialize Stealth mode (bypass bot detection)
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    log_msg("NaukriFlow Shield (Stealth) Activated.")
    driver.implicitly_wait(5)
    driver.get(constants.NAUKRI_LOGIN_URL)
    return driver


def naukriLogin(headless=False):
    """Open Chrome browser and Login to Naukri.com"""
    status = False
    driver = None
    username_locator = "usernameField"
    password_locator = "passwordField"
    login_btn_locator = "//*[@type='submit' and normalize-space()='Login']"
    skip_locator = "//*[text() = 'SKIP AND CONTINUE']"
    close_locator = "//*[contains(@class, 'cross-icon') or @alt='cross-icon']"

    try:
        driver = LoadNaukri(headless)

        log_msg(driver.title)
        if "naukri.com" in driver.title.lower():
            log_msg("Website Connection Established.")

        email_el = None
        if wait_till_present(driver, username_locator, locator="ID", timeout=15):
            email_el = get_element(driver, username_locator, locator="ID")
            pass_el = get_element(driver, password_locator, locator="ID")
            login_btn = get_element(driver, login_btn_locator, locator="XPATH")
        else:
            log_msg("Login fields not found. Page might have changed.", level=logging.ERROR)

        if email_el and pass_el and login_btn:
            email_el.clear()
            email_el.send_keys(username)
            time.sleep(1)
            pass_el.clear()
            pass_el.send_keys(password)
            time.sleep(1)
            login_btn.send_keys(Keys.ENTER)
            time.sleep(3)

            # Handle post-login popups silently
            try_click(driver, close_locator)
            try_click(driver, skip_locator)

            # CheckPoint to verify login
            if wait_till_present(driver, "ff-inventory", locator="ID", timeout=40):
                if get_element(driver, "ff-inventory", locator="ID"):
                    log_msg("NaukriFlow Auth: SUCCESS")
                    status = True
                    return (status, driver)
            
            log_msg("Authentication state uncertain.", level=logging.WARNING)

    except Exception as e:
        catch(e)
    return (status, driver)


def UpdateProfile(driver: webdriver.Chrome) -> None:
    try:
        # Modernized XPaths for Profile Page
        mob_xpath = "//*[@name='mobile'] | //*[@id='mob_number'] | //input[contains(@placeholder, 'mobile')]"
        save_xpath = "//button[@id='saveBasicDetailsBtn'] | //button[@type='submit' and contains(@value, 'Save')]"
        view_profile_xpath = "//*[contains(@class, 'view-profile')]//a"
        edit_xpath = "(//*[contains(@class, 'icon edit')])[1] | //span[contains(text(), 'Edit')]"
        save_confirm_xpath = "//*[contains(text(), 'today')] | //*[contains(text(), 'Today')]"
        close_xpath = "//*[contains(@class, 'crossIcon')]"

        if not wait_till_present(driver, view_profile_xpath, "XPATH", 20):
            log_msg("Profile view link not found.", level=logging.WARNING)
            return

        prof_el = get_element(driver, view_profile_xpath, locator="XPATH")
        if prof_el: prof_el.click()
        
        # Humanize
        time.sleep(randint(3, 5))
        try_click(driver, close_xpath)

        if wait_till_present(driver, edit_xpath + " | " + save_xpath, "XPATH", 20):
            # Case 1: Need to click Edit first
            if is_element_present(driver, By.XPATH, edit_xpath):
                edit_el = get_element(driver, edit_xpath, locator="XPATH")
                if edit_el: edit_el.click()
                time.sleep(2)

            # Case 2: In the edit form
            wait_till_present(driver, mob_xpath, "XPATH", 10)
            mob_el = get_element(driver, mob_xpath, locator="XPATH", silent=True)
            if mob_el:
                mob_el.clear()
                mob_el.send_keys(mob)
                time.sleep(1)
            
            save_el = get_element(driver, save_xpath, locator="XPATH")
            if save_el: 
                save_el.send_keys(Keys.ENTER)
                log_msg("Profile: Save triggered.")

            # Wait for confirmation (check if updated today)
            time.sleep(3)
            if wait_till_present(driver, save_confirm_xpath, "XPATH", 15):
                log_msg("Profile Sync: SUCCESS")
            else:
                log_msg("Profile Sync: Verification timed out (check results manually).", level=logging.WARNING)

        time.sleep(randint(2, 4))

    except Exception as e:
        catch(e)



def UpdateResume():
    try:
        # Random text with random location and size
        txt = randomText()
        xloc = randint(700, 1000)  # This ensures that text is 'out of page'
        fsize = randint(1, 10)

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", fsize)
        can.drawString(xloc, 100, txt)
        can.save()

        packet.seek(0)
        new_pdf = PdfReader(packet)
        with open(originalResumePath, "rb") as f:
            existing_pdf = PdfReader(f)
            pagecount = len(existing_pdf.pages)
            print("Found %s pages in PDF" % pagecount)

            output = PdfWriter()
            # Merging new pdf with last page of existing pdf
            for pageNum in range(pagecount - 1):
                output.add_page(existing_pdf.pages[pageNum])
            page = existing_pdf.pages[pagecount - 1]
            page.merge_page(new_pdf.pages[0])
            output.add_page(page)

            # Save the new resume file
            with open(modifiedResumePath, "wb") as outputStream:
                output.write(outputStream)
            print("Saved modified PDF: %s" % modifiedResumePath)
            return os.path.abspath(modifiedResumePath)
    except Exception as e:
        catch(e)
    return os.path.abspath(originalResumePath)



def UploadResume(driver: webdriver.Chrome, resume_path: Union[str, Path]) -> None:
    try:
        # XPaths and locators
        attach_id = "attachCV"
        lazy_attach_id = "lazyAttachCV"
        update_resume_xpath = "//*[contains(@class, 'upload')]//input[@value='Update resume']"
        checkpoint_xpath = "//*[contains(@class, 'updateOn')]"
        save_xpath = "//button[@type='button' and contains(text(), 'Save')]"
        close_xpath = "//*[contains(@class, 'crossIcon')]"

        driver.get(constants.NAUKRI_PROFILE_URL)
        time.sleep(randint(2, 4)) # Humanized jitter

        # Handle random popups silently
        try_click(driver, close_xpath)

        abs_path = str(Path(resume_path).resolve())

        # Logic for different upload containers
        if wait_till_present(driver, lazy_attach_id, locator="ID", timeout=5):
            el = get_element(driver, update_resume_xpath, locator="XPATH")
            if el: el.send_keys(abs_path)

        elif wait_till_present(driver, attach_id, locator="ID", timeout=5):
            el = get_element(driver, attach_id, locator="ID")
            if el: el.send_keys(abs_path)

        try_click(driver, save_xpath)

        # Verification
        if wait_till_present(driver, checkpoint_xpath, locator="XPATH", timeout=30):
            checkpoint = get_element(driver, checkpoint_xpath, locator="XPATH")
            if checkpoint:
                updated_date = checkpoint.text
                log_msg(f"Resume Sync Successful. Sync Date: {updated_date}")
            else:
                log_msg("Sync date visibility failed.", level=logging.WARNING)
        else:
            log_msg("Verification timeout: Resume upload status uncertain.")

    except Exception as e:
        catch(e)
    time.sleep(2)


def main():
    log_msg("-----NaukriFlow Script Run Begin-----")
    driver = None
    try:
        status, driver = naukriLogin(headless)
        if status and driver:
            UpdateProfile(driver)
            
            if originalResumePath.exists():
                if updatePDF:
                    resume_path = UpdateResume()
                    UploadResume(driver, resume_path)
                else:
                    UploadResume(driver, originalResumePath)
            else:
                log_msg(f"Resume not found at: {originalResumePath}", level=logging.WARNING)

    except Exception as e:
        catch(e)

    finally:
        if driver is not None:
            try:
                Logout(driver)
                time.sleep(2)
            except Exception as e:
                log_msg("Error during logout: %s" % e)
        tearDown(driver)

    log_msg("-----NaukriFlow Script Run Ended-----\n")


if __name__ == "__main__":
    main()
