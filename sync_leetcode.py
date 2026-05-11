import requests
import os
import time

SESSION = os.getenv('LEETCODE_SESSION')
CSRF_TOKEN = os.getenv('LEETCODE_CSRF_TOKEN')
LEETCODE_USERNAME = "Abhishek_Kumar31" 

def main():
    print(f"--- Syncing for {LEETCODE_USERNAME} ---")
    url = 'https://leetcode.com/graphql/'
    headers = {
        'Content-Type': 'application/json',
        'Referer': 'https://leetcode.com/',
        'x-csrftoken': CSRF_TOKEN,
        'User-Agent': 'Mozilla/5.0'
    }
    cookies = {'LEETCODE_SESSION': SESSION, 'csrftoken': CSRF_TOKEN}

    # Query 1: Get the list of recent submissions
    list_query = """
    query recentSubmissionList($username: String!, $limit: Int!) {
        recentSubmissionList(username: $username, limit: $limit) {
            title
            titleSlug
            statusDisplay
            lang
            id
        }
    }
    """
    
    payload = {
        'query': list_query,
        'variables': {'username': LEETCODE_USERNAME, 'limit': 15}
    }

    try:
        r = requests.post(url, json=payload, cookies=cookies, headers=headers)
        subs = r.json().get('data', {}).get('recentSubmissionList', [])
        
        if not subs:
            print("No submissions found in history.")
            return

        for sub in subs:
            if sub['statusDisplay'] == 'Accepted':
                # Map lang to file extension
                ext = 'cpp' if 'cpp' in sub['lang'] else 'py' if 'python' in sub['lang'] else 'txt'
                # Try 'frontendQuestionId' first, then 'id', then default to '0000'
                prob_id = sub.get('frontendQuestionId') or sub.get('id')
                filename = f"{int(prob_id):04d}_{sub['titleSlug']}.{ext}"
                
                # Check if file already exists to avoid duplicate work
                if os.path.exists(filename):
                    continue

                print(f"New Solution Found: {sub['title']}. Fetching code...")
                
                # Query 2: Get the actual code for this specific submission
                detail_query = """
                query submissionDetails($submissionId: Int!) {
                    submissionDetails(submissionId: $submissionId) {
                        code
                    }
                }
                """
                detail_payload = {
                    'query': detail_query,
                    'variables': {'submissionId': int(sub['id'])}
                }
                
                r_code = requests.post(url, json=detail_payload, cookies=cookies, headers=headers)
                full_code = r_code.json().get('data', {}).get('submissionDetails', {}).get('code', "")

                if full_code:
                    with open(filename, 'w') as f:
                        f.write(full_code)
                    print(f"Saved {filename}")
                    time.sleep(1) # Delay to be safe

        print("--- Sync Complete ---")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
