import requests
import re
from logger import Logger

class Controller:
    def __init__(self):
        self.session = requests.Session()
        self.logger = Logger(self.session)

    def log_in(self):
        print("Popup login status:", self.logger.log_in_to_popup())
        print("WP login status:", self.logger.log_in_to_website())

    def update_and_publish_post(self, post_id, new_title):
        """
        1) GET the edit screen to grab the _wpnonce
        2) POST to publish with new title
        """
        # --- 1) GET the edit page ---
        edit_url = f"https://esb-acc.level-level.nl/wp-admin/post.php?post={post_id}&action=edit"
        resp = self.session.get(edit_url)
        if resp.status_code != 200:
            print("Could not load edit screen:", resp.status_code)
            return
        
        # Attempt to extract the _wpnonce from the form HTML
        nonce_match = re.search(r'name="_wpnonce" value="([^"]+)"', resp.text)
        if not nonce_match:
            print("Could not find _wpnonce on edit screen")
            return
        
        wpnonce = nonce_match.group(1)
        
        # --- 2) POST form data to publish ---
        post_url = "https://esb-acc.level-level.nl/wp-admin/post.php"
        
        # These fields generally suffice to update title and publish.
        # (WordPress may include additional hidden fields, but these are usually the key ones.)
        form_data = {
            '_wpnonce': wpnonce,
            '_wp_http_referer': f'/wp-admin/post.php?post={post_id}&action=edit',
            'post_ID': post_id,
            'post_title': new_title,
            'content': '',
            
            'action': 'editpost',
            'originalaction': 'editpost',
            'publish': 'Publish',
            'post_type': 'post',
            'post_status': 'publish'
        }
        
        r = self.session.post(post_url, data=form_data)
        if r.status_code == 200:
            print(f"Post {post_id} updated & published with new title='{new_title}'.")
        else:
            print("Error during publish step:", r.status_code)


if __name__ == "__main__":
    controller = Controller()
    controller.log_in()
    # Suppose the post is ID=159645
    controller.update_and_publish_post(post_id=159645, new_title="Hello world")