
import requests
import os

SESSION = os.getenv('LEETCODE_SESSION')
CSRF_TOKEN = os.getenv('LEETCODE_CSRF_TOKEN')
# Add your username here manually for now to test
LEETCODE_USERNAME = "YOUR_ACTUAL_USERNAME_HERE" 

def main():
    print("--- Starting Deep Sync ---")
    url = 'https://leetcode.com/graphql/'
    
    # These headers are CRITICAL for LeetCode's security
    headers = {
        'Content-Type': 'application/json',
        'Referer': 'https://leetcode.com/',
        'x-csrftoken': CSRF_TOKEN,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    
    cookies = {
        'LEETCODE_SESSION': SESSION,
        'csrftoken': CSRF_TOKEN
    }
    
    # We use a broader query that often works better with cookies
    query = """
    query userRecentSubmissions($username: String!, $limit: Int!) {
        recentSubmissionList(username: $username, limit: $limit) {
            title
            statusDisplay
            lang
        }
    }
    """
    
    payload = {
        'query': query,
        'variables': {'username': "https://leetcode.com/u/Abhishek_Kumar31/", 'limit': 10}
    }
    
    try:
        r = requests.post(url, json=payload, cookies=cookies, headers=headers)
        print(f"HTTP Status: {r.status_code}")
        
        data = r.json()
        if 'errors' in data:
            print(f"LeetCode Error: {data['errors']}")
            return

        subs = data.get('data', {}).get('recentSubmissionList', [])
        
        if not subs:
            print("Result: Still no submissions found. Trying fallback...")
            # Fallback: check if the session is actually valid by getting profile info
            profile_query = "{ user { username } }"
            r_profile = requests.post(url, json={'query': profile_query}, cookies=cookies, headers=headers)
            print(f"Profile check: {r_profile.text}")
            return

        for s in subs:
            print(f"FOUND: {s['title']} | {s['statusDisplay']}")

    except Exception as e:
        print(f"System Error: {e}")

if __name__ == "__main__":
    main()
