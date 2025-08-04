import requests
from bs4 import BeautifulSoup

def fetch_github_profile(username_or_url):
    """
    Extract basic info from GitHub user profile page using scraping:
    - username, name, bio, followers count, public repo count
    """
    
    if not username_or_url or not username_or_url.strip():
        return{
            "username":"",
            "name":"",
            "bio":"",
            "followers":0,
            "repo_count":0  
        }

    try:
        if "github.com/" in username_or_url:
            username = username_or_url.strip().split("github.com/")[-1].strip("/")
        else:
            username = username_or_url.strip()

        url = f"https://github.com/{username}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        name = soup.select_one('span.p-name')
        bio = soup.select_one('div.p-note')
        followers = soup.select_one('a[href$="?tab=followers"] span')
        repo_count = soup.select_one('a[href$="?tab=repositories"] span')

        return {
            "username": username,
            "name": name.text.strip() if name else "",
            "bio": bio.text.strip() if bio else "",
            "followers": int(followers.text.strip()) if followers and followers.text.strip().isdigit() else 0,
            "repo_count": int(repo_count.text.strip()) if repo_count and repo_count.text.strip().isdigit() else 0
        }

    except Exception as e:
        return {"error": str(e)}

def fetch_repo_info(repo_url):
    """
    Fetch public GitHub project repo info via API:
    - stars, forks, watchers, language, commit count, last commit date
    """
    if not repo_url or not repo_url.strip():
        return {
            "repo_name": "",
            "stars": 0,
            "forks": 0,
            "watchers": 0,
            "language": "",
            "commit_count": 0,
            "last_commit_date": None
        }
    
    try:
        parts = repo_url.strip("/").split("/")
        if len(parts) < 2:
            return {"error": "Invalid GitHub repo URL"}

        owner, repo = parts[-2], parts[-1]
        repo_api_url = f"https://api.github.com/repos/{owner}/{repo}"
        commits_api_url = f"{repo_api_url}/commits?per_page=100"

        repo_resp = requests.get(repo_api_url)
        commits_resp = requests.get(commits_api_url)

        if repo_resp.status_code != 200:
            return {"error": f"Repo API returned status {repo_resp.status_code}"}
        if commits_resp.status_code != 200:
            return {"error": f"Commits API returned status {commits_resp.status_code}"}

        repo_data = repo_resp.json()
        commits_data = commits_resp.json()

        return {
            "repo_name": repo_data.get("name"),
            "stars": repo_data.get("stargazers_count", 0),
            "forks": repo_data.get("forks_count", 0),
            "watchers": repo_data.get("watchers_count", 0),
            "language": repo_data.get("language", ""),
            "commit_count": len(commits_data),
            "last_commit_date": commits_data[0]['commit']['committer']['date'] if commits_data else None,
        }

    except Exception as e:
        return {"error": str(e)}
    
    
