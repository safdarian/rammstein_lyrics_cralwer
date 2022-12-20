import json

SELENIUM_CONFIG = "config/selenium_config.json"
LOGGER_CONFIG = "config/logger_config.json"

class ConfigManager:
    def __init__(self) -> None:
        with open(SELENIUM_CONFIG) as f:
            self.selenium_config = json.loads(f.read())

        with open(LOGGER_CONFIG) as f:
            self.logger_config = json.loads(f.read())
    
    def get_selenium_webdriver_path(self):
        try:
            return self.selenium_config["webdriver"]
        except:
            raise Exception("selenium webdriver address not found in selenium config")
    
    def get_selenium_logs_path(self):
        try:
            return self.logger_config["selenium_logs"]
        except:
            raise Exception("selenium logs address was not found in logger config")
    
    def get_affenknecht_lyrics_page(self):
        try:
            return self.selenium_config["affenknecht"]
        except:
            raise Exception("affenknecht lyrics page address not found")

    def get_output_path(self):
        try:
            return self.selenium_config["output_path"]
        except:
            raise Exception("output path not found")

    