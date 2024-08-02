import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

# Automatically install ChromeDriver
chromedriver_autoinstaller.install()

# Set up Chrome options for desktop usage (visible mode)
chrome_options = Options()
# Remove headless mode to run Chrome with a GUI
# chrome_options.add_argument("--headless")  # Commented out for visibility
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--start-maximized")  # Open Chrome in maximized mode

# Create a new instance of the Chrome driver
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

# Create the /sc directory if it does not exist
if not os.path.exists("sc"):
    os.makedirs("sc")

def take_screenshot(counter):
    screenshot_file = os.path.join("sc", f"screenshot_{counter}.png")
    driver.save_screenshot(screenshot_file)
    print(f"Saved screenshot: {screenshot_file}")

def smooth_scroll(scroll_amount, duration):
    start_time = time.time()
    end_time = start_time + duration
    initial_scroll_position = driver.execute_script("return window.scrollY;")

    while time.time() < end_time:
        elapsed = time.time() - start_time
        progress = elapsed / duration
        new_position = initial_scroll_position + (scroll_amount * progress)
        driver.execute_script(f"window.scrollTo(0, {new_position});")
        time.sleep(0.05)  # Sleep briefly to allow for smoother animation

def check_and_navigate_if_needed(previous_url):
    current_url = driver.current_url
    if "#google_vignette" in current_url:
        print("Google vignette detected. Navigating to previous URL...")
        driver.get(previous_url)  # Navigate back to the previous URL
        # Wait for the page to load
        time.sleep(5)

def scroll_and_screenshot(previous_url):
    end_time = time.time() + 70  # 70 seconds from now
    screenshot_counter = 0
    
    while time.time() < end_time:
        # Take a screenshot every 5 seconds
        if time.time() % 5 < 1:  # Roughly every 5 seconds
            take_screenshot(screenshot_counter)
            screenshot_counter += 1

        # Smoothly scroll down by 400-500 pixels over 1 second
        scroll_amount = random.randint(400, 500)
        smooth_scroll(scroll_amount, 1)  # Smooth scroll over 1 second

        # Wait for 10-17 seconds
        time.sleep(random.randint(10, 17))
        # Check for vignette and navigate if needed
        check_and_navigate_if_needed(previous_url)

def main():
    try:
        # Open the specified URL
        driver.get("https://www.probytace.com/2024/07/chromes-new-compact-mode-leys-you.html?m=1")
        
        # Wait for 5 seconds on the page
        time.sleep(5)

        previous_url = driver.current_url  # Store the initial URL

        while True:
            # Perform scrolling and screenshot taking
            scroll_and_screenshot(previous_url)

            # Attempt to click the 'older posts' link
            try:
                older_posts_link = driver.find_element(By.ID, "Blog1_blog-pager-older-link")
                previous_url = older_posts_link.get_attribute('href')  # Update previous URL to the new page
                older_posts_link.click()
                print("Clicked 'older posts' link")
                # Wait for 5 seconds after clicking
                time.sleep(5)
            except Exception as e:
                print("Older posts link not found or not clickable:", e)
                continue

            # Check for the dismiss button and click it if found
            try:
                dismiss_button = driver.find_element(By.ID, "dismiss-button")
                if dismiss_button:
                    dismiss_button.click()
                    print("Clicked 'dismiss button'")
                    # Wait 5 seconds
                    time.sleep(5)
                break
            except Exception as e:
                print("Dismiss button not found or not clickable:", e)
                # If dismiss button is not found, repeat the scrolling
                continue

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
