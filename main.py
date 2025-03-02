import requests

class Logger:
    def __init__(self):
        self.login_url = "https://esb-acc.level-level.nl/wp-login.php"

        self.popup_user = "levellevel"
        self.popup_pass = "staging"

        self.wp_user = "krzysztofgwiazda"
        self.wp_pass = "pO3wPTJjB2)p3&I#NMv6gZhc"

        self.session = requests.Session()
        self.session.auth = (self.popup_user, self.popup_pass)
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})

    def log_in_to_popup(self):
        r = self.session.get(self.login_url)
        return r.status_code

    def log_in_to_website(self):

        data = {
            "log": self.wp_user,
            "pwd": self.wp_pass,
            "wp-submit": "Log In",
            "testcookie": "1",
        }

        r = self.session.post(self.login_url, data=data)
        return r.status_code

if __name__ == "__main__":
    logger = Logger()
    print("Popup login status:", logger.log_in_to_popup())
    print("WP form login status:", logger.log_in_to_website())
