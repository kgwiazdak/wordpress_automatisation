import requests
from bs4 import BeautifulSoup

from logger import Logger


class Controller:
    def __init__(self):
        self.session = requests.Session()
        self.logger = Logger(self.session)
        self.wp_admin_url = "https://esb-acc.level-level.nl/wp-admin"

    def log_in(self):
        """
        Logs in to the popup auth, then logs in to WordPress,
        and prints out the status codes.
        """
        print("Popup login status:", self.logger.log_in_to_popup())
        print("WP login status:", self.logger.log_in_to_website())

    def _get_new_post_form(self):
        """
        Fetches the 'Add New Post' page to grab the _wpnonce,
        post_ID, and _wp_http_referer needed for form submission.
        """
        url = f"{self.wp_admin_url}/post-new.php"
        resp = self.session.get(url)
        if resp.status_code != 200:
            print("Could not load post-new.php:", resp.status_code)
            return None

        soup = BeautifulSoup(resp.text, "html.parser")

        # Attempt to find the necessary hidden fields
        nonce_el = soup.find("input", {"name": "_wpnonce"})
        post_id_el = soup.find("input", {"name": "post_ID"})
        referer_el = soup.find("input", {"name": "_wp_http_referer"})

        if not nonce_el or not post_id_el or not referer_el:
            print("Could not find all required fields (_wpnonce, post_ID, _wp_http_referer).")
            return None

        wpnonce = nonce_el.get("value")
        post_id = post_id_el.get("value")
        wp_http_referer = referer_el.get("value")

        return {
            "_wpnonce": wpnonce,
            "post_ID": post_id,
            "_wp_http_referer": wp_http_referer
        }

    def save_draft_with_title(self, title):
        """
        Saves a new draft post with the given title.
        """
        form_data = self._get_new_post_form()
        if not form_data:
            print("Cannot proceed without valid form data.")
            return

        data = {
            "_wpnonce": form_data["_wpnonce"],
            "_wp_http_referer": form_data["_wp_http_referer"],
            "post_ID": form_data["post_ID"],
            "post_title": title,
            "content": "",
            "action": "editpost",
            "post_type": "post",
            "post_status": "draft",
            "save": "Save Draft"  # This mimics hitting the 'Save Draft' button
        }

        post_url = f"{self.wp_admin_url}/post.php"
        resp = self.session.post(post_url, data=data)

        if resp.status_code == 200 and (
                "Post draft updated." in resp.text or "Post saved." in resp.text or "message=7" in resp.url):
            print(f"Draft '{title}' saved successfully.")
        else:
            print(f"Failed to save draft '{title}'. Response code: {resp.status_code}")

    def publish_post_with_title(self, title):
        """
        Publishes a new post immediately with the given title.
        """
        form_data = self._get_new_post_form()
        if not form_data:
            print("Cannot proceed without valid form data.")
            return

        data = {
            "_wpnonce": form_data["_wpnonce"],
            "_wp_http_referer": form_data["_wp_http_referer"],
            "post_ID": form_data["post_ID"],
            "post_title": title,
            "content": "",
            "action": "editpost",
            "post_type": "post",
            "post_status": "publish",
            "publish": "Publish"  # This mimics hitting the 'Publish' button
        }

        post_url = f"{self.wp_admin_url}/post.php"
        resp = self.session.post(post_url, data=data)

        # WordPress typically redirects with message=6 for a newly published post
        if resp.status_code == 200 and ("Post published." in resp.text or "message=6" in resp.url):
            print(f"Post '{title}' published successfully!")
        else:
            print(f"Failed to publish post '{title}'. Response code: {resp.status_code}")


if __name__ == "__main__":
    controller = Controller()
    controller.log_in()

    # Example usage:
    # Create and save a draft
    controller.save_draft_with_title("Draft Title Example")

    # Publish a new post
    controller.publish_post_with_title("Published Title Example")
