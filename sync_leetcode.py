import os
import json
import requests
import time

SESSION = os.getenv('LEETCODE_SESSION')
CSRF_TOKEN = os.getenv('LEETCODE_CSRF_TOKEN')
LEETCODE_USERNAME = "Abhishek_Kumar31" 

if not os.getenv('LEETCODE_SESSION'):
    print("❌ Error: .env file not found or LEETCODE_SESSION is empty!")
else:
    print("✅ Secrets loaded successfully. Starting Dry Run...")


def get_question_id(slug):
    url = "https://leetcode.com/graphql"
    # This is the "query" that asks for the ID specifically
    query = """
    query questionData($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionFrontendId
      }
    }
    """
    variables = {"titleSlug": slug}
    
    try:
        r = requests.post(url, json={'query': query, 'variables': variables})
        if r.status_code == 200:
            return r.json()['data']['question']['questionFrontendId']
    except Exception as e:
        print(f"Error fetching ID for {slug}: {e}")
    return "0000" # Fallback if API fails

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
        processed_slugs = set()

        for sub in subs:
            slug = sub.get('titleSlug')
    
            if sub['statusDisplay'] != 'Accepted':
                continue
            if slug in processed_slugs:
               continue

            lang = sub['lang'].lower()
            ext = 'cpp' if 'cpp' in lang else 'py' if 'python' in lang else 'txt'
            real_id = get_question_id(slug)
            filename = f"{int(real_id):04d}_{slug}.{ext}"
    
    # ... your existing GraphQL and Save logic ...
            if os.path.exists(filename):
                print(f"⏩ Skipping {filename} (Already exists)")
                processed_slugs.add(slug)
                continue



# Query 2: Get the actual code for this specific submission
            print(f"📥 New Solution! Fetching code for: {filename}...")
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
            processed_slugs.add(slug)

        print("\n--- ✅ Sync Complete ---")

    except Exception as e:
       print(f"Error: {e}")

if __name__ == "__main__":
    main()
