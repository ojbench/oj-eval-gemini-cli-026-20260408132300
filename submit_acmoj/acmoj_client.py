import argparse
import json
import os
import urllib.request
import urllib.error
from typing import Optional, Dict, Any

class ACMOJClient:
    def __init__(self, access_token: str):
        self.base_url = "http://172.17.0.1:5000/api"
        self.access_token = access_token
        self.submission_log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "submission_ids.log")

    def _make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Optional[Dict]:
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        req = urllib.request.Request(url, method=method, headers=headers)
        if data:
            req.data = json.dumps(data).encode('utf-8')
            
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
            return None
        except Exception as e:
            print(f"Error making request: {e}")
            return None

    def _save_submission_id(self, submission_id):
        try:
            with open(self.submission_log_file, "a") as f:
                f.write(f"{submission_id}\n")
            print(f"✅ Submission ID {submission_id} saved to {self.submission_log_file}")
        except Exception as e:
            print(f"⚠️ Warning: Failed to save submission ID: {e}")

    def submit_git(self, problem_id: int, git_url: str) -> Optional[Dict]:
        data = {"language": "git", "code": git_url}
        result = self._make_request("POST", f"/problem/{problem_id}/submit", data=data)
        if result and 'id' in result:
            self._save_submission_id(result['id'])
        return result

    def get_submission_detail(self, submission_id: int) -> Optional[Dict]:
        return self._make_request("GET", f"/submission/{submission_id}")

    def abort_submission(self, submission_id: int) -> Optional[Dict]:
        return self._make_request("POST", f"/submission/{submission_id}/abort")

def main():
    parser = argparse.ArgumentParser(description="ACMOJ API Command Line Client")
    parser.add_argument("--token", help="ACMOJ Access Token",
                       default=os.environ.get("ACMOJ_TOKEN"))
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    submit_git_parser = subparsers.add_parser("submit-git", help="Submit a Git repository")
    submit_git_parser.add_argument("--problem-id", type=int, required=True, help="Problem ID")
    submit_git_parser.add_argument("--git-url", type=str, required=True, help="Git repository URL")
    
    status_parser = subparsers.add_parser("status", help="Check submission status")
    status_parser.add_argument("--submission-id", type=int, required=True, help="Submission ID")
    
    abort_parser = subparsers.add_parser("abort", help="Abort submission evaluation")
    abort_parser.add_argument("--submission-id", type=int, required=True, help="Submission ID")
    
    args = parser.parse_args()
    
    if not args.token:
        print("Error: Access token not provided. Use --token or set ACMOJ_TOKEN environment variable.")
        return
        
    client = ACMOJClient(args.token)
    
    if args.command == "submit-git":
        result = client.submit_git(args.problem_id, args.git_url)
    elif args.command == "status":
        result = client.get_submission_detail(args.submission_id)
    elif args.command == "abort":
        result = client.abort_submission(args.submission_id)
        
    if result:
        print(json.dumps(result))

if __name__ == "__main__":
    main()
