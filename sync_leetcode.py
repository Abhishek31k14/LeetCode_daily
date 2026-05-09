import requests
import os
import time

# Secrets from GitHub Environment
SESSION = os.getenv('LEETCODE_SESSION')
CSRF_TOKEN = os.getenv('LEETCODE_CSRF_TOKEN')

def get_submissions():
    url = 'https://leetcode.com/graphql/'
    cookies = {'LEETCODE_SESSION': SESSION, 'csrftoken': CSRF_TOKEN}
    
    # Query to get the list of recent submissions
    query = """
    query recentSubmissions($username: String!, $limit: Int!) {
        recentSubmissionList(username: $username, limit: $limit) {
            title
            titleSlug
            timestamp
            statusDisplay
            lang
            id
        }
    }
    """
    
    headers = {
        'Referer': 'https://leetcode.com/',
        'X-CSRFToken': CSRF_TOKEN,
        'Content-Type': 'application/json',
    }
    
    payload = {
        'query': query,
        'variables': {'username': "", 'limit': 20}
    }
    
    response = requests.post(url, json=payload, cookies=cookies, headers=headers)
    if response.status_code == 200:
        return response.json().get('data', {}).get('recentSubmissionList', [])
    return []

def get_code(submission_id):
    # This fetches the actual source code for a specific submission ID
    url = 'https://leetcode.com/graphql/'
    cookies = {'LEETCODE_SESSION': SESSION, 'csrftoken': CSRF_TOKEN}
    
    query = """
    query submissionDetails($submissionId: Int!) {
        submissionDetails(submissionId: $submissionId) {
            code
        }
    }
    """
    
    payload = {
        'query': query,
        'variables': {'submissionId': int(submission_id)}
    }
    
    headers = {
        'Referer': f'https://leetcode.com/submissions/detail/{submission_id}/',
        'X-CSRFToken': CSRF_TOKEN,
    }
    
    response = requests.post(url, json=payload, cookies=cookies, headers=headers)
    if response.status_code == 200:
        return response.json().get('data', {}).get('submissionDetails', {}).get('code', "")
    return ""

def main():
    if not SESSION or not CSRF_TOKEN:
        print("Missing Secrets!")
        return

    submissions = get_submissions()
    for sub in submissions:
        if sub['statusDisplay'] == 'Accepted':
            # Map languages to extensions
            ext_map = {'cpp': 'cpp', 'python3': 'py', 'java': 'java', 'javascript': 'js'}
            extension = ext_map.get(sub['lang'], 'txt')
            
            folder = sub['lang']
            filename = f"{sub['titleSlug']}.{extension}"
            os.makedirs(folder, exist_ok=True)
            path = os.path.join(folder, filename)

            # Only fetch and write if the file doesn't exist
            if not os.path.exists(path):
                print(f"Fetching code for: {sub['title']}")
                full_code = get_code(sub['id'])
                
                if full_code:
                    with open(path, 'w') as f:
                        f.write(full_code)
                    print(f"Successfully saved {filename}")
                    time.sleep(1) # Be nice to the API
                else:
                    print(f"Could not retrieve code for {sub['title']}")

if __name__ == "__main__":
    main()
