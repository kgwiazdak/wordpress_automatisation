import requests

from logger import Logger


class Controller:
    def __init__(self):
        self.session = requests.Session()
        self.logger = Logger(self.session)

    def log_in(self):
        self.logger.log_in_to_popup()
        self.logger.log_in_to_website()


if __name__ == "__main__":
    controller = Controller()
    logger = controller.logger
    print("Popup login status:", logger.log_in_to_popup())
    print("WP form login status:", logger.log_in_to_website())
