
import requests
import os

SESSION = os.getenv('LEETCODE_SESSION')
CSRF_TOKEN = os.getenv('LEETCODE_CSRF_TOKEN')

def main():
    print("--- Starting Sync ---")
    if not SESSION or not CSRF_TOKEN:
        print("CRITICAL: Secrets are missing!")
        return

    url = 'https://leetcode.com/graphql/'
    headers = {
        'Referer': 'https://leetcode.com/',
        'X-CSRFToken': CSRF_TOKEN,
        'Content-Type': 'application/json',
    }
    cookies = {'LEETCODE_SESSION': SESSION, 'csrftoken': CSRF_TOKEN}
    
    query = """
    query {
        recentSubmissionList(username: "", limit: 5) {
            title
            statusDisplay
            lang
        }
    }
    """
    
    try:
        r = requests.post(url, json={'query': query}, cookies=cookies, headers=headers)
        print(f"LeetCode Response Code: {r.status_code}")
        
        data = r.json()
        subs = data.get('data', {}).get('recentSubmissionList', [])
        
        if not subs:
            print("Result: No submissions found. Your LEETCODE_SESSION might be expired or incorrect.")
            return

        for s in subs:
            print(f"Found: {s['title']} | Status: {s['statusDisplay']}")
            if s['statusDisplay'] == 'Accepted':
                # Create dummy file to test the push
                filename = f"TEST_{s['title'].replace(' ', '_')}.cpp"
                with open(filename, "w") as f:
                    f.write("// Success")
                print(f"Created file: {filename}")

    except Exception as e:
        print(f"Script Error: {e}")

if __name__ == "__main__":
    main()
