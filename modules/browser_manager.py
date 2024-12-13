from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random

class BrowserManager:
    def __init__(self, viewports, user_agents):
        self.viewports = viewports
        self.user_agents = user_agents

    def get_random_viewport(self):
        return random.choice(self.viewports)

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def get_random_location(self):
        lat_range = (33.7, 34.3)  # Latitude range for Los Angeles area
        long_range = (-118.6, -118.1)  # Longitude range for Los Angeles area
        latitude = round(random.uniform(*lat_range), 6)
        longitude = round(random.uniform(*long_range), 6)
        accuracy = 100
        return latitude, longitude, accuracy

    def create_driver(self):
        options = Options()
        
        # Select a random viewport and user agent
        viewport = self.get_random_viewport()
        user_agent = self.get_random_user_agent()
        
        # Set user-agent and window-size for mobile emulation
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument(f"--window-size={viewport['width']},{viewport['height']}")  # Correctly format the window size
        
        # Enable geolocation and allow location access
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.geolocation": 1
        })
        
        # Initialize the Chrome driver with options
        driver = webdriver.Chrome(options=options)

        # Spoof location using the generated random location
        latitude, longitude, accuracy = self.get_random_location()
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "accuracy": accuracy
        }
        driver.execute_cdp_cmd("Page.setGeolocationOverride", params)
        
        # Debug: Confirm user-agent and viewport
        print(f"Using user agent: {user_agent}")
        print(f"Viewport size set to: {viewport['width']}x{viewport['height']}")

        return driver
