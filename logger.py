import logging
from config_manager import ConfigManager
config = ConfigManager()

class Logger:
    def __init__(self) -> None:                
        self.logger = logging.getLogger("test")
        self.logger.setLevel(level=logging.DEBUG)

        logFileFormatter = logging.Formatter(
            fmt=f"%(levelname)s %(asctime)s (%(relativeCreated)d) \t %(pathname)s F%(funcName)s L%(lineno)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        fileHandler = logging.FileHandler(filename=config.get_selenium_logs_path())
        fileHandler.setFormatter(logFileFormatter)
        fileHandler.setLevel(level=logging.INFO)

        self.logger.addHandler(fileHandler)
    
    def write(self, s):
        self.logger.info(s)