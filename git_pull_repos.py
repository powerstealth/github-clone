import os
import subprocess
import sys
import time
import requests
from urllib.parse import quote

def run_command(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error executing '{cmd}': {result.stderr.decode()}")
        return False
    print(result.stdout.decode())
    return True

def get_repos_from_github(token):
    headers = {"Authorization": f"token {token}"}
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/user/repos?per_page=100&page={page}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching repos: {response.status_code} - {response.text}")
            break
        data = response.json()
        if not data:
            break
        for repo in data:
            repos.append(repo["clone_url"])
        page += 1
    return repos

def pull_loop(token, base_dir, interval_minutes):
    encoded_token = quote(token)
    interval_seconds = interval_minutes * 60
    while True:
        print("Starting update cycle...")
        repos = get_repos_from_github(token)
        if not repos:
            print("No repositories found or error fetching repos.")
        for repo_url in repos:
            if repo_url.startswith("https://github.com/"):
                repo_url = repo_url.replace(
                    "https://github.com/",
                    f"https://{encoded_token}:x-oauth-basic@github.com/"
                )
            repo_name = repo_url.split("/")[-1]
            if repo_name.endswith(".git"):
                repo_name = repo_name[:-4]
            repo_path = os.path.join(base_dir, repo_name)
            if os.path.isdir(repo_path):
                print(f"Repository '{repo_name}' found. Executing git pull...")
                run_command("git pull", cwd=repo_path)
            else:
                print(f"Repository '{repo_name}' not found. Cloning from scratch...")
                run_command(f"git clone {repo_url} {repo_path}")
        print(f"Update cycle completed. Waiting {interval_minutes} minutes...\n")
        time.sleep(interval_seconds)

if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable is missing.")
        sys.exit(1)

    base_dir = os.environ.get("BASE_DIR", "/app/repos")
    os.makedirs(base_dir, exist_ok=True)

    interval_str = os.environ.get("PULL_INTERVAL_MINUTES", "10")
    try:
        interval_minutes = int(interval_str)
    except ValueError:
        print(f"Invalid PULL_INTERVAL_MINUTES value '{interval_str}', defaulting to 10")
        interval_minutes = 10

    pull_loop(token, base_dir, interval_minutes)