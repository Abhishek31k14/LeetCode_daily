import requests
import os

# Configuration from Secrets
SESSION = os.getenv('LEETCODE_SESSION')
CSRF_TOKEN = os.getenv('LEETCODE_CSRF_TOKEN')

def get_latest_submissions():
    url = "https://leetcode.com/graphql/"
    cookies = {'LEETCODE_SESSION': SESSION, 'csrftoken': CSRF_TOKEN}
    
    query = """
    query {
        submissionList(offset: 0, limit: 5) {
            submissions {
                title
                titleSlug
                statusDisplay
                lang
                timestamp
            }
        }
    }
    """
    # ... logic to fetch code via titleSlug and save to file ...
    # You would then use standard Git commands within the script 
    # or the Action to commit the changes.